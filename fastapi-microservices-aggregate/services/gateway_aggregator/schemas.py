"""Pydantic schemas for Gateway Aggregator."""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

__all__ = [
    "AggregationTelemetry",
    "InventorySection",
    "OrderLineItemView",
    "OrderPageResponse",
    "ProductPageResponse",
    "ProductSection",
    "ReviewsSection",
]


class ProductSection(BaseModel):
    id: int
    sku: str
    name: str
    description: str
    price: Decimal
    currency: str
    category: str


class InventorySection(BaseModel):
    available_quantity: int
    reserved_quantity: int
    in_stock: bool
    warehouse_code: str
    is_fallback: bool = False


class ReviewSnippet(BaseModel):
    id: int
    author: str
    rating: int
    comment: str


class ReviewsSection(BaseModel):
    average_rating: float
    total_reviews: int
    recent_reviews: list[ReviewSnippet] = Field(default_factory=list)
    is_fallback: bool = False


class AggregationTelemetry(BaseModel):
    mode: Literal["parallel", "sequential"]
    total_latency_ms: float
    sum_of_downstream_ms: float
    latency_saved_ms: float
    downstream_timings_ms: dict[str, float]
    degraded_services: list[str] = Field(default_factory=list)


class ProductPageResponse(BaseModel):
    product_id: int
    composition_status: Literal["complete", "degraded"]
    product: ProductSection
    inventory: InventorySection
    reviews: ReviewsSection
    telemetry: AggregationTelemetry


class OrderLineItemView(BaseModel):
    sku: str
    product_id: int
    product_name: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    inventory_available: int | None = None
    inventory_status: str = "unknown"


class OrderPageResponse(BaseModel):
    order_id: str
    customer_id: str
    status: str
    version: int
    total_amount: Decimal
    currency: str
    items: list[OrderLineItemView]
    telemetry: AggregationTelemetry
