"""Domain layer for Order Service."""

from __future__ import annotations

from services.order_service.domain.events import (
    DomainEvent,
    OrderCancelled,
    OrderConfirmed,
    OrderCreated,
    OrderItemAdded,
    OrderItemQuantityUpdated,
    OrderItemRemoved,
)
from services.order_service.domain.exceptions import (
    DomainException,
    DomainInvariantViolation,
    InvalidOrderStateError,
    LineItemNotFoundError,
    OptimisticConcurrencyError,
    OrderNotFoundError,
)
from services.order_service.domain.order_aggregate import Order, OrderLineItem, OrderStatus
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)

__all__ = [
    "CustomerId",
    "DomainEvent",
    "DomainException",
    "DomainInvariantViolation",
    "InvalidOrderStateError",
    "LineItemNotFoundError",
    "Money",
    "OptimisticConcurrencyError",
    "Order",
    "OrderCancelled",
    "OrderConfirmed",
    "OrderCreated",
    "OrderId",
    "OrderItemAdded",
    "OrderItemQuantityUpdated",
    "OrderItemRemoved",
    "OrderLineItem",
    "OrderNotFoundError",
    "OrderStatus",
    "ProductId",
    "Quantity",
    "Sku",
]
