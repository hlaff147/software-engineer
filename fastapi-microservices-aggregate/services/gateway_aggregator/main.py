"""Gateway Aggregator entrypoint and API endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, Query

from services.gateway_aggregator.aggregator import (
    OrderPageAggregator,
    ProductPageAggregator,
)
from services.gateway_aggregator.clients import DownstreamClientRegistry
from services.gateway_aggregator.config import get_settings
from services.gateway_aggregator.schemas import OrderPageResponse, ProductPageResponse
from shared.constants import ApiEndpoints
from shared.errors import register_problem_handlers
from shared.health import create_health_router
from shared.logging import configure_logging

__all__ = ["app", "get_registry"]

settings = get_settings()
logger = configure_logging(settings.service_name)
registry: DownstreamClientRegistry | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global registry
    logger.info("Initializing Gateway Aggregator downstream HTTP clients...")
    if registry is None:
        registry = DownstreamClientRegistry(settings)
    yield
    logger.info("Closing Gateway Aggregator HTTP clients...")
    if registry is not None:
        await registry.close_all()


app = FastAPI(
    title="Gateway Aggregator Service",
    description="Implements Gateway Aggregation Pattern: One client call, parallel downstream fan-out, merged response.",
    version="1.0.0",
    lifespan=lifespan,
)

register_problem_handlers(app)
app.include_router(create_health_router(settings.service_name))


def get_registry() -> DownstreamClientRegistry:
    global registry
    if registry is None:
        registry = DownstreamClientRegistry(settings)
    return registry


@app.get(
    f"{ApiEndpoints.PAGES_PRODUCTS}/{{product_id}}",
    response_model=ProductPageResponse,
    summary="Get aggregated product details page with parallel fan-out and fallbacks",
)
async def get_product_page(
    product_id: int,
    mode: Annotated[
        Literal["parallel", "sequential"],
        Query(description="Fan-out execution strategy for latency comparison"),
    ] = "parallel",
    timeout_ms: Annotated[
        int, Query(ge=1, description="Per-downstream timeout limit in ms")
    ] = 1000,
    product_delay_ms: Annotated[
        int, Query(ge=0, description="Injected delay for product-service")
    ] = 0,
    inventory_delay_ms: Annotated[
        int, Query(ge=0, description="Injected delay for inventory-service")
    ] = 0,
    reviews_delay_ms: Annotated[
        int, Query(ge=0, description="Injected delay for reviews-service")
    ] = 0,
    fail_product: Annotated[
        bool, Query(description="Simulate product-service failure (critical)")
    ] = False,
    fail_inventory: Annotated[
        bool, Query(description="Simulate inventory-service failure (fallback)")
    ] = False,
    fail_reviews: Annotated[
        bool, Query(description="Simulate reviews-service failure (fallback)")
    ] = False,
    reg: DownstreamClientRegistry = Depends(get_registry),
) -> ProductPageResponse:
    aggregator = ProductPageAggregator(reg)
    return await aggregator.compose(
        product_id=product_id,
        mode=mode,
        timeout_ms=timeout_ms,
        product_delay_ms=product_delay_ms,
        inventory_delay_ms=inventory_delay_ms,
        reviews_delay_ms=reviews_delay_ms,
        fail_product=fail_product,
        fail_inventory=fail_inventory,
        fail_reviews=fail_reviews,
    )


@app.get(
    f"{ApiEndpoints.PAGES_ORDERS}/{{order_id}}",
    response_model=OrderPageResponse,
    summary="Get enriched order page combining DDD Order Aggregate with catalog and stock",
)
async def get_order_page(
    order_id: str,
    reg: DownstreamClientRegistry = Depends(get_registry),
) -> OrderPageResponse:
    aggregator = OrderPageAggregator(reg)
    return await aggregator.compose_order_page(order_id)
