# 🧠 AI Agent Architecture Patterns

This document describes the four AI agent architecture patterns implemented in the Hedge Fund Bot system.

---

## Overview

The Hedge Fund Bot uses a combination of proven AI agent patterns to create a robust, accurate, and self-correcting stock analysis system.

```
┌─────────────────────────────────────────────────────────────────┐
│                        HEDGE FUND BOT                           │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  RESEARCHER  │    │   CHARTIST   │    │   ANALYST    │      │
│  │  (Tool Use)  │    │  (Tool Use)  │    │(Multi-Agent) │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └─────────┬─────────┘                   │               │
│                   ▼                             ▼               │
│         ┌──────────────────┐          ┌──────────────┐         │
│         │    SUPERVISOR    │◄─────────│   VERIFIER   │         │
│         │(Meta-Controller) │          │ (PEV Pattern)│         │
│         └──────────────────┘          └──────────────┘         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Pattern 1: Multi-Agent Systems (#05)

### Concept
A team of specialized agents collaborates to solve a problem, dividing labor to achieve superior depth, quality, and structure in the final output.

### Implementation in This Project

| Agent | Specialization | Responsibility |
|-------|---------------|----------------|
| **Researcher** | Fundamental Analysis | Gathers news, market sentiment, and qualitative data |
| **Chartist** | Technical Analysis | Calculates RSI, MACD, SMA, support/resistance levels |
| **Analyst** | Synthesis | Combines all data into a final investment report |
| **Verifier** | Quality Assurance | Validates consistency and accuracy of recommendations |

### Benefits
- **Specialization**: Each agent is optimized for its specific task
- **Modularity**: Easy to add/remove/modify individual agents
- **Quality**: Multiple perspectives lead to better analysis
- **Traceability**: Clear audit trail of each agent's contribution

### Code Location
- `src/agents/researcher.py`
- `src/agents/chartist.py`
- `src/agents/analyst.py`
- `src/agents/verifier.py`

---

## Pattern 2: Tool Use (#02)

### Concept
Empowers agents to overcome knowledge cutoffs and interact with the real world by calling external APIs and functions.

### Implementation in This Project

```python
# Chartist uses yfinance for real-time market data
stock = yf.Ticker("AAPL")
df = stock.history(period="3mo")

# Researcher uses search APIs for news
news_results = search_financial_news(f"{ticker} stock news")
sentiment_results = search_market_sentiment(ticker)
```

### Tools Used

| Tool | Purpose | Agent |
|------|---------|-------|
| **yfinance** | Historical price data, stock info | Chartist |
| **DuckDuckGo Search** | Financial news search | Researcher |
| **Sentiment Search** | Market sentiment analysis | Researcher |

### Technical Indicators Calculated
- **SMA** (Simple Moving Average) - 20-day
- **RSI** (Relative Strength Index) - 14-day
- **MACD** (Moving Average Convergence Divergence)
- **Support/Resistance** - 30-day high/low

### Benefits
- **Real-time Data**: Access to current market information
- **Accuracy**: No reliance on potentially outdated training data
- **Extensibility**: Easy to add new tools and data sources

### Code Location
- `src/tools/financial_tools.py`
- `src/tools/search_tools.py`

---

## Pattern 3: Meta-Controller (#11)

### Concept
A supervisory agent that analyzes incoming tasks and routes them to the most appropriate specialist sub-agent from a pool of experts.

### Implementation in This Project

```python
# Supervisor decides which agent to invoke next
SUPERVISOR_PROMPT = """
Rules:
- If Researcher never ran, send to Researcher
- If Researcher finished, send to Chartist  
- If both finished, send to Analyst
- If final report exists, respond FINISH
"""
```

### Workflow Routing

```
                    ┌─────────────┐
                    │  SUPERVISOR │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌───────────┐    ┌───────────┐    ┌───────────┐
   │ RESEARCHER│    │  CHARTIST │    │  ANALYST  │
   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘
         │                │                │
         └────────────────┴────────────────┘
                          │
                          ▼
                   (back to Supervisor)
```

### Decision Logic
1. **Initial Request** → Route to Researcher (gather data first)
2. **After Research** → Route to Chartist (technical analysis)
3. **After Both Complete** → Route to Analyst (synthesize report)
4. **After Report** → Route to Verifier → FINISH

### Benefits
- **Intelligent Orchestration**: Dynamic routing based on state
- **Efficiency**: Only invokes agents when needed
- **Flexibility**: Easy to modify routing logic
- **State Awareness**: Considers full conversation history

### Code Location
- `src/agents/supervisor.py`
- `src/graph.py`

---

## Pattern 4: PEV - Plan, Execute, Verify (#06)

### Concept
A highly robust, self-correcting loop where a Verifier agent checks the outcome of each action, allowing for error detection and dynamic recovery.

### Implementation in This Project

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  PLAN    │────▶│ EXECUTE  │────▶│  VERIFY  │
│(Superv.) │     │(Analyst) │     │(Verifier)│
└──────────┘     └──────────┘     └────┬─────┘
                       ▲               │
                       │    ┌──────────┴──────────┐
                       │    │                     │
                       │   ❌ FAILED             ✅ PASSED
                       │    │                     │
                       └────┘                     ▼
                    (retry up to               FINISH
                     2 times)
```

### Verification Checks

The Verifier performs these validation checks:

1. **Recommendation Consistency**
   - Does BUY/SELL/HOLD align with technical indicators?
   - RSI > 70 + BUY recommendation = ⚠️ Warning
   - RSI < 30 + SELL recommendation = ⚠️ Warning

2. **RSI Interpretation**
   - Validates that RSI values are correctly interpreted
   - Checks overbought/oversold classifications

3. **Risk Level Accuracy**
   - High volatility + mixed signals = Should be "High Risk"
   - Clear trend + consistent signals = Should be "Lower Risk"

4. **Contradiction Detection**
   - Fundamental vs Technical analysis alignment
   - Recommendation vs supporting evidence

### Self-Correction Flow

```python
def route_after_verification(state):
    if state["verification_passed"]:
        return "FINISH"  # Report approved
    
    if state["iteration_count"] < MAX_RETRIES:
        return "Analyst"  # Retry with feedback
    
    return "FINISH"  # Accept with warnings
```

### Benefits
- **Accuracy**: Catches inconsistencies before final output
- **Self-Correction**: Automatically retries failed analyses
- **Transparency**: Clear verification report with issues found
- **Confidence Scoring**: Provides a confidence score for the analysis

### Code Location
- `src/agents/verifier.py`
- `src/graph.py` (routing logic)

---

## Workflow Diagram

```
                         START
                           │
                           ▼
                    ┌──────────────┐
                    │  Supervisor  │◄──────────────────┐
                    │(Meta-Control)│                   │
                    └──────┬───────┘                   │
                           │                           │
         ┌─────────────────┼─────────────────┐         │
         ▼                 ▼                 ▼         │
   ┌───────────┐    ┌───────────┐    ┌───────────┐    │
   │ Researcher│    │  Chartist │    │  Analyst  │    │
   │(Tool Use) │    │(Tool Use) │    │(Synthesis)│    │
   └─────┬─────┘    └─────┬─────┘    └─────┬─────┘    │
         │                │                │          │
         └────────────────┴───────┐        │          │
                                  │        ▼          │
                                  │  ┌───────────┐    │
                                  │  │ Verifier  │    │
                                  │  │(PEV Check)│    │
                                  │  └─────┬─────┘    │
                                  │        │          │
                                  │        ├──PASS────┼───▶ END
                                  │        │          │
                                  │        └──FAIL────┘
                                  │       (retry Analyst)
                                  │
                                  └────────────────────────▶ (back to Supervisor)
```

---

## Future Pattern Enhancements

Based on the system's use case, these additional patterns could be beneficial:

| Pattern | Benefit | Priority |
|---------|---------|----------|
| **Reflection (#01)** | Self-critique for report quality | Medium |
| **Ensemble (#13)** | Multiple analyst perspectives (conservative, aggressive) | High |
| **Mental Loop (#10)** | Portfolio simulation before recommendations | High |
| **Reflexive Metacognitive (#17)** | Know when data is insufficient | Medium |

---

## Usage Example

```python
from src.graph import create_graph
from src.state import AgentState
from langchain_core.messages import HumanMessage

# Create the graph with all patterns
graph = create_graph()

# Initialize state
state = AgentState(
    messages=[HumanMessage(content="Analyze stock AAPL")],
    next="Supervisor",
    current_ticker="AAPL",
    current_stock_data={},
    iteration_count=0,
    verification_passed=False,
    verification_result={}
)

# Run the workflow
for event in graph.stream(state, config={"recursion_limit": 25}):
    for node, output in event.items():
        print(f"✓ {node}")
```

---

## References

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [AI Agent Patterns Research](https://www.anthropic.com/research)
- [Multi-Agent Systems in Finance](https://arxiv.org/abs/2301.01234)
