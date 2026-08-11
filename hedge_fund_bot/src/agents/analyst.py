"""
Analyst Agent - Investment Report Synthesis Node (Native Structured Output)
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.llm import get_structured_llm, LLMProfile
from src.schemas import InvestmentReport
from src.telemetry import TelemetryTimer
from src.config import AgentPrefix
import logging

logger = logging.getLogger(__name__)

ANALYST_SYSTEM_PROMPT = """You are a Chief Investment Officer (CIO) and Senior Portfolio Manager at an elite hedge fund.

Synthesize the structured fundamental research data and technical indicators into a comprehensive, professional investment report for stock ticker '{ticker}'.

FUNDAMENTAL RESEARCH DATA:
- Market Sentiment: {sentiment}
- Executive Summary: {research_summary}
- Catalysts: {catalysts}
- Red Flags: {red_flags}

TECHNICAL INDICATORS & ANALYSIS:
- Current Price: ${current_price:.2f}
- Price Change: {price_change}%
- RSI (14): {rsi} ({rsi_status})
- MACD Histogram: {macd_hist}
- Price vs SMA20: {price_vs_sma}
- Technical Outlook: {tech_outlook}
- Technical Summary: {tech_summary}

VERIFICATION REVISION FEEDBACK (if any):
{verifier_feedback}

INSTRUCTIONS:
1. Recommendation MUST be one of: BUY, SELL, HOLD.
2. Risk level MUST be one of: HIGH, MEDIUM, LOW.
3. Provide a clear 2-3 sentence justification matching the technical and fundamental evidence.
4. Set a confidence score between 0 and 100."""


def analyst_node(state: AgentState) -> dict:
    """Synthesize structured research & technical data into an InvestmentReport model."""
    ticker = state.get("current_ticker", "UNKNOWN")
    research = state.get("research_data")
    technical = state.get("technical_data")
    verification = state.get("verification_result")

    logger.info(f"Analyst node synthesizing investment report for {ticker}...")

    # Extract clean typed attributes from state
    sentiment = research.market_sentiment if research else "NEUTRAL"
    research_summary = research.summary if research else "N/A"
    catalysts = ", ".join(research.catalysts) if research and research.catalysts else "None"
    red_flags = ", ".join(research.red_flags) if research and research.red_flags else "None"

    if technical and technical.indicators:
        current_price = technical.indicators.current_price
        price_change = technical.indicators.price_change_pct
        rsi = technical.indicators.rsi
        rsi_status = technical.rsi_status
        macd_hist = technical.indicators.macd_histogram
        price_vs_sma = technical.price_vs_sma
        tech_outlook = technical.technical_outlook
        tech_summary = technical.analysis_summary
    else:
        current_price, price_change, rsi, macd_hist = 0.0, 0.0, 50.0, 0.0
        rsi_status, price_vs_sma, tech_outlook, tech_summary = "NEUTRAL", "EQUAL", "NEUTRAL", "N/A"

    verifier_feedback = "None"
    if verification and verification.recommendations:
        verifier_feedback = "\n".join([f"- {rec}" for rec in verification.recommendations])

    prompt = ANALYST_SYSTEM_PROMPT.format(
        ticker=ticker,
        sentiment=sentiment,
        research_summary=research_summary,
        catalysts=catalysts,
        red_flags=red_flags,
        current_price=current_price,
        price_change=price_change,
        rsi=rsi,
        rsi_status=rsi_status,
        macd_hist=macd_hist,
        price_vs_sma=price_vs_sma,
        tech_outlook=tech_outlook,
        tech_summary=tech_summary,
        verifier_feedback=verifier_feedback
    )

    with TelemetryTimer("Analyst") as timer:
        try:
            structured_llm = get_structured_llm(InvestmentReport, profile=LLMProfile.SYNTHESIS)
            report: InvestmentReport = structured_llm.invoke([HumanMessage(content=prompt)])
            report.ticker = ticker
            telemetry = timer.record(prompt_tokens=500, completion_tokens=400)
        except Exception as e:
            logger.warning(f"Analyst structured output error ({e}), constructing fallback report...")
            recommendation = "BUY" if (sentiment == "BULLISH" and tech_outlook == "BULLISH") else ("SELL" if sentiment == "BEARISH" else "HOLD")
            report = InvestmentReport(
                ticker=ticker,
                executive_summary=f"Synthesized analysis for {ticker}. Fundamental sentiment is {sentiment}, technical outlook is {tech_outlook}.",
                fundamental_analysis=research_summary,
                technical_analysis=tech_summary,
                recommendation=recommendation,
                risk_level="MEDIUM",
                justification=f"Analysis combines {sentiment} fundamental sentiment with {tech_outlook} technical signals.",
                confidence_score=75
            )
            telemetry = timer.record(prompt_tokens=250, completion_tokens=100, status="FALLBACK")

    telemetry_list = list(state.get("telemetry", []))
    telemetry_list.append(telemetry)

    formatted_msg = (
        f"{AgentPrefix.ANALYST} - FINAL REPORT]\n\n"
        f"# Investment Report: {ticker}\n"
        f"**Recommendation:** {report.recommendation} | **Risk Level:** {report.risk_level} | **Confidence:** {report.confidence_score}%\n\n"
        f"## Executive Summary\n{report.executive_summary}\n\n"
        f"## Fundamental Analysis\n{report.fundamental_analysis}\n\n"
        f"## Technical Analysis\n{report.technical_analysis}\n\n"
        f"## Justification\n{report.justification}"
    )

    return {
        "final_report": report,
        "telemetry": telemetry_list,
        "messages": [HumanMessage(content=formatted_msg)]
    }
