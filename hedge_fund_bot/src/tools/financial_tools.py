"""
Financial Tools for the Chartist Agent
"""

from typing import Dict
import yfinance as yf
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def fetch_stock_data(ticker: str, period: str = "1y", interval: str = "1d") -> Dict:
    """Fetch historical stock data using yfinance."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            return {"success": False, "error": f"No data found for {ticker}", "ticker": ticker}
        
        return {
            "success": True,
            "data": df,
            "ticker": ticker,
            "shape": df.shape,
            "date_range": f"{df.index[0].date()} to {df.index[-1].date()}"
        }
    except Exception as e:
        logger.error(f"Error fetching data for {ticker}: {str(e)}")
        return {"success": False, "error": str(e), "ticker": ticker}


def calculate_sma(df: pd.DataFrame, window: int = 20) -> pd.Series:
    """Calculate Simple Moving Average."""
    return df['Close'].rolling(window=window).mean()


def calculate_rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculate Relative Strength Index (full series)."""
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def get_latest_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """Calculate RSI and return the latest value."""
    return calculate_rsi(df, period).iloc[-1]


def calculate_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """Calculate MACD (full series)."""
    ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return {"macd": macd_line, "signal": signal_line, "histogram": macd_line - signal_line}


def get_latest_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
    """Calculate MACD and return the latest values."""
    result = calculate_macd(df, fast, slow, signal)
    return {
        "macd": result["macd"].iloc[-1],
        "signal": result["signal"].iloc[-1],
        "histogram": result["histogram"].iloc[-1]
    }


def get_stock_info(ticker: str) -> Dict:
    """Get general stock information."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "success": True,
            "longName": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "currentPrice": info.get("currentPrice", "N/A"),
            "marketCap": info.get("marketCap", "N/A"),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
