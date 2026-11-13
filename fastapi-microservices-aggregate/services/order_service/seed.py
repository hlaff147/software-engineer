"""Idempotent seed data for Order Service."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from services.order_service.domain.order_aggregate import Order
from services.order_service.domain.value_objects import (
    CustomerId,
    Money,
    OrderId,
    ProductId,
    Quantity,
    Sku,
)
from services.order_service.infrastructure.repository import SqlAlchemyOrderRepository

__all__ = ["DEMO_ORDER_ID", "seed_orders"]

DEMO_ORDER_ID = "00000000-0000-4000-8000-000000000042"


async def seed_orders(session: AsyncSession) -> None:
    """Seeds a sample confirmed order if it does not already exist."""
    repo = SqlAlchemyOrderRepository(session)
    existing = await repo.get_by_id(OrderId(DEMO_ORDER_ID))
    if existing is None:
        order = Order.create(
            order_id=OrderId(DEMO_ORDER_ID),
            customer_id=CustomerId("cust-vip-100"),
            currency="USD",
        )
        order.add_item(
            product_id=ProductId(42),
            sku=Sku("TECH-LAPTOP-42"),
            product_name="UltraPro Developer Laptop 16-inch",
            unit_price=Money(Decimal("2499.00"), "USD"),
            quantity=Quantity(1),
        )
        order.add_item(
            product_id=ProductId(43),
            sku=Sku("ACC-KEYBOARD-43"),
            product_name="Mechanical Ergonomic Split Keyboard",
            unit_price=Money(Decimal("189.50"), "USD"),
            quantity=Quantity(2),
        )
        order.confirm()
        await repo.save(order)
