"""Pydantic schemas for Product Service."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from shared.constants import DomainConstants

__all__ = ["ProductCreate", "ProductResponse", "ProductUpdate"]


class ProductCreate(BaseModel):
    sku: str = Field(..., min_length=3, max_length=64, examples=["TECH-LAPTOP-42"])
    name: str = Field(
        ..., min_length=1, max_length=255, examples=["UltraPro Developer Laptop 16-inch"]
    )
    description: str = Field(default="", max_length=1000)
    price: Decimal = Field(..., gt=0, examples=[Decimal("1999.99")])
    currency: str = Field(default=DomainConstants.DEFAULT_CURRENCY, min_length=3, max_length=3)
    category: str = Field(default="electronics", max_length=100)

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    price: Decimal | None = Field(default=None, gt=0)
    category: str | None = Field(default=None, max_length=100)

    model_config = ConfigDict(from_attributes=True)


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: str
    price: Decimal
    currency: str
    category: str

    model_config = ConfigDict(from_attributes=True)
