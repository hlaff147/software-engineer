"""Contract tests verifying OpenAPI specs and health endpoints across all 5 microservices."""

from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from services.gateway_aggregator.main import app as gateway_app
from services.inventory_service.main import app as inventory_app
from services.order_service.main import app as order_app
from services.product_service.main import app as product_app
from services.reviews_service.main import app as reviews_app
from shared.constants import ApiEndpoints
from shared.health import HealthResponse, ReadyResponse

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
        health_resp = await client.get(ApiEndpoints.HEALTH)
        assert health_resp.status_code == 200
        health = HealthResponse.model_validate(health_resp.json())
        assert health.status == "UP"
        assert health.service == service_name

        ready_resp = await client.get(ApiEndpoints.READY)
        assert ready_resp.status_code == 200
        ready = ReadyResponse.model_validate(ready_resp.json())
        assert ready.status == "READY"
        assert ready.service == service_name
