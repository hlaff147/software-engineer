"""Integration tests for Gateway Aggregator parallel fan-out, timeouts, and fallbacks."""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from services.gateway_aggregator.schemas import OrderPageResponse, ProductPageResponse
from services.order_service.seed import DEMO_ORDER_ID
from shared.constants import ApiEndpoints, MediaTypes, ServiceNames
from shared.errors import ProblemDetails


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
    seq_page = ProductPageResponse.model_validate(seq_resp.json())
    assert seq_page.telemetry.total_latency_ms >= 200.0

    par_resp = await gateway_client.get(
        f"{ApiEndpoints.PAGES_PRODUCTS}/42"
        "?mode=parallel&product_delay_ms=60&inventory_delay_ms=120&reviews_delay_ms=90"
    )
    assert par_resp.status_code == 200
    par_page = ProductPageResponse.model_validate(par_resp.json())

    # Parallel latency must be significantly faster than sequential
    assert par_page.telemetry.total_latency_ms < seq_page.telemetry.total_latency_ms
    assert par_page.telemetry.latency_saved_ms > 50.0


@pytest.mark.asyncio
async def test_graceful_degradation_fallbacks(gateway_client: AsyncClient) -> None:
    # Non-critical reviews failure falls back gracefully
    resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/42?fail_reviews=true")
    assert resp.status_code == 200
    page = ProductPageResponse.model_validate(resp.json())

    assert page.composition_status == "degraded"
    assert ServiceNames.REVIEWS_SERVICE.value in page.telemetry.degraded_services
    assert page.reviews.is_fallback is True
    assert page.reviews.average_rating == 0.0
    assert page.reviews.total_reviews == 0

    # Critical product data and inventory still present!
    assert page.product.id == 42
    assert page.inventory.in_stock is True
    assert page.inventory.is_fallback is False


@pytest.mark.asyncio
async def test_critical_product_failure_propagates_problem_details(
    gateway_client: AsyncClient,
) -> None:
    # 1. Product not found downstream raises 404 Problem Details
    nf_resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/99999")
    assert nf_resp.status_code == 404
    assert nf_resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON
    nf_problem = ProblemDetails.model_validate(nf_resp.json())
    assert nf_problem.status == 404

    # 2. Product 500 error raises 502/503 Problem Details (critical service fail-fast)
    fail_resp = await gateway_client.get(f"{ApiEndpoints.PAGES_PRODUCTS}/42?fail_product=true")
    assert fail_resp.status_code in (502, 503)
    assert fail_resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON
    fail_problem = ProblemDetails.model_validate(fail_resp.json())
    assert fail_problem.status in (502, 503)


@pytest.mark.asyncio
async def test_timeout_enforcement_on_critical_service(gateway_client: AsyncClient) -> None:
    # If product exceeds timeout limit, gateway returns 504 Gateway Timeout
    resp = await gateway_client.get(
        f"{ApiEndpoints.PAGES_PRODUCTS}/42?timeout_ms=50&product_delay_ms=200"
    )
    assert resp.status_code == 504
    assert resp.headers.get("content-type") == MediaTypes.APPLICATION_PROBLEM_JSON
    problem = ProblemDetails.model_validate(resp.json())
    assert problem.status == 504
    assert "timed out" in (problem.detail or "").lower()


@pytest.mark.asyncio
async def test_order_page_aggregation(gateway_client: AsyncClient) -> None:
    # Fetches aggregate root + enriches line items with product names and live inventory
    resp = await gateway_client.get(f"{ApiEndpoints.PAGES_ORDERS}/{DEMO_ORDER_ID}")
    assert resp.status_code == 200
    page = OrderPageResponse.model_validate(resp.json())

    assert page.order_id == DEMO_ORDER_ID
    assert page.status == "CONFIRMED"
    assert len(page.items) == 2

    # Check line items are enriched
    laptop_item = next(it for it in page.items if it.sku == "TECH-LAPTOP-42")
    assert laptop_item.product_id == 42
    assert laptop_item.product_name == "UltraPro Developer Laptop 16-inch"
    assert laptop_item.inventory_available is not None
    assert laptop_item.inventory_status == "in_stock"
