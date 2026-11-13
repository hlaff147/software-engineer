"""Integration tests for Order Service REST API and Persistence."""

from __future__ import annotations

from decimal import Decimal

import pytest
from httpx import AsyncClient

from services.order_service.application.dtos import (
    AddOrderItemCommand,
    CreateOrderCommand,
    OrderResponse,
    OutboxEventResponse,
)
from shared.constants import ApiEndpoints, HttpHeaders
from shared.errors import ProblemDetails
from shared.pagination import PaginatedResponse


@pytest.mark.asyncio
async def test_order_crud_lifecycle_and_invariants(order_client: AsyncClient) -> None:
    # 1. Create Order
    create_cmd = CreateOrderCommand(customer_id="cust-integration-1", currency="USD")
    create_resp = await order_client.post(
        ApiEndpoints.ORDERS,
        json=create_cmd.model_dump(mode="json"),
    )
    assert create_resp.status_code == 201
    assert HttpHeaders.LOCATION in create_resp.headers
    order = OrderResponse.model_validate(create_resp.json())
    order_id = order.id
    assert order.status == "DRAFT"
    assert order.version == 1
    assert order.total_amount == Decimal("0.00")

    # 2. Add Item
    add_cmd = AddOrderItemCommand(
        product_id=42,
        sku="TECH-LAPTOP-42",
        product_name="UltraPro Laptop",
        unit_price=Decimal("2499.00"),
        quantity=2,
    )
    add_resp = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/items",
        json=add_cmd.model_dump(mode="json"),
    )
    assert add_resp.status_code == 200
    updated_order = OrderResponse.model_validate(add_resp.json())
    assert updated_order.version == 2
    assert updated_order.total_amount == Decimal("4998.00")
    assert len(updated_order.items) == 1
    assert updated_order.items[0].sku == "TECH-LAPTOP-42"

    # 3. Invariant violation: quantity > 10 returns RFC 7807 422
    invalid_qty_resp = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/items",
        json={
            "product_id": 43,
            "sku": "ACC-KEYBOARD-43",
            "product_name": "Keyboard",
            "unit_price": "150.00",
            "quantity": 15,
        },
    )
    assert invalid_qty_resp.status_code == 422
    qty_problem = ProblemDetails.model_validate(invalid_qty_resp.json())
    assert qty_problem.status == 422
    assert qty_problem.detail is not None

    # 4. Invariant violation: total > 50,000 returns RFC 7807 422
    cap_cmd = AddOrderItemCommand(
        product_id=99,
        sku="EXP-SUPERCOMPUTER",
        product_name="Supercomputer",
        unit_price=Decimal("30000.00"),
        quantity=2,
    )
    cap_resp = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/items",
        json=cap_cmd.model_dump(mode="json"),
    )
    assert cap_resp.status_code == 422
    cap_problem = ProblemDetails.model_validate(cap_resp.json())
    assert cap_problem.status == 422
    assert "exceeding maximum allowed order cap" in (cap_problem.detail or "")

    # 5. Optimistic Concurrency Check: passing wrong expected_version returns 409
    conflict_resp = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/confirm",
        headers={HttpHeaders.IF_MATCH: "999"},
    )
    assert conflict_resp.status_code == 409
    conflict_problem = ProblemDetails.model_validate(conflict_resp.json())
    assert conflict_problem.status == 409
    assert "version mismatch" in (conflict_problem.detail or "").lower()

    # 6. Confirm Order successfully
    confirm_resp = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/confirm",
        headers={HttpHeaders.IF_MATCH: str(updated_order.version)},
    )
    assert confirm_resp.status_code == 200
    confirmed = OrderResponse.model_validate(confirm_resp.json())
    assert confirmed.status == "CONFIRMED"

    # 7. Modify confirmed order returns 409 Invalid Order State
    post_confirm_cmd = AddOrderItemCommand(
        product_id=43,
        sku="ACC-KEYBOARD-43",
        product_name="Keyboard",
        unit_price=Decimal("100.00"),
        quantity=1,
    )
    post_confirm_add = await order_client.post(
        f"{ApiEndpoints.ORDERS}/{order_id}/items",
        json=post_confirm_cmd.model_dump(mode="json"),
    )
    assert post_confirm_add.status_code == 409
    state_problem = ProblemDetails.model_validate(post_confirm_add.json())
    assert state_problem.status == 409
    assert "not in draft status" in (state_problem.detail or "").lower()

    # 8. Check Transactional Outbox Events
    events_resp = await order_client.get(f"{ApiEndpoints.ORDERS}/{order_id}/events")
    assert events_resp.status_code == 200
    events = [OutboxEventResponse.model_validate(e) for e in events_resp.json()]
    assert len(events) >= 3
    event_types = [e.event_type for e in events]
    assert "OrderCreated" in event_types
    assert "OrderItemAdded" in event_types
    assert "OrderConfirmed" in event_types


@pytest.mark.asyncio
async def test_order_pagination_and_not_found(order_client: AsyncClient) -> None:
    # Seeded demo order exists
    list_resp = await order_client.get(f"{ApiEndpoints.ORDERS}?page=1&page_size=5")
    assert list_resp.status_code == 200
    page = PaginatedResponse[OrderResponse].model_validate(list_resp.json())
    assert len(page.items) >= 1
    assert page.total_count >= 1

    # Not found returns RFC 7807 404
    nf_resp = await order_client.get(f"{ApiEndpoints.ORDERS}/non-existent-order-id")
    assert nf_resp.status_code == 404
    nf_problem = ProblemDetails.model_validate(nf_resp.json())
    assert nf_problem.status == 404
