"""
Structured Output Models and Parsers (Pydantic v2)

Provides strict, strongly-typed domain models for native LLM function calling
and state machine transitions, eliminating regex and string parsing.

Patterns applied:
- Pydantic v2 Strong Typing & Schema Enforcement
- Native Structured Outputs via Provider APIs
- Enterprise Validation & Field Constraints
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, List, Optional, Dict, Any


# =============================================================================
# Researcher Domain Models
# =============================================================================

class NewsArticle(BaseModel):
    """Structured model for a single news article."""
    title: str = Field(description="Article headline")
    url: Optional[str] = Field(default="", description="Source URL")
    snippet: str = Field(description="Brief summary/snippet")


class ResearchSummary(BaseModel):
    """
    Structured output for Researcher Agent.
    Replaces raw markdown string outputs.
    """
    ticker: str = Field(description="Stock ticker symbol")
    summary: str = Field(description="Executive summary of news and research")
    market_sentiment: Literal["BULLISH", "BEARISH", "NEUTRAL"] = Field(
        description="Overall market sentiment"
    )
    key_events: List[str] = Field(default_factory=list, description="Key recent events")
    catalysts: List[str] = Field(default_factory=list, description="Positive growth catalysts")
    red_flags: List[str] = Field(default_factory=list, description="Risks and red flags")


# =============================================================================
# Chartist Technical Analysis Models
# =============================================================================

class TechnicalIndicators(BaseModel):
    """Strict numerical values for technical indicators."""
    current_price: float = Field(description="Latest closing price")
    price_change_pct: float = Field(description="Price change percentage over period")
    sma_20: float = Field(description="Simple Moving Average (20 days)")
    rsi: float = Field(ge=0.0, le=100.0, description="Relative Strength Index (14 days)")
    macd_line: float = Field(description="MACD main line value")
    macd_signal: float = Field(description="MACD signal line value")
    macd_histogram: float = Field(description="MACD histogram value")
    high_resistance: float = Field(description="Period high / resistance price")
    low_support: float = Field(description="Period low / support price")


class TechnicalAnalysisResult(BaseModel):
    """
    Structured output for Chartist Agent.
    Combines numerical indicators and technical interpretation.
    """
    ticker: str = Field(description="Stock ticker symbol")
    indicators: TechnicalIndicators = Field(description="Calculated numerical indicators")
    technical_outlook: Literal["BULLISH", "BEARISH", "NEUTRAL"] = Field(
        description="Overall technical perspective"
    )
    rsi_status: Literal["OVERBOUGHT", "OVERSOLD", "NEUTRAL"] = Field(
        description="RSI condition assessment"
    )
    price_vs_sma: Literal["ABOVE", "BELOW", "EQUAL"] = Field(
        description="Current price vs SMA20"
    )
    analysis_summary: str = Field(description="Detailed technical analysis explanation")
    key_signals: List[str] = Field(default_factory=list, description="Key technical signals observed")


# =============================================================================
# Analyst Output Models
# =============================================================================

class InvestmentReport(BaseModel):
    """
    Structured output for Analyst Agent.
    Final synthesized report presented to portfolio managers and users.
    """
    ticker: str = Field(description="Stock ticker symbol")
    executive_summary: str = Field(description="High-level executive summary")
    fundamental_analysis: str = Field(description="Fundamental research findings")
    technical_analysis: str = Field(description="Technical research findings")
    recommendation: Literal["BUY", "SELL", "HOLD"] = Field(
        description="Final investment recommendation"
    )
    risk_level: Literal["HIGH", "MEDIUM", "LOW"] = Field(
        description="Assessed risk level"
    )
    justification: str = Field(description="Clear justification for recommendation (2-3 sentences)")
    confidence_score: int = Field(
        ge=0, le=100, default=70, description="Confidence score from 0 to 100"
    )


# =============================================================================
# Supervisor Routing Models
# =============================================================================

class SupervisorDecision(BaseModel):
    """
    Structured output for Supervisor routing decisions.
    """
    next: Literal["Researcher", "Chartist", "Analyst", "FINISH"] = Field(
        description="Next target worker node or FINISH"
    )
    reasoning: str = Field(default="", description="Brief rationale for the routing choice")


# =============================================================================
# Verifier Output Models (PEV Pattern)
# =============================================================================

class VerifierResult(BaseModel):
    """
    Structured output for Verifier validation.
    Enforces deterministic consistency between technicals, research, and report.
    """
    is_valid: bool = Field(description="Whether the report passed all consistency checks")
    confidence_score: int = Field(ge=0, le=100, description="Confidence score in the evaluation")
    issues_found: List[str] = Field(default_factory=list, description="List of detected inconsistencies")
    recommendations: List[str] = Field(default_factory=list, description="Actionable revision notes for Analyst")
    verdict: Literal["APPROVED", "NEEDS_REVISION", "REJECTED"] = Field(description="Final verdict")
    summary: str = Field(default="", description="Explanation of the verdict")
