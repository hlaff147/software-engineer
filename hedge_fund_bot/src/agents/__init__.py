# Agents Module
"""
Hedge Fund Bot Agents

This module contains all specialized agents:
- supervisor: Routes workflow based on current state (Meta-Controller pattern)
- researcher: Searches for news and market sentiment (Tool Use pattern)
- chartist: Performs technical analysis using yfinance (Tool Use pattern)
- analyst: Synthesizes final investment report (Multi-Agent pattern)
- verifier: Validates analyst recommendations (PEV pattern)
"""

from src.agents.supervisor import supervisor_node
from src.agents.researcher import researcher_node
from src.agents.chartist import chartist_node
from src.agents.analyst import analyst_node
from src.agents.verifier import verifier_node

__all__ = [
    "supervisor_node",
    "researcher_node",
    "chartist_node",
    "analyst_node",
    "verifier_node",
]
