"""
Centralized LLM Factory

This module provides a single source of truth for LLM configuration.
All agents should import from here instead of creating their own LLM instances.

Patterns applied:
- Factory Pattern: Centralized object creation
- DRY: Single configuration point
- Separation of Concerns: LLM config separate from business logic
"""

from enum import Enum
from typing import Dict, Any
from langchain_groq import ChatGroq
import logging

logger = logging.getLogger(__name__)


class LLMProfile(Enum):
    """
    Predefined LLM configurations for different use cases.
    
    Each profile has optimized settings for its specific purpose:
    - ROUTING: Low creativity for deterministic routing decisions
    - ANALYSIS: Balanced for research and analysis tasks
    - SYNTHESIS: Higher creativity for report generation
    - STRICT: Zero creativity for validation and verification
    """
    ROUTING = {
        "temperature": 0,
        "max_tokens": 256,
        "description": "For supervisor routing decisions - deterministic"
    }
    ANALYSIS = {
        "temperature": 0.3,
        "max_tokens": 1500,
        "description": "For researcher analysis - balanced creativity"
    }
    SYNTHESIS = {
        "temperature": 0.4,
        "max_tokens": 1500,
        "description": "For analyst report generation - more creative"
    }
    STRICT = {
        "temperature": 0,
        "max_tokens": 1500,
        "description": "For chartist and verifier - zero creativity"
    }


# Default model - can be overridden via environment variable in config.py
DEFAULT_MODEL = "llama-3.3-70b-versatile"


def get_llm(
    profile: LLMProfile = LLMProfile.ANALYSIS,
    model: str = None,
    **kwargs
) -> ChatGroq:
    """
    Centralized LLM factory.
    
    Args:
        profile: Predefined configuration profile (LLMProfile enum)
        model: Override the default model (optional)
        **kwargs: Additional arguments to pass to ChatGroq
    
    Returns:
        Configured ChatGroq instance
    
    Example:
        >>> from src.llm import get_llm, LLMProfile
        >>> llm = get_llm(LLMProfile.ROUTING)
        >>> llm = get_llm(LLMProfile.ANALYSIS, temperature=0.5)  # Override
    """
    # Get profile settings (excluding description)
    profile_settings = {
        k: v for k, v in profile.value.items() 
        if k != "description"
    }
    
    # Merge with any overrides
    settings = {**profile_settings, **kwargs}
    
    # Use provided model or default
    model_name = model or DEFAULT_MODEL
    
    logger.debug(f"Creating LLM with profile={profile.name}, model={model_name}")
    
    return ChatGroq(model=model_name, **settings)


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
