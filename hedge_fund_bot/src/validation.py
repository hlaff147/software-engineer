"""
Input Validation Module

This module provides Pydantic models for validating inputs across the application.
All user inputs should be validated using these models to fail fast and provide
clear error messages.

Patterns applied:
- Fail-Fast: Validate early, reject invalid inputs immediately
- Type Safety: Pydantic provides runtime type checking
- Security: Prevents injection attacks in prompts
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
import re
import logging

logger = logging.getLogger(__name__)


class TickerInput(BaseModel):
    """
    Validates stock ticker symbols.
    
    Supports:
    - US tickers: AAPL, MSFT, GOOGL (1-5 uppercase letters)
    - International: PETR4.SA, VOD.L (with exchange suffix)
    
    Example:
        >>> ticker = TickerInput(ticker="AAPL")
        >>> ticker = TickerInput(ticker="PETR4.SA")
    """
    ticker: str = Field(
        ...,
        min_length=1,
        max_length=15,
        description="Stock ticker symbol (e.g., AAPL, MSFT, PETR4.SA)"
    )
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker_format(cls, v: str) -> str:
        """Validate ticker format and normalize to uppercase."""
        v = v.strip().upper()
        
        if not v:
            raise ValueError("Ticker cannot be empty")
        
        # Pattern: 1-5 alphanumeric chars, optionally followed by .XX suffix
        # Examples: AAPL, MSFT, PETR4, PETR4.SA, VOD.L
        pattern = r'^[A-Z0-9]{1,5}(\.[A-Z]{1,2})?$'
        
        if not re.match(pattern, v):
            raise ValueError(
                f"Invalid ticker format: '{v}'. "
                "Expected 1-5 alphanumeric characters, optionally with exchange suffix (e.g., AAPL, PETR4.SA)"
            )
        
        return v


class AnalysisRequest(BaseModel):
    """
    Validates a complete analysis request.
    
    Example:
        >>> request = AnalysisRequest(ticker="AAPL", period="3mo")
    """
    ticker: str = Field(..., description="Stock ticker to analyze")
    period: Optional[str] = Field(
        default="3mo",
        description="Historical data period (1mo, 3mo, 6mo, 1y, 2y, 5y)"
    )
    
    @field_validator('ticker')
    @classmethod
    def validate_ticker(cls, v: str) -> str:
        """Delegate to TickerInput for validation."""
        validated = TickerInput(ticker=v)
        return validated.ticker
    
    @field_validator('period')
    @classmethod
    def validate_period(cls, v: str) -> str:
        """Validate period format."""
        valid_periods = ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if v not in valid_periods:
            raise ValueError(f"Invalid period: '{v}'. Must be one of {valid_periods}")
        return v


class RecommendationType(BaseModel):
    """Validates recommendation output."""
    recommendation: Literal["BUY", "SELL", "HOLD"]
    risk_level: Literal["HIGH", "MEDIUM", "LOW"]
    confidence: int = Field(ge=0, le=100)


def validate_ticker(ticker: str) -> str:
    """
    Convenience function to validate a ticker string.
    
    Args:
        ticker: Raw ticker string from user input
        
    Returns:
        Validated and normalized ticker (uppercase)
        
    Raises:
        ValueError: If ticker format is invalid
        
    Example:
        >>> validate_ticker("aapl")  # Returns "AAPL"
        >>> validate_ticker("INVALID123")  # Raises ValueError
    """
    try:
        validated = TickerInput(ticker=ticker)
        return validated.ticker
    except Exception as e:
        logger.warning(f"Invalid ticker: {ticker} - {e}")
        raise ValueError(f"Invalid ticker: {ticker}") from e


def validate_analysis_request(ticker: str, period: str = "3mo") -> AnalysisRequest:
    """
    Convenience function to validate an analysis request.
    
    Args:
        ticker: Stock ticker symbol
        period: Historical data period
        
    Returns:
        Validated AnalysisRequest object
        
    Raises:
        ValueError: If any validation fails
    """
    return AnalysisRequest(ticker=ticker, period=period)
