"""
Verifier Agent - PEV Pattern (Plan, Execute, Verify)

This agent validates the Analyst's recommendations by:
1. Checking recommendation consistency with technical data
2. Validating RSI interpretation against actual values
3. Ensuring risk level aligns with analysis
4. Flagging contradictions between fundamental and technical analysis
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.llm import get_strict_llm
from src.config import AgentPrefix
from src.schemas import parse_verifier_result, VERIFIER_FORMAT_INSTRUCTION
from src.exceptions import LLMError, VerificationError
import logging
import re

logger = logging.getLogger(__name__)


VERIFIER_PROMPT = """You are a senior risk manager and quality assurance specialist at a hedge fund.

Your job is to VERIFY the analyst's report for consistency and accuracy.

## ANALYST REPORT TO VERIFY:
{analyst_report}

## FULL CONTEXT (Technical & Fundamental Data):
{full_context}

## VERIFICATION CHECKLIST:

1. **Recommendation Consistency**: Does the BUY/SELL/HOLD recommendation align with:
   - RSI values (>70 overbought suggests caution, <30 oversold suggests opportunity)
   - MACD signals (positive histogram = bullish, negative = bearish)
   - Price vs SMA (above = bullish, below = bearish)
   - News sentiment (positive/negative catalysts)

2. **RSI Interpretation**: Is the RSI correctly interpreted?
   - RSI > 70: Should mention overbought/caution
   - RSI < 30: Should mention oversold/opportunity
   - RSI 30-70: Neutral zone

3. **Risk Level Accuracy**: Does the risk level (High/Medium/Low) match the analysis?
   - High volatility + mixed signals = High Risk
   - Clear trend + consistent signals = Lower Risk
   - Negative news + weak technicals = High Risk

4. **Contradiction Detection**: Are there contradictions between:
   - Fundamental analysis (news) vs Technical analysis (indicators)
   - The recommendation vs the supporting evidence

{format_instruction}

Be strict but fair. Only mark as invalid if there are significant inconsistencies."""


def extract_technical_data(messages: list) -> dict:
    """Extract technical data from Chartist message."""
    data = {}
    for msg in messages:
        content = msg.content
        if "[CHARTIST" in content:
            # Extract RSI
            rsi_match = re.search(r'RSI.*?:\s*([\d.]+)', content)
            if rsi_match:
                data['rsi'] = float(rsi_match.group(1))
            
            # Extract MACD Histogram
            macd_match = re.search(r'MACD Histogram:\s*([-\d.]+)', content)
            if macd_match:
                data['macd_histogram'] = float(macd_match.group(1))
            
            # Extract Price vs SMA
            sma_match = re.search(r'Price vs SMA20:\s*(\w+)', content)
            if sma_match:
                data['price_vs_sma'] = sma_match.group(1)
            
            # Extract price change
            change_match = re.search(r'Price Change:\s*([-\d.]+)%', content)
            if change_match:
                data['price_change'] = float(change_match.group(1))
                
    return data


def extract_analyst_recommendation(messages: list) -> dict:
    """Extract recommendation from Analyst message."""
    result = {'recommendation': None, 'risk_level': None}
    for msg in messages:
        if "[ANALYST" in msg.content:
            content = msg.content.upper()
            
            # Extract recommendation
            if 'BUY' in content:
                result['recommendation'] = 'BUY'
            elif 'SELL' in content:
                result['recommendation'] = 'SELL'
            elif 'HOLD' in content:
                result['recommendation'] = 'HOLD'
            
            # Extract risk level
            if 'HIGH RISK' in content or 'RISK: HIGH' in content or 'RISK LEVEL: HIGH' in content:
                result['risk_level'] = 'HIGH'
            elif 'LOW RISK' in content or 'RISK: LOW' in content or 'RISK LEVEL: LOW' in content:
                result['risk_level'] = 'LOW'
            elif 'MEDIUM RISK' in content or 'RISK: MEDIUM' in content or 'RISK LEVEL: MEDIUM' in content:
                result['risk_level'] = 'MEDIUM'
                
    return result


def quick_validation(tech_data: dict, analyst_rec: dict) -> list:
    """Perform quick rule-based validation checks."""
    issues = []
    
    rsi = tech_data.get('rsi')
    recommendation = analyst_rec.get('recommendation')
    macd_histogram = tech_data.get('macd_histogram')
    
    if rsi and recommendation:
        # Check RSI consistency
        if rsi > 70 and recommendation == 'BUY':
            issues.append(f"RSI is {rsi:.1f} (overbought) but recommendation is BUY")
        if rsi < 30 and recommendation == 'SELL':
            issues.append(f"RSI is {rsi:.1f} (oversold) but recommendation is SELL")
    
    if macd_histogram and recommendation:
        # Check MACD consistency
        if macd_histogram < -0.5 and recommendation == 'BUY':
            issues.append(f"MACD histogram is strongly negative ({macd_histogram:.4f}) but recommendation is BUY")
        if macd_histogram > 0.5 and recommendation == 'SELL':
            issues.append(f"MACD histogram is strongly positive ({macd_histogram:.4f}) but recommendation is SELL")
    
    return issues


def verifier_node(state: AgentState) -> dict:
    """Verify the analyst's report for consistency and accuracy."""
    ticker = state.get("current_ticker", "UNKNOWN")
    messages = state.get("messages", [])
    current_iteration = state.get("iteration_count", 0)  # Track iteration for retry logic
    
    # Find analyst report
    analyst_report = None
    for msg in reversed(messages):
        if "[ANALYST" in msg.content:
            analyst_report = msg.content
            break
    
    if not analyst_report:
        return {
            "messages": [HumanMessage(content="[VERIFIER - ERROR]\n\nNo analyst report found to verify.")],
            "verification_passed": False
        }
    
    # Extract data for validation
    tech_data = extract_technical_data(messages)
    analyst_rec = extract_analyst_recommendation(messages)
    
    # Quick rule-based checks
    quick_issues = quick_validation(tech_data, analyst_rec)
    
    # Build full context
    full_context = "\n\n---\n\n".join([msg.content for msg in messages[-6:]])
    
    try:
        # LLM-based deep verification (using centralized factory)
        prompt = VERIFIER_PROMPT.format(
            analyst_report=analyst_report,
            full_context=full_context,
            format_instruction=VERIFIER_FORMAT_INSTRUCTION
        )
        
        response = get_strict_llm().invoke([HumanMessage(content=prompt)])
        text = response.content.strip()
        
        # Use structured parsing from schemas module
        result = parse_verifier_result(text, quick_issues=quick_issues)
        
        # Merge quick issues with LLM findings
        all_issues = list(set(quick_issues + result.issues_found))
        
        # Determine if verification passed
        is_valid = result.is_valid and result.verdict != "REJECTED"
        confidence = result.confidence_score
        
        # Build verification report
        verification_report = f"""[VERIFIER - {'✅ APPROVED' if is_valid else '⚠️ NEEDS REVIEW'}]

**Ticker:** {ticker}
**Verdict:** {result.verdict}
**Confidence Score:** {confidence}/100

## Verification Results

### Quick Checks
- Recommendation: {analyst_rec.get('recommendation', 'N/A')}
- Risk Level: {analyst_rec.get('risk_level', 'N/A')}
- RSI Extracted: {tech_data.get('rsi', 'N/A')}
- MACD Histogram: {tech_data.get('macd_histogram', 'N/A')}

### Issues Found ({len(all_issues)})
{chr(10).join([f"- ⚠️ {issue}" for issue in all_issues]) if all_issues else "- ✅ No significant issues detected"}

### Recommendations
{chr(10).join([f"- 💡 {rec}" for rec in result.recommendations]) if result.recommendations else "- No additional recommendations"}

### Summary
{result.summary}
"""
        
        logger.info(f"Verifier executed for {ticker}: {result.verdict}")
        
        # INCREMENT iteration_count when verification fails (for retry limiting)
        new_iteration = current_iteration + 1 if not is_valid else current_iteration
        
        return {
            "messages": [HumanMessage(content=verification_report)],
            "verification_passed": is_valid,
            "verification_result": result.model_dump(),  # Convert Pydantic model to dict
            "iteration_count": new_iteration  # Track retries to prevent infinite loops
        }
    
    except LLMError as e:
        logger.error(f"Verifier LLM error: {e}")
        return {
            "messages": [HumanMessage(content=f"[VERIFIER ERROR] LLM parsing failed: {str(e)}")],
            "verification_passed": True,  # Don't block on verification errors
            "iteration_count": current_iteration
        }
    except VerificationError as e:
        logger.error(f"Verifier validation error: {e}")
        return {
            "messages": [HumanMessage(content=f"[VERIFIER ERROR] Validation failed: {str(e)}")],
            "verification_passed": False,
            "iteration_count": current_iteration + 1
        }
    except Exception as e:
        logger.error(f"Verifier unexpected error: {e}")
        return {
            "messages": [HumanMessage(content=f"[VERIFIER ERROR] {str(e)}")],
            "verification_passed": True,  # Don't block on unexpected errors
            "iteration_count": current_iteration
        }
