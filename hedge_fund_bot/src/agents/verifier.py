"""
Verifier Agent - PEV Pattern (Plan, Execute, Verify)

Validates the Analyst's report using deterministic rule-based checks
combined with native LLM structured verification. Zero regex parsing.
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.llm import get_structured_llm, LLMProfile
from src.schemas import VerifierResult, InvestmentReport, TechnicalAnalysisResult, ResearchSummary
from src.telemetry import TelemetryTimer
from src.config import AgentPrefix
import logging

logger = logging.getLogger(__name__)

VERIFIER_SYSTEM_PROMPT = """You are a Senior Risk Manager and Compliance Auditor at an institutional hedge fund.

Audit the Analyst's investment report against the gathered fundamental and technical data for ticker '{ticker}'.

ANALYST REPORT:
- Recommendation: {recommendation}
- Risk Level: {risk_level}
- Confidence Score: {confidence}%
- Justification: {justification}
- Executive Summary: {exec_summary}

TECHNICAL DATA:
- Current Price: ${current_price:.2f}
- RSI (14): {rsi} ({rsi_status})
- MACD Histogram: {macd_hist}
- Technical Outlook: {tech_outlook}

FUNDAMENTAL RESEARCH:
- Sentiment: {sentiment}
- Red Flags: {red_flags}

PRE-CHECKED DETERMINISTIC ISSUES (Rule Engine):
{rule_issues}

VERIFICATION GUIDELINES:
1. Recommendation MUST align with technicals (e.g. overbought RSI > 70 with BUY is suspicious).
2. Risk Level MUST accurately reflect volatile or negative signals.
3. If rule-based issues exist, flag verdict as 'NEEDS_REVISION'.
4. Provide actionable suggestions in 'recommendations' to help the Analyst revise."""


def run_deterministic_rule_checks(
    technical: TechnicalAnalysisResult,
    research: ResearchSummary,
    report: InvestmentReport
) -> list[str]:
    """
    Pure Python rule-based validation engine.
    Detects quantitative contradictions deterministically.
    """
    issues = []
    
    if not report:
        return ["No investment report provided for verification."]

    rec = report.recommendation
    risk = report.risk_level

    # RSI Checks
    if technical and technical.indicators:
        rsi = technical.indicators.rsi
        macd_hist = technical.indicators.macd_histogram

        if rsi > 72.0 and rec == "BUY":
            issues.append(f"Inconsistency: RSI is overbought ({rsi:.1f}) but recommendation is BUY.")
        
        if rsi < 28.0 and rec == "SELL":
            issues.append(f"Inconsistency: RSI is oversold ({rsi:.1f}) but recommendation is SELL.")

        if macd_hist < -1.0 and rec == "BUY":
            issues.append(f"Inconsistency: MACD histogram is strongly negative ({macd_hist:.4f}) but recommendation is BUY.")

        if macd_hist > 1.0 and rec == "SELL":
            issues.append(f"Inconsistency: MACD histogram is strongly positive ({macd_hist:.4f}) but recommendation is SELL.")

    # Risk level checks
    if research and research.red_flags and len(research.red_flags) >= 2 and risk == "LOW":
        issues.append(f"Inconsistency: Research detected multiple red flags ({', '.join(research.red_flags[:2])}) but risk level is set to LOW.")

    return issues


def verifier_node(state: AgentState) -> dict:
    """Verify report accuracy using deterministic rules + native structured LLM audit."""
    ticker = state.get("current_ticker", "UNKNOWN")
    report = state.get("final_report")
    technical = state.get("technical_data")
    research = state.get("research_data")
    current_iteration = state.get("iteration_count", 0)

    logger.info(f"Verifier node auditing report for {ticker} (iteration {current_iteration})...")

    if not report:
        logger.error("No report available in state for Verifier node.")
        return {
            "verification_passed": False,
            "iteration_count": current_iteration + 1
        }

    # 1. Deterministic Rule Checks (Pure Math/Logic)
    rule_issues = run_deterministic_rule_checks(technical, research, report)

    # 2. Extract values safely
    current_price = technical.indicators.current_price if technical and technical.indicators else 0.0
    rsi = technical.indicators.rsi if technical and technical.indicators else 50.0
    rsi_status = technical.rsi_status if technical else "NEUTRAL"
    macd_hist = technical.indicators.macd_histogram if technical and technical.indicators else 0.0
    tech_outlook = technical.technical_outlook if technical else "NEUTRAL"

    sentiment = research.market_sentiment if research else "NEUTRAL"
    red_flags = ", ".join(research.red_flags) if research and research.red_flags else "None"

    rule_issues_text = "\n".join([f"- {issue}" for issue in rule_issues]) if rule_issues else "None"

    prompt = VERIFIER_SYSTEM_PROMPT.format(
        ticker=ticker,
        recommendation=report.recommendation,
        risk_level=report.risk_level,
        confidence=report.confidence_score,
        justification=report.justification,
        exec_summary=report.executive_summary,
        current_price=current_price,
        rsi=rsi,
        rsi_status=rsi_status,
        macd_hist=macd_hist,
        tech_outlook=tech_outlook,
        sentiment=sentiment,
        red_flags=red_flags,
        rule_issues=rule_issues_text
    )

    with TelemetryTimer("Verifier") as timer:
        try:
            structured_llm = get_structured_llm(VerifierResult, profile=LLMProfile.STRICT)
            result: VerifierResult = structured_llm.invoke([HumanMessage(content=prompt)])
            
            # Combine rule issues with LLM issues
            all_issues = list(set(rule_issues + result.issues_found))
            result.issues_found = all_issues

            if rule_issues:
                result.is_valid = False
                result.verdict = "NEEDS_REVISION"

            telemetry = timer.record(prompt_tokens=450, completion_tokens=250)

        except Exception as e:
            logger.warning(f"Verifier LLM error ({e}), using deterministic rule result...")
            is_valid = len(rule_issues) == 0
            result = VerifierResult(
                is_valid=is_valid,
                confidence_score=90 if is_valid else 60,
                issues_found=rule_issues,
                recommendations=["Align recommendation with technical indicators and red flags"] if rule_issues else [],
                verdict="APPROVED" if is_valid else "NEEDS_REVISION",
                summary="Deterministic rule check verification fallback."
            )
            telemetry = timer.record(prompt_tokens=200, completion_tokens=80, status="FALLBACK")

    is_passed = result.is_valid and result.verdict == "APPROVED"
    new_iteration = current_iteration if is_passed else (current_iteration + 1)

    telemetry_list = list(state.get("telemetry", []))
    telemetry_list.append(telemetry)

    formatted_msg = (
        f"{AgentPrefix.VERIFIER} - Verdict: {result.verdict}]\n"
        f"Passed: {is_passed} | Confidence: {result.confidence_score}%\n"
        f"Issues ({len(result.issues_found)}): {', '.join(result.issues_found) if result.issues_found else 'None'}\n"
        f"Summary: {result.summary}"
    )

    return {
        "verification_passed": is_passed,
        "verification_result": result,
        "iteration_count": new_iteration,
        "telemetry": telemetry_list,
        "messages": [HumanMessage(content=formatted_msg)]
    }
