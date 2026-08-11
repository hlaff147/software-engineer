"""
Global State for the Autonomous Hedge Fund System (LangGraph Typed State)

Maintains structured domain objects alongside context window messages.
"""

from typing import Annotated, List, Optional, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from src.schemas import (
    ResearchSummary,
    TechnicalAnalysisResult,
    InvestmentReport,
    VerifierResult,
)
from src.telemetry import NodeTelemetry


class AgentState(TypedDict):
    """
    State schema for LangGraph workflow.
    
    Attributes:
        messages: Conversation message history with add_messages reducer
        next: Next agent node to execute or "FINISH"
        current_ticker: Stock ticker being analyzed
        research_data: Typed summary from Researcher node
        technical_data: Typed indicators & analysis from Chartist node
        final_report: Typed investment report from Analyst node
        verification_passed: Whether the Verifier approved the report (PEV pattern)
        verification_result: Detailed verification output
        iteration_count: Loop guard counter for retries
        telemetry: Execution metrics collected per node
    """
    messages: Annotated[List[BaseMessage], add_messages]
    next: str
    current_ticker: str
    research_data: Optional[ResearchSummary]
    technical_data: Optional[TechnicalAnalysisResult]
    final_report: Optional[InvestmentReport]
    verification_passed: bool
    verification_result: Optional[VerifierResult]
    iteration_count: int
    telemetry: List[NodeTelemetry]
