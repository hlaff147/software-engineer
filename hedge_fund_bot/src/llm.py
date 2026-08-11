"""
Centralized LLM Factory with Native Structured Output Support

This module provides a single source of truth for LLM configuration across agents.

Patterns applied:
- Factory Pattern: Centralized object creation
- Profile Optimization: Temperature & token tuning per agent role
- Native Structured Output: Support for Pydantic schema extraction
"""

from enum import Enum
from typing import Dict, Any, Type, TypeVar
from pydantic import BaseModel
from langchain_groq import ChatGroq
from src.config import settings
import logging

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class LLMProfile(Enum):
    """
    Predefined LLM configurations for different use cases.
    """
    ROUTING = {
        "temperature": 0.0,
        "max_tokens": 256,
        "description": "For supervisor routing decisions - deterministic"
    }
    ANALYSIS = {
        "temperature": 0.2,
        "max_tokens": 1500,
        "description": "For researcher analysis - balanced creativity"
    }
    SYNTHESIS = {
        "temperature": 0.3,
        "max_tokens": 1500,
        "description": "For analyst report generation - structured synthesis"
    }
    STRICT = {
        "temperature": 0.0,
        "max_tokens": 1500,
        "description": "For chartist and verifier - zero creativity"
    }


def get_llm(
    profile: LLMProfile = LLMProfile.ANALYSIS,
    model: str = None,
    **kwargs
) -> ChatGroq:
    """
    Centralized LLM factory.
    """
    profile_settings = {
        k: v for k, v in profile.value.items() 
        if k != "description"
    }
    
    merged_settings = {**profile_settings, **kwargs}
    model_name = model or settings.MODEL_NAME
    
    logger.debug(f"Creating LLM instance: profile={profile.name}, model={model_name}")
    return ChatGroq(model=model_name, **merged_settings)


def get_structured_llm(
    schema: Type[T],
    profile: LLMProfile = LLMProfile.STRICT,
    model: str = None,
    **kwargs
):
    """
    Get an LLM instance configured with native Pydantic structured output.
    """
    llm = get_llm(profile=profile, model=model, **kwargs)
    return llm.with_structured_output(schema)


# Convenience functions for common use cases
def get_routing_llm(**kwargs) -> ChatGroq:
    """Get LLM configured for routing decisions (Supervisor)."""
    return get_llm(LLMProfile.ROUTING, **kwargs)


def get_analysis_llm(**kwargs) -> ChatGroq:
    """Get LLM configured for analysis tasks (Researcher)."""
    return get_llm(LLMProfile.ANALYSIS, **kwargs)


def get_synthesis_llm(**kwargs) -> ChatGroq:
    """Get LLM configured for synthesis/report generation (Analyst)."""
    return get_llm(LLMProfile.SYNTHESIS, **kwargs)


def get_strict_llm(**kwargs) -> ChatGroq:
    """Get LLM configured for strict validation (Chartist, Verifier)."""
    return get_llm(LLMProfile.STRICT, **kwargs)
