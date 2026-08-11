# Autonomous Hedge Fund - Enterprise AI Agent Architecture

Multi-agent stock analysis system built with **LangGraph StateGraph**, **Pydantic v2 Native Structured Outputs**, **Tenacity Resilient Tools**, **PEV (Plan, Execute, Verify) Pattern**, and **System Telemetry Observability**.

> 🇧🇷 **Documentação completa em Português**: Veja [docs/ARQUITETURA_E_FLUXO_PTBR.md](docs/ARQUITETURA_E_FLUXO_PTBR.md)

---

## 🏛️ Senior AI Engineering Pillars Applied

| Pilar | Abordagem Enterprise Sênior |
|---|---|
| **Orquestração** | `LangGraph` StateGraph explícito com validação de ciclo e guards de iteração |
| **Tipagem Rígida** | Native Structured Outputs via `llm.with_structured_output(PydanticModel)` (zero regex) |
| **Resiliência** | Decoradores `@retry` do `tenacity` com backoff exponencial em todas as chamadas de rede/API |
| **Estado Tipado** | `AgentState` carregando modelos Pydantic (`research_data`, `technical_data`, `final_report`, `verifier_result`) |
| **Observabilidade** | Rastreador de latência, contagem detalhada de tokens (Prompt/Completion) e custos em USD por nó |
| **Testabilidade** | Suíte de testes unitários com `pytest` testando matemática financeira, validações e motor do Verifier |

---

## ⚡ Fluxo de Execução (PEV Pattern)

```
User (CLI) → Supervisor → Researcher → Chartist → Analyst → Verifier → Report + Telemetry
                 ↑___________|____________|          │         │
                 │                                   │    ❌ REVISION (retry)
                 └───────────────────────────────────┴─────────┘
```

| Agente | Função | Saída Estruturada (Pydantic v2) | Resiliência |
|-------|------|---------------------------------|-------------|
| **Supervisor** | Roteador determinístico e inteligente | `SupervisorDecision` | Native Function Calling |
| **Researcher** | Coleta fundamentalista e notícias | `ResearchSummary` | Tenacity Retry Backoff |
| **Chartist** | Indicadores quantitativos (RSI, MACD, SMA) | `TechnicalAnalysisResult` | Tenacity Retry + Pure Math |
| **Analyst** | Síntese de relatório de investimento | `InvestmentReport` | Native Structured Output |
| **Verifier** | Auditoria determinística + Auditoria LLM | `VerifierResult` | Rules Engine + Native Audit |

---

## 🚀 Instalação e Execução

### 1. Criar ambiente virtual e instalar dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente (`.env`)
```env
GROQ_API_KEY=gsk_sua_chave_aqui
MODEL_NAME=llama-3.3-70b-versatile
```

### 3. Executar o sistema CLI
```bash
python main.py
```

### 4. Executar os testes automatizados
```bash
pytest tests/ -v
```

---

## 📊 Estrutura do Projeto Refatorado

```
hedge_fund_bot/
├── main.py                    # CLI principal com relatórios e telemetria
├── requirements.txt           # Dependências congeladas (pydantic, langgraph, tenacity, pytest)
├── src/
│   ├── config.py              # Configurações Pydantic Settings
│   ├── state.py               # AgentState com objetos de domínio tipados
│   ├── schemas.py             # Schemas Pydantic v2 (ResearchSummary, TechnicalAnalysisResult, etc)
│   ├── telemetry.py           # Rastreador de latência, tokens e custos
│   ├── exceptions.py          # Hierarquia de exceções da aplicação
│   ├── llm.py                 # LLM Factory com suporte a Native Structured Outputs
│   ├── validation.py          # Validação de tickers e entradas
│   ├── tools/
│   │   ├── financial_tools.py # Resilient yfinance + indicadores (RSI, MACD, SMA)
│   │   └── search_tools.py    # Resilient DuckDuckGo search news
│   ├── agents/
│   │   ├── supervisor.py      # Meta-Controller Node
│   │   ├── researcher.py      # Fundamental Analysis Node
│   │   ├── chartist.py        # Technical Analysis Node
│   │   ├── analyst.py         # Report Synthesis Node
│   │   └── verifier.py        # PEV Auditor Node
│   └── graph.py               # LangGraph Workflow & PEV State Machine
├── tests/                     # Suíte de testes automatizados com pytest
│   ├── test_tools.py          # Testes unitários para matemática financeira
│   ├── test_validation.py     # Testes de validação de tickers
│   └── test_verifier.py       # Testes da máquina de regras do Verifier
└── docs/
    └── ARQUITETURA_E_FLUXO_PTBR.md # Documentação técnica detalhada em Português
```

---

## 📜 Licença

MIT
