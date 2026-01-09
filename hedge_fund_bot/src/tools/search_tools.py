"""
Search Tools for the Researcher Agent
"""

from duckduckgo_search import DDGS
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def search_financial_news(query: str, max_results: int = 5) -> List[Dict]:
    """Search financial news using DuckDuckGo."""
    try:
        results = DDGS().text(query, max_results=max_results)
        return list(results) if results else []
    except Exception as e:
        logger.error(f"Error searching news: {str(e)}")
        return []


def search_market_sentiment(ticker: str, max_results: int = 5) -> List[Dict]:
    """Search market sentiment for a stock."""
    query = f"{ticker} stock analysis market sentiment"
    return search_financial_news(query, max_results)
