"""Simulation utility for injecting network latency and faults for didactic demonstrations."""

from __future__ import annotations

import asyncio

from shared.errors import ProblemDetailsException

__all__ = ["apply_simulation"]


async def apply_simulation(
    delay_ms: int = 0,
    simulate_failure: bool = False,
    service_name: str = "service",
) -> None:
    """Applies artificial sleep and/or simulates transient 500 error."""
    if delay_ms > 0:
        await asyncio.sleep(delay_ms / 1000.0)

    if simulate_failure:
        raise ProblemDetailsException(
            status=500,
            title="Simulated Service Failure",
            detail=f"{service_name} injected an intentional transient failure for didactic demonstration.",
            type_uri="https://api.example.com/errors/simulated-failure",
        )
