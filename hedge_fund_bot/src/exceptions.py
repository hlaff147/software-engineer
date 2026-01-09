"""
Custom Exceptions Module

This module defines a hierarchy of custom exceptions for better error handling.
Each exception type represents a specific failure mode that can be handled appropriately.

Patterns applied:
- Exception Hierarchy: Specific exceptions for different failure types
- Fail-Fast vs Graceful Degradation: Some errors are recoverable, others are not
- Error Context: Each exception carries meaningful context
"""

from typing import Optional, Dict, Any


class AgentError(Exception):
    """
    Base exception for all agent-related errors.
    
    All custom exceptions inherit from this, allowing for:
    - Catching all agent errors with one except clause
    - Adding common functionality (logging, context)
    """
    
    def __init__(
        self,
        message: str,
        agent_name: Optional[str] = None,
        ticker: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.agent_name = agent_name
        self.ticker = ticker
        self.context = context or {}
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        """Format error message with context."""
        parts = [self.message]
        if self.agent_name:
            parts.insert(0, f"[{self.agent_name}]")
        if self.ticker:
            parts.append(f"(ticker: {self.ticker})")
        return " ".join(parts)


class DataFetchError(AgentError):
    """
    Failed to fetch external data (API calls, web requests).
    
    This is often a transient error that can be retried.
    
    Example:
        >>> raise DataFetchError("Failed to fetch stock data", ticker="AAPL")
    """
    
    def __init__(
        self,
        message: str,
        source: Optional[str] = None,
        **kwargs
    ):
        self.source = source  # e.g., "yfinance", "duckduckgo"
        super().__init__(message, **kwargs)


class LLMError(AgentError):
    """
    LLM API error (rate limits, model errors, parsing failures).
    
    Some of these are transient (rate limits), others are not (parsing).
    
    Example:
        >>> raise LLMError("Rate limit exceeded", agent_name="Supervisor")
    """
    
    def __init__(
        self,
        message: str,
        model: Optional[str] = None,
        is_rate_limit: bool = False,
        **kwargs
    ):
        self.model = model
        self.is_rate_limit = is_rate_limit
        super().__init__(message, **kwargs)


class ValidationError(AgentError):
    """
    Input or output validation failed.
    
    This is typically not recoverable - the input needs to be fixed.
    
    Example:
        >>> raise ValidationError("Invalid ticker format", ticker="INVALID123")
    """
    
    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Optional[Any] = None,
        **kwargs
    ):
        self.field = field
        self.value = value
        super().__init__(message, **kwargs)


class VerificationError(AgentError):
    """
    Verification step failed (PEV pattern).
    
    This triggers a retry in the workflow.
    
    Example:
        >>> raise VerificationError("Recommendation inconsistent with data")
    """
    
    def __init__(
        self,
        message: str,
        issues: Optional[list] = None,
        **kwargs
    ):
        self.issues = issues or []
        super().__init__(message, **kwargs)


class WorkflowError(AgentError):
    """
    Workflow-level errors (graph execution, routing).
    
    Example:
        >>> raise WorkflowError("Max iterations exceeded")
    """
    pass


# =============================================================================
# Retry Configuration
# =============================================================================

# Define which exceptions should trigger retries
RETRYABLE_EXCEPTIONS = (
    DataFetchError,
)

# Define which exceptions indicate rate limiting
RATE_LIMIT_EXCEPTIONS = (
    LLMError,  # Check is_rate_limit attribute
)


def is_retryable(exception: Exception) -> bool:
    """
    Check if an exception should trigger a retry.
    
    Args:
        exception: The exception to check
        
    Returns:
        True if the exception is retryable
    """
    if isinstance(exception, RETRYABLE_EXCEPTIONS):
        return True
    if isinstance(exception, LLMError) and exception.is_rate_limit:
        return True
    return False


def format_error_for_user(exception: Exception) -> str:
    """
    Format an exception into a user-friendly message.
    
    Args:
        exception: The exception to format
        
    Returns:
        User-friendly error message
    """
    if isinstance(exception, ValidationError):
        return f"❌ Invalid input: {exception.message}"
    elif isinstance(exception, DataFetchError):
        return f"⚠️ Could not fetch data: {exception.message}"
    elif isinstance(exception, LLMError):
        if exception.is_rate_limit:
            return "⏳ Rate limit reached. Please try again in a moment."
        return f"🤖 AI processing error: {exception.message}"
    elif isinstance(exception, VerificationError):
        return f"⚠️ Verification failed: {exception.message}"
    elif isinstance(exception, AgentError):
        return f"❌ Error: {exception.message}"
    else:
        return f"❌ Unexpected error: {str(exception)}"
