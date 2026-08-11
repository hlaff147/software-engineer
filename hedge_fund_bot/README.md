# Autonomous Hedge Fund - Enterprise AI Agent Architecture

<p align="center">
  <a href="#-english-version"><b>🇺🇸 English Version</b></a> &nbsp;•&nbsp;
  <a href="#-vers%C3%A3o-em-portugu%C3%AAs-pt-br"><b>🇧🇷 Versão em Português</b></a>
</p>

---

<details open>
<summary><h2>🇺🇸 English Version (Click to collapse/expand)</h2></summary>

Multi-agent stock analysis system built with **LangGraph StateGraph**, **Pydantic v2 Native Structured Outputs**, **Tenacity Resilient Tools**, **Abstract Interfaces (`SearchProvider`, `MarketDataProvider`)**, **PEV (Plan, Execute, Verify) Pattern**, **Executive HTML Reporting**, and **System Telemetry Observability**.

---

### 🏛️ Senior AI Engineering Pillars Applied

| Pillar | Senior Enterprise Approach |
|---|---|
| **Orchestration** | Explicit `LangGraph` StateGraph with cycle validation and iteration guards |
| **Strict Typing** | Native Structured Outputs via `llm.with_structured_output(PydanticModel)` (zero regex) |
| **Interface Abstraction** | Abstract Base Classes (`SearchProvider`, `MarketDataProvider`) for loose coupling & mock testing |
| **Resilience** | `@retry` backoff decorators from `tenacity` on network/API providers with automatic `.SA` fallback |
| **Typed State** | `AgentState` carrying typed domain models (`research_data`, `technical_data`, `final_report`, `verification_result`) |
| **HTML Reporting** | Automatic generation of standalone, executive dark-themed HTML investment reports in `reports/` |
| **Observability** | Per-node execution time tracking, detailed token usage (Prompt/Completion), and estimated USD costs |
| **Testability** | Unit test suite with `pytest` testing financial math, ticker validations, verifier rules, and HTML generation |

---

### ⚡ Execution Flow (PEV Pattern)

```
User (CLI) → Supervisor → Researcher → Chartist → Analyst → Verifier → Report + Telemetry + HTML Output
                 ↑___________|____________|          │         │
                 │                                   │    ❌ REVISION (retry)
                 └───────────────────────────────────┴─────────┘
```

| Agent | Responsibility | Structured Output (Pydantic v2) | Resilience & Abstraction |
|-------|----------------|---------------------------------|---------------------------|
| **Supervisor** | Intelligent deterministic router | `SupervisorDecision` | Native Function Calling |
| **Researcher** | Fundamental & sentiment search | `ResearchSummary` | `SearchProvider` (DuckDuckGo / Mock) |
| **Chartist** | Quantitative technical indicators | `TechnicalAnalysisResult` | `MarketDataProvider` (yfinance / Mock) + Pure Math |
| **Analyst** | Investment report synthesis | `InvestmentReport` | Native Structured Output |
| **Verifier** | Deterministic audit + LLM consistency check | `VerifierResult` | Rules Engine + Native Audit |

---

### 🚀 Setup and Quickstart

#### 1. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Configure Environment Variables (`.env`)
```env
GROQ_API_KEY=gsk_your_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

#### 3. Run System CLI
```bash
python main.py
```

#### 4. Run Automated Tests
```bash
.venv/bin/pytest -v
```

---

### 📊 Project Directory Architecture

```
hedge_fund_bot/
├── main.py                    # Main CLI entry point with HTML report & telemetry output
├── requirements.txt           # Frozen dependencies (pydantic, langgraph, tenacity, pytest)
├── src/
│   ├── config.py              # Pydantic Settings configuration
│   ├── state.py               # Typed AgentState carrying domain models
│   ├── schemas.py             # Pydantic v2 schemas (ResearchSummary, TechnicalAnalysisResult, etc.)
│   ├── telemetry.py           # Per-node latency, token usage, and cost tracking
│   ├── reporting.py           # Standalone HTML report generator module
│   ├── exceptions.py          # Application exception hierarchy
│   ├── llm.py                 # LLM Factory supporting Native Structured Outputs
│   ├── validation.py          # Ticker input validation
│   ├── tools/
│   │   ├── financial_tools.py # MarketDataProvider interface (yfinance / Mock) + Pure Math (RSI, MACD, SMA)
│   │   └── search_tools.py    # SearchProvider interface (DuckDuckGo / Mock)
│   ├── agents/
│   │   ├── supervisor.py      # Meta-Controller Routing Node
│   │   ├── researcher.py      # Fundamental Analysis Node
│   │   ├── chartist.py        # Technical Analysis Node
│   │   ├── analyst.py         # Investment Report Synthesis Node
│   │   └── verifier.py        # PEV Auditor Node
│   └── graph.py               # LangGraph Workflow & PEV State Machine
├── tests/                     # Unit test suite with pytest
│   ├── test_tools.py          # Unit tests for Search/Market interfaces & quantitative math
│   ├── test_reporting.py      # Unit tests for HTML report generator
│   ├── test_validation.py     # Ticker validation unit tests
│   └── test_verifier.py       # Verifier rules engine tests
└── docs/
    └── ARQUITETURA_E_FLUXO_PTBR.md # Detailed technical documentation in Portuguese
```

</details>

---

<details>
<summary><h2>🇧🇷 Versão em Português (Clique para expandir/recolher)</h2></summary>

Sistema de análise de ações baseado em múltiplos agentes inteligentes, construído com **LangGraph StateGraph**, **Saídas Estruturadas Nativas Pydantic v2**, **Ferramentas Resilientes Tenacity**, **Interfaces Abstratas (`SearchProvider`, `MarketDataProvider`)**, **Padrão PEV (Plano, Execução, Verificação)**, **Gerador de Relatórios Executivos em HTML** e **Telemetria/Observabilidade**.

---

### 🏛️ Pilares de Engenharia de IA Sênior Aplicados

| Pilar | Abordagem Enterprise Sênior |
|---|---|
| **Orquestração** | `LangGraph` StateGraph explícito com validação de ciclo e guards de iteração |
| **Tipagem Rígida** | Saídas Estruturadas Nativas via `llm.with_structured_output(PydanticModel)` (zero regex) |
| **Abstração por Interfaces** | Classes Abstratas (`SearchProvider`, `MarketDataProvider`) para desacoplamento e testes mock |
| **Resiliência** | Decoradores `@retry` do `tenacity` com backoff exponencial e fallback automático `.SA` para B3 |
| **Estado Tipado** | `AgentState` carregando modelos Pydantic (`research_data`, `technical_data`, `final_report`, `verifier_result`) |
| **Relatórios HTML** | Geração automática de relatórios executivos em HTML autocontido com tema dark em `reports/` |
| **Observabilidade** | Rastreador de latência por nó, contagem detalhada de tokens (Prompt/Completion) e custos em USD |
| **Testabilidade** | Suíte de testes unitários com `pytest` testando matemática financeira, validação, verifier e HTML |

---

### ⚡ Fluxo de Execução (Padrão PEV)

```
Usuário (CLI) → Supervisor → Researcher → Chartist → Analyst → Verifier → Relatório + Telemetria + HTML
                    ↑___________|____________|          │         │
                    │                                   │    ❌ REVISÃO (retry)
                    └───────────────────────────────────┴─────────┘
```

| Agente | Responsabilidade | Saída Estruturada (Pydantic v2) | Resiliência & Abstração |
|-------|------------------|---------------------------------|-------------------------|
| **Supervisor** | Roteador determinístico inteligente | `SupervisorDecision` | Native Function Calling |
| **Researcher** | Notícias e sentimento de mercado | `ResearchSummary` | Interface `SearchProvider` (DuckDuckGo / Mock) |
| **Chartist** | Indicadores quantitativos (RSI, MACD, SMA) | `TechnicalAnalysisResult` | Interface `MarketDataProvider` (yfinance / Mock) + Matemática Pura |
| **Analyst** | Síntese do relatório de investimento | `InvestmentReport` | Native Structured Output |
| **Verifier** | Auditoria determinística + Auditoria LLM | `VerifierResult` | Motor de Regras + Auditoria Nativa |

---

### 🚀 Instalação e Execução Rápida

#### 1. Criar ambiente virtual e instalar dependências
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Configurar variáveis de ambiente (`.env`)
```env
GROQ_API_KEY=gsk_sua_chave_aqui
MODEL_NAME=llama-3.3-70b-versatile
```

#### 3. Executar o sistema CLI
```bash
python main.py
```

#### 4. Executar os testes automatizados
```bash
.venv/bin/pytest -v
```

---

### 📊 Estrutura de Arquivos do Projeto

```
hedge_fund_bot/
├── main.py                    # CLI principal com geração de relatórios HTML e telemetria
├── requirements.txt           # Dependências congeladas (pydantic, langgraph, tenacity, pytest)
├── src/
│   ├── config.py              # Configurações Pydantic Settings
│   ├── state.py               # AgentState com objetos de domínio tipados
│   ├── schemas.py             # Schemas Pydantic v2 (ResearchSummary, TechnicalAnalysisResult, etc.)
│   ├── telemetry.py           # Rastreador de latência, tokens e custos em USD
│   ├── reporting.py           # Gerador de relatórios executivos em HTML autocontido
│   ├── exceptions.py          # Hierarquia de exceções da aplicação
│   ├── llm.py                 # LLM Factory com suporte a Saídas Estruturadas Nativas
│   ├── validation.py          # Validação de tickers e entradas
│   ├── tools/
│   │   ├── financial_tools.py # Interface MarketDataProvider (yfinance / Mock) + Indicadores (RSI, MACD, SMA)
│   │   └── search_tools.py    # Interface SearchProvider (DuckDuckGo / Mock)
│   ├── agents/
│   │   ├── supervisor.py      # Nó Roteador Meta-Controller
│   │   ├── researcher.py      # Nó de Análise Fundamentalista
│   │   ├── chartist.py        # Nó de Análise Técnica
│   │   ├── analyst.py         # Nó de Síntese de Relatório
│   │   └── verifier.py        # Nó Auditor do Padrão PEV
│   └── graph.py               # LangGraph Workflow & Máquina de Estados PEV
├── tests/                     # Suíte de testes automatizados com pytest
│   ├── test_tools.py          # Testes unitários para interfaces de busca/cotação e matemática financeira
│   ├── test_reporting.py      # Testes unitários para gerador de relatórios HTML
│   ├── test_validation.py     # Testes de validação de tickers
│   └── test_verifier.py       # Testes do motor de regras do Verifier
└── docs/
    └── ARQUITETURA_E_FLUXO_PTBR.md # Documentação técnica detalhada em Português
```

</details>

---

## 📜 License / Licença

MIT
