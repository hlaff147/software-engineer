"""Product service configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["Settings", "get_settings"]


class Settings(BaseSettings):
    """Product service environment settings."""

    service_name: str = "product-service"
    port: int = 8001
    database_url: str = "postgresql+asyncpg://app_user:app_password@postgres:5432/products_db"
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="PRODUCT_",
        env_file=".env",
        extra="ignore",
    )


def get_settings() -> Settings:
    return Settings()
