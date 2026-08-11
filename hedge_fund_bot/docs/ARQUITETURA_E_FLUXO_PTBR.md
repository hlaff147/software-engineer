# 🏛️ Documentação de Arquitetura e Fluxo de Execução (PT-BR)
## Autonomous Hedge Fund Bot - Enterprise Agentic Architecture

Este documento descreve a arquitetura, design de software, fluxo de execução e boas práticas aplicadas no projeto **`hedge_fund_bot`**, elevado ao padrão **Senior/Enterprise AI Engineering**.

---

## 📑 Sumário
1. [Visão Geral do Sistema](#1-visão-geral-do-sistema)
2. [Os 5 Pilares da Arquitetura Refatorada](#2-os-5-pilares-da-arquitetura-refatorada)
3. [Máquina de Estados & Padrão PEV (Plan, Execute, Verify)](#3-máquina-de-estados--padrão-pev-plan-execute-verify)
4. [Detalhamento das Ferramentas (Tools) & Resiliência](#4-detalhamento-das-ferramentas-tools--resiliência)
5. [Guia de Observabilidade, Telemetria & Custos](#5-guia-de-observabilidade-telemetria--custos)
6. [Guia de Testes Automatizados (Pytest)](#6-guia-de-testes-automatizados-pytest)
7. [Como Executar a Aplicação](#7-como-executar-a-aplicação)

---

## 1. Visão Geral do Sistema

O **Autonomous Hedge Fund Bot** é um sistema multi-agente de análise de ativos financeiros que combina **análise fundamentalista** (notícias e sentimento de mercado) com **análise técnica quantitativa** (indicadores como RSI, MACD, SMA 20, níveis de suporte e resistência) para emitir relatórios institucionais de investimento (`BUY`, `SELL` ou `HOLD`) acompanhados de pontuação de confiança e auditoria de risco.

```
                      +-------------------+
                      |   Usuário (CLI)   |
                      +---------+---------+
                                | Ticker (ex: AAPL, PETR4.SA)
                                v
                      +-------------------+
                      |   LangGraph State |
                      |     Machine       |
                      +---------+---------+
                                |
      +-------------------------+-------------------------+
      |                         |                         |
      v                         v                         v
+-----------+             +-----------+             +-----------+
| Researcher|             | Chartist  |             |  Analyst  |
|  Agent    |             |  Agent    |             |   Agent   |
+-----+-----+             +-----+-----+             +-----+-----+
      |                         |                         |
      +-------------------------+-------------------------+
                                |
                                v
                      +-------------------+
                      |  Verifier Agent   |
                      |  (PEV Audit Node) |
                      +---------+---------+
                                | Validado / Max Retries
                                v
                      +-------------------+
                      | Relatório Final + |
                      |    Telemetria     |
                      +-------------------+
```

---

## 2. Os 5 Pilares da Arquitetura Refatorada

### Pilar 1: Orquestração Explícita via LangGraph
- **Abordagem Sênior**: Em vez de loops imperativos `while True` com prompts gigantescos pedindo roteamento textual, o sistema usa uma **StateGraph** compilada do LangGraph (`src/graph.py`).
- **Garantia de Ciclo**: Roteamento por condições explícitas (`route_after_verification`), com limite de tentativas de correção para evitar loops infinitos.

### Pilar 2: Tipagem Rígida e Structured Output Nativo (Pydantic v2)
- **Abordagem Sênior**: Eliminação completa de parsing manual de textos por regex ou `json.loads` customizados.
- **Saídas Estruturadas Nativas**: Todos os nós utilizam `llm.with_structured_output(PydanticModel)` nativo da API do provedor (Groq/OpenAI).
- **Schemas Definidos**:
  - `ResearchSummary`: Resumo de notícias, sentimento (`BULLISH`/`BEARISH`/`NEUTRAL`), catalisadores e red flags.
  - `TechnicalAnalysisResult`: Indicadores puramente numéricos (`rsi`, `macd_histogram`, `sma_20`, `current_price`) e perspectiva técnica.
  - `InvestmentReport`: Recomendação final, nível de risco, justificativa e score de confiança (0-100).
  - `VerifierResult`: Parecer de compliance, checklist de regras e lista de inconsistências.

### Pilar 3: Resiliência e Tolerância a Falhas em Ferramentas (Tools)
- **Abordagem Sênior**: As ferramentas em `src/tools/` utilizam o decorador `@retry` da biblioteca `tenacity` com **backoff exponencial com jitter**.
- **Comportamento Gracioso**: Em caso de falha de rede temporária no `yfinance` ou `duckduckgo_search`, o sistema tenta novamente (até 3 tentativas com pausa progressiva de 2s a 10s) antes de retornar exceções formatadas.

### Pilar 4: Gestão de Memória e Estado Tipado
- **Abordagem Sênior**: O estado da aplicação (`AgentState` em `src/state.py`) armazena instâncias de modelos Pydantic nos campos `research_data`, `technical_data`, `final_report` e `verification_result`.
- **Benefício**: Os agentes não precisam re-ler históricos de mensagens extensos para descobrir o RSI ou a notícia anterior; eles leem o atributo fortemente tipado no estado Python.

### Pilar 5: Telemetria, Observabilidade e Evals
- **Abordagem Sênior**: Cada execução de nó é cronometrada e monitorada por um gerenciador de contexto `TelemetryTimer` em `src/telemetry.py`.
- **Métricas Capturadas**:
  - Latência em segundos por nó.
  - Contagem de tokens (Prompt Tokens, Completion Tokens, Total Tokens).
  - Custo estimado em USD baseado no modelo LLM utilizado.
  - Suíte de testes automatizada em `tests/` com `pytest`.

---

## 3. Máquina de Estados & Padrão PEV (Plan, Execute, Verify)

O fluxo de execução implementa o padrão **PEV**:

1. **Supervisor Node (`src/agents/supervisor.py`)**:
   - Avalia o estado atual do ativo.
   - Direciona a execução para o `Researcher` (se faltarem dados fundamentalistas) ou `Chartist` (se faltarem indicadores).
   - Quando ambos estiverem presentes, direciona para o `Analyst`.

2. **Researcher Node (`src/agents/researcher.py`)**:
   - Executa buscas na web com `tenacity` retry.
   - Emite um objeto `ResearchSummary` validado por Pydantic v2.

3. **Chartist Node (`src/agents/chartist.py`)**:
   - Coleta dados de cotações históricas do `yfinance` com `tenacity` retry.
   - Executa os cálculos matemáticos dos indicadores (RSI 14, MACD, SMA 20).
   - Emite um objeto `TechnicalAnalysisResult`.

4. **Analyst Node (`src/agents/analyst.py`)**:
   - **Execute Phase**: Lê diretamente os objetos Pydantic `research_data` e `technical_data` presentes no estado.
   - Emite a proposta de relatório em `InvestmentReport`.

5. **Verifier Node (`src/agents/verifier.py`)**:
   - **Verify Phase**: Executa duas camadas de verificação:
     - **Regras Determinísticas (Pure Python)**: Valida inconsistências numéricas (ex: RSI > 72 com recomendação `BUY`, ou MACD fortemente negativo com `BUY`, ou múltiplos red flags com risco `LOW`).
     - **Auditoria LLM Nativa**: Submete o relatório e o contexto ao modelo auditante para obter um `VerifierResult`.
   - Se `is_valid == True` e `verdict == 'APPROVED'`, o fluxo finaliza (`END`).
   - Se houver problemas e o limite de tentativas (`MAX_VERIFICATION_RETRIES`) não tiver sido atingido, o fluxo retorna ao `Analyst` acompanhado das recomendações de revisão.

---

## 4. Detalhamento das Ferramentas (Tools) & Resiliência

### Ferramentas Financeiras (`src/tools/financial_tools.py`)
- `fetch_stock_dataframe_with_retry(ticker, period)`: Busca histórico de preços com retry exponencial. Possui fallback automático para sufixos internacionais (ex: `.SA` para ações brasileiras).
- `calculate_sma(df, window)`: Cálculo de Média Móvel Simples em Pandas.
- `calculate_rsi(df, period)`: Cálculo do Índice de Força Relativa com proteção contra divisão por zero.
- `calculate_macd(df, fast, slow, signal)`: Cálculo da linha MACD, Sinal e Histograma.
- `compute_technical_indicators(df)`: Empacota todos os cálculos matemáticos diretamente no modelo Pydantic `TechnicalIndicators`.

### Ferramentas de Busca (`src/tools/search_tools.py`)
- `search_financial_news_with_retry(query, max_results)`: Realiza buscas no DuckDuckGo com retry exponencial e retorna lista de objetos `NewsArticle`.
- `search_market_sentiment(ticker, max_results)`: Busca notícias focadas em sentimento e perspectivas para o ativo.

---

## 5. Guia de Observabilidade, Telemetria & Custos

Toda execução de análise produz um relatório consolidado de telemetria no terminal:

```text
======================================================================
⚡ SYSTEM TELEMETRY & OBSERVABILITY SUMMARY
======================================================================
⏱️ Total Execution Latency: 4.85s
🔤 Total Tokens Consumed:  2,150 (Prompt: 1,450, Completion: 700)
💵 Estimated Cost:         $0.001408 USD

Breakdown by Node:
  • [Supervisor] 0.32s |   130 tokens | $0.000085
  • [Researcher] 1.45s |   700 tokens | $0.000458
  • [Chartist  ] 1.10s |   600 tokens | $0.000393
  • [Analyst   ] 1.28s |   500 tokens | $0.000327
  • [Verifier  ] 0.70s |   220 tokens | $0.000145
======================================================================
```

---

## 6. Guia de Testes Automatizados (Pytest)

A suíte de testes em `tests/` garante a corretude matemática, a validação de entradas e a integridade do motor de regras do Verifier:

### Estrutura dos Testes:
1. `tests/test_tools.py`: Testes unitários para cálculos de SMA, RSI (garantindo limites entre 0 e 100) e MACD.
2. `tests/test_validation.py`: Testes para validação de tickers americanos e internacionais (`AAPL`, `PETR4.SA`) e rejeição de formatos inválidos.
3. `tests/test_verifier.py`: Testes determinísticos para a máquina de regras do Verifier (detecção de inconsistências entre RSI/MACD/Red Flags e recomendações).

### Como Executar os Testes:
```bash
# Executar todos os testes com saída detalhada
pytest tests/ -v
```

---

## 7. Como Executar a Aplicação

### Pré-requisitos:
1. Python 3.11+ instalado.
2. Chave de API da Groq configurada no arquivo `.env`:
```env
GROQ_API_KEY=gsk_sua_chave_aqui
MODEL_NAME=llama-3.3-70b-versatile
```

### Instalação de Dependências:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Execução via CLI:
```bash
python main.py
```
Ao iniciar, digite o ticker da ação desejada (ex: `AAPL`, `MSFT`, `NVDA`, `PETR4.SA`) para acompanhar a execução autônoma dos agentes.
