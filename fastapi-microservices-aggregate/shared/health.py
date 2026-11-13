"""Health and readiness probe routers for Kubernetes and Docker Compose."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, Response, status
from pydantic import BaseModel

from shared.constants import ApiEndpoints

if TYPE_CHECKING:
    from shared.db import DatabaseManager

__all__ = ["HealthResponse", "ReadyResponse", "create_health_router"]


class HealthResponse(BaseModel):
    status: str
    service: str


class ReadyResponse(BaseModel):
    status: str
    service: str
    database: str


def create_health_router(
    service_name: str,
    db_manager: DatabaseManager | None = None,
) -> APIRouter:
    """Creates a router exposing /health and /ready endpoints."""
    router = APIRouter(tags=["Health"])

    @router.get(ApiEndpoints.HEALTH, response_model=HealthResponse, summary="Liveness probe")
    async def liveness() -> HealthResponse:
        return HealthResponse(status="UP", service=service_name)

    @router.get(ApiEndpoints.READY, response_model=ReadyResponse, summary="Readiness probe")
    async def readiness(response: Response) -> ReadyResponse:
        db_healthy = True
        if db_manager is not None:
            db_healthy = await db_manager.health_check()

        if db_healthy:
            return ReadyResponse(status="READY", service=service_name, database="UP")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadyResponse(status="NOT_READY", service=service_name, database="DOWN")

    return router
