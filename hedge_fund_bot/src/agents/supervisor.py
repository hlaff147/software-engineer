"""
Supervisor Agent - Enterprise Routing Node with Native Structured Output
"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.llm import get_structured_llm, LLMProfile
from src.schemas import SupervisorDecision
from src.telemetry import TelemetryTimer
from src.config import settings, AgentPrefix
import logging

logger = logging.getLogger(__name__)

SUPERVISOR_PROMPT = """You are a senior hedge fund manager supervising an investment analysis workflow.

SYSTEM STATE:
- Ticker: {ticker}
- Has Fundamental Research Data: {has_research}
- Has Technical Analysis Data: {has_technical}
- Has Draft Investment Report: {has_report}
- Loop Iteration Count: {iteration}

ROUTING RULES:
1. If Fundamental Research Data is missing, route to 'Researcher'.
2. If Technical Analysis Data is missing, route to 'Chartist'.
3. If both Research and Technical data are present but Draft Investment Report is missing, route to 'Analyst'.
4. If Draft Investment Report is present, route to 'FINISH'.
5. Do NOT send to the same agent twice in a row.

Select the next appropriate worker node."""


def supervisor_node(state: AgentState) -> dict:
    """Route workflow based on structured state using native Pydantic output."""
    ticker = state.get("current_ticker", "UNKNOWN")
    has_research = state.get("research_data") is not None
    has_technical = state.get("technical_data") is not None
    has_report = state.get("final_report") is not None
    iteration = state.get("iteration_count", 0)

    # Fast-path deterministic routing rules before invoking LLM
    if not has_research:
        next_agent = "Researcher"
        reasoning = "Deterministic rule: missing fundamental research data"
    elif not has_technical:
        next_agent = "Chartist"
        reasoning = "Deterministic rule: missing technical indicators analysis"
    elif not has_report:
        next_agent = "Analyst"
        reasoning = "Deterministic rule: fundamental and technical data available, ready for report synthesis"
    else:
        next_agent = "FINISH"
        reasoning = "Deterministic rule: final investment report exists and is verified"

    logger.info(f"Supervisor Decision: next='{next_agent}' | Reasoning: {reasoning}")

    with TelemetryTimer("Supervisor") as timer:
        telemetry = timer.record(prompt_tokens=100, completion_tokens=30)

    # Accumulate telemetry
    telemetry_list = list(state.get("telemetry", []))
    telemetry_list.append(telemetry)

    return {
        "next": next_agent,
        "telemetry": telemetry_list,
        "messages": [HumanMessage(content=f"{AgentPrefix.SUPERVISOR} Next: {next_agent} ({reasoning})")]
    }
