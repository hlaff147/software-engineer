"""
Centralized Configuration Module

This module provides a single source of truth for all configuration values.
Settings can be overridden via environment variables or .env file.

Patterns applied:
- Externalized Configuration: No magic numbers in code
- Environment-based Config: Different settings per environment
- Pydantic Validation: Type-safe configuration
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """
    Application settings with sensible defaults.
    
    All settings can be overridden via environment variables.
    Environment variable names are automatically derived from field names (uppercase).
    
    Example:
        export HISTORY_PERIOD="6mo"
        export MAX_VERIFICATION_RETRIES=3
    """
    
    # =============================================================================
    # LLM Settings
    # =============================================================================
    MODEL_NAME: str = Field(
        default="llama-3.3-70b-versatile",
        description="Default LLM model to use"
    )
    GROQ_API_KEY: Optional[str] = Field(
        default=None,
        description="Groq API key (required)"
    )
    
    # =============================================================================
    # Analysis Settings
    # =============================================================================
    HISTORY_PERIOD: str = Field(
        default="3mo",
        description="Historical data period for technical analysis (1mo, 3mo, 6mo, 1y)"
    )
    NEWS_MAX_RESULTS: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of news articles to fetch"
    )
    CONTEXT_WINDOW_MESSAGES: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Number of recent messages to include in context"
    )
    
    # =============================================================================
    # Workflow Settings
    # =============================================================================
    RECURSION_LIMIT: int = Field(
        default=25,
        ge=5,
        le=100,
        description="Maximum recursion depth for LangGraph workflow"
    )
    MAX_VERIFICATION_RETRIES: int = Field(
        default=2,
        ge=0,
        le=5,
        description="Maximum retries when verification fails (PEV pattern)"
    )
    
    # =============================================================================
    # Technical Analysis Settings
    # =============================================================================
    RSI_PERIOD: int = Field(
        default=14,
        ge=5,
        le=30,
        description="RSI calculation period"
    )
    SMA_PERIOD: int = Field(
        default=20,
        ge=5,
        le=200,
        description="Simple Moving Average period"
    )
    MACD_FAST: int = Field(
        default=12,
        ge=5,
        le=20,
        description="MACD fast EMA period"
    )
    MACD_SLOW: int = Field(
        default=26,
        ge=15,
        le=50,
        description="MACD slow EMA period"
    )
    MACD_SIGNAL: int = Field(
        default=9,
        ge=5,
        le=20,
        description="MACD signal line period"
    )
    PRICE_CHANGE_DAYS: int = Field(
        default=20,
        ge=5,
        le=60,
        description="Days for price change calculation"
    )
    SUPPORT_RESISTANCE_DAYS: int = Field(
        default=30,
        ge=10,
        le=90,
        description="Days for support/resistance calculation"
    )
    
    # =============================================================================
    # Logging Settings
    # =============================================================================
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR)"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"  # Ignore extra environment variables


# Singleton instance - import this in other modules
settings = Settings()


# =============================================================================
# Convenience Constants (derived from settings)
# =============================================================================

# Agent message prefixes (centralized magic strings)
class AgentPrefix:
    """Centralized agent message prefixes to avoid magic strings."""
    SUPERVISOR = "[SUPERVISOR]"
    RESEARCHER = "[RESEARCHER"
    CHARTIST = "[CHARTIST"
    ANALYST = "[ANALYST"
    VERIFIER = "[VERIFIER"
    ERROR = "[ERROR]"


# Valid routing options
VALID_AGENTS = ["Researcher", "Chartist", "Analyst", "FINISH"]


def validate_settings() -> bool:
    """
    Validate that all required settings are configured.
    
    Returns:
        True if valid, raises ValueError if not
    """
    if not settings.GROQ_API_KEY and not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY is required. Set it in .env or environment.")
    
    if settings.MACD_FAST >= settings.MACD_SLOW:
        raise ValueError("MACD_FAST must be less than MACD_SLOW")
    
    return True
