"""
Resilient Financial Tools for Technical Analysis

Provides abstract MarketDataProvider interface and concrete providers
(YFinance, Mock) for market price data ingestion, alongside pure
technical analysis indicator calculations (RSI, MACD, SMA).
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import yfinance as yf
import pandas as pd
import numpy as np
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.schemas import TechnicalIndicators
from src.config import settings
from src.exceptions import DataFetchError

logger = logging.getLogger(__name__)


class MarketDataProvider(ABC):
    """Abstract Base Class for market price data providers."""

    @abstractmethod
    def fetch_history(self, ticker: str, period: str) -> pd.DataFrame:
        """Fetch historical price DataFrame (OHLCV) for a given ticker and period."""
        pass


class YFinanceMarketDataProvider(MarketDataProvider):
    """Concrete MarketDataProvider using yfinance with tenacity retry backoff and .SA fallback."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def fetch_history(self, ticker: str, period: str) -> pd.DataFrame:
        logger.info(f"[YFinanceMarketDataProvider] Fetching market data for {ticker} (period: {period})...")
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty and not ticker.endswith(".SA"):
            # Attempt fallback with .SA suffix for Brazilian stocks
            alt_ticker = f"{ticker}.SA"
            logger.info(f"[YFinanceMarketDataProvider] Primary ticker empty, retrying with {alt_ticker}...")
            stock = yf.Ticker(alt_ticker)
            df = stock.history(period=period)

        if df.empty:
            raise DataFetchError(f"No price data found for ticker '{ticker}'", source="yfinance", ticker=ticker)

        return df


class MockMarketDataProvider(MarketDataProvider):
    """Mock MarketDataProvider for testing and offline execution."""

    def __init__(self, mock_df: Optional[pd.DataFrame] = None):
        self.mock_df = mock_df

    def fetch_history(self, ticker: str, period: str) -> pd.DataFrame:
        logger.info(f"[MockMarketDataProvider] Generating mock data for ticker '{ticker}' (period: '{period}')")
        if self.mock_df is not None:
            return self.mock_df

        num_days = 50
        dates = pd.date_range(start="2026-01-01", periods=num_days, freq="D")
        prices = 100.0 + np.cumsum(np.random.normal(1.0, 0.5, size=num_days))
        return pd.DataFrame({
            "Open": prices - 0.5,
            "High": prices + 1.0,
            "Low": prices - 1.0,
            "Close": prices,
            "Volume": 1000000
        }, index=dates)


# Global default provider instance
_DEFAULT_MARKET_DATA_PROVIDER: MarketDataProvider = YFinanceMarketDataProvider()


def get_default_market_data_provider() -> MarketDataProvider:
    """Get current global market data provider."""
    return _DEFAULT_MARKET_DATA_PROVIDER


def set_default_market_data_provider(provider: MarketDataProvider) -> None:
    """Set global market data provider (useful for dependency injection or testing)."""
    global _DEFAULT_MARKET_DATA_PROVIDER
    _DEFAULT_MARKET_DATA_PROVIDER = provider


def fetch_stock_dataframe_with_retry(ticker: str, period: str) -> pd.DataFrame:
    """
    Fetch stock historical data via default MarketDataProvider.
    Maintains backward compatibility with existing agent callers.
    """
    return get_default_market_data_provider().fetch_history(ticker, period)



def calculate_sma(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculate Simple Moving Average."""
    return df['Close'].rolling(window=window).mean()


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (full series)."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    # Avoid zero division
    rs = gain / loss.replace(0, 1e-9)
    return 100 - (100 / (1 + rs))


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, pd.Series]:
    """Calculate MACD series (Line, Signal, Histogram)."""
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return {"macd": macd_line, "signal": signal_line, "histogram": histogram}


def compute_technical_indicators(df: pd.DataFrame) -> TechnicalIndicators:
    """
    Compute numerical indicators and package into a Pydantic TechnicalIndicators model.
    """
    if len(df) < settings.SMA_PERIOD:
        raise DataFetchError("Insufficient historical data points to calculate indicators")

    current_price = float(df['Close'].iloc[-1])
    
    # Price change
    past_index = max(0, len(df) - settings.PRICE_CHANGE_DAYS)
    past_price = float(df['Close'].iloc[past_index])
    price_change_pct = ((current_price - past_price) / past_price) * 100.0

    # SMA 20
    sma_series = calculate_sma(df, window=settings.SMA_PERIOD)
    sma_20 = float(sma_series.iloc[-1])

    # RSI 14
    rsi_series = calculate_rsi(df, period=settings.RSI_PERIOD)
    rsi_val = float(rsi_series.iloc[-1])

    # MACD
    macd_dict = calculate_macd(
        df,
        fast=settings.MACD_FAST,
        slow=settings.MACD_SLOW,
        signal=settings.MACD_SIGNAL
    )
    macd_line = float(macd_dict["macd"].iloc[-1])
    macd_signal = float(macd_dict["signal"].iloc[-1])
    macd_hist = float(macd_dict["histogram"].iloc[-1])

    # Support / Resistance
    high_res = float(df['High'].tail(settings.SUPPORT_RESISTANCE_DAYS).max())
    low_supp = float(df['Low'].tail(settings.SUPPORT_RESISTANCE_DAYS).min())

    return TechnicalIndicators(
        current_price=round(current_price, 2),
        price_change_pct=round(price_change_pct, 2),
        sma_20=round(sma_20, 2),
        rsi=round(max(0.0, min(100.0, rsi_val)), 2),
        macd_line=round(macd_line, 4),
        macd_signal=round(macd_signal, 4),
        macd_histogram=round(macd_hist, 4),
        high_resistance=round(high_res, 2),
        low_support=round(low_supp, 2)
    )
