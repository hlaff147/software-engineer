"""Gateway Aggregator configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.constants import DomainConstants, ServiceNames, ServiceUrls

__all__ = ["AggregatorSettings", "get_settings"]


class AggregatorSettings(BaseSettings):
    """Aggregator environment settings."""

    service_name: str = ServiceNames.GATEWAY_AGGREGATOR.value
    port: int = 8000
    product_service_url: str = ServiceUrls.PRODUCT_SERVICE
    inventory_service_url: str = ServiceUrls.INVENTORY_SERVICE
    reviews_service_url: str = ServiceUrls.REVIEWS_SERVICE
    order_service_url: str = ServiceUrls.ORDER_SERVICE
    default_timeout_ms: int = DomainConstants.DEFAULT_TIMEOUT_MS

    model_config = SettingsConfigDict(
        env_prefix="GATEWAY_",
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> AggregatorSettings:
    return AggregatorSettings()
