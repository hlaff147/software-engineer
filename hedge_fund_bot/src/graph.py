"""
LangGraph Workflow - Multi-Agent State Machine Architecture

Architecture Patterns Applied:
- Strongly Typed State Machine: LangGraph StateGraph with Pydantic AgentState
- Multi-Agent Orchestration: Supervisor, Researcher, Chartist, Analyst, Verifier
- PEV Pattern: Execute (Analyst) -> Verify (Verifier) -> Retry or Finish
- Deterministic Loop Guards: Iteration counter prevents infinite agent loops
"""

from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.agents.supervisor import supervisor_node
from src.agents.researcher import researcher_node
from src.agents.chartist import chartist_node
from src.agents.analyst import analyst_node
from src.agents.verifier import verifier_node
from src.config import settings
import logging

logger = logging.getLogger(__name__)


def route_after_verification(state: AgentState) -> str:
    """
    PEV Pattern Router: Direct execution flow based on verification verdict.
    
    - If verification_passed is True -> END
    - If verification_passed is False and iteration_count < MAX_VERIFICATION_RETRIES -> Analyst (retry)
    - If max retries reached -> END (accept best report with log warning)
    """
    verification_passed = state.get("verification_passed", False)
    iteration_count = state.get("iteration_count", 0)
    
    if verification_passed:
        logger.info("PEV Routing: Verification PASSED - Completing workflow.")
        return "FINISH"
    
    if iteration_count < settings.MAX_VERIFICATION_RETRIES:
        logger.info(f"PEV Routing: Verification FAILED - Triggering Analyst retry (Attempt {iteration_count + 1}/{settings.MAX_VERIFICATION_RETRIES})")
        return "Analyst"
    
    logger.warning(f"PEV Routing: Max verification retries ({settings.MAX_VERIFICATION_RETRIES}) exceeded. Finishing workflow with warnings.")
    return "FINISH"


def create_graph():
    """
    Construct and compile the LangGraph multi-agent workflow.
    
    Workflow Topology:
    1. Entry -> Supervisor
    2. Supervisor routes conditionally:
       - Researcher -> returns to Supervisor
       - Chartist -> returns to Supervisor
       - Analyst -> advances to Verifier
    3. Analyst -> Verifier (PEV pattern)
    4. Verifier -> conditional routing:
       - Approved -> END
       - Failed (within retry budget) -> Analyst
       - Failed (exceeded budget) -> END
    """
    workflow = StateGraph(AgentState)
    
    # Register graph nodes
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Chartist", chartist_node)
    workflow.add_node("Analyst", analyst_node)
    workflow.add_node("Verifier", verifier_node)
    
    # Worker completion edges back to Supervisor
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Chartist", "Supervisor")
    
    # Analyst advances to Verifier (Execute -> Verify)
    workflow.add_edge("Analyst", "Verifier")
    
    # Conditional verification routing (Verify -> Retry or Finish)
    workflow.add_conditional_edges(
        "Verifier",
        route_after_verification,
        {"Analyst": "Analyst", "FINISH": END}
    )
    
    # Supervisor conditional routing
    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {
            "Researcher": "Researcher",
            "Chartist": "Chartist",
            "Analyst": "Analyst",
            "FINISH": END
        }
    )
    
    workflow.set_entry_point("Supervisor")
    
    return workflow.compile()
