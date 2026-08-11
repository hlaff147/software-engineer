"""
Unit Tests for HTML Report Generation Module
"""

import os
import pytest
import tempfile
from src.reporting import generate_html_report
from src.schemas import (
    ResearchSummary,
    TechnicalAnalysisResult,
    TechnicalIndicators,
    InvestmentReport,
    VerifierResult,
)
from src.telemetry import NodeTelemetry


def test_generate_html_report_success():
    """Test generating HTML report with complete AgentState data."""
    mock_state = {
        "current_ticker": "AAPL",
        "research_data": ResearchSummary(
            ticker="AAPL",
            summary="Apple reported strong earnings growth driven by iPhone and Services.",
            market_sentiment="BULLISH",
            key_events=["Q4 Earnings Beat", "AI Feature Launch"],
            catalysts=["Services Expansion", "High Margin AI Tier"],
            red_flags=["China Competition"],
        ),
        "technical_data": TechnicalAnalysisResult(
            ticker="AAPL",
            indicators=TechnicalIndicators(
                current_price=230.50,
                price_change_pct=2.45,
                sma_20=225.10,
                rsi=62.4,
                macd_line=1.20,
                macd_signal=0.85,
                macd_histogram=0.35,
                high_resistance=235.00,
                low_support=220.00,
            ),
            technical_outlook="BULLISH",
            rsi_status="NEUTRAL",
            price_vs_sma="ABOVE",
            analysis_summary="Stock is in a strong uptrend above 20-day SMA with positive MACD.",
            key_signals=["RSI in neutral range", "Price above SMA 20"],
        ),
        "final_report": InvestmentReport(
            ticker="AAPL",
            executive_summary="Solid fundamental performance combined with bullish technical setup.",
            fundamental_analysis="Robust revenue growth across key segments.",
            technical_analysis="Price trading above key moving averages.",
            recommendation="BUY",
            risk_level="LOW",
            justification="High market share, strong cash flows, and positive momentum.",
            confidence_score=85,
        ),
        "verification_result": VerifierResult(
            is_valid=True,
            confidence_score=90,
            issues_found=[],
            recommendations=[],
            verdict="APPROVED",
            summary="Investment report is fully consistent with technical and fundamental findings.",
        ),
        "telemetry": [
            NodeTelemetry(
                node_name="Researcher",
                execution_time_seconds=1.2,
                prompt_tokens=400,
                completion_tokens=300,
                status="SUCCESS",
            ),
            NodeTelemetry(
                node_name="Chartist",
                execution_time_seconds=0.8,
                prompt_tokens=350,
                completion_tokens=250,
                status="SUCCESS",
            ),
        ],
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = generate_html_report(mock_state, output_dir=tmp_dir)

        assert os.path.exists(filepath)
        assert filepath.endswith(".html")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert "AAPL" in content
        assert "BUY" in content
        assert "230.50" in content
        assert "APPROVED" in content
        assert "Apple reported strong earnings growth" in content
        assert "Services Expansion" in content
        assert "China Competition" in content
        assert "Total Execution Latency" in content


def test_generate_html_report_empty_state():
    """Test generating HTML report with empty/minimal state without throwing exceptions."""
    minimal_state = {
        "current_ticker": "UNKNOWN",
        "research_data": None,
        "technical_data": None,
        "final_report": None,
        "verification_result": None,
        "telemetry": [],
    }

    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = generate_html_report(minimal_state, output_dir=tmp_dir)

        assert os.path.exists(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        assert "UNKNOWN" in content
        assert "No analyst report was generated" in content
