"""Contract tests verifying OpenAPI specs and health endpoints across all 5 microservices."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from services.gateway_aggregator.main import app as gateway_app
from services.inventory_service.main import app as inventory_app
from services.order_service.main import app as order_app
from services.product_service.main import app as product_app
from services.reviews_service.main import app as reviews_app

ALL_SERVICES = [
    ("gateway-aggregator", gateway_app),
    ("product-service", product_app),
    ("inventory-service", inventory_app),
    ("reviews-service", reviews_app),
    ("order-service", order_app),
]


@pytest.mark.parametrize("service_name,app", ALL_SERVICES)
def test_openapi_schema_generated_successfully(service_name: str, app: object) -> None:
    schema = app.openapi()  # type: ignore[attr-defined]
    assert schema is not None
    assert "paths" in schema
    assert "info" in schema
    assert schema["info"]["version"] == "1.0.0"


@pytest.mark.parametrize("service_name,app", ALL_SERVICES)
@pytest.mark.asyncio
async def test_health_and_ready_endpoints(service_name: str, app: object) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),  # type: ignore[arg-type]
        base_url="http://testserver",
    ) as client:
        health_resp = await client.get("/health")
        assert health_resp.status_code == 200
        health_data = health_resp.json()
        assert health_data["status"] == "UP"

        ready_resp = await client.get("/ready")
        assert ready_resp.status_code == 200
        ready_data = ready_resp.json()
        assert ready_data["status"] == "READY"
