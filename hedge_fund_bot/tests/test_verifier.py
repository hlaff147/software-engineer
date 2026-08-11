"""
Unit Tests for Verifier Deterministic Rule Engine
"""

import pytest
from src.agents.verifier import run_deterministic_rule_checks
from src.schemas import (
    TechnicalAnalysisResult,
    TechnicalIndicators,
    ResearchSummary,
    InvestmentReport,
)


@pytest.fixture
def sample_technical_data():
    return TechnicalAnalysisResult(
        ticker="AAPL",
        indicators=TechnicalIndicators(
            current_price=150.0,
            price_change_pct=2.5,
            sma_20=145.0,
            rsi=75.0,  # Overbought!
            macd_line=1.2,
            macd_signal=1.0,
            macd_histogram=0.2,
            high_resistance=155.0,
            low_support=140.0
        ),
        technical_outlook="BULLISH",
        rsi_status="OVERBOUGHT",
        price_vs_sma="ABOVE",
        analysis_summary="Strong momentum",
        key_signals=["RSI > 70"]
    )


@pytest.fixture
def sample_research_data():
    return ResearchSummary(
        ticker="AAPL",
        summary="Positive earnings report.",
        market_sentiment="BULLISH",
        key_events=["Q3 Record Revenue"],
        catalysts=["iPhone sales surge"],
        red_flags=["Regulatory investigation in EU", "Supply chain bottleneck"]
    )


def test_verifier_flags_overbought_buy(sample_technical_data, sample_research_data):
    """Test that RSI > 70 combined with BUY recommendation triggers an inconsistency issue."""
    report = InvestmentReport(
        ticker="AAPL",
        executive_summary="Buy recommendation.",
        fundamental_analysis="Strong fundamentals.",
        technical_analysis="RSI is 75.",
        recommendation="BUY",
        risk_level="MEDIUM",
        justification="Strong momentum.",
        confidence_score=80
    )

    issues = run_deterministic_rule_checks(sample_technical_data, sample_research_data, report)
    assert len(issues) > 0
    assert any("overbought" in issue.lower() for issue in issues)


def test_verifier_flags_low_risk_with_multiple_red_flags(sample_technical_data, sample_research_data):
    """Test that multiple red flags combined with LOW risk level triggers an inconsistency issue."""
    # Modify RSI to neutral
    sample_technical_data.indicators.rsi = 50.0
    
    report = InvestmentReport(
        ticker="AAPL",
        executive_summary="Buy recommendation.",
        fundamental_analysis="Fundamentals.",
        technical_analysis="Technicals.",
        recommendation="HOLD",
        risk_level="LOW",  # Contradicts 2 red flags!
        justification="Low risk hold.",
        confidence_score=80
    )

    issues = run_deterministic_rule_checks(sample_technical_data, sample_research_data, report)
    assert len(issues) > 0
    assert any("red flags" in issue.lower() for issue in issues)


def test_verifier_passes_consistent_report(sample_technical_data, sample_research_data):
    """Test that a consistent report passes without issues."""
    sample_technical_data.indicators.rsi = 55.0
    sample_research_data.red_flags = []

    report = InvestmentReport(
        ticker="AAPL",
        executive_summary="Consistent report.",
        fundamental_analysis="Fundamentals.",
        technical_analysis="Technicals.",
        recommendation="BUY",
        risk_level="MEDIUM",
        justification="Solid metrics across fundamental and technical analysis.",
        confidence_score=85
    )

    issues = run_deterministic_rule_checks(sample_technical_data, sample_research_data, report)
    assert len(issues) == 0
