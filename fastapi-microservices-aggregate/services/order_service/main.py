"""Order Service entrypoint and application setup."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from services.order_service.api.routes import get_db_session
from services.order_service.api.routes import router as order_router
from services.order_service.config import get_settings
from services.order_service.seed import seed_orders
from shared.db import DatabaseManager
from shared.errors import register_problem_handlers
from shared.health import create_health_router
from shared.logging import configure_logging

__all__ = ["app", "db_manager"]

settings = get_settings()
logger = configure_logging(settings.service_name)
db_manager = DatabaseManager(settings.database_url, echo=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing Order Service schema and seed data...")
    await db_manager.init_tables()
    async with db_manager.session() as session:
        await seed_orders(session)
    logger.info("Order Service startup complete.")
    yield
    logger.info("Shutting down Order Service...")
    await db_manager.close()


app = FastAPI(
    title="Order Service (DDD Aggregate Root)",
    description="Microservice demonstrating DDD Aggregate Root consistency boundaries, invariants, optimistic locking, and transactional outbox.",
    version="1.0.0",
    lifespan=lifespan,
)

register_problem_handlers(app)
app.include_router(create_health_router(settings.service_name, db_manager))

# Wire runtime session dependency
app.dependency_overrides[get_db_session] = db_manager.get_session
app.include_router(order_router)
