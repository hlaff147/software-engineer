"""Product Service entrypoint and REST endpoints."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.product_service.config import get_settings
from services.product_service.models import ProductModel
from services.product_service.schemas import ProductCreate, ProductResponse
from services.product_service.seed import seed_products
from shared.db import DatabaseManager
from shared.errors import ProblemDetailsException, register_problem_handlers
from shared.health import create_health_router
from shared.logging import configure_logging
from shared.pagination import PaginatedResponse
from shared.simulation import apply_simulation

__all__ = ["app", "db_manager"]

settings = get_settings()
logger = configure_logging(settings.service_name)
db_manager = DatabaseManager(settings.database_url, echo=settings.debug)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Initializing Product Service schema and seed data...")
    await db_manager.init_tables()
    async with db_manager.session() as session:
        await seed_products(session)
    logger.info("Product Service startup complete.")
    yield
    logger.info("Shutting down Product Service...")
    await db_manager.close()


app = FastAPI(
    title="Product Catalog Service",
    description="Microservice managing catalog products, pricing, and details.",
    version="1.0.0",
    lifespan=lifespan,
)

register_problem_handlers(app)
app.include_router(create_health_router(settings.service_name, db_manager))


@app.get(
    "/api/v1/products",
    response_model=PaginatedResponse[ProductResponse],
    summary="List products with pagination",
)
async def list_products(
    page: Annotated[int, Query(ge=1, description="Page number")] = 1,
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    session: AsyncSession = Depends(db_manager.get_session),
) -> PaginatedResponse[ProductResponse]:
    offset = (page - 1) * page_size
    total_count_res = await session.execute(select(func.count(ProductModel.id)))
    total_count = total_count_res.scalar_one() or 0

    items_res = await session.execute(
        select(ProductModel).offset(offset).limit(page_size).order_by(ProductModel.id)
    )
    products = [ProductResponse.model_validate(p) for p in items_res.scalars().all()]
    return PaginatedResponse.create(
        items=products,
        total_count=total_count,
        page=page,
        page_size=page_size,
    )


@app.get(
    "/api/v1/products/{product_id}",
    response_model=ProductResponse,
    summary="Get product by ID with optional didactic delay/failure simulation",
)
async def get_product(
    product_id: int,
    delay_ms: Annotated[int, Query(ge=0, description="Injected delay in milliseconds")] = 0,
    simulate_failure: Annotated[bool, Query(description="Injected 500 error")] = False,
    session: AsyncSession = Depends(db_manager.get_session),
) -> ProductResponse:
    await apply_simulation(delay_ms, simulate_failure, service_name="product-service")

    result = await session.execute(select(ProductModel).where(ProductModel.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise ProblemDetailsException(
            status=status.HTTP_404_NOT_FOUND,
            title="Product Not Found",
            detail=f"Product with ID {product_id} does not exist in the catalog.",
            type_uri="https://api.example.com/errors/product-not-found",
        )
    return ProductResponse.model_validate(product)


@app.post(
    "/api/v1/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new catalog product",
)
async def create_product(
    payload: ProductCreate,
    response: Response,
    session: AsyncSession = Depends(db_manager.get_session),
) -> ProductResponse:
    # Check duplicate SKU
    existing = await session.execute(select(ProductModel).where(ProductModel.sku == payload.sku))
    if existing.scalar_one_or_none() is not None:
        raise ProblemDetailsException(
            status=status.HTTP_409_CONFLICT,
            title="Product SKU Conflict",
            detail=f"A product with SKU '{payload.sku}' already exists.",
            type_uri="https://api.example.com/errors/sku-conflict",
        )

    product = ProductModel(
        sku=payload.sku,
        name=payload.name,
        description=payload.description,
        price=payload.price,
        currency=payload.currency,
        category=payload.category,
    )
    session.add(product)
    await session.commit()
    await session.refresh(product)

    response.headers["Location"] = f"/api/v1/products/{product.id}"
    return ProductResponse.model_validate(product)
