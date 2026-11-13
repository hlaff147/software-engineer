"""SQLAlchemy models for Product Service."""

from __future__ import annotations

from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.constants import DomainConstants, TableNames
from shared.db import Base

__all__ = ["ProductModel"]


class ProductModel(Base):
    """Database entity representing a product catalog item."""

    __tablename__ = TableNames.PRODUCTS

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False, default="")
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(
        String(3), nullable=False, default=DomainConstants.DEFAULT_CURRENCY
    )
    category: Mapped[str] = mapped_column(String(100), nullable=False, default="general")
