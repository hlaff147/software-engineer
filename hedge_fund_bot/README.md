# Autonomous Hedge Fund

Multi-agent stock analysis system using LangGraph, LangChain, and Groq with **self-correcting verification**.

## 🧠 AI Agent Patterns

This project implements 4 proven AI agent architecture patterns:

| # | Pattern | Description |
|---|---------|-------------|
| 02 | **Tool Use** | Real-time data via yfinance & search APIs |
| 05 | **Multi-Agent** | Specialized agents collaborate (Researcher, Chartist, Analyst) |
| 06 | **PEV** | Plan, Execute, Verify with auto-retry on failed validation |
| 11 | **Meta-Controller** | Supervisor routes to appropriate specialists |

> 📖 See [docs/PATTERNS.md](docs/PATTERNS.md) for detailed documentation.

## Architecture

```
User → Supervisor → Researcher → Chartist → Analyst → Verifier → Report
            ↑___________|____________|          │         │
            │                                   │    ❌ FAIL (retry)
            └───────────────────────────────────┴─────────┘
```

| Agent | Role | Tools | Pattern |
|-------|------|-------|---------|
| **Supervisor** | Routes workflow | JSON routing | Meta-Controller |
| **Researcher** | News & sentiment | DuckDuckGo | Tool Use |
| **Chartist** | Technical analysis | yfinance (RSI, MACD, SMA) | Tool Use |
| **Analyst** | Final report | LLM synthesis | Multi-Agent |
| **Verifier** | Validates recommendations | Rule-based + LLM | PEV Pattern |

### PEV (Plan, Execute, Verify) Pattern

The **Verifier** agent ensures quality by:
- ✅ Checking recommendation consistency with technical data
- ✅ Validating RSI interpretation (overbought/oversold)
- ✅ Ensuring risk level aligns with analysis
- ✅ Detecting contradictions between fundamental & technical analysis
- 🔄 Auto-retrying Analyst up to 2 times if verification fails

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Add GROQ_API_KEY to .env
```

## Usage

```bash
# CLI
python main.py

# Notebook
jupyter notebook notebooks/hedge_fund_analysis.ipynb
```

## Structure

```
hedge_fund_bot/
├── src/
│   ├── agents/
│   │   ├── supervisor.py   # Meta-Controller pattern
│   │   ├── researcher.py   # Tool Use pattern
│   │   ├── chartist.py     # Tool Use pattern
│   │   ├── analyst.py      # Multi-Agent pattern
│   │   └── verifier.py     # PEV pattern (NEW)
│   ├── tools/
│   │   ├── financial_tools.py
│   │   └── search_tools.py
│   ├── state.py            # AgentState schema
│   └── graph.py            # LangGraph workflow
├── docs/
│   └── PATTERNS.md         # Architecture patterns documentation
├── notebooks/
├── main.py
└── requirements.txt
```

## Example Output

```
🚀 Analyzing AAPL...
  ✓ Supervisor
  ✓ Researcher
  ✓ Supervisor
  ✓ Chartist
  ✓ Supervisor
  ✓ Analyst
  ✓ Verifier      ← PEV validation
✅ Done
```

## License

MIT
