"""Chartist Agent - Technical analysis using yfinance"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.tools.financial_tools import get_latest_rsi, get_latest_macd
from src.llm import get_strict_llm
from src.config import settings, AgentPrefix
from src.exceptions import DataFetchError, LLMError, format_error_for_user
import yfinance as yf
import logging

logger = logging.getLogger(__name__)


CHARTIST_PROMPT = """You are a technical analyst. Analyze these indicators for {ticker}:

TECHNICAL DATA:
{technical_data}

Provide analysis covering:
1. Price action and trend
2. RSI interpretation (overbought >70, oversold <30)
3. MACD signal (bullish/bearish crossover)
4. Support and resistance levels
5. Overall technical outlook"""


def chartist_node(state: AgentState) -> dict:
    """Run technical analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    # Normalize ticker for yfinance
    ticker_yf = ticker if ticker.endswith(".SA") or "." in ticker else ticker
    
    try:
        # Fetch data (using config for period)
        stock = yf.Ticker(ticker_yf)
        df = stock.history(period=settings.HISTORY_PERIOD)
        
        if df.empty:
            # Try with .SA suffix for Brazilian stocks
            ticker_yf = f"{ticker}.SA"
            stock = yf.Ticker(ticker_yf)
            df = stock.history(period=settings.HISTORY_PERIOD)
        
        if df.empty:
            raise DataFetchError(
                f"No data available for {ticker}",
                source="yfinance",
                ticker=ticker,
                agent_name="Chartist"
            )
        
        # Calculate indicators (using centralized functions and config)
        current_price = df['Close'].iloc[-1]
        price_change = ((current_price - df['Close'].iloc[-settings.PRICE_CHANGE_DAYS]) / df['Close'].iloc[-settings.PRICE_CHANGE_DAYS]) * 100
        sma = df['Close'].rolling(settings.SMA_PERIOD).mean().iloc[-1]
        rsi = get_latest_rsi(df, period=settings.RSI_PERIOD)
        macd = get_latest_macd(df, fast=settings.MACD_FAST, slow=settings.MACD_SLOW, signal=settings.MACD_SIGNAL)
        high_nd = df['High'].tail(settings.SUPPORT_RESISTANCE_DAYS).max()
        low_nd = df['Low'].tail(settings.SUPPORT_RESISTANCE_DAYS).min()
        
        technical_data = f"""
Current Price: ${current_price:.2f}
{settings.PRICE_CHANGE_DAYS}-day Price Change: {price_change:.1f}%
SMA {settings.SMA_PERIOD}: ${sma:.2f}
RSI ({settings.RSI_PERIOD}): {rsi:.1f}
MACD: {macd['macd']:.4f}
MACD Signal: {macd['signal']:.4f}
MACD Histogram: {macd['histogram']:.4f}
{settings.SUPPORT_RESISTANCE_DAYS}-day High (Resistance): ${high_nd:.2f}
{settings.SUPPORT_RESISTANCE_DAYS}-day Low (Support): ${low_nd:.2f}
Price vs SMA{settings.SMA_PERIOD}: {'Above' if current_price > sma else 'Below'}
"""
        
        # Generate analysis with LLM (using centralized factory)
        prompt = CHARTIST_PROMPT.format(ticker=ticker, technical_data=technical_data)
        response = get_strict_llm().invoke([HumanMessage(content=prompt)])
        
        logger.info(f"Chartist executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"{AgentPrefix.CHARTIST} - {ticker}]\n\n{technical_data}\n\nANALYSIS:\n{response.content}")]}
    
    except DataFetchError as e:
        # Specific handling for data fetch errors
        logger.warning(f"Chartist data fetch error: {e}", exc_info=True)
        return {"messages": [HumanMessage(content=f"{AgentPrefix.CHARTIST} ERROR] {format_error_for_user(e)}")]}
    
    except LLMError as e:
        # Specific handling for LLM errors
        logger.error(f"Chartist LLM error: {e}", exc_info=True)
        return {"messages": [HumanMessage(content=f"{AgentPrefix.CHARTIST} ERROR] {format_error_for_user(e)}")]}
    
    except Exception as e:
        # Catch-all for unexpected errors (log full stack trace)
        logger.error(f"Chartist unexpected error: {e}", exc_info=True)
        return {"messages": [HumanMessage(content=f"{AgentPrefix.CHARTIST} ERROR] Unexpected error: {str(e)}")]}
