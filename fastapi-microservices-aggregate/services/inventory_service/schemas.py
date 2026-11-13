"""Pydantic schemas for Inventory Service."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, computed_field

__all__ = ["StockResponse", "StockUpdate"]


class StockUpdate(BaseModel):
    available_quantity: int | None = Field(default=None, ge=0)
    reserved_quantity: int | None = Field(default=None, ge=0)


class StockResponse(BaseModel):
    product_id: int
    sku: str
    available_quantity: int
    reserved_quantity: int
    warehouse_code: str

    @computed_field
    @property
    def in_stock(self) -> bool:
        return self.available_quantity > 0

    model_config = ConfigDict(from_attributes=True)
