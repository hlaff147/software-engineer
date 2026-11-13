"""Idempotent seed data for Product Service."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.product_service.models import ProductModel

__all__ = ["seed_products"]

INITIAL_PRODUCTS = [
    {
        "id": 42,
        "sku": "TECH-LAPTOP-42",
        "name": "UltraPro Developer Laptop 16-inch",
        "description": "High-performance workstation with 64GB Unified Memory and 2TB SSD.",
        "price": Decimal("2499.00"),
        "currency": "USD",
        "category": "workstations",
    },
    {
        "id": 43,
        "sku": "ACC-KEYBOARD-43",
        "name": "Mechanical Ergonomic Split Keyboard",
        "description": "Hot-swappable tactile switches with low-profile keycaps.",
        "price": Decimal("189.50"),
        "currency": "USD",
        "category": "accessories",
    },
    {
        "id": 44,
        "sku": "ACC-MOUSE-44",
        "name": "Precision Wireless Trackball",
        "description": "Ergonomic 2.4GHz + Bluetooth multi-device trackball.",
        "price": Decimal("99.99"),
        "currency": "USD",
        "category": "accessories",
    },
]


async def seed_products(session: AsyncSession) -> None:
    """Inserts initial demo products if they do not already exist."""
    for item in INITIAL_PRODUCTS:
        stmt = select(ProductModel).where(ProductModel.id == item["id"])
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing is None:
            product = ProductModel(
                id=item["id"],
                sku=item["sku"],
                name=item["name"],
                description=item["description"],
                price=item["price"],
                currency=item["currency"],
                category=item["category"],
            )
            session.add(product)
    await session.commit()
