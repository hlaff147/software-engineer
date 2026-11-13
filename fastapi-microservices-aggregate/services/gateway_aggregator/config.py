"""Gateway Aggregator configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["AggregatorSettings", "get_settings"]


class AggregatorSettings(BaseSettings):
    """Aggregator environment settings."""

    service_name: str = "gateway-aggregator"
    port: int = 8000
    product_service_url: str = "http://product-service:8001"
    inventory_service_url: str = "http://inventory-service:8002"
    reviews_service_url: str = "http://reviews-service:8003"
    order_service_url: str = "http://order-service:8004"
    default_timeout_ms: int = 1000

    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_",
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> AggregatorSettings:
    return AggregatorSettings()
