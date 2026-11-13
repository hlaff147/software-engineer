"""Idempotent seed data for Reviews Service."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.reviews_service.models import ReviewModel

__all__ = ["seed_reviews"]

INITIAL_REVIEWS = [
    {
        "product_id": 42,
        "author": "Alice Tech Lead",
        "rating": 5,
        "comment": "Exceptional compilation speed and battery life for large microservice repos.",
    },
    {
        "product_id": 42,
        "author": "Bob Staff Architect",
        "rating": 4,
        "comment": "Screen is brilliant, quiet fans under load. Slightly heavy in the backpack.",
    },
    {
        "product_id": 43,
        "author": "Carol Backend Dev",
        "rating": 5,
        "comment": "Best split ergonomic keyboard I have used. Wrist pain is gone.",
    },
]


async def seed_reviews(session: AsyncSession) -> None:
    """Inserts initial reviews if they do not exist."""
    for item in INITIAL_REVIEWS:
        stmt = select(ReviewModel).where(
            ReviewModel.product_id == item["product_id"],
            ReviewModel.author == item["author"],
        )
        result = await session.execute(stmt)
        existing = result.scalar_one_or_none()
        if existing is None:
            review = ReviewModel(
                product_id=item["product_id"],
                author=item["author"],
                rating=item["rating"],
                comment=item["comment"],
            )
            session.add(review)
    await session.commit()
