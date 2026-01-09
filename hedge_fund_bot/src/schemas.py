"""
Structured Output Models and Parsers

This module provides Pydantic models for structured LLM outputs,
ensuring type-safe parsing with fallback handling.

Patterns applied:
- Type Safety: Pydantic models validate LLM outputs
- Graceful Degradation: Fallback parsing when strict parsing fails
- Schema Validation: Ensures outputs match expected structure
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Any
import json
import re
import logging

logger = logging.getLogger(__name__)


# =============================================================================
# Supervisor Output Models
# =============================================================================

class SupervisorDecision(BaseModel):
    """
    Structured output for Supervisor routing decisions.
    
    Example:
        {"next": "Researcher", "reasoning": "Need to gather news first"}
    """
    next: Literal["Researcher", "Chartist", "Analyst", "FINISH"]
    reasoning: Optional[str] = Field(default="", description="Brief reasoning for the decision")


# =============================================================================
# Verifier Output Models
# =============================================================================

class VerifierResult(BaseModel):
    """
    Structured output for Verifier validation results.
    
    Example:
        {
            "is_valid": true,
            "confidence_score": 85,
            "issues_found": [],
            "verdict": "APPROVED"
        }
    """
    is_valid: bool = Field(description="Whether the analysis passed verification")
    confidence_score: int = Field(ge=0, le=100, description="Confidence in the verification (0-100)")
    issues_found: List[str] = Field(default_factory=list, description="List of issues detected")
    recommendations: List[str] = Field(default_factory=list, description="Suggestions for improvement")
    verdict: Literal["APPROVED", "NEEDS_REVISION", "REJECTED"] = Field(description="Final verdict")
    summary: str = Field(default="", description="Brief explanation of the result")


# =============================================================================
# Analyst Output Models
# =============================================================================

class AnalystRecommendation(BaseModel):
    """
    Structured output for Analyst recommendations.
    """
    recommendation: Literal["BUY", "SELL", "HOLD"]
    risk_level: Literal["HIGH", "MEDIUM", "LOW"]
    confidence: int = Field(ge=0, le=100, default=70)
    summary: str = Field(default="")


# =============================================================================
# Parsing Functions
# =============================================================================

def extract_json_from_text(text: str) -> str:
    """
    Extract JSON from text that may contain markdown code blocks.
    
    Handles:
    - ```json ... ```
    - ``` ... ```
    - Raw JSON
    
    Args:
        text: Raw text that may contain JSON
        
    Returns:
        Extracted JSON string
    """
    text = text.strip()
    
    # Try to extract from code blocks
    if "```" in text:
        # Match ```json ... ``` or ``` ... ```
        pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        matches = re.findall(pattern, text)
        if matches:
            text = matches[0].strip()
    
    # Try to find JSON object in text
    if not text.startswith("{"):
        # Look for first { and last }
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]
    
    return text


def parse_supervisor_decision(text: str) -> SupervisorDecision:
    """
    Parse supervisor decision from LLM response.
    
    Args:
        text: Raw LLM response text
        
    Returns:
        Validated SupervisorDecision
        
    Raises:
        ValueError: If parsing fails completely
    """
    try:
        json_str = extract_json_from_text(text)
        data = json.loads(json_str)
        return SupervisorDecision(**data)
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to parse supervisor JSON: {e}, attempting fallback")
        
        # Fallback: try to extract agent name from text
        text_upper = text.upper()
        for agent in ["RESEARCHER", "CHARTIST", "ANALYST", "FINISH"]:
            if agent in text_upper:
                return SupervisorDecision(
                    next=agent if agent != "FINISH" else "FINISH",
                    reasoning=f"Fallback parsing: found '{agent}' in response"
                )
        
        # Default to FINISH if nothing found
        logger.error(f"Could not parse supervisor decision, defaulting to FINISH")
        return SupervisorDecision(next="FINISH", reasoning="Fallback: parsing failed")


def parse_verifier_result(text: str, quick_issues: List[str] = None) -> VerifierResult:
    """
    Parse verifier result from LLM response.
    
    Args:
        text: Raw LLM response text
        quick_issues: Pre-computed issues from rule-based checks
        
    Returns:
        Validated VerifierResult
    """
    quick_issues = quick_issues or []
    
    try:
        json_str = extract_json_from_text(text)
        data = json.loads(json_str)
        
        # Merge quick issues
        existing_issues = data.get("issues_found", [])
        data["issues_found"] = list(set(quick_issues + existing_issues))
        
        return VerifierResult(**data)
    except (json.JSONDecodeError, Exception) as e:
        logger.warning(f"Failed to parse verifier JSON: {e}, using fallback")
        
        # Fallback based on quick issues
        has_issues = len(quick_issues) > 0
        return VerifierResult(
            is_valid=not has_issues,
            confidence_score=70 if not has_issues else 50,
            issues_found=quick_issues,
            recommendations=[],
            verdict="NEEDS_REVISION" if has_issues else "APPROVED",
            summary=text[:500] if text else "Fallback verification"
        )


def extract_recommendation_from_text(text: str) -> Optional[AnalystRecommendation]:
    """
    Extract recommendation from analyst report text.
    
    Args:
        text: Analyst report text
        
    Returns:
        AnalystRecommendation if found, None otherwise
    """
    text_upper = text.upper()
    
    # Extract recommendation
    recommendation = None
    for rec in ["BUY", "SELL", "HOLD"]:
        if rec in text_upper:
            recommendation = rec
            break
    
    if not recommendation:
        return None
    
    # Extract risk level
    risk_level = "MEDIUM"  # Default
    if "HIGH RISK" in text_upper or "RISK: HIGH" in text_upper or "RISK LEVEL: HIGH" in text_upper:
        risk_level = "HIGH"
    elif "LOW RISK" in text_upper or "RISK: LOW" in text_upper or "RISK LEVEL: LOW" in text_upper:
        risk_level = "LOW"
    elif "MEDIUM RISK" in text_upper or "RISK: MEDIUM" in text_upper or "RISK LEVEL: MEDIUM" in text_upper:
        risk_level = "MEDIUM"
    
    return AnalystRecommendation(
        recommendation=recommendation,
        risk_level=risk_level,
        confidence=70
    )


# =============================================================================
# Format Instructions for Prompts
# =============================================================================

SUPERVISOR_FORMAT_INSTRUCTION = """
Respond with JSON only, no other text:
{"next": "Researcher|Chartist|Analyst|FINISH", "reasoning": "brief reason"}
"""

VERIFIER_FORMAT_INSTRUCTION = """
Respond with JSON only:
{
    "is_valid": true/false,
    "confidence_score": 0-100,
    "issues_found": ["issue1", "issue2"],
    "recommendations": ["suggestion1", "suggestion2"],
    "verdict": "APPROVED" / "NEEDS_REVISION" / "REJECTED",
    "summary": "Brief explanation"
}
"""
