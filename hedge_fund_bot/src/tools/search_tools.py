"""
Resilient Search Tools for Researcher Agent

Provides abstract SearchProvider interface and concrete providers
(DuckDuckGo, Mock) for financial news & market sentiment searches.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from src.schemas import NewsArticle

logger = logging.getLogger(__name__)


class SearchProvider(ABC):
    """Abstract Base Class for financial news search providers."""

    @abstractmethod
    def search_news(self, query: str, max_results: int = 5) -> List[NewsArticle]:
        """Search financial news matching query."""
        pass

    @abstractmethod
    def search_sentiment(self, ticker: str, max_results: int = 5) -> List[NewsArticle]:
        """Search news targeting sentiment for a stock ticker."""
        pass


class DuckDuckGoSearchProvider(SearchProvider):
    """Concrete SearchProvider using duckduckgo_search with tenacity retry backoff."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        retry=retry_if_exception_type(Exception),
        reraise=False
    )
    def search_news(self, query: str, max_results: int = 5) -> List[NewsArticle]:
        try:
            logger.info(f"[DuckDuckGoSearchProvider] Searching web news for query: '{query}'")
            results = DDGS().text(query, max_results=max_results)
            articles = []
            if results:
                for item in results:
                    articles.append(
                        NewsArticle(
                            title=item.get("title", "No Title"),
                            url=item.get("href", ""),
                            snippet=item.get("body", "")
                        )
                    )
            return articles
        except Exception as e:
            logger.warning(f"[DuckDuckGoSearchProvider] Search query failed for '{query}': {str(e)}")
            return []

    def search_sentiment(self, ticker: str, max_results: int = 5) -> List[NewsArticle]:
        query = f"{ticker} stock news market sentiment forecast"
        return self.search_news(query, max_results=max_results)


class MockSearchProvider(SearchProvider):
    """Mock SearchProvider for testing and offline execution."""

    def __init__(self, mock_articles: Optional[List[NewsArticle]] = None):
        self.mock_articles = mock_articles

    def search_news(self, query: str, max_results: int = 5) -> List[NewsArticle]:
        logger.info(f"[MockSearchProvider] Returning mock news for query: '{query}'")
        if self.mock_articles is not None:
            return self.mock_articles[:max_results]
        return [
            NewsArticle(
                title=f"Mock News for {query}",
                url="https://example.com/mock-news",
                snippet=f"Synthetic financial news article payload for search query '{query}'."
            )
        ][:max_results]

    def search_sentiment(self, ticker: str, max_results: int = 5) -> List[NewsArticle]:
        logger.info(f"[MockSearchProvider] Returning mock sentiment for ticker: '{ticker}'")
        if self.mock_articles is not None:
            return self.mock_articles[:max_results]
        return [
            NewsArticle(
                title=f"{ticker} Market Outlook Bullish",
                url=f"https://example.com/sentiment/{ticker}",
                snippet=f"Analyst consensus expects revenue growth and strong margins for {ticker}."
            )
        ][:max_results]


# Global default provider instance
_DEFAULT_PROVIDER: SearchProvider = DuckDuckGoSearchProvider()


def get_default_search_provider() -> SearchProvider:
    """Get current global search provider."""
    return _DEFAULT_PROVIDER


def set_default_search_provider(provider: SearchProvider) -> None:
    """Set global search provider (useful for dependency injection or testing)."""
    global _DEFAULT_PROVIDER
    _DEFAULT_PROVIDER = provider


def search_financial_news_with_retry(query: str, max_results: int = 5) -> List[NewsArticle]:
    """
    Search financial news via default SearchProvider.
    Maintains backward compatibility with existing agent callers.
    """
    return get_default_search_provider().search_news(query, max_results=max_results)


def search_market_sentiment(ticker: str, max_results: int = 5) -> List[NewsArticle]:
    """
    Search market sentiment via default SearchProvider.
    Maintains backward compatibility with existing agent callers.
    """
    return get_default_search_provider().search_sentiment(ticker, max_results=max_results)

