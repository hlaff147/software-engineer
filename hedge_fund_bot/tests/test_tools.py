"""
Unit Tests for Financial Tools & Quantitative Math
"""

import pytest
import pandas as pd
import numpy as np
from src.tools.financial_tools import (
    calculate_sma,
    calculate_rsi,
    calculate_macd,
    compute_technical_indicators
)
from src.validation import validate_ticker, TickerInput


def create_sample_price_dataframe(num_days: int = 50, trend: float = 1.0) -> pd.DataFrame:
    """Helper to generate mock price DataFrame."""
    dates = pd.date_range(start="2026-01-01", periods=num_days, freq="D")
    prices = 100.0 + np.cumsum(np.random.normal(trend, 0.5, size=num_days))
    df = pd.DataFrame({
        "Open": prices - 0.5,
        "High": prices + 1.0,
        "Low": prices - 1.0,
        "Close": prices,
        "Volume": 1000000
    }, index=dates)
    return df


def test_calculate_sma():
    """Test Simple Moving Average calculation."""
    df = create_sample_price_dataframe(num_days=30)
    sma = calculate_sma(df, window=20)
    
    assert len(sma) == 30
    assert pd.isna(sma.iloc[18])  # Window not reached yet
    assert not pd.isna(sma.iloc[19])  # 20th element valid
    assert round(sma.iloc[19], 2) == round(df['Close'].iloc[:20].mean(), 2)


def test_calculate_rsi_bounds():
    """Test RSI calculation returns values bounded between 0 and 100."""
    df = create_sample_price_dataframe(num_days=40, trend=2.0)
    rsi = calculate_rsi(df, period=14)
    
    latest_rsi = rsi.iloc[-1]
    assert 0.0 <= latest_rsi <= 100.0


def test_calculate_macd_keys():
    """Test MACD calculation returns correct dictionary keys."""
    df = create_sample_price_dataframe(num_days=50)
    macd_dict = calculate_macd(df, fast=12, slow=26, signal=9)
    
    assert "macd" in macd_dict
    assert "signal" in macd_dict
    assert "histogram" in macd_dict
    assert len(macd_dict["macd"]) == 50


def test_compute_technical_indicators_model():
    """Test indicators model packaging."""
    df = create_sample_price_dataframe(num_days=40)
    indicators = compute_technical_indicators(df)
    
    assert indicators.current_price > 0
    assert 0.0 <= indicators.rsi <= 100.0
    assert indicators.high_resistance >= indicators.low_support


def test_mock_search_provider():
    """Test MockSearchProvider returns structured NewsArticle results."""
    from src.tools.search_tools import MockSearchProvider
    from src.schemas import NewsArticle

    provider = MockSearchProvider()
    news = provider.search_news("AAPL stock news", max_results=2)
    sentiment = provider.search_sentiment("AAPL", max_results=2)

    assert len(news) == 1
    assert isinstance(news[0], NewsArticle)
    assert "AAPL stock news" in news[0].title

    assert len(sentiment) == 1
    assert isinstance(sentiment[0], NewsArticle)
    assert "AAPL" in sentiment[0].title


def test_search_provider_dependency_injection():
    """Test setting global default provider to MockSearchProvider."""
    from src.tools.search_tools import (
        MockSearchProvider,
        DuckDuckGoSearchProvider,
        set_default_search_provider,
        get_default_search_provider,
        search_financial_news_with_retry,
        search_market_sentiment,
    )
    from src.schemas import NewsArticle

    custom_article = NewsArticle(
        title="Custom Injection Test",
        url="https://test.org",
        snippet="Injected article snippet."
    )
    mock_provider = MockSearchProvider(mock_articles=[custom_article])
    
    original_provider = get_default_search_provider()
    try:
        set_default_search_provider(mock_provider)
        assert get_default_search_provider() is mock_provider

        news_results = search_financial_news_with_retry("test query")
        assert len(news_results) == 1
        assert news_results[0].title == "Custom Injection Test"

        sentiment_results = search_market_sentiment("NVDA")
        assert len(sentiment_results) == 1
        assert sentiment_results[0].title == "Custom Injection Test"
    finally:
        set_default_search_provider(original_provider)


def test_mock_market_data_provider():
    """Test MockMarketDataProvider generates synthetic price DataFrame."""
    from src.tools.financial_tools import MockMarketDataProvider

    provider = MockMarketDataProvider()
    df = provider.fetch_history("PETR4", "1mo")

    assert not df.empty
    assert "Close" in df.columns
    assert "High" in df.columns
    assert len(df) == 50


def test_market_data_provider_dependency_injection():
    """Test setting global market data provider to MockMarketDataProvider."""
    from src.tools.financial_tools import (
        MockMarketDataProvider,
        get_default_market_data_provider,
        set_default_market_data_provider,
        fetch_stock_dataframe_with_retry,
        compute_technical_indicators,
    )

    custom_df = create_sample_price_dataframe(num_days=45, trend=1.5)
    mock_provider = MockMarketDataProvider(mock_df=custom_df)

    original_provider = get_default_market_data_provider()
    try:
        set_default_market_data_provider(mock_provider)
        assert get_default_market_data_provider() is mock_provider

        fetched_df = fetch_stock_dataframe_with_retry("VALE3", "1mo")
        assert len(fetched_df) == 45
        
        indicators = compute_technical_indicators(fetched_df)
        assert indicators.current_price > 0
        assert 0.0 <= indicators.rsi <= 100.0
    finally:
        set_default_market_data_provider(original_provider)


