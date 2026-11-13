"""Integration tests for Gateway Aggregator parallel fan-out, timeouts, and fallbacks."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from services.order_service.seed import DEMO_ORDER_ID
from shared.constants import ApiEndpoints, MediaTypes, ServiceNames


@pytest.mark.asyncio
async def test_parallel_vs_sequential_timing_empirically(gateway_client: AsyncClient) -> None:
    # Delays: Product 60ms, Inventory 120ms, Reviews 90ms.
    # Sequential total should be >= 270ms.
    # Parallel total should be ~120ms (slowest call).
    seq_resp = await gateway_client.get(
        f"{ApiEndpoints.PAGES_PRODUCTS}/42"
        "?mode=sequential&product_delay_ms=60&inventory_delay_ms=120&reviews_delay_ms=90"
    )
    assert seq_resp.status_code == 200
    seq_data = seq_resp.json()
    seq_telemetry = seq_data["telemetry"]
    assert seq_telemetry["total_latency_ms"] >= 200.0

    par_resp = await gateway_client.get(
        f"{ApiEndpoints.PAGES_PRODUCTS}/42"
        "?mode=parallel&product_delay_ms=60&inventory_delay_ms=120&reviews_delay_ms=90"
    )
    assert par_resp.status_code == 200
    par_data = par_resp.json()
    par_telemetry = par_data["telemetry"]

    # Parallel latency must be significantly faster than sequential
    assert par_telemetry["total_latency_ms"] < seq_telemetry["total_latency_ms"]
    assert par_telemetry["latency_saved_ms"] > 50.0


@pytest.mark.asyncio
async def test_graceful_degradation_fallbacks(gateway_client: AsyncClient) -> None:
    # Non-critical reviews failure falls back gracefully
    resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/42?fail_reviews=true")
    assert resp.status_code == 200
    data = resp.json()

    assert data["composition_status"] == "degraded"
    assert ServiceNames.REVIEWS_SERVICE.value in data["telemetry"]["degraded_services"]
    assert data["reviews"]["is_fallback"] is True
    assert data["reviews"]["average_rating"] == 0.0
    assert data["reviews"]["total_reviews"] == 0

    # Critical product data and inventory still present!
    assert data["product"]["id"] == 42
    assert data["inventory"]["in_stock"] is True
    assert data["inventory"]["is_fallback"] is False


@pytest.mark.asyncio
async def test_critical_product_failure_propagates_problem_details(
    gateway_client: AsyncClient,
) -> None:
    # 1. Product not found downstream raises 404 Problem Details
    nf_resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/99999")
    assert nf_resp.status_code == 404
    assert nf_resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON
    assert nf_resp.json()["status"] == 404

    # 2. Product 500 error raises 502/503 Problem Details (critical service fail-fast)
    fail_resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/42?fail_product=true")
    assert fail_resp.status_code in (502, 503)
    assert fail_resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON


@pytest.mark.asyncio
async def test_timeout_enforcement_on_critical_service(gateway_client: AsyncClient) -> None:
    # If product exceeds timeout limit, gateway returns 504 Gateway Timeout
    resp = await gateway_client.get(
        f"{ApiEndpoints.PAGES_PRODUCTS}/42?timeout_ms=50&product_delay_ms=200"
    )
    assert resp.status_code == 504
    assert resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON
    assert "timed out" in resp.json()["detail"].lower()


@pytest.mark.asyncio
async def test_order_page_aggregation(gateway_client: AsyncClient) -> None:
    # Fetches aggregate root + enriches line items with product names and live inventory
    resp = await gateway_client.get(f"{ApiEndpoints.PAGES_ORDERS}/{DEMO_ORDER_ID}")
    assert resp.status_code == 200
    data = resp.json()

    assert data["order_id"] == DEMO_ORDER_ID
    assert data["status"] == "CONFIRMED"
    assert len(data["items"]) == 2

    # Check line items are enriched
    laptop_item = next(it for it in data["items"] if it["sku"] == "TECH-LAPTOP-42")
    assert laptop_item["product_id"] == 42
    assert laptop_item["product_name"] == "UltraPro Developer Laptop 16-inch"
    assert laptop_item["inventory_available"] is not None
    assert laptop_item["inventory_status"] == "in_stock"
