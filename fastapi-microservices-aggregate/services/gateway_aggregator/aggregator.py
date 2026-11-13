"""Gateway Aggregation business logic: Parallel fan-out, timeouts, fallbacks, and composition."""

from __future__ import annotations

import asyncio
import time
from typing import Literal

import httpx
from fastapi import status

from services.gateway_aggregator.clients import DownstreamClientRegistry, timed_get
from services.gateway_aggregator.schemas import (
    AggregationTelemetry,
    InventorySection,
    OrderLineItemView,
    OrderPageResponse,
    ProductPageResponse,
    ProductSection,
    ReviewSnippet,
    ReviewsSection,
)
from services.inventory_service.schemas import StockResponse
from services.order_service.application.dtos import OrderLineItemResponse, OrderResponse
from services.product_service.schemas import ProductResponse
from services.reviews_service.schemas import ProductReviewsResponse
from shared.constants import ApiEndpoints, ErrorTitles, ErrorTypes, ServiceNames
from shared.errors import ProblemDetailsException

__all__ = ["OrderPageAggregator", "ProductPageAggregator"]


class ProductPageAggregator:
    """Aggregates Product, Inventory, and Reviews services into a unified Product Page."""

    def __init__(self, registry: DownstreamClientRegistry) -> None:
        self.registry = registry

    async def compose(
        self,
        product_id: int,
        mode: Literal["parallel", "sequential"] = "parallel",
        timeout_ms: int = 1000,
        product_delay_ms: int = 0,
        inventory_delay_ms: int = 0,
        reviews_delay_ms: int = 0,
        fail_product: bool = False,
        fail_inventory: bool = False,
        fail_reviews: bool = False,
    ) -> ProductPageResponse:
        timeout_s = timeout_ms / 1000.0

        async def fetch_product() -> tuple[httpx.Response | None, float, Exception | None]:
            client = self.registry.get_client("product")
            params = {"delay_ms": product_delay_ms, "simulate_failure": str(fail_product).lower()}
            return await timed_get(
                client, f"{ApiEndpoints.PRODUCTS}/{product_id}", params, timeout_s
            )

        async def fetch_inventory() -> tuple[httpx.Response | None, float, Exception | None]:
            client = self.registry.get_client("inventory")
            params = {
                "delay_ms": inventory_delay_ms,
                "simulate_failure": str(fail_inventory).lower(),
            }
            return await timed_get(client, f"{ApiEndpoints.STOCK}/{product_id}", params, timeout_s)

        async def fetch_reviews() -> tuple[httpx.Response | None, float, Exception | None]:
            client = self.registry.get_client("reviews")
            params = {"delay_ms": reviews_delay_ms, "simulate_failure": str(fail_reviews).lower()}
            return await timed_get(
                client, f"{ApiEndpoints.REVIEWS}/{product_id}", params, timeout_s
            )

        wall_start = time.perf_counter()

        if mode == "parallel":
            # Fan-out concurrent execution via asyncio.gather
            (
                (prod_resp, prod_ms, prod_err),
                (inv_resp, inv_ms, inv_err),
                (rev_resp, rev_ms, rev_err),
            ) = await asyncio.gather(fetch_product(), fetch_inventory(), fetch_reviews())
        else:
            # Sequential execution for didactic comparison
            prod_resp, prod_ms, prod_err = await fetch_product()
            inv_resp, inv_ms, inv_err = await fetch_inventory()
            rev_resp, rev_ms, rev_err = await fetch_reviews()

        total_latency_ms = round((time.perf_counter() - wall_start) * 1000.0, 2)
        sum_of_downstream_ms = round(prod_ms + inv_ms + rev_ms, 2)
        latency_saved_ms = max(0.0, round(sum_of_downstream_ms - total_latency_ms, 2))

        # 1. Product is CRITICAL: Fail fast if product fails or does not exist
        if prod_err is not None:
            if isinstance(prod_err, httpx.TimeoutException):
                raise ProblemDetailsException(
                    status=status.HTTP_504_GATEWAY_TIMEOUT,
                    title=ErrorTitles.PRODUCT_TIMEOUT,
                    detail=f"Product Service timed out after {timeout_ms}ms.",
                    type_uri=ErrorTypes.GATEWAY_TIMEOUT,
                )
            raise ProblemDetailsException(
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
                title=ErrorTitles.PRODUCT_UNAVAILABLE,
                detail=f"Failed to communicate with Product Service: {prod_err}",
                type_uri=ErrorTypes.SERVICE_UNAVAILABLE,
            )

        if prod_resp is None or prod_resp.status_code != 200:
            status_code = prod_resp.status_code if prod_resp is not None else 500
            if status_code == 404:
                raise ProblemDetailsException(
                    status=status.HTTP_404_NOT_FOUND,
                    title=ErrorTitles.PRODUCT_NOT_FOUND,
                    detail=f"Product with ID {product_id} not found downstream.",
                    type_uri=ErrorTypes.PRODUCT_NOT_FOUND,
                )
            raise ProblemDetailsException(
                status=status.HTTP_502_BAD_GATEWAY,
                title=ErrorTitles.PRODUCT_ERROR,
                detail=f"Product Service returned HTTP status {status_code}.",
                type_uri=ErrorTypes.BAD_GATEWAY,
            )

        product_dto = ProductResponse.model_validate(prod_resp.json())
        product_section = ProductSection(
            id=product_dto.id,
            sku=product_dto.sku,
            name=product_dto.name,
            description=product_dto.description,
            price=product_dto.price,
            currency=product_dto.currency,
            category=product_dto.category,
        )

        degraded_services: list[str] = []

        # 2. Inventory is NON-CRITICAL: Apply graceful degradation fallback
        if inv_err is not None or inv_resp is None or inv_resp.status_code != 200:
            degraded_services.append(ServiceNames.INVENTORY_SERVICE.value)
            inventory_section = InventorySection(
                available_quantity=0,
                reserved_quantity=0,
                in_stock=False,
                warehouse_code="N/A",
                is_fallback=True,
            )
        else:
            stock_dto = StockResponse.model_validate(inv_resp.json())
            inventory_section = InventorySection(
                available_quantity=stock_dto.available_quantity,
                reserved_quantity=stock_dto.reserved_quantity,
                in_stock=stock_dto.in_stock,
                warehouse_code=stock_dto.warehouse_code,
                is_fallback=False,
            )

        # 3. Reviews is NON-CRITICAL: Apply graceful degradation fallback
        if rev_err is not None or rev_resp is None or rev_resp.status_code != 200:
            degraded_services.append(ServiceNames.REVIEWS_SERVICE.value)
            reviews_section = ReviewsSection(
                average_rating=0.0,
                total_reviews=0,
                recent_reviews=[],
                is_fallback=True,
            )
        else:
            reviews_dto = ProductReviewsResponse.model_validate(rev_resp.json())
            snippets = [
                ReviewSnippet(
                    id=r.id,
                    author=r.author,
                    rating=r.rating,
                    comment=r.comment,
                )
                for r in reviews_dto.reviews[:3]
            ]
            reviews_section = ReviewsSection(
                average_rating=reviews_dto.average_rating,
                total_reviews=reviews_dto.total_reviews,
                recent_reviews=snippets,
                is_fallback=False,
            )

        telemetry = AggregationTelemetry(
            mode=mode,
            total_latency_ms=total_latency_ms,
            sum_of_downstream_ms=sum_of_downstream_ms,
            latency_saved_ms=latency_saved_ms,
            downstream_timings_ms={
                "product_service_ms": prod_ms,
                "inventory_service_ms": inv_ms,
                "reviews_service_ms": rev_ms,
            },
            degraded_services=degraded_services,
        )

        return ProductPageResponse(
            product_id=product_id,
            composition_status="degraded" if degraded_services else "complete",
            product=product_section,
            inventory=inventory_section,
            reviews=reviews_section,
            telemetry=telemetry,
        )


class OrderPageAggregator:
    """Aggregates DDD Order Aggregate with catalog details and live stock levels."""

    def __init__(self, registry: DownstreamClientRegistry) -> None:
        self.registry = registry

    async def compose_order_page(self, order_id: str) -> OrderPageResponse:
        order_client = self.registry.get_client("order")
        product_client = self.registry.get_client("product")
        inventory_client = self.registry.get_client("inventory")

        wall_start = time.perf_counter()

        # 1. Fetch Order Aggregate Root from Order Service
        order_resp, order_ms, order_err = await timed_get(
            order_client, f"{ApiEndpoints.ORDERS}/{order_id}"
        )
        if order_err is not None or order_resp is None or order_resp.status_code != 200:
            if order_resp is not None and order_resp.status_code == 404:
                raise ProblemDetailsException(
                    status=status.HTTP_404_NOT_FOUND,
                    title=ErrorTitles.ORDER_NOT_FOUND,
                    detail=f"Order '{order_id}' was not found.",
                    type_uri=ErrorTypes.ORDER_NOT_FOUND,
                )
            raise ProblemDetailsException(
                status=status.HTTP_502_BAD_GATEWAY,
                title=ErrorTitles.PRODUCT_ERROR,
                detail="Failed to retrieve order aggregate root.",
                type_uri=ErrorTypes.BAD_GATEWAY,
            )

        order_dto = OrderResponse.model_validate(order_resp.json())

        # 2. Concurrently enrich each line item with Product and Inventory
        async def enrich_item(item: OrderLineItemResponse) -> tuple[OrderLineItemView, float]:
            p_id = item.product_id
            p_resp, p_ms, _ = await timed_get(product_client, f"{ApiEndpoints.PRODUCTS}/{p_id}")
            i_resp, i_ms, _ = await timed_get(inventory_client, f"{ApiEndpoints.STOCK}/{p_id}")

            available = None
            inv_status = "unavailable"
            if i_resp is not None and i_resp.status_code == 200:
                stock_dto = StockResponse.model_validate(i_resp.json())
                available = stock_dto.available_quantity
                inv_status = "in_stock" if available >= item.quantity else "low_stock"

            p_name = item.product_name
            if p_resp is not None and p_resp.status_code == 200:
                product_cat_dto = ProductResponse.model_validate(p_resp.json())
                p_name = product_cat_dto.name

            view = OrderLineItemView(
                sku=item.sku,
                product_id=p_id,
                product_name=p_name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=item.subtotal,
                inventory_available=available,
                inventory_status=inv_status,
            )
            return view, p_ms + i_ms

        enriched_tasks = [enrich_item(item) for item in order_dto.items]
        enriched_results = await asyncio.gather(*enriched_tasks) if enriched_tasks else []

        views = [res[0] for res in enriched_results]
        enrichment_sum_ms = sum(res[1] for res in enriched_results)

        total_latency_ms = round((time.perf_counter() - wall_start) * 1000.0, 2)
        sum_of_downstream_ms = round(order_ms + enrichment_sum_ms, 2)
        latency_saved_ms = max(0.0, round(sum_of_downstream_ms - total_latency_ms, 2))

        telemetry = AggregationTelemetry(
            mode="parallel",
            total_latency_ms=total_latency_ms,
            sum_of_downstream_ms=sum_of_downstream_ms,
            latency_saved_ms=latency_saved_ms,
            downstream_timings_ms={"order_service_ms": order_ms},
            degraded_services=[],
        )

        return OrderPageResponse(
            order_id=order_dto.id,
            customer_id=order_dto.customer_id,
            status=order_dto.status,
            version=order_dto.version,
            total_amount=order_dto.total_amount,
            currency=order_dto.currency,
            items=views,
            telemetry=telemetry,
        )
