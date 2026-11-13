#!/usr/bin/env python3
"""Interactive didactic showcase script for fastapi-microservices-aggregate.

Demonstrates:
1. Gateway Aggregation Pattern: Parallel fan-out vs Sequential execution latency comparison.
2. Graceful Degradation: Reviews failure fallback vs Critical Product failure fail-fast.
3. DDD Order Aggregate Root: Invariants, quantity limits, monetary caps, optimistic concurrency control, and transactional outbox.
4. Typed Pydantic v2 DTOs: .model_validate() for type-safe dot-notation access mirroring Java Jackson DTOs.
"""

from __future__ import annotations

import asyncio
import json
import time
from decimal import Decimal
from typing import Any

import httpx

from services.gateway_aggregator.schemas import OrderPageResponse, ProductPageResponse
from services.order_service.application.dtos import (
    AddOrderItemCommand,
    CreateOrderCommand,
    OrderResponse,
    OutboxEventResponse,
)
from shared.constants import ApiEndpoints, ServiceUrls
from shared.errors import ProblemDetails

GATEWAY_URL = ServiceUrls.GATEWAY_AGGREGATOR
ORDER_URL = ServiceUrls.ORDER_SERVICE.replace("order-service:8004", "localhost:8004")


def print_header(title: str) -> None:
    print("\n" + "=" * 76)
    print(f" 🚀 {title}")
    print("=" * 76)


def print_step(step: str, detail: str) -> None:
    print(f"\n👉 [{step}] {detail}")


def format_json(obj: Any) -> str:
    return json.dumps(obj, indent=2)


async def run_live_demo(client: httpx.AsyncClient) -> None:
    print_header("SCENARIO 1: Gateway Aggregation Pattern (Parallel vs. Sequential)")
    print("Simulating downstream delays: Product 80ms, Inventory 150ms, Reviews 100ms")

    # Sequential execution
    print_step("1.1", "Executing in SEQUENTIAL mode (?mode=sequential)...")
    t0 = time.perf_counter()
    seq_resp = await client.get(
        f"{GATEWAY_URL}{ApiEndpoints.PAGES_PRODUCTS}/42",
        params={
            "mode": "sequential",
            "product_delay_ms": 80,
            "inventory_delay_ms": 150,
            "reviews_delay_ms": 100,
        },
    )
    seq_wall_ms = round((time.perf_counter() - t0) * 1000.0, 2)
    seq_page = ProductPageResponse.model_validate(seq_resp.json())
    print(
        f"   ⏱️  Sequential Total Latency: {seq_page.telemetry.total_latency_ms} ms "
        f"(Client wall: {seq_wall_ms} ms, sum of all calls: {seq_page.telemetry.sum_of_downstream_ms} ms)"
    )

    # Parallel execution
    print_step("1.2", "Executing in PARALLEL mode (?mode=parallel via asyncio.gather)...")
    t1 = time.perf_counter()
    par_resp = await client.get(
        f"{GATEWAY_URL}{ApiEndpoints.PAGES_PRODUCTS}/42",
        params={
            "mode": "parallel",
            "product_delay_ms": 80,
            "inventory_delay_ms": 150,
            "reviews_delay_ms": 100,
        },
    )
    par_wall_ms = round((time.perf_counter() - t1) * 1000.0, 2)
    par_page = ProductPageResponse.model_validate(par_resp.json())
    print(
        f"   ⚡ Parallel Total Latency:   {par_page.telemetry.total_latency_ms} ms "
        f"(Client wall: {par_wall_ms} ms, ≈ slowest call: 150ms)"
    )
    print(f"   🎉 Latency Saved:          {par_page.telemetry.latency_saved_ms} ms faster!")

    print_header("SCENARIO 2: Gateway Aggregator Resilience & Graceful Fallbacks")
    print_step("2.1", "Simulating Reviews Service outage (?fail_reviews=true)...")
    fallback_resp = await client.get(
        f"{GATEWAY_URL}{ApiEndpoints.PAGES_PRODUCTS}/42?fail_reviews=true"
    )
    fallback_page = ProductPageResponse.model_validate(fallback_resp.json())
    print(f"   Status Code: {fallback_resp.status_code}")
    print(f"   Composition Status: {fallback_page.composition_status}")
    print(f"   Degraded Services:  {fallback_page.telemetry.degraded_services}")
    print(
        f"   Reviews Fallback:   is_fallback={fallback_page.reviews.is_fallback}, rating={fallback_page.reviews.average_rating}"
    )

    print_step("2.2", "Simulating Critical Product Service outage (?fail_product=true)...")
    crit_resp = await client.get(f"{GATEWAY_URL}{ApiEndpoints.PAGES_PRODUCTS}/42?fail_product=true")
    crit_problem = ProblemDetails.model_validate(crit_resp.json())
    print(f"   Status Code: {crit_resp.status_code} (Fail-Fast Problem Details)")
    print(f"   RFC 7807 Error Title: {crit_problem.title} | Detail: {crit_problem.detail}")

    print_header("SCENARIO 3: DDD Order Aggregate Root & Domain Invariants (Pydantic DTOs)")
    print_step("3.1", "Creating new Order Aggregate Root in DRAFT status via CreateOrderCommand...")
    create_cmd = CreateOrderCommand(customer_id="cust-demo-99", currency="USD")
    new_ord_resp = await client.post(
        f"{ORDER_URL}{ApiEndpoints.ORDERS}",
        json=create_cmd.model_dump(mode="json"),
    )
    order = OrderResponse.model_validate(new_ord_resp.json())
    order_id = order.id
    print(f"   Created Order ID: {order_id} (Status: {order.status}, Version: {order.version})")

    print_step("3.2", "Adding valid line item (UltraPro Laptop x 2) via AddOrderItemCommand...")
    add_cmd = AddOrderItemCommand(
        product_id=42,
        sku="TECH-LAPTOP-42",
        product_name="UltraPro Laptop",
        unit_price=Decimal("2499.00"),
        quantity=2,
    )
    add_resp = await client.post(
        f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/items",
        json=add_cmd.model_dump(mode="json"),
    )
    order = OrderResponse.model_validate(add_resp.json())
    print(f"   Order Total: ${order.total_amount} | Version: {order.version}")

    print_step("3.3", "Testing Invariant: Attempting to add 15 keyboards (limit is 10)...")
    invalid_qty = await client.post(
        f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/items",
        json={
            "product_id": 43,
            "sku": "ACC-KEYBOARD-43",
            "product_name": "Keyboard",
            "unit_price": "189.50",
            "quantity": 15,
        },
    )
    qty_problem = ProblemDetails.model_validate(invalid_qty.json())
    print(f"   Status Code: {invalid_qty.status_code} | Invariant Blocked: {qty_problem.detail}")

    print_step("3.4", "Testing Invariant: Exceeding $50,000 maximum order cap...")
    cap_cmd = AddOrderItemCommand(
        product_id=99,
        sku="TECH-CLUSTER",
        product_name="AI Supercluster",
        unit_price=Decimal("30000.00"),
        quantity=2,
    )
    cap_viol = await client.post(
        f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/items",
        json=cap_cmd.model_dump(mode="json"),
    )
    cap_problem = ProblemDetails.model_validate(cap_viol.json())
    print(f"   Status Code: {cap_viol.status_code} | Invariant Blocked: {cap_problem.detail}")

    print_step("3.5", "Confirming the Order Aggregate...")
    confirm_resp = await client.post(f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/confirm")
    confirmed_order = OrderResponse.model_validate(confirm_resp.json())
    print(
        f"   Order Confirmed! Status: {confirmed_order.status}, Version: {confirmed_order.version}"
    )

    print_step("3.6", "Verifying Aggregate Immutability after confirmation...")
    post_confirm_cmd = AddOrderItemCommand(
        product_id=43,
        sku="ACC-KEYBOARD-43",
        product_name="Keyboard",
        unit_price=Decimal("189.50"),
        quantity=1,
    )
    mutate_post_confirm = await client.post(
        f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/items",
        json=post_confirm_cmd.model_dump(mode="json"),
    )
    state_problem = ProblemDetails.model_validate(mutate_post_confirm.json())
    print(
        f"   Status Code: {mutate_post_confirm.status_code} | Mutation Blocked: {state_problem.detail}"
    )

    print_step("3.7", "Inspecting Transactional Outbox Events emitted by the Aggregate Root...")
    events_resp = await client.get(f"{ORDER_URL}{ApiEndpoints.ORDERS}/{order_id}/events")
    events = [OutboxEventResponse.model_validate(e) for e in events_resp.json()]
    print(f"   Emitted Events ({len(events)}):")
    for ev in events:
        print(f"   - {ev.event_type} at {ev.occurred_at}")

    print_header("SCENARIO 4: Gateway Aggregation of Enriched Order Page")
    print_step("4.1", "Fetching unified Order Page via Gateway Aggregator...")
    order_page_resp = await client.get(f"{GATEWAY_URL}{ApiEndpoints.PAGES_ORDERS}/{order_id}")
    order_page = OrderPageResponse.model_validate(order_page_resp.json())
    print(f"   Order Page Total: ${order_page.total_amount} {order_page.currency}")
    print("   Enriched Items:")
    for item in order_page.items:
        print(
            f"   - SKU: {item.sku} | Qty: {item.quantity} | Stock: {item.inventory_available} units ({item.inventory_status})"
        )

    print("\n✅ All Didactic Demonstrations Succeeded Perfectly!\n")


async def main() -> None:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            health = await client.get(f"{GATEWAY_URL}{ApiEndpoints.HEALTH}")
            if health.status_code != 200:
                raise httpx.ConnectError("Gateway not ready")
            await run_live_demo(client)
        except Exception:
            print("\n⚠️ Docker containers do not appear to be running on localhost:8000.")
            print("To start the full stack, run:\n")
            print("    docker compose up --build -d\n")
            print("Then re-run this demo script:")
            print("    python3 scripts/demo_showcase.py\n")


if __name__ == "__main__":
    asyncio.run(main())


async def main() -> None:
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            health = await client.get(f"{GATEWAY_URL}{ApiEndpoints.HEALTH}")
            if health.status_code != 200:
                raise httpx.ConnectError("Gateway not ready")
            await run_live_demo(client)
        except Exception:
            print("\n⚠️ Docker containers do not appear to be running on localhost:8000.")
            print("To start the full stack, run:\n")
            print("    docker compose up --build -d\n")
            print("Then re-run this demo script:")
            print("    python3 scripts/demo_showcase.py\n")


if __name__ == "__main__":
    asyncio.run(main())
