"""Integration tests for Order Service REST API and Persistence."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_order_crud_lifecycle_and_invariants(order_client: AsyncClient) -> None:
    # 1. Create Order
    create_resp = await order_client.post(
        "/api/v1/orders",
        json={"customer_id": "cust-integration-1", "currency": "USD"},
    )
    assert create_resp.status_code == 201
    assert "Location" in create_resp.headers
    order = create_resp.json()
    order_id = order["id"]
    assert order["status"] == "DRAFT"
    assert order["version"] == 1
    assert order["total_amount"] == "0.00"

    # 2. Add Item
    add_resp = await order_client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": 42,
            "sku": "TECH-LAPTOP-42",
            "product_name": "UltraPro Laptop",
            "unit_price": "2499.00",
            "quantity": 2,
        },
    )
    assert add_resp.status_code == 200
    updated_order = add_resp.json()
    assert updated_order["version"] == 2
    assert updated_order["total_amount"] == "4998.00"
    assert len(updated_order["items"]) == 1

    # 3. Invariant violation: quantity > 10 returns RFC 7807 422
    invalid_qty_resp = await order_client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": 43,
            "sku": "ACC-KEYBOARD-43",
            "product_name": "Keyboard",
            "unit_price": "150.00",
            "quantity": 15,
        },
    )
    assert invalid_qty_resp.status_code == 422
    problem = invalid_qty_resp.json()
    assert problem["status"] == 422
    assert "detail" in problem

    # 4. Invariant violation: total > 50,000 returns RFC 7807 422
    cap_resp = await order_client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": 99,
            "sku": "EXP-SUPERCOMPUTER",
            "product_name": "Supercomputer",
            "unit_price": "30000.00",
            "quantity": 2,
        },
    )
    assert cap_resp.status_code == 422
    assert "exceeding maximum allowed order cap" in cap_resp.json()["detail"]

    # 5. Optimistic Concurrency Check: passing wrong expected_version returns 409
    conflict_resp = await order_client.post(
        f"/api/v1/orders/{order_id}/confirm",
        headers={"if-match": "999"},
    )
    assert conflict_resp.status_code == 409
    assert "version mismatch" in conflict_resp.json()["detail"].lower()

    # 6. Confirm Order successfully
    confirm_resp = await order_client.post(
        f"/api/v1/orders/{order_id}/confirm",
        headers={"if-match": str(updated_order["version"])},
    )
    assert confirm_resp.status_code == 200
    confirmed = confirm_resp.json()
    assert confirmed["status"] == "CONFIRMED"

    # 7. Modify confirmed order returns 409 Invalid Order State
    post_confirm_add = await order_client.post(
        f"/api/v1/orders/{order_id}/items",
        json={
            "product_id": 43,
            "sku": "ACC-KEYBOARD-43",
            "product_name": "Keyboard",
            "unit_price": "100.00",
            "quantity": 1,
        },
    )
    assert post_confirm_add.status_code == 409
    assert "not in draft status" in post_confirm_add.json()["detail"].lower()

    # 8. Check Transactional Outbox Events
    events_resp = await order_client.get(f"/api/v1/orders/{order_id}/events")
    assert events_resp.status_code == 200
    events = events_resp.json()
    assert len(events) >= 3
    event_types = [e["event_type"] for e in events]
    assert "OrderCreated" in event_types
    assert "OrderItemAdded" in event_types
    assert "OrderConfirmed" in event_types


@pytest.mark.asyncio
async def test_order_pagination_and_not_found(order_client: AsyncClient) -> None:
    # Seeded demo order exists
    list_resp = await order_client.get("/api/v1/orders?page=1&page_size=5")
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert "items" in data
    assert "total_count" in data
    assert data["total_count"] >= 1

    # Not found returns RFC 7807 404
    nf_resp = await order_client.get("/api/v1/orders/non-existent-order-id")
    assert nf_resp.status_code == 404
    assert nf_resp.json()["status"] == 404
