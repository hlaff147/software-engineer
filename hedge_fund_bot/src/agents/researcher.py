"""Researcher Agent - Searches for news and market sentiment"""

from langchain_core.messages import HumanMessage
from src.tools.search_tools import search_financial_news, search_market_sentiment
from src.state import AgentState
from src.llm import get_analysis_llm
from src.config import settings, AgentPrefix
import logging

logger = logging.getLogger(__name__)


RESEARCHER_PROMPT = """You are a financial researcher at a hedge fund.

Analyze the following news and market sentiment data for {ticker}, then provide a summary.

NEWS:
{news}

MARKET SENTIMENT:
{sentiment}

Provide a concise summary (max 300 words) covering:
1. Key recent news and events
2. Overall market sentiment (bullish/bearish/neutral)
3. Any red flags or positive catalysts"""


def researcher_node(state: AgentState) -> dict:
    """Search for news and analysis."""
    ticker = state.get("current_ticker", "UNKNOWN")
    
    try:
        # Search for news (using config for max_results)
        news_results = search_financial_news(f"{ticker} stock news", max_results=settings.NEWS_MAX_RESULTS)
        news_text = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')[:200]}" for r in news_results]) or "No news found"
        
        # Search for sentiment
        sentiment_results = search_market_sentiment(ticker, max_results=settings.NEWS_MAX_RESULTS)
        sentiment_text = "\n".join([f"- {r.get('title', '')}: {r.get('body', '')[:200]}" for r in sentiment_results]) or "No sentiment data found"
        
        # Generate summary with LLM (using centralized factory)
        prompt = RESEARCHER_PROMPT.format(ticker=ticker, news=news_text, sentiment=sentiment_text)
        response = get_analysis_llm().invoke([HumanMessage(content=prompt)])
        
        logger.info(f"Researcher executed for {ticker}")
        
        return {"messages": [HumanMessage(content=f"{AgentPrefix.RESEARCHER} - {ticker}]\n\n{response.content}")]}
    
    except Exception as e:
        logger.error(f"Researcher error: {e}")
        return {"messages": [HumanMessage(content=f"{AgentPrefix.RESEARCHER} ERROR] {str(e)}")]}
