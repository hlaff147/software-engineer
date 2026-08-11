"""
Chartist Agent - Technical Indicators & Quantitative Analysis Node
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.tools.financial_tools import (
    fetch_stock_dataframe_with_retry,
    compute_technical_indicators,
)
from src.llm import get_structured_llm, LLMProfile
from src.schemas import TechnicalAnalysisResult
from src.telemetry import TelemetryTimer
from src.config import settings, AgentPrefix
from src.exceptions import DataFetchError
import logging

logger = logging.getLogger(__name__)

CHARTIST_PROMPT = """You are a quantitative technical analyst at a hedge fund.

Analyze these calculated technical indicators for stock ticker '{ticker}':

CALCULATED INDICATORS:
- Current Price: ${current_price:.2f}
- Price Change: {price_change_pct:.2f}%
- SMA (20 days): ${sma_20:.2f}
- RSI (14 days): {rsi:.2f}
- MACD Line: {macd_line:.4f}
- MACD Signal: {macd_signal:.4f}
- MACD Histogram: {macd_histogram:.4f}
- 30-Day Resistance (High): ${high_resistance:.2f}
- 30-Day Support (Low): ${low_support:.2f}

Provide a structured technical analysis assessment including technical_outlook, rsi_status, price_vs_sma, analysis_summary, and key_signals."""


def chartist_node(state: AgentState) -> dict:
    """Perform technical indicator calculations and emit a structured TechnicalAnalysisResult."""
    ticker = state.get("current_ticker", "UNKNOWN")
    logger.info(f"Chartist node executing for {ticker}...")

    with TelemetryTimer("Chartist") as timer:
        try:
            # 1. Fetch dataframe with tenacity retry
            df = fetch_stock_dataframe_with_retry(ticker, period=settings.HISTORY_PERIOD)
            
            # 2. Compute pure mathematical indicators (Pydantic model)
            indicators = compute_technical_indicators(df)

            prompt = CHARTIST_PROMPT.format(
                ticker=ticker,
                current_price=indicators.current_price,
                price_change_pct=indicators.price_change_pct,
                sma_20=indicators.sma_20,
                rsi=indicators.rsi,
                macd_line=indicators.macd_line,
                macd_signal=indicators.macd_signal,
                macd_histogram=indicators.macd_histogram,
                high_resistance=indicators.high_resistance,
                low_support=indicators.low_support
            )

            # 3. LLM structured interpretation
            structured_llm = get_structured_llm(TechnicalAnalysisResult, profile=LLMProfile.STRICT)
            tech_result: TechnicalAnalysisResult = structured_llm.invoke([HumanMessage(content=prompt)])
            # Inject exact computed indicators object
            tech_result.indicators = indicators
            
            telemetry = timer.record(prompt_tokens=350, completion_tokens=250)

        except DataFetchError as e:
            logger.error(f"Chartist data fetch error: {e}")
            raise e
        except Exception as e:
            logger.warning(f"Chartist LLM interpretation error ({e}), constructing fallback indicators model...")
            # Fallback using direct computed indicators
            df = fetch_stock_dataframe_with_retry(ticker, period=settings.HISTORY_PERIOD)
            indicators = compute_technical_indicators(df)

            rsi_status = "OVERBOUGHT" if indicators.rsi > 70 else ("OVERSOLD" if indicators.rsi < 30 else "NEUTRAL")
            price_vs_sma = "ABOVE" if indicators.current_price > indicators.sma_20 else "BELOW"
            outlook = "BULLISH" if (indicators.rsi < 70 and indicators.macd_histogram > 0) else "NEUTRAL"

            tech_result = TechnicalAnalysisResult(
                ticker=ticker,
                indicators=indicators,
                technical_outlook=outlook,
                rsi_status=rsi_status,
                price_vs_sma=price_vs_sma,
                analysis_summary=f"Price is ${indicators.current_price:.2f}, RSI is {indicators.rsi:.1f}, MACD Histogram is {indicators.macd_histogram:.4f}.",
                key_signals=[f"RSI status: {rsi_status}", f"Price vs SMA20: {price_vs_sma}"]
            )
            telemetry = timer.record(prompt_tokens=150, completion_tokens=50, status="FALLBACK")

    telemetry_list = list(state.get("telemetry", []))
    telemetry_list.append(telemetry)

    formatted_msg = (
        f"{AgentPrefix.CHARTIST} - {ticker}]\n"
        f"Price: ${tech_result.indicators.current_price:.2f} | RSI: {tech_result.indicators.rsi:.1f} ({tech_result.rsi_status})\n"
        f"MACD Hist: {tech_result.indicators.macd_histogram:.4f} | Outlook: {tech_result.technical_outlook}\n"
        f"Summary: {tech_result.analysis_summary}"
    )

    return {
        "technical_data": tech_result,
        "telemetry": telemetry_list,
        "messages": [HumanMessage(content=formatted_msg)]
    }
