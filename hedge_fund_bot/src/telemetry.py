"""
Telemetry and Metrics Module for Agent System Observability

Tracks:
- Execution latency per graph node
- Token counts (prompt, completion, total)
- Estimated cost based on model pricing
- Aggregated session metrics
"""

import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


# Cost per 1M tokens (Groq Llama 3.3 70B rates as benchmark)
MODEL_PRICING = {
    "llama-3.3-70b-versatile": {"input": 0.59 / 1_000_000, "output": 0.79 / 1_000_000},
    "llama3-70b-8192": {"input": 0.59 / 1_000_000, "output": 0.79 / 1_000_000},
    "default": {"input": 0.50 / 1_000_000, "output": 0.70 / 1_000_000},
}


class NodeTelemetry(BaseModel):
    """Telemetry data for a single agent node execution."""
    node_name: str = Field(description="Name of the graph node")
    execution_time_seconds: float = Field(description="Execution latency in seconds")
    prompt_tokens: int = Field(default=0, description="Input tokens used")
    completion_tokens: int = Field(default=0, description="Output tokens generated")
    total_tokens: int = Field(default=0, description="Total tokens for this call")
    estimated_cost_usd: float = Field(default=0.0, description="Estimated cost in USD")
    status: str = Field(default="SUCCESS", description="Execution status: SUCCESS or ERROR")


class SessionTelemetry(BaseModel):
    """Aggregated session telemetry across all graph nodes."""
    ticker: str
    total_execution_time_seconds: float = 0.0
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    node_telemetries: List[NodeTelemetry] = Field(default_factory=list)

    def add_node_telemetry(self, telemetry: NodeTelemetry) -> None:
        """Add node telemetry and update session aggregates."""
        self.node_telemetries.append(telemetry)
        self.total_execution_time_seconds += telemetry.execution_time_seconds
        self.total_prompt_tokens += telemetry.prompt_tokens
        self.total_completion_tokens += telemetry.completion_tokens
        self.total_tokens += telemetry.total_tokens
        self.total_cost_usd += telemetry.estimated_cost_usd


def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model_name: str = "llama-3.3-70b-versatile") -> float:
    """Calculate estimated cost for token usage."""
    pricing = MODEL_PRICING.get(model_name, MODEL_PRICING["default"])
    input_cost = prompt_tokens * pricing["input"]
    output_cost = completion_tokens * pricing["output"]
    return round(input_cost + output_cost, 6)


class TelemetryTimer:
    """Context manager to measure node latency and build NodeTelemetry."""
    def __init__(self, node_name: str, model_name: str = "llama-3.3-70b-versatile"):
        self.node_name = node_name
        self.model_name = model_name
        self.start_time: float = 0.0
        self.end_time: float = 0.0

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()

    def record(
        self,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        status: str = "SUCCESS"
    ) -> NodeTelemetry:
        """Create NodeTelemetry record from timer run."""
        latency = round(self.end_time - self.start_time, 3)
        total_tokens = prompt_tokens + completion_tokens
        cost = calculate_token_cost(prompt_tokens, completion_tokens, self.model_name)
        
        telemetry = NodeTelemetry(
            node_name=self.node_name,
            execution_time_seconds=latency,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost_usd=cost,
            status=status
        )
        logger.info(
            f"Telemetry [{self.node_name}]: Latency={latency}s | "
            f"Tokens={total_tokens} (Prompt: {prompt_tokens}, Completion: {completion_tokens}) | "
            f"Cost=${cost:.6f}"
        )
        return telemetry
