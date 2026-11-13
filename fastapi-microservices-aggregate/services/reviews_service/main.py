"""Reviews Service entrypoint and REST endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.reviews_service.config import get_settings
from services.reviews_service.models import ReviewModel
from services.reviews_service.schemas import (
    ProductReviewsResponse,
    ReviewCreate,
    ReviewItem,
)
from services.reviews_service.seed import seed_reviews
from shared.db import DatabaseManager
from shared.errors import register_problem_handlers
from shared.health import create_health_router
from shared.logging import configure_logging
from shared.simulation import apply_simulation

__all__ = ["app", "db_manager"]

settings = get_settings()
logger = configure_logging(settings.service_name)
db_manager = DatabaseManager(settings.database_url, echo=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing Reviews Service schema and seed data...")
    await db_manager.init_tables()
    async with db_manager.session() as session:
        await seed_reviews(session)
    logger.info("Reviews Service startup complete.")
    yield
    logger.info("Shutting down Reviews Service...")
    await db_manager.close()


app = FastAPI(
    title="Customer Reviews Service",
    description="Microservice managing ratings and reviews per product.",
    version="1.0.0",
    lifespan=lifespan,
)

register_problem_handlers(app)
app.include_router(create_health_router(settings.service_name, db_manager))


@app.get(
    "/api/v1/reviews/{product_id}",
    response_model=ProductReviewsResponse,
    summary="Get aggregated reviews for a product with optional didactic delay/failure simulation",
)
async def get_reviews(
    product_id: int,
    delay_ms: Annotated[int, Query(ge=0, description="Injected delay in milliseconds")] = 0,
    simulate_failure: Annotated[bool, Query(description="Injected 500 error")] = False,
    session: AsyncSession = Depends(db_manager.get_session),
) -> ProductReviewsResponse:
    await apply_simulation(delay_ms, simulate_failure, service_name="reviews-service")

    # Fetch reviews
    stmt = (
        select(ReviewModel)
        .where(ReviewModel.product_id == product_id)
        .order_by(ReviewModel.created_at.desc())
    )
    result = await session.execute(stmt)
    reviews = [ReviewItem.model_validate(r) for r in result.scalars().all()]

    if not reviews:
        return ProductReviewsResponse(
            product_id=product_id,
            average_rating=0.0,
            total_reviews=0,
            reviews=[],
        )

    avg_stmt = select(func.avg(ReviewModel.rating)).where(ReviewModel.product_id == product_id)
    avg_res = await session.execute(avg_stmt)
    avg_rating = round(float(avg_res.scalar_one() or 0.0), 2)

    return ProductReviewsResponse(
        product_id=product_id,
        average_rating=avg_rating,
        total_reviews=len(reviews),
        reviews=reviews,
    )


@app.post(
    "/api/v1/reviews/{product_id}",
    response_model=ReviewItem,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a review for a product",
)
async def create_review(
    product_id: int,
    payload: ReviewCreate,
    response: Response,
    session: AsyncSession = Depends(db_manager.get_session),
) -> ReviewItem:
    review = ReviewModel(
        product_id=product_id,
        author=payload.author,
        rating=payload.rating,
        comment=payload.comment,
    )
    session.add(review)
    await session.commit()
    await session.refresh(review)

    response.headers["Location"] = f"/api/v1/reviews/{product_id}"
    return ReviewItem.model_validate(review)
