"""
LangGraph Workflow - Multi-agent orchestration with PEV (Plan, Execute, Verify) Pattern

Architecture Patterns Used:
- Multi-Agent Systems: Specialized agents collaborate (Researcher, Chartist, Analyst)
- Tool Use: Agents use yfinance, search APIs for real-world data
- Meta-Controller: Supervisor routes to appropriate specialist agents
- PEV Pattern: Verifier validates Analyst output before finalizing
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
    PEV Pattern: Route based on verification result.
    
    - If verification passed → FINISH
    - If verification failed and retries remain → back to Analyst
    - If max retries exceeded → FINISH (accept with warnings)
    """
    verification_passed = state.get("verification_passed", True)
    iteration_count = state.get("iteration_count", 0)
    
    if verification_passed:
        logger.info("Verification PASSED - workflow complete")
        return "FINISH"
    
    if iteration_count < settings.MAX_VERIFICATION_RETRIES:
        logger.info(f"Verification FAILED - retrying (attempt {iteration_count + 1}/{settings.MAX_VERIFICATION_RETRIES})")
        return "Analyst"
    
    logger.warning("Max verification retries exceeded - completing with warnings")
    return "FINISH"


def create_graph():
    """
    Create and compile the LangGraph workflow with PEV pattern.
    
    Flow:
    1. Supervisor → routes to appropriate agent
    2. Researcher → gathers news and sentiment
    3. Chartist → performs technical analysis
    4. Analyst → generates investment report
    5. Verifier → validates the report (PEV pattern)
       - If valid → FINISH
       - If invalid → retry Analyst (up to MAX_VERIFICATION_RETRIES times)
    """
    workflow = StateGraph(AgentState)
    
    # Add nodes (including Verifier for PEV pattern)
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Chartist", chartist_node)
    workflow.add_node("Analyst", analyst_node)
    workflow.add_node("Verifier", verifier_node)  # PEV Pattern
    
    # Workers return to Supervisor
    workflow.add_edge("Researcher", "Supervisor")
    workflow.add_edge("Chartist", "Supervisor")
    
    # Analyst goes to Verifier (PEV pattern: Execute → Verify)
    workflow.add_edge("Analyst", "Verifier")
    
    # Verifier conditionally routes (PEV pattern: Verify → retry or finish)
    workflow.add_conditional_edges(
        "Verifier",
        route_after_verification,
        {"Analyst": "Analyst", "FINISH": END}
    )
    
    # Supervisor routes conditionally
    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {"Researcher": "Researcher", "Chartist": "Chartist", "Analyst": "Analyst", "FINISH": END}
    )
    
    workflow.set_entry_point("Supervisor")
    
    return workflow.compile()
