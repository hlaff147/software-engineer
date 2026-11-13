"""Order Service configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

from shared.constants import ServiceNames

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Order service environment settings."""

    service_name: str = ServiceNames.ORDER_SERVICE.value
    port: int = 8004
    database_url: str = "postgresql+asyncpg://app_user:app_password@postgres:5432/orders_db"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="ORDER_",
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
