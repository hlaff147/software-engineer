"""Generic pagination envelope adhering to REST contract-first standards."""

from __future__ import annotations

import math
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

__all__ = ["PaginatedResponse"]

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard pagination envelope."""

    items: list[T] = Field(..., description="List of items for the current page.")
    page: int = Field(..., ge=1, description="Current page number (1-indexed).")
    page_size: int = Field(..., ge=1, description="Number of items per page.")
    total_count: int = Field(..., ge=0, description="Total count of items across all pages.")
    total_pages: int = Field(..., ge=0, description="Total number of pages available.")

    @classmethod
    def create(
        cls,
        items: list[T],
        total_count: int,
        page: int,
        page_size: int,
    ) -> PaginatedResponse[T]:
        """Factory method to compute total_pages and assemble response."""
        total_pages = math.ceil(total_count / page_size) if total_count > 0 else 0
        return cls(
            items=items,
            page=page,
            page_size=page_size,
            total_count=total_count,
            total_pages=total_pages,
        )
