# 🤖 Experiências para CV — AI Engineer

> Texto gerado com base na análise completa da codebase `software-engineer`, focando em experiências com **Python, AI, Agentes, LLMs e tecnologias relacionadas**.

---

## 🧠 Resumo de Competências AI/ML

| Área | Tecnologias & Frameworks |
|------|--------------------------|
| **Agentes de IA** | LangGraph, LangChain, multi-agent systems, PEV pattern |
| **LLMs** | Groq API, Llama 3.3 70B, prompt engineering, structured outputs |
| **Python Backend** | FastAPI, Click CLI, asyncio, Pydantic |
| **Data & Analytics** | yfinance, pandas, Jupyter Notebooks, PyMongo |
| **Testes** | pytest, testes unitários e de integração |
| **Infra** | Docker, Docker Compose |

---

## 📌 Experiências Detalhadas

### 1. Autonomous Hedge Fund Bot — Sistema Multi-Agente com IA

**Projeto:** Sistema autônomo de análise de ações utilizando **5 agentes especializados** orquestrados via **LangGraph** com padrão **PEV (Plan, Execute, Verify)**.

**Responsabilidades e entregas:**
- Arquitetura e implementação de **sistema multi-agente completo** com orquestração via grafo de estados (LangGraph `StateGraph`)
- Desenvolvimento de **5 agentes especializados:**
  - **Supervisor (Meta-Controller)** — roteamento inteligente de tarefas entre agentes
  - **Researcher** — coleta de notícias e análise de sentimento via DuckDuckGo Search
  - **Chartist** — análise técnica com cálculos reais (RSI, MACD, SMA) usando yfinance e pandas
  - **Analyst** — geração de relatório de investimento estruturado via LLM
  - **Verifier** — validação de outputs com detecção de contradições e self-correction loop
- Implementação de **Tool Use pattern** — integração com APIs externas (yfinance para dados financeiros, DuckDuckGo para pesquisa) para evitar alucinação do LLM em cálculos
- Construção de **pipeline de verificação (PEV Pattern)** com retry automático quando o Verifier detecta inconsistências (máximo de N tentativas configurável)
- **Structured outputs** via Pydantic para garantir respostas do LLM em formato JSON válido
- Configuração externalizada via `pydantic-settings`, suportando variáveis de ambiente e `.env`
- Tratamento robusto de erros com exceções customizadas e logging estruturado

**Tecnologias:** `Python 3.11+` · `LangGraph` · `LangChain` · `Groq API` · `Llama 3.3 70B` · `yfinance` · `pandas` · `DuckDuckGo Search` · `Pydantic` · `Docker`

**Padrões AI aplicados:** Multi-Agent, Tool Use, PEV (Plan-Execute-Verify), Meta-Controller, Reflection, Structured Outputs

---

### 2. Vulnerability Analyzer Agent — CLI Inteligente de Segurança

**Projeto:** Agente CLI em Python para **análise automatizada de vulnerabilidades** em projetos Java/Spring com capacidade de **auto-fix**.

**Responsabilidades e entregas:**
- Desenvolvimento de CLI completa usando **Click** com comandos `scan` e `fix`
- Integração com **3 fontes de dados de segurança:**
  - **OWASP Dependency-Check** — análise offline de dependências
  - **NVD (National Vulnerability Database)** — consultas diretas via API
  - **Mend.io** — integração opcional para vulnerabilidades proprietárias
- Implementação de sistema de **parsers** modulares para diferentes formatos de relatório
- Engine de **auto-fix** com modo dry-run para preview seguro de correções
- Geração de relatórios em **múltiplos formatos:** Console (colorido), HTML, JSON
- Arquitetura modular: `analyzers/`, `parsers/`, `fixers/`, `reporters/`
- Configuração via **YAML** com suporte a profiles
- Testes automatizados com projetos de teste dedicados

**Tecnologias:** `Python 3.11+` · `Click CLI` · `OWASP` · `NVD API` · `Mend.io` · `YAML` · `HTML templating`

---

### 3. Kafka Consumer Groups — Prova de Conceito com Python Async

**Projeto:** API e sistema de demonstração provando o comportamento de **consumer groups independentes no Kafka** usando Python assíncrono.

**Responsabilidades e entregas:**
- Desenvolvimento de API REST com **FastAPI** e consumidores Kafka assíncronos com **aiokafka**
- Implementação de múltiplos consumers com group IDs independentes demonstrando offset tracking isolado
- Testes automatizados com **pytest**
- Infraestrutura completa com **Docker Compose** (Kafka + Zookeeper)
- Jupyter Notebook com análise e visualização dos resultados

**Tecnologias:** `Python 3.11+` · `FastAPI` · `aiokafka` · `Apache Kafka` · `Docker Compose` · `pytest` · `Jupyter`

---

### 4. MongoDB ObjectId Timestamp Proof — Análise de Dados com Python

**Projeto:** API e notebooks demonstrando a extração de **timestamps embutidos em ObjectIds do MongoDB** para ordenação cronológica.

**Responsabilidades e entregas:**
- Desenvolvimento de API REST com **FastAPI** para operações CRUD e análise de ObjectIds
- Implementação de endpoints para comparação de timestamps entre primeiro e último documento
- Análise exploratória com **Jupyter Notebooks**
- Integração com MongoDB via **PyMongo**

**Tecnologias:** `Python 3.11+` · `FastAPI` · `MongoDB` · `PyMongo` · `Jupyter Notebooks`

---

### 5. AI Engineer Study Guide — Documentação Técnica de 17 Padrões de Agentes

**Projeto:** Guia de estudo abrangente cobrindo **17 padrões de arquitetura de agentes de IA**, com diagramas, código de exemplo e insights de implementação.

**Conteúdo produzido:**
- Documentação detalhada de **17 padrões:** Reflection, Tool Use, ReAct, Planning, Multi-Agent, PEV, Blackboard, Dual Memory, Tree of Thoughts, Mental Loop, Meta-Controller, Graph Memory, Ensemble, Dry-Run, RLHF Loop, Cellular Automata, Metacognitive
- **Design Principles** para sistemas agênticos: State-First Design, Separation of Concerns, Fail Gracefully, Limit Iterations, Structured Outputs
- **Insights de implementação** reais: LLMs são ruins em aritmética (use tools), prompt engineering, message history management, temperature tuning, verificação contra alucinações
- **Guia de seleção de padrões** — decision tree para escolher o padrão correto por caso de uso
- Referências ao stack recomendado: LangGraph, Groq, Pinecone, FAISS, LangSmith

---

## 🎯 Texto Sugerido para Seção de Experiência no CV

> **AI & Python Engineer** com experiência prática no design e implementação de **sistemas multi-agente autônomos** utilizando LangGraph/LangChain, com foco em arquiteturas robustas e auto-corretivas (PEV pattern). Expertise em orquestração de agentes especializados, integração de LLMs (Groq/Llama 3.3) com ferramentas externas (Tool Use), e construção de pipelines de verificação para mitigar alucinações. Proficiente em Python (FastAPI, Click, pandas, asyncio), com experiência em análise de segurança automatizada (OWASP, NVD), event streaming (Kafka + aiokafka), e análise de dados com Jupyter/MongoDB. Conhecimento sólido de 17 padrões de arquitetura de agentes de IA, desde Reflection e ReAct até Meta-Controller e Ensemble, com aplicação prática em projetos reais.

---

## 💡 Keywords para ATS (Applicant Tracking System)

`AI Engineer` · `Python` · `LangGraph` · `LangChain` · `Multi-Agent Systems` · `LLM` · `Groq` · `Llama` · `Prompt Engineering` · `FastAPI` · `Agentic AI` · `Tool Use` · `RAG` · `Pydantic` · `pandas` · `yfinance` · `Docker` · `Kafka` · `MongoDB` · `OWASP` · `NVD` · `Vulnerability Analysis` · `pytest` · `asyncio` · `Jupyter` · `Click CLI`
