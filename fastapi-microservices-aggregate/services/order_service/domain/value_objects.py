"""Domain Value Objects for the Order Aggregate."""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

from shared.constants import DomainConstants

__all__ = ["CustomerId", "Money", "OrderId", "ProductId", "Quantity", "Sku"]

_SKU_REGEX = re.compile(r"^[A-Z0-9\-_]{3,64}$")


@dataclass(frozen=True, slots=True)
class Money:
    """Immutable monetary value object enforcing two-decimal exact arithmetic."""

    amount: Decimal
    currency: str = DomainConstants.DEFAULT_CURRENCY

    def __post_init__(self) -> None:
        if not isinstance(self.amount, Decimal):
            object.__setattr__(self, "amount", Decimal(str(self.amount)))
        # Quantize to 2 decimal places
        quantized = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", quantized)
        object.__setattr__(self, "currency", self.currency.upper())

        if self.amount < Decimal("0.00"):
            raise ValueError(f"Monetary amount cannot be negative: {self.amount}")

    def __add__(self, other: Money) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )
        return Money(self.amount + other.amount, self.currency)

    def __mul__(self, factor: int | Decimal) -> Money:
        if isinstance(factor, int):
            factor = Decimal(factor)
        if not isinstance(factor, Decimal):
            return NotImplemented
        return Money(self.amount * factor, self.currency)

    def __lt__(self, other: Money) -> bool:
        if not isinstance(other, Money) or self.currency != other.currency:
            return NotImplemented
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        if not isinstance(other, Money) or self.currency != other.currency:
            return NotImplemented
        return self.amount <= other.amount


@dataclass(frozen=True, slots=True)
class Sku:
    """Immutable Stock Keeping Unit value object."""

    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().upper()
        if not _SKU_REGEX.match(normalized):
            raise ValueError(
                f"Invalid SKU format '{self.value}'. Must be 3-64 alphanumeric characters, dashes, or underscores."
            )
        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Quantity:
    """Immutable item quantity value object enforcing per-item limits."""

    value: int

    def __post_init__(self) -> None:
        if not isinstance(self.value, int):
            raise ValueError("Quantity must be an integer.")
        if self.value < DomainConstants.MIN_QUANTITY_PER_LINE_ITEM:
            raise ValueError(
                f"Quantity must be at least {DomainConstants.MIN_QUANTITY_PER_LINE_ITEM}."
            )
        if self.value > DomainConstants.MAX_QUANTITY_PER_LINE_ITEM:
            raise ValueError(
                f"Maximum allowed quantity per order line item is {DomainConstants.MAX_QUANTITY_PER_LINE_ITEM} units."
            )

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class OrderId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("OrderId cannot be empty.")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class CustomerId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("CustomerId cannot be empty.")
        object.__setattr__(self, "value", self.value.strip())

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ProductId:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("ProductId must be a positive integer.")

    def __int__(self) -> int:
        return self.value
