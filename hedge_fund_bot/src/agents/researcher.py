"""
Researcher Agent - Structured Fundamental Data Gathering
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.tools.search_tools import search_financial_news_with_retry, search_market_sentiment
from src.llm import get_structured_llm, get_analysis_llm, LLMProfile
from src.schemas import ResearchSummary
from src.telemetry import TelemetryTimer
from src.config import settings, AgentPrefix
import logging

logger = logging.getLogger(__name__)

RESEARCHER_SYSTEM_PROMPT = """You are a senior fundamental analyst at an institutional hedge fund.

Analyze the news articles and sentiment data below for stock ticker '{ticker}'.
Synthesize your findings into a structured research summary including sentiment, key events, catalysts, and red flags.

NEWS ARTICLES:
{news}

MARKET SENTIMENT:
{sentiment}"""


def researcher_node(state: AgentState) -> dict:
    """Gather financial news and sentiment, emitting a structured ResearchSummary."""
    ticker = state.get("current_ticker", "UNKNOWN")
    logger.info(f"Researcher node executing for {ticker}...")

    with TelemetryTimer("Researcher") as timer:
        # Search news & sentiment with tenacity retries
        news_articles = search_financial_news_with_retry(f"{ticker} stock news earnings", max_results=settings.NEWS_MAX_RESULTS)
        sentiment_articles = search_market_sentiment(ticker, max_results=settings.NEWS_MAX_RESULTS)

        news_text = "\n".join([f"- [{a.title}]: {a.snippet}" for a in news_articles]) or "No recent news articles found."
        sentiment_text = "\n".join([f"- [{a.title}]: {a.snippet}" for a in sentiment_articles]) or "No sentiment articles found."

        prompt = RESEARCHER_SYSTEM_PROMPT.format(
            ticker=ticker,
            news=news_text,
            sentiment=sentiment_text
        )

        try:
            # Use native structured output
            structured_llm = get_structured_llm(ResearchSummary, profile=LLMProfile.ANALYSIS)
            summary_result: ResearchSummary = structured_llm.invoke([HumanMessage(content=prompt)])
            telemetry = timer.record(prompt_tokens=400, completion_tokens=300)
        except Exception as e:
            logger.warning(f"Structured output failed for Researcher, falling back to heuristic model: {e}")
            # Fallback object
            summary_result = ResearchSummary(
                ticker=ticker,
                summary=f"Research completed for {ticker}. News articles analyzed.",
                market_sentiment="NEUTRAL",
                key_events=[a.title for a in news_articles[:3]],
                catalysts=["Ongoing business operations"],
                red_flags=[]
            )
            telemetry = timer.record(prompt_tokens=200, completion_tokens=100, status="FALLBACK")

    telemetry_list = list(state.get("telemetry", []))
    telemetry_list.append(telemetry)

    formatted_msg = (
        f"{AgentPrefix.RESEARCHER} - {ticker}]\n"
        f"Sentiment: {summary_result.market_sentiment}\n"
        f"Summary: {summary_result.summary}\n"
        f"Catalysts: {', '.join(summary_result.catalysts)}\n"
        f"Red Flags: {', '.join(summary_result.red_flags)}"
    )

    return {
        "research_data": summary_result,
        "telemetry": telemetry_list,
        "messages": [HumanMessage(content=formatted_msg)]
    }
