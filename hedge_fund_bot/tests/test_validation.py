"""
Unit Tests for Input Validation
"""

import pytest
from src.validation import validate_ticker, TickerInput, AnalysisRequest


def test_valid_us_tickers():
    """Test US stock ticker formats."""
    assert validate_ticker("aapl") == "AAPL"
    assert validate_ticker("MSFT") == "MSFT"
    assert validate_ticker("googl") == "GOOGL"


def test_valid_international_tickers():
    """Test international stock ticker formats with exchange suffix."""
    assert validate_ticker("petr4.sa") == "PETR4.SA"
    assert validate_ticker("VOD.L") == "VOD.L"


def test_invalid_tickers():
    """Test invalid ticker symbols throw ValueError."""
    with pytest.raises(ValueError):
        validate_ticker("INVALID_TICKER_NAME_TOO_LONG")
    
    with pytest.raises(ValueError):
        validate_ticker("")


def test_analysis_request_period_validation():
    """Test AnalysisRequest period validation."""
    req = AnalysisRequest(ticker="AAPL", period="3mo")
    assert req.ticker == "AAPL"
    assert req.period == "3mo"

    with pytest.raises(ValueError):
        AnalysisRequest(ticker="AAPL", period="999years")
