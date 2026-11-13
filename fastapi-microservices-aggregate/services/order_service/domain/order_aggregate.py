"""DDD Order Aggregate Root and LineItem Entity.

An Aggregate is a cluster of associated domain objects treated as a single unit
for data changes. References from outside the aggregate should go only to the root.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum
from typing import ClassVar

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
    DomainInvariantViolation,
    InvalidOrderStateError,
    LineItemNotFoundError,
)
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)

__all__ = ["Order", "OrderLineItem", "OrderStatus"]


class OrderStatus(StrEnum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass(slots=True)
class OrderLineItem:
    """Internal Entity belonging strictly to the Order Aggregate boundary."""

    line_item_id: str
    product_id: ProductId
    sku: Sku
    product_name: str
    unit_price: Money
    quantity: Quantity

    @property
    def subtotal(self) -> Money:
        return self.unit_price * self.quantity.value


@dataclass(slots=True)
class Order:
    """Aggregate Root: Sole entry point for all state mutations and domain invariant checks."""

    MAX_ORDER_TOTAL: ClassVar[Decimal] = Decimal("50000.00")
    MAX_ITEMS_PER_ORDER: ClassVar[int] = 50

    order_id: OrderId
    customer_id: CustomerId
    currency: str = "USD"
    status: OrderStatus = OrderStatus.DRAFT
    version: int = 1
    _loaded_version: int = 1
    _items: dict[str, OrderLineItem] = field(default_factory=dict)
    _domain_events: list[DomainEvent] = field(default_factory=list, repr=False)

    @classmethod
    def create(
        cls,
        order_id: OrderId,
        customer_id: CustomerId,
        currency: str = "USD",
    ) -> Order:
        """Factory method to instantiate a new Order Aggregate Root."""
        order = cls(
            order_id=order_id,
            customer_id=customer_id,
            currency=currency.upper(),
            status=OrderStatus.DRAFT,
            version=1,
            _loaded_version=0,  # 0 indicates brand new entity not yet persisted
        )
        order._record_event(
            OrderCreated(
                order_id=str(order_id),
                customer_id=str(customer_id),
                currency=order.currency,
            )
        )
        return order

    @property
    def items(self) -> tuple[OrderLineItem, ...]:
        """Provides an immutable snapshot of line items. Outside callers cannot mutate directly."""
        return tuple(self._items.values())

    @property
    def total_amount(self) -> Money:
        """Calculates aggregate total by summing all encapsulated line item subtotals."""
        total = sum(
            (item.subtotal.amount for item in self._items.values()),
            Decimal("0.00"),
        )
        return Money(total, self.currency)

    def add_item(
        self,
        product_id: ProductId,
        sku: Sku,
        product_name: str,
        unit_price: Money,
        quantity: Quantity,
    ) -> OrderLineItem:
        """Adds or consolidates a line item while enforcing aggregate invariants."""
        self._ensure_draft_state("Cannot add items to an order that is not in DRAFT status.")

        if unit_price.currency != self.currency:
            raise DomainInvariantViolation(
                f"Currency mismatch: Item currency '{unit_price.currency}' does not match order currency '{self.currency}'."
            )

        sku_key = str(sku)
        if sku_key in self._items:
            existing = self._items[sku_key]
            new_qty_val = existing.quantity.value + quantity.value
            try:
                new_qty = Quantity(new_qty_val)
            except ValueError as err:
                raise DomainInvariantViolation(
                    f"Consolidating item '{sku_key}' exceeds max limit: {err}"
                ) from err

            # Evaluate prospective new total
            prospective_subtotal = existing.unit_price * new_qty.value
            current_other_total = sum(
                (it.subtotal.amount for k, it in self._items.items() if k != sku_key),
                Decimal("0.00"),
            )
            if (current_other_total + prospective_subtotal.amount) > self.MAX_ORDER_TOTAL:
                raise DomainInvariantViolation(
                    f"Adding item exceeds aggregate maximum total of ${self.MAX_ORDER_TOTAL:,.2f}."
                )

            old_qty = existing.quantity.value
            existing.quantity = new_qty
            self.version += 1
            self._record_event(
                OrderItemQuantityUpdated(
                    order_id=str(self.order_id),
                    sku=sku_key,
                    old_quantity=old_qty,
                    new_quantity=new_qty_val,
                    new_subtotal=str(existing.subtotal.amount),
                )
            )
            return existing

        if len(self._items) >= self.MAX_ITEMS_PER_ORDER:
            raise DomainInvariantViolation(
                f"Order cannot contain more than {self.MAX_ITEMS_PER_ORDER} distinct items."
            )

        item = OrderLineItem(
            line_item_id=str(uuid.uuid4()),
            product_id=product_id,
            sku=sku,
            product_name=product_name,
            unit_price=unit_price,
            quantity=quantity,
        )

        # Invariant: Total order amount cannot exceed MAX_ORDER_TOTAL
        new_total_amount = self.total_amount.amount + item.subtotal.amount
        if new_total_amount > self.MAX_ORDER_TOTAL:
            raise DomainInvariantViolation(
                f"Adding item would result in total ${new_total_amount:,.2f}, "
                f"exceeding maximum allowed order cap of ${self.MAX_ORDER_TOTAL:,.2f}."
            )

        self._items[sku_key] = item
        self.version += 1
        self._record_event(
            OrderItemAdded(
                order_id=str(self.order_id),
                sku=sku_key,
                product_id=int(product_id),
                product_name=product_name,
                quantity=quantity.value,
                unit_price=str(unit_price.amount),
                subtotal=str(item.subtotal.amount),
            )
        )
        return item

    def update_item_quantity(self, sku: Sku, new_quantity: Quantity) -> OrderLineItem:
        """Updates the quantity of an existing line item, re-validating aggregate invariants."""
        self._ensure_draft_state(
            "Cannot update item quantity in an order that is not in DRAFT status."
        )

        sku_key = str(sku)
        if sku_key not in self._items:
            raise LineItemNotFoundError(f"Item with SKU '{sku_key}' not found in order.")

        item = self._items[sku_key]
        old_qty = item.quantity.value
        if old_qty == new_quantity.value:
            return item

        # Verify prospective total cap
        other_total = sum(
            (it.subtotal.amount for k, it in self._items.items() if k != sku_key),
            Decimal("0.00"),
        )
        new_subtotal = item.unit_price * new_quantity.value
        if (other_total + new_subtotal.amount) > self.MAX_ORDER_TOTAL:
            raise DomainInvariantViolation(
                f"Updating item quantity exceeds maximum allowed order cap of ${self.MAX_ORDER_TOTAL:,.2f}."
            )

        item.quantity = new_quantity
        self.version += 1
        self._record_event(
            OrderItemQuantityUpdated(
                order_id=str(self.order_id),
                sku=sku_key,
                old_quantity=old_qty,
                new_quantity=new_quantity.value,
                new_subtotal=str(item.subtotal.amount),
            )
        )
        return item

    def remove_item(self, sku: Sku) -> None:
        """Removes a line item by SKU."""
        self._ensure_draft_state("Cannot remove items from an order that is not in DRAFT status.")

        sku_key = str(sku)
        if sku_key not in self._items:
            raise LineItemNotFoundError(f"Item with SKU '{sku_key}' not found in order.")

        del self._items[sku_key]
        self.version += 1
        self._record_event(OrderItemRemoved(order_id=str(self.order_id), sku=sku_key))

    def confirm(self) -> None:
        """Transitions order state to CONFIRMED."""
        self._ensure_draft_state("Only orders in DRAFT status can be confirmed.")

        if not self._items:
            raise DomainInvariantViolation(
                "Cannot confirm an empty order. At least one line item is required."
            )

        self.status = OrderStatus.CONFIRMED
        self.version += 1
        self._record_event(
            OrderConfirmed(
                order_id=str(self.order_id),
                total_amount=str(self.total_amount.amount),
                items_count=len(self._items),
            )
        )

    def cancel(self, reason: str = "Customer requested cancellation") -> None:
        """Transitions order state to CANCELLED."""
        if self.status == OrderStatus.CANCELLED:
            raise InvalidOrderStateError("Order is already cancelled.")

        self.status = OrderStatus.CANCELLED
        self.version += 1
        self._record_event(OrderCancelled(order_id=str(self.order_id), reason=reason))

    def pull_domain_events(self) -> list[DomainEvent]:
        """Drains and returns all pending domain events recorded by this aggregate root."""
        events = list(self._domain_events)
        self._domain_events.clear()
        return events

    def _ensure_draft_state(self, message: str) -> None:
        if self.status != OrderStatus.DRAFT:
            raise InvalidOrderStateError(f"{message} Current order status is '{self.status}'.")

    def _record_event(self, event: DomainEvent) -> None:
        self._domain_events.append(event)
