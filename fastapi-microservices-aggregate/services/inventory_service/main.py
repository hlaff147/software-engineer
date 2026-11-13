"""Inventory Service entrypoint and REST endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.inventory_service.config import get_settings
from services.inventory_service.models import StockItemModel
from services.inventory_service.schemas import StockResponse, StockUpdate
from services.inventory_service.seed import seed_inventory
from shared.constants import ApiEndpoints, ErrorTitles, ErrorTypes
from shared.db import DatabaseManager
from shared.errors import ProblemDetailsException, register_problem_handlers
from shared.health import create_health_router
from shared.logging import configure_logging
from shared.simulation import apply_simulation

__all__ = ["app", "db_manager"]

settings = get_settings()
logger = configure_logging(settings.service_name)
db_manager = DatabaseManager(settings.database_url, echo=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing Inventory Service schema and seed data...")
    await db_manager.init_tables()
    async with db_manager.session() as session:
        await seed_inventory(session)
    logger.info("Inventory Service startup complete.")
    yield
    logger.info("Shutting down Inventory Service...")
    await db_manager.close()


app = FastAPI(
    title="Inventory Stock Service",
    description="Microservice managing warehouse inventory and real-time stock levels.",
    version="1.0.0",
    lifespan=lifespan,
)

register_problem_handlers(app)
app.include_router(create_health_router(settings.service_name, db_manager))


@app.get(
    f"{ApiEndpoints.STOCK}/{{product_id}}",
    response_model=StockResponse,
    summary="Get stock details for a product with optional didactic delay/failure simulation",
)
async def get_stock(
    product_id: int,
    delay_ms: Annotated[int, Query(ge=0, description="Injected delay in milliseconds")] = 0,
    simulate_failure: Annotated[bool, Query(description="Injected 500 error")] = False,
    session: AsyncSession = Depends(db_manager.get_session),
) -> StockResponse:
    await apply_simulation(delay_ms, simulate_failure, service_name=settings.service_name)

    result = await session.execute(
        select(StockItemModel).where(StockItemModel.product_id == product_id)
    )
    stock = result.scalar_one_or_none()
    if stock is None:
        raise ProblemDetailsException(
            status=status.HTTP_404_NOT_FOUND,
            title=ErrorTitles.STOCK_NOT_FOUND,
            detail=f"Stock record for product ID {product_id} does not exist.",
            type_uri=ErrorTypes.STOCK_NOT_FOUND,
        )
    return StockResponse.model_validate(stock)


@app.put(
    f"{ApiEndpoints.STOCK}/{{product_id}}",
    response_model=StockResponse,
    summary="Update stock levels for a product",
)
async def update_stock(
    product_id: int,
    payload: StockUpdate,
    session: AsyncSession = Depends(db_manager.get_session),
) -> StockResponse:
    result = await session.execute(
        select(StockItemModel).where(StockItemModel.product_id == product_id)
    )
    stock = result.scalar_one_or_none()
    if stock is None:
        raise ProblemDetailsException(
            status=status.HTTP_404_NOT_FOUND,
            title=ErrorTitles.STOCK_NOT_FOUND,
            detail=f"Stock record for product ID {product_id} does not exist.",
            type_uri=ErrorTypes.STOCK_NOT_FOUND,
        )

    if payload.available_quantity is not None:
        stock.available_quantity = payload.available_quantity
    if payload.reserved_quantity is not None:
        stock.reserved_quantity = payload.reserved_quantity

    await session.commit()
    await session.refresh(stock)
    return StockResponse.model_validate(stock)
