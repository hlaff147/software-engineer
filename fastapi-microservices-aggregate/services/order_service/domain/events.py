"""Domain events emitted by the Order Aggregate Root for Transactional Outbox."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

__all__ = [
    "DomainEvent",
    "OrderCancelled",
    "OrderConfirmed",
    "OrderCreated",
    "OrderItemAdded",
    "OrderItemQuantityUpdated",
    "OrderItemRemoved",
]


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for all immutable domain events."""

    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def event_type(self) -> str:
        return self.__class__.__name__

    def to_payload(self) -> dict[str, Any]:
        """Serializes event details for database outbox storage."""
        data: dict[str, Any] = {}
        for key in self.__slots__:
            if key in ("event_id", "occurred_at"):
                continue
            val = getattr(self, key)
            if hasattr(val, "amount"):
                data[key] = str(val.amount)
            elif hasattr(val, "value"):
                data[key] = val.value
            else:
                data[key] = val
        return data


@dataclass(frozen=True, slots=True)
class OrderCreated(DomainEvent):
    order_id: str = ""
    customer_id: str = ""
    currency: str = "USD"


@dataclass(frozen=True, slots=True)
class OrderItemAdded(DomainEvent):
    order_id: str = ""
    sku: str = ""
    product_id: int = 0
    product_name: str = ""
    quantity: int = 0
    unit_price: str = "0.00"
    subtotal: str = "0.00"


@dataclass(frozen=True, slots=True)
class OrderItemQuantityUpdated(DomainEvent):
    order_id: str = ""
    sku: str = ""
    old_quantity: int = 0
    new_quantity: int = 0
    new_subtotal: str = "0.00"


@dataclass(frozen=True, slots=True)
class OrderItemRemoved(DomainEvent):
    order_id: str = ""
    sku: str = ""


@dataclass(frozen=True, slots=True)
class OrderConfirmed(DomainEvent):
    order_id: str = ""
    total_amount: str = "0.00"
    items_count: int = 0


@dataclass(frozen=True, slots=True)
class OrderCancelled(DomainEvent):
    order_id: str = ""
    reason: str = ""
