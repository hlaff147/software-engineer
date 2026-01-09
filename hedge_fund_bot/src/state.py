"""
Global State for the Autonomous Hedge Fund System
"""

from typing import Annotated, List, TypedDict
from langchain_core.messages import BaseMessage
import operator


class AgentState(TypedDict):
    """
    State schema for LangGraph workflow.
    
    Attributes:
        messages: Full conversation history (append-only)
        next: Next agent to execute or "FINISH"
        current_ticker: Stock ticker being analyzed
        current_stock_data: Structured data scratchpad
        iteration_count: Loop guard counter
        verification_passed: Whether the Verifier approved the report (PEV pattern)
        verification_result: Detailed verification output
    """
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    current_ticker: str
    current_stock_data: dict
    iteration_count: int
    verification_passed: bool
    verification_result: dict
