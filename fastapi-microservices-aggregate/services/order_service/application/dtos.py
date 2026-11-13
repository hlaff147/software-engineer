"""Application DTOs and Command models for Order Service."""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "AddOrderItemCommand",
    "CancelOrderCommand",
    "CreateOrderCommand",
    "OrderLineItemResponse",
    "OrderResponse",
    "OutboxEventResponse",
    "UpdateItemQuantityCommand",
]


class CreateOrderCommand(BaseModel):
    customer_id: str = Field(..., min_length=1, max_length=64, examples=["cust-1001"])
    currency: str = Field(default="USD", min_length=3, max_length=3, examples=["USD"])


class AddOrderItemCommand(BaseModel):
    product_id: int = Field(..., gt=0, examples=[42])
    sku: str = Field(..., min_length=3, max_length=64, examples=["TECH-LAPTOP-42"])
    product_name: str = Field(..., min_length=1, max_length=255, examples=["UltraPro Laptop"])
    unit_price: Decimal = Field(..., gt=0, examples=[Decimal("2499.00")])
    quantity: int = Field(..., ge=1, le=10, examples=[1])
    expected_version: int | None = Field(
        default=None,
        description="Optional expected aggregate version for optimistic concurrency control",
    )


class UpdateItemQuantityCommand(BaseModel):
    quantity: int = Field(..., ge=1, le=10, examples=[3])
    expected_version: int | None = Field(
        default=None,
        description="Optional expected aggregate version for optimistic concurrency control",
    )


class CancelOrderCommand(BaseModel):
    reason: str = Field(default="Customer requested cancellation", max_length=255)
    expected_version: int | None = None


class OrderLineItemResponse(BaseModel):
    line_item_id: str
    product_id: int
    sku: str
    product_name: str
    unit_price: Decimal
    quantity: int
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    currency: str
    status: str
    version: int
    total_amount: Decimal
    items: list[OrderLineItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OutboxEventResponse(BaseModel):
    event_id: str
    order_id: str
    event_type: str
    payload: dict[str, Any]
    occurred_at: str
    processed: bool
