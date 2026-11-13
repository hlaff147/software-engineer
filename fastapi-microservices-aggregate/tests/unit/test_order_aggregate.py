"""Unit tests for DDD Order Aggregate Root invariants and behavior."""

from __future__ import annotations

from decimal import Decimal

import pytest

from services.order_service.domain.events import OrderConfirmed, OrderCreated, OrderItemAdded
from services.order_service.domain.exceptions import (
    DomainInvariantViolation,
    InvalidOrderStateError,
    LineItemNotFoundError,
)
from services.order_service.domain.order_aggregate import Order, OrderStatus
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)


def test_order_creation_emits_created_event() -> None:
    order = Order.create(OrderId("ord-001"), CustomerId("cust-1"), currency="USD")

    assert order.status == OrderStatus.DRAFT
    assert order.version == 1
    assert order.total_amount == Money(Decimal("0.00"), "USD")
    assert len(order.items) == 0

    events = order.pull_domain_events()
    assert len(events) == 1
    assert isinstance(events[0], OrderCreated)
    assert events[0].order_id == "ord-001"
    # Drained events list should be empty now
    assert len(order.pull_domain_events()) == 0


def test_add_item_enforces_invariants_and_calculates_total() -> None:
    order = Order.create(OrderId("ord-002"), CustomerId("cust-1"), currency="USD")

    order.add_item(
        product_id=ProductId(42),
        sku=Sku("TECH-LAPTOP-42"),
        product_name="Pro Laptop",
        unit_price=Money(Decimal("1500.00"), "USD"),
        quantity=Quantity(2),
    )

    assert len(order.items) == 1
    assert order.total_amount == Money(Decimal("3000.00"), "USD")
    assert order.version == 2

    # Consolidating existing SKU
    order.add_item(
        product_id=ProductId(42),
        sku=Sku("TECH-LAPTOP-42"),
        product_name="Pro Laptop",
        unit_price=Money(Decimal("1500.00"), "USD"),
        quantity=Quantity(3),
    )

    assert len(order.items) == 1
    assert order.items[0].quantity.value == 5
    assert order.total_amount == Money(Decimal("7500.00"), "USD")
    assert order.version == 3


def test_cannot_mutate_aggregate_items_collection_directly() -> None:
    order = Order.create(OrderId("ord-003"), CustomerId("cust-1"))
    order.add_item(
        product_id=ProductId(42),
        sku=Sku("TECH-LAPTOP-42"),
        product_name="Laptop",
        unit_price=Money(Decimal("1000.00")),
        quantity=Quantity(1),
    )

    # Outside references cannot mutate items because it is an immutable tuple
    items_snapshot = order.items
    assert isinstance(items_snapshot, tuple)
    with pytest.raises(AttributeError):
        # Tuple has no append or pop
        items_snapshot.append(None)  # type: ignore[attr-defined]


def test_exceeding_per_line_item_quantity_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Maximum allowed quantity"):
        Quantity(11)


def test_consolidating_sku_beyond_max_quantity_raises_invariant_violation() -> None:
    order = Order.create(OrderId("ord-004"), CustomerId("cust-1"))
    order.add_item(
        product_id=ProductId(42),
        sku=Sku("TECH-LAPTOP-42"),
        product_name="Laptop",
        unit_price=Money(Decimal("1000.00")),
        quantity=Quantity(8),
    )

    with pytest.raises(DomainInvariantViolation, match="exceeds max limit"):
        order.add_item(
            product_id=ProductId(42),
            sku=Sku("TECH-LAPTOP-42"),
            product_name="Laptop",
            unit_price=Money(Decimal("1000.00")),
            quantity=Quantity(3),  # 8 + 3 = 11 > 10
        )


def test_order_total_cannot_exceed_max_cap() -> None:
    order = Order.create(OrderId("ord-005"), CustomerId("cust-1"))

    # Invariant: MAX_ORDER_TOTAL is $50,000.00
    with pytest.raises(DomainInvariantViolation, match="exceeding maximum allowed order cap"):
        order.add_item(
            product_id=ProductId(99),
            sku=Sku("TECH-SUPERCOMPUTER"),
            product_name="HPC Cluster",
            unit_price=Money(Decimal("30000.00")),
            quantity=Quantity(2),  # 60,000 > 50,000
        )


def test_currency_mismatch_rejected() -> None:
    order = Order.create(OrderId("ord-006"), CustomerId("cust-1"), currency="USD")

    with pytest.raises(DomainInvariantViolation, match="Currency mismatch"):
        order.add_item(
            product_id=ProductId(42),
            sku=Sku("TECH-EUR-ITEM"),
            product_name="European Item",
            unit_price=Money(Decimal("100.00"), "EUR"),
            quantity=Quantity(1),
        )


def test_confirm_empty_order_rejected() -> None:
    order = Order.create(OrderId("ord-007"), CustomerId("cust-1"))
    with pytest.raises(DomainInvariantViolation, match="Cannot confirm an empty order"):
        order.confirm()


def test_order_lifecycle_confirm_and_lock_mutations() -> None:
    order = Order.create(OrderId("ord-008"), CustomerId("cust-1"))
    order.add_item(
        product_id=ProductId(42),
        sku=Sku("TECH-LAPTOP-42"),
        product_name="Laptop",
        unit_price=Money(Decimal("1000.00")),
        quantity=Quantity(1),
    )

    order.confirm()
    assert order.status == OrderStatus.CONFIRMED

    # Any mutation on confirmed aggregate must be rejected
    with pytest.raises(InvalidOrderStateError, match="not in DRAFT status"):
        order.add_item(
            product_id=ProductId(43),
            sku=Sku("ACC-KEYBOARD-43"),
            product_name="Keyboard",
            unit_price=Money(Decimal("100.00")),
            quantity=Quantity(1),
        )

    with pytest.raises(InvalidOrderStateError, match="not in DRAFT status"):
        order.remove_item(Sku("TECH-LAPTOP-42"))

    events = order.pull_domain_events()
    event_types = [type(e) for e in events]
    assert OrderCreated in event_types
    assert OrderItemAdded in event_types
    assert OrderConfirmed in event_types


def test_remove_nonexistent_item_raises_not_found() -> None:
    order = Order.create(OrderId("ord-009"), CustomerId("cust-1"))
    with pytest.raises(LineItemNotFoundError):
        order.remove_item(Sku("NONEXISTENT-SKU"))
