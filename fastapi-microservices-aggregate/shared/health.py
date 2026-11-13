"""Health and readiness probe routers for Kubernetes and Docker Compose."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

if TYPE_CHECKING:
    from shared.db import DatabaseManager

__all__ = ["create_health_router"]


def create_health_router(
    service_name: str,
    db_manager: DatabaseManager | None = None,
) -> APIRouter:
    """Creates a router exposing /health and /ready endpoints."""
    router = APIRouter(tags=["Health"])

    @router.get("/health", summary="Liveness probe")
    async def liveness() -> dict[str, str]:
        return {"status": "UP", "service": service_name}

    @router.get("/ready", summary="Readiness probe")
    async def readiness() -> JSONResponse:
        db_healthy = True
        if db_manager is not None:
            db_healthy = await db_manager.health_check()

        if db_healthy:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "READY", "service": service_name, "database": "UP"},
            )
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "NOT_READY", "service": service_name, "database": "DOWN"},
        )

    return router
