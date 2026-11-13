"""Test configuration and ASGI client fixtures."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from services.gateway_aggregator.clients import DownstreamClientRegistry
from services.gateway_aggregator.config import AggregatorSettings
from services.gateway_aggregator.main import app as gateway_app
from services.gateway_aggregator.main import get_registry
from services.inventory_service.main import app as inventory_app
from services.inventory_service.main import db_manager as inv_db
from services.inventory_service.seed import seed_inventory
from services.order_service.api.routes import get_db_session
from services.order_service.main import app as order_app
from services.order_service.main import db_manager as ord_db
from services.order_service.seed import seed_orders
from services.product_service.main import app as product_app
from services.product_service.main import db_manager as prod_db
from services.product_service.seed import seed_products
from services.reviews_service.main import app as reviews_app
from services.reviews_service.main import db_manager as rev_db
from services.reviews_service.seed import seed_reviews
from shared.db import DatabaseManager


@pytest.fixture(autouse=True)
async def setup_databases(tmp_path: Path) -> AsyncGenerator[None, None]:
    """Sets up isolated async SQLite databases for all services in each test."""
    p_db = DatabaseManager(f"sqlite+aiosqlite:///{tmp_path}/products.db")
    i_db = DatabaseManager(f"sqlite+aiosqlite:///{tmp_path}/inventory.db")
    r_db = DatabaseManager(f"sqlite+aiosqlite:///{tmp_path}/reviews.db")
    o_db = DatabaseManager(f"sqlite+aiosqlite:///{tmp_path}/orders.db")

    # Override service db managers
    prod_db.engine = p_db.engine
    prod_db.session_factory = p_db.session_factory

    inv_db.engine = i_db.engine
    inv_db.session_factory = i_db.session_factory

    rev_db.engine = r_db.engine
    rev_db.session_factory = r_db.session_factory

    ord_db.engine = o_db.engine
    ord_db.session_factory = o_db.session_factory

    order_app.dependency_overrides[get_db_session] = o_db.get_session

    # Initialize tables and seeds
    await p_db.init_tables()
    await i_db.init_tables()
    await r_db.init_tables()
    await o_db.init_tables()

    async with p_db.session() as s:
        await seed_products(s)
    async with i_db.session() as s:
        await seed_inventory(s)
    async with r_db.session() as s:
        await seed_reviews(s)
    async with o_db.session() as s:
        await seed_orders(s)

    yield

    await p_db.close()
    await i_db.close()
    await r_db.close()
    await o_db.close()


@pytest.fixture
async def order_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=order_app),
        base_url="http://test-order",
    ) as client:
        yield client


@pytest.fixture
async def product_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=product_app),
        base_url="http://test-product",
    ) as client:
        yield client


@pytest.fixture
async def gateway_client() -> AsyncGenerator[AsyncClient, None]:
    """Gateway client wired to downstream ASGI apps without real network sockets."""
    settings = AggregatorSettings(default_timeout_ms=1000)

    downstream_clients = {
        "product": AsyncClient(
            transport=ASGITransport(app=product_app),
            base_url="http://testserver",
            timeout=1.0,
        ),
        "inventory": AsyncClient(
            transport=ASGITransport(app=inventory_app),
            base_url="http://testserver",
            timeout=1.0,
        ),
        "reviews": AsyncClient(
            transport=ASGITransport(app=reviews_app),
            base_url="http://testserver",
            timeout=1.0,
        ),
        "order": AsyncClient(
            transport=ASGITransport(app=order_app),
            base_url="http://testserver",
            timeout=1.0,
        ),
    }

    test_registry = DownstreamClientRegistry(settings, clients=downstream_clients)
    gateway_app.dependency_overrides[get_registry] = lambda: test_registry

    async with AsyncClient(
        transport=ASGITransport(app=gateway_app),
        base_url="http://test-gateway",
    ) as client:
        yield client

    await test_registry.close_all()
