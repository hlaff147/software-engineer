"""Pydantic schemas for Reviews Service."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["ProductReviewsResponse", "ReviewCreate", "ReviewItem"]


class ReviewCreate(BaseModel):
    author: str = Field(..., min_length=2, max_length=100, examples=["Alice Engineer"])
    rating: int = Field(..., ge=1, le=5, examples=[5])
    comment: str = Field(default="", max_length=1000, examples=["Outstanding performance!"])


class ReviewItem(BaseModel):
    id: int
    product_id: int
    author: str
    rating: int
    comment: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductReviewsResponse(BaseModel):
    product_id: int
    average_rating: float = Field(..., ge=0.0, le=5.0)
    total_reviews: int = Field(..., ge=0)
    reviews: list[ReviewItem]

    model_config = ConfigDict(from_attributes=True)
