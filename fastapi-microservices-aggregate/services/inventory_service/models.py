"""SQLAlchemy models for Inventory Service."""

from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from shared.db import Base

__all__ = ["StockItemModel"]


class StockItemModel(Base):
    """Database entity representing stock levels for a product."""

    __tablename__ = "stock_items"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reserved_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    warehouse_code: Mapped[str] = mapped_column(String(32), nullable=False, default="WH-MAIN")
