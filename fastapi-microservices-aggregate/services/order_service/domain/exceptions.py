"""Domain-specific exceptions representing business invariant violations."""

from __future__ import annotations

__all__ = [
    "DomainException",
    "DomainInvariantViolation",
    "InvalidOrderStateError",
    "LineItemNotFoundError",
    "OptimisticConcurrencyError",
    "OrderNotFoundError",
]


class DomainException(Exception):
    """Base exception for all domain logic failures."""


class DomainInvariantViolation(DomainException):
    """Raised when an action violates an aggregate invariant (e.g. max total, item limits)."""


class InvalidOrderStateError(DomainException):
    """Raised when an operation is invalid for the aggregate's current state (e.g. modifying confirmed order)."""


class OptimisticConcurrencyError(DomainException):
    """Raised when an update conflicts with a newer version of the aggregate root."""


class OrderNotFoundError(DomainException):
    """Raised when an order aggregate cannot be found."""


class LineItemNotFoundError(DomainException):
    """Raised when a specific item SKU does not exist within the order aggregate."""
