"""Supervisor Agent - Routes workflow based on current state"""

from langchain_core.messages import HumanMessage
from src.state import AgentState
from src.llm import get_routing_llm
from src.config import settings, AgentPrefix
from src.schemas import parse_supervisor_decision, SUPERVISOR_FORMAT_INSTRUCTION
from src.exceptions import LLMError
import logging

logger = logging.getLogger(__name__)

SUPERVISOR_PROMPT = """You are a senior hedge fund manager.

Workers: Researcher, Chartist, Analyst

Rules:
- If Researcher never ran, send to Researcher
- If Researcher finished, send to Chartist  
- If both finished, send to Analyst
- If final report exists, respond FINISH
- Never send to same agent twice in a row

{format_instruction}

History: {messages}
Ticker: {ticker}
Iteration: {iteration}"""


def supervisor_node(state: AgentState) -> dict:
    """Route to next agent using structured output parsing."""
    messages_str = "\n".join([f"[{m.type}]: {m.content[:100]}..." for m in state["messages"][-settings.CONTEXT_WINDOW_MESSAGES:]])
    
    prompt = SUPERVISOR_PROMPT.format(
        format_instruction=SUPERVISOR_FORMAT_INSTRUCTION,
        messages=messages_str,
        ticker=state.get("current_ticker", "UNKNOWN"),
        iteration=state.get("iteration_count", 0),
    )
    
    try:
        response = get_routing_llm().invoke([HumanMessage(content=prompt)])
        text = response.content.strip()
        
        decision = parse_supervisor_decision(text)
        next_agent = decision.next
        
        logger.info(f"Supervisor: {next_agent} (reason: {decision.reasoning})")
        return {"next": next_agent, "messages": [HumanMessage(content=f"{AgentPrefix.SUPERVISOR} Next: {next_agent}")]}
    
    except LLMError as e:
        logger.error(f"Supervisor LLM error: {e}")
        return {"next": "FINISH"}
    except Exception as e:
        logger.error(f"Supervisor error: {e}")
        return {"next": "FINISH"}
