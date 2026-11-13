"""HTTP client registry and timing helpers for downstream microservices."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import httpx

from services.gateway_aggregator.config import AggregatorSettings

__all__ = ["DownstreamClientRegistry", "timed_get"]


class DownstreamClientRegistry:
    """Manages long-lived HTTP client connections to downstream microservices."""

    def __init__(
        self,
        settings: AggregatorSettings,
        clients: dict[str, httpx.AsyncClient] | None = None,
    ) -> None:
        self.settings = settings
        if clients is not None:
            self.clients = clients
        else:
            timeout = httpx.Timeout(self.settings.default_timeout_ms / 1000.0)
            limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
            self.clients = {
                "product": httpx.AsyncClient(
                    base_url=settings.product_service_url,
                    timeout=timeout,
                    limits=limits,
                ),
                "inventory": httpx.AsyncClient(
                    base_url=settings.inventory_service_url,
                    timeout=timeout,
                    limits=limits,
                ),
                "reviews": httpx.AsyncClient(
                    base_url=settings.reviews_service_url,
                    timeout=timeout,
                    limits=limits,
                ),
                "order": httpx.AsyncClient(
                    base_url=settings.order_service_url,
                    timeout=timeout,
                    limits=limits,
                ),
            }

    def get_client(self, service_key: str) -> httpx.AsyncClient:
        return self.clients[service_key]

    async def close_all(self) -> None:
        for client in self.clients.values():
            await client.aclose()


async def timed_get(
    client: httpx.AsyncClient,
    path: str,
    params: dict[str, Any] | None = None,
    timeout_s: float | None = None,
) -> tuple[httpx.Response | None, float, Exception | None]:
    """Executes a GET request while accurately recording wall-clock round-trip duration in ms."""
    start = time.perf_counter()
    try:
        kwargs: dict[str, Any] = {"params": params}
        if timeout_s is not None:
            kwargs["timeout"] = timeout_s
            response = await asyncio.wait_for(client.get(path, **kwargs), timeout=timeout_s)
        else:
            response = await client.get(path, **kwargs)
        duration_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return response, duration_ms, None
    except (TimeoutError, httpx.TimeoutException):
        duration_ms = round((time.perf_counter() - start) * 1000.0, 2)
        timeout_exc = httpx.TimeoutException(f"Request to {path} timed out after {timeout_s}s")
        return None, duration_ms, timeout_exc
    except Exception as exc:
        duration_ms = round((time.perf_counter() - start) * 1000.0, 2)
        return None, duration_ms, exc
