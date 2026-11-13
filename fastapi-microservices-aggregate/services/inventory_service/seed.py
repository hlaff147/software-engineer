"""Idempotent seed data for Inventory Service."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.inventory_service.models import StockItemModel

__all__ = ["seed_inventory"]

INITIAL_STOCK = [
    {
        "product_id": 42,
        "sku": "TECH-LAPTOP-42",
        "available_quantity": 25,
        "reserved_quantity": 3,
        "warehouse_code": "WH-US-EAST",
    },
    {
        "product_id": 43,
        "sku": "ACC-KEYBOARD-43",
        "available_quantity": 120,
        "reserved_quantity": 5,
        "warehouse_code": "WH-US-WEST",
    },
    {
        "product_id": 44,
        "sku": "ACC-MOUSE-44",
        "available_quantity": 0,
        "reserved_quantity": 0,
        "warehouse_code": "WH-US-CENTRAL",
    },
]


async def seed_inventory(session: AsyncSession) -> None:
    """Inserts initial stock records if they do not exist."""
    for item in INITIAL_STOCK:
        stmt = select(StockItemModel).where(StockItemModel.product_id == item["product_id"])
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing is None:
            stock = StockItemModel(
                product_id=item["product_id"],
                sku=item["sku"],
                available_quantity=item["available_quantity"],
                reserved_quantity=item["reserved_quantity"],
                warehouse_code=item["warehouse_code"],
            )
            session.add(stock)
    await session.commit()
