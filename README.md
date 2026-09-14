<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Java-17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java">
  <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=for-the-badge&logo=kotlin&logoColor=white" alt="Kotlin">
  <img src="https://img.shields.io/badge/Spring%20Boot-3.x-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangGraph">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

# 🛠️ Software & AI Engineer Portfolio

> A curated collection of hands-on projects exploring software engineering, AI/ML, system design, and modern technologies. Each project demonstrates production-ready patterns and real-world best practices.

---

## 🎯 Repository Highlights

| Category | Projects | Key Technologies |
|----------|----------|------------------|
| **🤖 AI/ML & Agents** | 3 projects | LangGraph, LangChain, Groq, Llama 3.3, Pydantic v2, Hypothesis |
| **🔌 Backend APIs** | 6 projects | Micronaut Data JPA, Spring Boot, Kotlin, Hexagonal Architecture, Strategy Pattern, Incognia SDK |
| **🏦 Open Finance** | 3 microservices | Spring Boot, Feign Client, MongoDB, Microservices |
| **📨 Event Streaming** | 2 projects | Kafka, Azure Service Bus |
| **🗄️ Database** | 1 project | MongoDB ObjectId internals |
| **🧪 Testing & Quality** | 1 project | Mutation Testing, AST, mutmut, Hypothesis |
| **📐 Observability** | 1 library | Spring Boot Starter, AOP, Logback, Kafka, MongoDB |
| **📚 Study Guides & Architecture** | 10 modules | AI Patterns, Token Optimization & Routing, Change Data Capture (CDC), AI Coding Skills (Multi-IDE), Java Core, Collectors/Gatherers, System Design, Floating Point, Java 21/25, SDE-2 Prep |

---

## 📚 Study Guides & Documentation

| Guide | Description | Topics |
|-------|-------------|--------|
| [⚡ Agentic Token Optimization](./agentic-token-optimization) | Model Routing, Pre-Tool Hooks & delegação de I/O (redução de 90% em tokens) | Model Routing, Token Optimization, PreToolUse Hooks, Bulk Reader, Code Writer |
| [🧠 AI Coding Skills](./ai-coding-skills) | 13 production-ready AI coding skills for Cursor, Copilot, Windsurf, Cline, Claude Code & Gemini | Multi-IDE Portability, Cursor Rules, Deploy Guardrail, Empty Deploy Trigger, Micronaut, Spring Boot |
| [🤖 AI Engineer Hub](./ai-engineer) | Comprehensive AI agent patterns, MCP/RAG/Agents guide & CV portfolio | 17 patterns, MCP protocol, RAG pipelines, Autonomous Agents |
| [🔄 Change Data Capture (CDC)](./change-data-capture) | Guia aprofundado de CDC, transaction logs (WAL/binlog), outbox pattern & pipeline serverless na AWS | CDC Fundamentals, Transaction Logs, Dual-Write, DynamoDB Streams, EventBridge, SQS, Lambda |
| [☕ Java Developer Guide](./java-developer) | Backend interview preparation & JVM internals | Java Core, Spring Boot, Microservices, Under the Hood |
| [🧩 Java Collectors & Gatherers](./java-collectors-gatherers) | Custom Collectors, Gatherers (Java 24+) & functional Streams | Collector API, Gatherer API, groupingBy, collectingAndThen, sealed interfaces |
| [💼 Interview Study & System Design](./study_interview_system_design) | Quick reference & comprehensive SDE-2 interview prep | Idempotência vs Deduplicação, Mastercard SDE-2, SOLID, CAP/ACID, LeetCode |
| [🏛️ System Design Diagrams](./system-design) | Visual system design references | Payment systems, Saga patterns, CAP theorem |
| [🧮 Floating Point Precision (IEEE 754)](./floating-point-precision) | Floating point drift theory and multi-language benchmarks | IEEE 754, Binary Fractions, Turing vs Lambda, Decimal, Fraction |
| [⚡ Java 25 & 21 LTS Features](./java25-lts-features) | Mini-project showcasing ScopedValue, Virtual Threads & Loom | ScopedValue, Virtual Threads, Structured Concurrency (Java vs Kotlin) |

---

## 🤖 AI & Machine Learning Projects

### [Autonomous Hedge Fund Bot](./hedge_fund_bot)

Multi-agent AI system for automated stock analysis with **self-correcting verification**.

<table>
<tr>
<td width="50%">

**🏗️ Architecture**
```
User → Supervisor → Researcher → Chartist
            ↑______________|         |
            |                        ▼
            │               Analyst → Verifier
            │                  │         │
            │                  │    ❌ FAIL
            └──────────────────┴─────────┘
                         (retry loop)
```

</td>
<td width="50%">

**🧠 AI Patterns Used**
| Pattern | Implementation |
|---------|----------------|
| Tool Use | yfinance, DuckDuckGo |
| Multi-Agent | 5 specialized agents |
| PEV | Verifier validates outputs |
| Meta-Controller | Supervisor routes |

</td>
</tr>
</table>

**Tech Stack:** `LangGraph` `LangChain` `Groq` `Llama 3.3 70B` `yfinance` `Python 3.11+`

**Features:**
- 🤖 **Multi-Agent System** — Supervisor, Researcher, Chartist, Analyst, Verifier
- 📊 **Technical Analysis** — RSI, MACD, SMA indicators (calculated, not hallucinated)
- 📰 **Sentiment Analysis** — Real-time news and market sentiment via DuckDuckGo
- ✅ **Self-Correction** — Verifier catches contradictions and triggers retries

---

### [Spec-Driven Development (SDD) in the Agentic Era](./spec-driven-development-agentic)

Explores the transformation of Software Design Documents from static text into **executable specifications and autonomous evaluation harnesses** with AI self-healing feedback loops.

<table>
<tr>
<td width="50%">

**🏗️ Continuous Evaluation Loop**
```
Intent & Invariants (Pydantic / Contracts)
                │
                ▼
┌───────────────────────────────┐
│ Continuous Evaluation Harness │ ◄──┐
└───────────────┬───────────────┘    │
                ▼                    │
    AI Agent Generates Code          │ (Retry loop)
                ▼                    │
      Invariant Checks Pass? ────────┘
          │ (YES)
          ▼
   Production Code Verified
```

</td>
<td width="50%">

**🔬 3 Paradigms Demonstrated**
| Approach | Mechanism |
|----------|-----------|
| **Classic SDD** | Static Markdown specifications |
| **Executable SDD** | Pydantic contracts + Hypothesis Property-Based Testing |
| **Agentic SDD** | Continuous Evaluation Harness + Automated Agent Correction Loop |

**Key Invariants:**
- Financial conservation of money
- Non-negative ledger balance guarantees

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `Pydantic v2` `Hypothesis` `pytest` `Rich CLI`

---

### [Vulnerability Analyzer Agent](./vuln-analyzer-agent)

Intelligent Python CLI agent for **automated vulnerability analysis in Java/Spring projects** with OWASP, NVD API integration, and automated `pom.xml` auto-remediation.

<table>
<tr>
<td width="50%">

**🔍 Data Sources & Integrations**
| Source | Type |
|--------|------|
| OWASP Dependency-Check | Offline vulnerability analysis |
| NVD (National Vulnerability DB) | Real-time CVE queries via API |
| Mend.io (Optional) | Proprietary "WS-" vulnerabilities |

**📊 Output Formats:**
- Rich terminal console output
- Standalone HTML reports
- Structured JSON for CI/CD pipelines

</td>
<td width="50%">

**⚡ Key Agent Capabilities**
```bash
# Scan project dependencies
vuln-analyzer scan /path/to/project

# Scan with live NVD CVE enrichment
vuln-analyzer scan /path --nvd-api-key $KEY

# Preview automated security upgrades
vuln-analyzer fix /path --dry-run

# Apply auto-remediation to pom.xml
vuln-analyzer fix /path --apply
```

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `Click CLI` `OWASP` `NVD API` `Jinja2` `BeautifulSoup4`

---

### [Agentic Token Optimization & Model Routing](./agentic-token-optimization)

Arquitetura de **roteamento de modelos (*Model Routing*)** e interceptação determinística via *Pre-Tool Hooks*, reduzindo em até **90% o consumo de tokens** ao delegar I/O pesado e *boilerplate* para *workers* leves.

<table>
<tr>
<td width="50%">

**🏗️ Arquitetura em 3 Camadas**
```
[ Agente Principal ]
        │
        ▼ (Leitura de arquivo grande)
┌─────────────────────────────────────────┐
│ Camada 1: Pre-Tool Interception Hook    │ (Linhas >= 350 -> Bloqueio)
└───────────────────┬─────────────────────┘
        │ Redirecionamento
        ▼
┌─────────────────────────────────────────┐
│ Camada 3: Agent Skills / Tool Registry  │ (Guia de invocação CLI)
└───────────────────┬─────────────────────┘
        │ Invoca Script
        ▼
┌─────────────────────────────────────────┐
│ Camada 2: Execution Scripts & Workers   │ (Bulk-Reader / Code-Writer)
└─────────────────────────────────────────┘
```

</td>
<td width="50%">

**⚡ Destaques & Técnicas**
| Técnica | Aplicação |
|---------|-----------|
| **Model Routing** | Desacopla raciocínio analítico de I/O pesado |
| **Pre-Tool Hooks** | Bloqueio determinístico por threshold (>350 linhas) |
| **Bulk Reader Mode** | Síntese densa em bullets sem preâmbulos |
| **Code Writer Mode** | Geração direta em disco ("output only code") |
| **Targeted Reads Pass** | Leituras pontuais com offset/limit liberadas |

**Economia Comprovada:**
- ~90% de redução de tokens em operações de leitura em monorepos
- Preservação da janela de contexto para decisões de alta complexidade

</td>
</tr>
</table>

**Tech Stack:** `Python 3.9+` `Standalone Package` `Unified CLI` `Pre-Tool Hooks` `Cursor Skills` `Make` `unittest`

---

## 🔌 API & Backend Projects

### [Micronaut Data JPA Masterclass — Global Fleet & Asset Management](./micronaut-jpa-masterclass)

Comprehensive enterprise backend mastering **all 6 pillars of Jakarta Persistence (JPA 3.2) & Hibernate** on **Java 25** and **Micronaut Data JPA**.

<table>
<tr>
<td width="50%">

**🏗️ Persistence Architecture & Inheritance**
```
              ┌───────────────────────────┐
              │      AuditableEntity      │
              │  (@PrePersist, @PreUpdate)│
              └─────────────┬─────────────┘
                            │ extends
              ┌─────────────▼─────────────┐
              │           Asset           │
              │    (JOINED Table Strategy)│
              │    - version (@Version)   │
              │    - location (@Embedded) │
              └───┬───────────────────┬───┘
                  │                   │
    ┌─────────────▼─────────┐   ┌─────▼─────────────────┐
    │        Vehicle        │   │       IoTSensor       │
    │  - license_plate (UQ) │   │  - mac_address (UQ)   │
    │  - mileage, fuel_type │   │  - firmware, battery  │
    └─────────────┬─────────┘   └───────────────────────┘
                  │
                  ▼ @OneToMany (BatchSize = 25)
    ┌───────────────────────────────────────────────────┐
    │     MaintenanceSchedule  →  MaintenanceLogs       │
    └───────────────────────────────────────────────────┘
```

</td>
<td width="50%">

**⚡ The 6 JPA Pillars Mastered**
| Pillar | Pattern / Feature |
|:---|:---|
| **1. Mappings** | Joined Table, Single Table, `@Embeddable`, `@ElementCollection` |
| **2. Fetching** | First-Level Cache hit, Dirty Checking, N+1 fix via `@BatchSize(25)` |
| **3. Querying** | Constructor DTO Projections (`SELECT new ...`), Criteria API |
| **4. Locking** | Optimistic (`@Version`) + Retry, Pessimistic (`PESSIMISTIC_WRITE`) |
| **5. Auditing** | JPA Callbacks (`@PrePersist`), Async Audit Events (Virtual Threads) |
| **6. Enterprise**| JDBC Batching (`batch_size=30`), L2 Cache (Ehcache), `flush`/`clear` |

**💡 Key JPA Insight:**
```java
// Inside @Transactional:
Vehicle v1 = repo.findById(id).orElseThrow(); // SQL SELECT hits DB
Vehicle v2 = repo.findById(id).orElseThrow(); // L1 Cache hit (NO SQL!)
v1.setMileage(150000L); // Dirty Checking auto-updates on commit!
```

</td>
</tr>
</table>

**Tech Stack:** `Java 25` `Micronaut 4` `Micronaut Data JPA` `Hibernate 6/7` `PostgreSQL 16` `Docker Compose` `Makefile` `JCache / Ehcache` `Gradle`

**Features:**
- ⚡ **First-Level Cache & Dirty Checking** — Proven object identity guarantee (`v1 == v2`) without explicit `.save()` calls
- 🐳 **Containerized Orchestration** — Multi-stage Dockerfile + Docker Compose with PostgreSQL 16 Alpine and healthchecks
- 🔧 **Developer Automation** — GNU Makefile with 13 targets: `make up`, `make down`, `make verify-jpa`, `make bench`, `make logs`
- 🔬 **Automated JPA Diagnostics** — Live test suite and REST endpoints verifying L1 cache, dirty checking, detach/merge, and `@Version` conflicts
- 🏛️ **Polymorphic Inheritance** — Joined Table (`Vehicle`, `IoTSensor`) and Single Table (`HeavyEquipment`, `LightEquipment`)
- 🔍 **Type-Safe Dynamic Queries** — Custom repository using `CriteriaBuilder`, `CriteriaQuery`, and `Root` with dynamic pagination
- 🔒 **Dual Locking Strategies** — Optimistic `@Version` with exponential retry & Pessimistic `FOR UPDATE` for financial transactions
- 🚀 **High-Throughput Batching** — JDBC batch operations combined with periodic `flush()` and `clear()` to prevent heap exhaustion
- 📚 **In-Depth Study Guides** — 6 pillar guides + [JPA Behind the Scenes Architecture Guide](./micronaut-jpa-masterclass/docs/jpa-behind-the-scenes.md)

---

### [API Versioning with Strategy Pattern](./api-versioning)

URL-based API versioning using **Strategy + Factory Pattern** with Spring's automatic Map injection.

<table>
<tr>
<td width="50%">

**🏗️ System Design**
```
            ┌────────────────────────┐
            │    PaymentController    │
            │   /api/v{version}/...  │
            └───────────┬────────────┘
                        │
            ┌───────────▼────────────┐
            │  PaymentServiceFactory  │
            │   Map<String, Strategy> │
            └───────────┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ PaymentV1_0_0 │ │ PaymentV2_0_0 │ │ PaymentV3_0_0 │
│   Strategy    │ │   Strategy    │ │   Strategy    │
└───────────────┘ └───────────────┘ └───────────────┘
```

</td>
<td width="50%">

**🎨 Design Patterns**
| Pattern | Purpose |
|---------|---------|
| **Strategy** | Encapsulate version-specific logic |
| **Factory** | Dynamic strategy resolution |
| **SPI** | Spring auto-discovers implementations |

**Key Insight:**
```java
// Spring auto-injects ALL implementations!
Map<String, PaymentStrategy> strategies;
// "Payment_1_0_0" → PaymentStrategyV1
// "Payment_2_0_0" → PaymentStrategyV2
```

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot 3` `Maven`

---

### [Wallet API](./wallet-api)

Production-ready REST service for managing **digital wallets** with full audit trail and ledger-based balance tracking.

<table>
<tr>
<td width="50%">

**🏗️ Architecture**
```
HTTP → Controller → Service → Mapper → Repository → MongoDB
            ↕            ↕
          DTOs          Domain
                         │
                    Ledger Entries
              (immutable audit trail)
```

</td>
<td width="50%">

**✨ Features**
| Feature | Description |
|---------|-------------|
| **Multi-Currency** | BRL, USD, EUR support |
| **Audit Trail** | Immutable ledger entries |
| **Full CRUD** | Create, deposit, withdraw, transfer |
| **Swagger** | Interactive API documentation |

**📡 Operations**
- 💰 Create wallet
- ➕ Deposit funds
- ➖ Withdraw funds
- 🔄 Transfer between users

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot 3` `MongoDB` `Docker` `Swagger/OpenAPI` `Maven`

---

### [CoraBank API](./corabank-api)

Technical challenge: a **bank account creation API** with referral code support and bug fixing exercise.

<table>
<tr>
<td width="50%">

**📡 API Endpoint**
```
POST /corabank
{
  "name": "User Name",
  "cpf": "12345678901",
  "referralCode": "CORA10"
}
```

**💡 Referral Logic**
- Valid code → account starts with **R$10.00**
- No code → account starts with **R$0.00**
- All accounts default to **active** status

</td>
<td width="50%">

**🎯 Challenge Objectives**
| Goal | Description |
|------|-------------|
| **Bug Fixing** | Identify and fix AI-generated bugs |
| **Refactoring** | Eliminate code smells |
| **Implementation** | Complete missing features |
| **Testing** | Add automated tests (bonus) |

**🗄️ Database:** H2 in-memory

</td>
</tr>
</table>

**Tech Stack:** `Java` `Spring Boot` `H2 Database` `Gradle`

---

### [User API](./userApi)

RESTful CRUD API for user management built with **Kotlin** and **Spring Boot**, using MongoDB and BCrypt password hashing.

<table>
<tr>
<td width="50%">

**📂 Project Structure**
```
src/main/kotlin/user/userApi/
├── UserApiApplication.kt
├── domain/         # Domain entities
├── dto/            # Request/Response DTOs
├── repository/     # MongoRepository
├── service/        # Business logic
├── controller/     # REST endpoints
└── config/         # Extra configs
```

</td>
<td width="50%">

**📡 API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users` | Create user |
| GET | `/api/users` | List (paginated) |
| GET | `/api/users/{id}` | Get by ID |
| PATCH | `/api/users/{id}` | Update user |
| DELETE | `/api/users/{id}` | Delete user |

**🛡️ Validations:** Name (2-120 chars), Email (unique), Password (6+ chars, BCrypt hashed)

</td>
</tr>
</table>

**Tech Stack:** `Kotlin` `Spring Boot` `Spring Data MongoDB` `BCrypt` `Maven` `Docker`

---

### [Open Finance Microservices](./open-finance)

Implementation of **Open Finance Brazil Payment Initiation API v5.0.0-beta.1** as Account Holder (Detentora). Refactored from monolith to **microservices architecture**.

<table>
<tr>
<td width="50%">

**🏗️ Microservices Architecture**
```
┌─────────────────────────────────────────┐
│           open-finance-common           │
│  (Shared DTOs, Enums, Exceptions)       │
└─────────────────┬───────────────────────┘
                  │
      ┌───────────┴───────────┐
      ▼                       ▼
┌─────────────────┐   ┌─────────────────┐
│ open-finance-   │   │ open-finance-   │
│    consent      │   │    payment      │
│  (Port 8081)    │   │  (Port 8082)    │
└─────────────────┘   └─────────────────┘
      ▲                       │
      │       Feign Client    │
      └───────────────────────┘
```

</td>
<td width="50%">

**📦 Microservices**
| Service | Description |
|---------|-------------|
| **common** | Shared library (DTOs, enums) |
| **consent** | Consent management API |
| **payment** | Payment initiation API |

**📡 API Endpoints**
| Service | Endpoints |
|---------|----------|
| Consent | `POST/GET /consents` |
| Payment | `POST/GET/PATCH /pix/payments` |

**🎨 Patterns**
- Hexagonal Architecture
- Strategy + Factory (versioning)
- Inter-service communication (Feign)

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot 3` `Feign Client` `MongoDB` `Docker` `Swagger/OpenAPI`

---

## 📨 Event Streaming & Messaging Projects

### [Kafka Consumer Groups](./kafka-consumer-groups)

Proves that **Kafka consumers with different group IDs independently process messages**.

<table>
<tr>
<td width="50%">

**🏗️ Architecture**
```
          ┌──────────────────────┐
          │    Kafka Topic       │
          │  [msg0][msg1][msg2]  │
          └──────────┬───────────┘
                     │
     ┌───────────────┴───────────────┐
     ▼                               ▼
┌──────────────┐           ┌──────────────┐
│ Consumer A   │           │ Consumer B   │
│ group: "A"   │           │ group: "B"   │
│              │           │              │
│ Offset: 5    │           │ Offset: 3    │
│ (5 msgs ACK) │           │ (3 msgs ACK) │
└──────────────┘           └──────────────┘
       │                          │
       ▼                          ▼
  A's ACK does NOT          Independent
  affect B!                 tracking!
```

</td>
<td width="50%">

**💡 Key Concept**
| Scenario | Behavior |
|----------|----------|
| Same Group ID | Load balancing |
| Different Group ID | Each gets ALL messages |

**🛠️ Real-World Use Case**

Order events processed by multiple services:
- 📧 **Notifications** (group: `notifications`)
- 📊 **Analytics** (group: `analytics`)
- 📦 **Inventory** (group: `inventory`)

Each service tracks its own offset!

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `FastAPI` `aiokafka` `Docker` `pytest`

---

### [Azure Service Bus Connection Management](./servicebus-poc)

Demonstrates **critical importance of proper connection management** — showing memory leak anti-patterns.

<table>
<tr>
<td width="50%">

**❌ Anti-Pattern (Memory Leak)**
```java
// Creates NEW connection per request!
// NEVER closes it = MEMORY LEAK
@PostMapping
public String sendMessage() {
    ServiceBusSenderClient client = 
        new ServiceBusClientBuilder()
            .connectionString(conn)
            .sender()
            .buildClient();
    
    client.sendMessage(msg);
    // NO CLOSE! Leaked forever
}
```

</td>
<td width="50%">

**✅ Best Practice**
```java
// Reuses Spring-managed singleton
@Component
public class GoodProducer {
    private final ServiceBusSenderClient client;
    
    @PostMapping
    public String sendMessage() {
        client.sendMessage(msg);
        return "Success";
    }
}
```

**📊 Impact**
| Metric | Bad | Good |
|--------|-----|------|
| Memory per request | ~2MB | 0 |
| Leaked connections | ∞ | 0 |

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot` `Azure Service Bus` `k6 Load Testing` `Docker`

---

### [Change Data Capture (CDC) Architecture & Serverless Pipeline](./change-data-capture)

Guia aprofundado de **Change Data Capture (CDC)** e implementação de referência serverless na AWS (*DynamoDB Streams → EventBridge Pipes → SQS & DLQ → Lambda*), eliminando o *Dual-Write Anti-Pattern*.

<table>
<tr>
<td width="50%">

**🏗️ Serverless CDC Pipeline**
```
DynamoDB Table (OLTP)
        │
        ▼ (NEW_AND_OLD_IMAGES)
DynamoDB Streams (24h Buffer)
        │
        ▼ (Event Filtering)
EventBridge Pipes
        │
        ▼ (Custom Event Bus)
EventBridge Rules ──► SQS DLQ (Poison Pills)
        │                     ▲
        ▼ (Buffer/Throttle)   │ (3 retries)
Amazon SQS Queue ─────────────┘
        │
        ▼ (ReportBatchItemFailures)
AWS Lambda (Consumer) ──► Redis / Downstream
```

</td>
<td width="50%">

**⚡ Key Concepts & Features**
| Feature | Implementation |
|---|---|
| **Eliminação de Dual-Write** | Leitura não-intrusiva do log de transações |
| **DynamoDB Streams** | Imagens antes/depois (`NEW_AND_OLD_IMAGES`) |
| **EventBridge Pipes** | Conexão nativa e filtragem na origem |
| **Backpressure & DLQ** | Fila SQS amortecedora e isolamento de poison pills |
| **Idempotência & Deltas** | Cálculo campo a campo e deduplicação lógica |
| **Partial Batch Failures** | Retentativa seletiva via `batchItemFailures` |

</td>
</tr>
</table>

**Tech Stack:** `AWS SAM` `DynamoDB Streams` `EventBridge Pipes` `Amazon SQS & DLQ` `AWS Lambda` `Python 3.11+`

---

## 🗄️ Database Projects

### [MongoDB ObjectId Timestamp Proof](./mongodb-objectid-proof)

Proves that **MongoDB ObjectIds contain embedded timestamps** for chronological ordering.

<table>
<tr>
<td width="50%">

**🧬 ObjectId Structure**
```
|--- 4 bytes ---|-- 3 bytes --|-- 2 bytes --|-- 3 bytes --|
|   Timestamp   | Machine ID  | Process ID  |   Counter   |
```

**Key Insight:**
```python
from bson import ObjectId

oid = ObjectId("507f1f77bcf86cd799439011")
timestamp = oid.generation_time
# → datetime(2012, 10, 17, 21, 59, 43)
```

</td>
<td width="50%">

**📡 API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents` | Insert doc |
| POST | `/documents/batch` | Batch insert |
| GET | `/documents` | List with timestamps |
| GET | `/compare-first-last` | Compare ObjectIds |

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `FastAPI` `MongoDB` `PyMongo` `Jupyter`

---

## 🔒 Security & Client SDKs

### [Incognia API Java Client](./incognia-api-java)

Java lightweight client library for **Incognia location identity APIs** — risk assessment for signups, logins and payments.

<table>
<tr>
<td width="50%">

**🔐 API Operations**
| Operation | Description |
|-----------|-------------|
| `registerSignup` | Risk assessment for signups |
| `registerLogin` | Risk assessment for logins |
| `registerPayment` | Risk assessment for payments |
| `registerFeedback` | Report fraud events |
| `registerWebSignup` | Web-based signup assessment |
| `registerWebLogin` | Web-based login assessment |

</td>
<td width="50%">

**🎨 Design Patterns**
| Pattern | Implementation |
|---------|----------------|
| **Multiton** | One instance per (clientId, clientSecret) |
| **Builder** | Fluent API for all requests |
| **Token Management** | Transparent auth renewal |

**⚙️ Customization**
```java
CustomOptions.builder()
  .timeoutMillis(2000L)
  .keepAliveSeconds(3000)
  .maxConnections(5)
  .build();
```

</td>
</tr>
</table>

**Tech Stack:** `Java 8+` `OkHttp` `Gradle` `JUnit` `MIT License`

---

## 🧪 Testing & Code Quality Projects

### [Mutation Testing in Python](./mutation-testing)

Demonstrates why **100% line coverage does not guarantee test quality**, contrasting a weak test suite (100% line coverage, 0% mutation score) with a strong test suite that catches all injected AST mutations.

<table>
<tr>
<td width="50%">

**🔀 The Coverage Illusion**
```
Original Code ──┬──> Weak Suite   ──> Line Coverage: 100%
                │                     Mutation Score: 0% ❌
                │
                └───> Strong Suite ──> Line Coverage: 100%
                                      Mutation Score: 100% ✅
```

**🧬 Mutation Operators Tested:**
- Relational Operator Replacement (ROR: `<` vs `<=`)
- Arithmetic Operator Replacement (AOR: `+` vs `-`)
- Logical Connector Replacement (LCR: `and` vs `or`)
- Constant Replacement (CR)

</td>
<td width="50%">

**⚡ Key Capabilities & CLI**
```bash
# Run interactive comparison CLI
python walkthrough_mutation.py

# Run weak suite (100% line coverage)
pytest tests/test_weak.py --cov=src

# Run strong suite (100% mutation killed)
pytest tests/test_strong.py --cov=src

# Run automated mutmut engine
mutmut run
```

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `pytest` `pytest-cov` `mutmut` `Python AST`

---

## 📐 Observability & Libraries

### [LoggingX Spring Boot Starter](./loggingx-spring-boot-starter)

Plug-and-play library to **standardize technical and business logs** across Java Spring microservices with end-to-end correlation.

<table>
<tr>
<td width="50%">

**🚀 Key Features**
| Feature | Description |
|---------|-------------|
| **Structured JSON** | All logs in JSON format |
| **Correlation** | Auto-propagation of correlationId |
| **AOP Logging** | `@Loggable` and `@BusinessEvent` annotations |
| **PII Redaction** | Automatic masking of sensitive data |
| **Performance** | <2% CPU overhead with smart sampling |

</td>
<td width="50%">

**🔌 Connectors**
| Connector | Auto-Enabled |
|-----------|------|
| HTTP Server | ✅ |
| HTTP Client | ✅ |
| Kafka | ✅ |
| MongoDB | ✅ |
| JDBC | ⚠️ Manual |
| Azure Service Bus | ✅ |

**Usage:**
```java
@Loggable
@Service
public class PaymentService {
    // Logs entry/exit automatically
}
```

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot 3.5+` `Logback` `AOP` `Maven`

---

## 🏛️ Architecture & Design Patterns Summary

### Patterns Demonstrated Across Projects

| Pattern | Project | Description |
|---------|---------|-------------|
| **Strategy** | api-versioning, open-finance | Encapsulate version-specific behavior |
| **Factory** | api-versioning, open-finance | Dynamic strategy and client resolution |
| **Hexagonal** | open-finance | Ports & Adapters architecture |
| **Microservices** | open-finance | Autonomous service decomposition (consent, payment) |
| **Layered** | wallet-api, userApi | Controller → Service → Repository pattern |
| **Multi-Agent** | hedge_fund_bot | 5 collaborating agents with state graph |
| **PEV** | hedge_fund_bot | Plan, Execute, Verify with automated retry |
| **Meta-Controller** | hedge_fund_bot | Intelligent supervisor routing |
| **Continuous Evaluation Harness** | spec-driven-development-agentic | Invariant testing in the agent loop |
| **Property-Based Testing** | spec-driven-development-agentic | Fuzzing business contracts with Hypothesis |
| **Mutation Testing** | mutation-testing | AST-level fault injection and suite scoring |
| **Multiton** | incognia-api-java | One instance per credential pair |
| **Builder** | incognia-api-java | Fluent API construction |
| **AOP** | loggingx-spring-boot-starter | Cross-cutting logging concerns |
| **Singleton** | servicebus-poc | Connection reuse and pool management |
| **Observer** | kafka-consumer-groups | Event-driven consumer group messaging |
| **First-Level Cache / Identity Map** | micronaut-jpa-masterclass | Guarantees reference equality & prevents duplicate SQL SELECT queries within transactions |
| **Optimistic / Pessimistic Locking** | micronaut-jpa-masterclass | Concurrency control via @Version stale detection and SELECT FOR UPDATE exclusivity |
| **Polymorphic Entity Inheritance** | micronaut-jpa-masterclass | Joined Table and Single Table relational inheritance mapping strategies |
| **Model Routing** | agentic-token-optimization | Decouple high-level reasoning from heavy I/O and boilerplate code generation |
| **Pre-Tool Interception Hook** | agentic-token-optimization | Deterministic enforcement to block expensive tool calls via threshold |
| **Ephemeral Worker Delegation** | agentic-token-optimization | Stateless one-shot worker execution with direct disk write |
| **Change Data Capture (CDC)** | change-data-capture | Non-intrusive transaction log interception for near real-time replication |
| **Transactional Outbox** | change-data-capture | Atomic domain event publishing avoiding dual-write anti-pattern |
| **EventBridge Pipes & Filtering** | change-data-capture | Native managed stream ingestion with source-level event filtering |

### System Design Concepts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CONCEPTS COVERED                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🔄 Event-Driven & CDC Architecture    │  🏗️ Hexagonal Architecture    │
│  ├─ Kafka consumer groups              │  ├─ Ports & Adapters          │
│  ├─ Change Data Capture (CDC)          │  ├─ Domain isolation          │
│  ├─ DynamoDB Streams & WAL log         │  └─ Testable design           │
│  ├─ EventBridge Pipes & SQS DLQ        │                                │
│  └─ Dual-Write elimination             │  🤖 AI Agent Architectures    │
│                                         │  ├─ Multi-agent systems       │
│  🔌 API Versioning                      │  ├─ Tool use patterns         │
│  ├─ URL-based versioning               │  ├─ Self-correcting loops     │
│  ├─ Strategy pattern routing           │  └─ Model routing & I/O hooks │
│  └─ Backward compatibility             │                                │
│                                         │  🔒 Security Analysis         │
│  💾 Connection Management               │  ├─ Dependency scanning       │
│  ├─ Singleton vs per-request           │  ├─ CVE detection             │
│  ├─ Memory leak prevention             │  └─ Auto-remediation          │
│  └─ Resource pooling                   │                                │
│                                         │  📐 Observability              │
│  💰 Digital Wallets                     │  ├─ Structured JSON logging   │
│  ├─ Ledger-based auditing              │  ├─ End-to-end correlation    │
│  ├─ Multi-currency support             │  └─ PII redaction             │
│  └─ Immutable transaction history      │                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           COMPLETE TECH STACK                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Languages        │  Python 3.11+, Java 17/25, Kotlin                      │
│                   │                                                      │
│  AI/ML            │  LangGraph, LangChain, Groq, Llama 3.3 70B          │
│                   │                                                      │
│  Backend          │  Micronaut 4, Spring Boot 3, FastAPI, AWS Lambda     │
│                   │                                                      │
│  Persistence/ORM  │  Micronaut Data JPA, Hibernate 6/7, JPA 3.2          │
│                   │                                                      │
│  Message Brokers  │  Apache Kafka, Azure Service Bus, EventBridge, SQS   │
│                   │                                                      │
│  Databases        │  DynamoDB Streams, MongoDB, H2, PostgreSQL           │
│                   │                                                      │
│  Security         │  OWASP Dependency-Check, NVD, Mend.io, Incognia     │
│                   │                                                      │
│  Observability    │  LoggingX, Logback, Structured JSON, AOP            │
│                   │                                                      │
│  Testing          │  pytest, mutmut (mutation testing), Hypothesis, JUnit, k6  │
│                   │                                                      │
│  DevOps           │  AWS SAM, Docker, Docker Compose, Makefile           │
│                   │                                                      │
│  Analysis         │  Jupyter Notebooks, pandas                          │
│                   │                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
software-engineer/
│
├── 🧠 Agent Rules & Memory Bank
│   ├── 📂 .agents/                      # Autonomous agent skills, rules & memory bank
│   │   ├── 📖 MEMORY.md                 # Source of truth project catalog
│   │   ├── 📂 skills/                   # doc-sync, memory-bank skills
│   │   └── 📂 rules/                    # documentation standards
│   └── 🤖 GEMINI.md                     # Root agent operating rules & project invariants
│
├── 📚 Study Guides & Architecture
│   ├── 📂 agentic-token-optimization/   # Standalone Model Routing & Token Optimization Engine
│   │   ├── 📖 README.md
│   │   ├── 📂 src/token_router/         # Core analyzer, routing decision engine & workers
│   │   ├── 📂 bin/                      # CLI wrapper (token-router) & universal pre-tool hook
│   │   ├── 📂 tests/                    # Automated unit tests (unittest)
│   │   ├── 📂 examples/                 # Playground (433-line service & run_demo.sh)
│   │   ├── 📂 agent/                    # Cursor agent skills (bulk-reader, code-writer)
│   │   └── 📂 scripts/                  # Legacy compatibility scripts
│   ├── 📂 ai-coding-skills/             # 13 AI Coding Skills for Multi-IDE (Cursor, Copilot, etc.)
│   │   ├── 📖 README.md                 # Main showcase & installation guide
│   │   ├── 📖 PORTABILITY.md            # IDE portability & format conversion guide
│   │   ├── 📂 01-java-spring-boot-standards/   # Java 21+ & Spring Boot 3 guardrails
│   │   ├── 📂 02-python-modern-standards/      # Python 3.11+, Pydantic v2 & Ruff
│   │   ├── 📂 03-nextjs-app-router/            # Next.js App Router & RSC
│   │   ├── 📂 04-tdd-unit-testing/             # TDD with AAA & mutation testing
│   │   ├── 📂 05-security-owasp-guardrail/     # OWASP Top 10 security rules
│   │   ├── 📂 06-conventional-commits/         # Git commits & PR descriptions
│   │   ├── 📂 07-memory-bank-continuity/       # Multi-session context memory
│   │   ├── 📂 08-anti-hallucination-verifier/  # Read-before-write guardrail
│   │   ├── 📂 09-rest-api-contract-first/      # REST API design standards
│   │   ├── 📂 10-token-router-optimizer/       # Token consumption optimization
│   │   ├── 📂 11-java-micronaut-standards/     # Java 21+ & Micronaut 4 AOT guardrails
│   │   ├── 📂 12-cursor-deploy-commit-guardrail/ # Interactive deploy commit guardrail
│   │   └── 📂 13-empty-deploy-commit-trigger/  # Empty trigger commit (ci: #deployuat #auto)
│   ├── 📂 ai-engineer/                  # AI agent patterns, study guide & CV portfolio
│   │   ├── 📖 AI_ENGINEER_STUDY_GUIDE.md
│   │   ├── 📖 AI_ENGINEER_CV_EXPERIENCE.md
│   │   └── 📖 MCP_RAG_AGENTS_ARCHITECTURE.md
│   ├── 📂 change-data-capture/          # Change Data Capture (CDC) & AWS Serverless Pipeline
│   │   ├── 📖 README.md                 # Master CDC architecture guide (pt-BR)
│   │   └── 📂 examples/
│   │       └── 📂 aws-serverless-cdc/   # Reference architecture: DynamoDB Streams -> Pipes -> SQS -> Lambda
│   │           ├── 📖 README.md
│   │           ├── 📄 template.yaml     # SAM / CloudFormation topology
│   │           └── 📂 src/              # order_processor.py & cdc_payload.json
│   ├── 📂 java-developer/               # Java interview prep & JVM under-the-hood
│   │   └── 📖 JAVA_SPRING_UNDER_THE_HOOD.md
│   ├── 📂 java-collectors-gatherers/     # Custom Collectors, Gatherers (Java 24+) & Streams
│   │   ├── 📖 01-collector-api-anatomy.md
│   │   ├── 📖 02-composing-collectors.md
│   │   ├── 📖 03-custom-collector-from-scratch.md
│   │   ├── 📖 04-gatherer-api-anatomy.md
│   │   ├── 📖 05-ineditos-repetidos.md
│   │   ├── 📖 06-streams-from-scratch.md
│   │   └── 📖 07-exercises.md
│   ├── 📂 study_interview_system_design/ # SOLID, CAP/ACID, patterns & Mastercard SDE-2
│   │   ├── 📖 idempotency-vs-deduplication.md
│   │   └── 📖 MASTERCARD_SDE2_INTERVIEW_PREP.md
│   ├── 📂 system-design/                # System design diagrams
│   ├── 📂 floating-point-precision/     # IEEE 754 precision analysis & benchmarks
│   └── 📂 java25-lts-features/          # Modern Java features & Structured Concurrency
│       └── docs/
│           └── 📖 STRUCTURED_CONCURRENCY_JAVA_VS_KOTLIN.md
│
├── 🤖 AI & Machine Learning
│   ├── 📂 hedge_fund_bot/               # LangGraph multi-agent system
│   │   ├── src/agents/                  # 5 specialized agents
│   │   ├── src/tools/                   # yfinance, search tools
│   │   └── docs/                        # Architecture diagrams
│   ├── 📂 vuln-analyzer-agent/          # Vulnerability scanner CLI & auto-fix
│   └── 📂 spec-driven-development-agentic/ # Spec-driven development with agents
│
├── 🔌 API & Backend
│   ├── 📂 micronaut-jpa-masterclass/    # Java 25 & Micronaut Data JPA 6-pillar masterclass
│   ├── 📂 api-versioning/               # Strategy + Factory pattern
│   ├── 📂 wallet-api/                   # Digital wallet with ledger
│   ├── 📂 corabank-api/                 # Bank account creation challenge
│   └── 📂 userApi/                      # Kotlin CRUD API
│
├── 🏦 Open Finance Microservices
│   └── 📂 open-finance/                 # Open Finance Brazil API
│       ├── 📂 open-finance-common/      # Shared library (DTOs, enums)
│       ├── 📂 open-finance-consent/     # Consent microservice
│       └── 📂 open-finance-payment/     # Payment microservice
│
├── 📨 Event Streaming
│   ├── 📂 kafka-consumer-groups/        # Consumer group isolation proof
│   └── 📂 servicebus-poc/               # Connection management PoC
│
├── 🗄️ Database
│   └── 📂 mongodb-objectid-proof/       # ObjectId timestamp extraction
│
├── 🔒 Security & Client SDKs
│   └── 📂 incognia-api-java/            # Location identity API client
│
├── 📐 Observability & Testing
│   ├── 📂 loggingx-spring-boot-starter/ # Structured logging library
│   └── 📂 mutation-testing/             # Mutation testing demo
│
├── 📄 .gitignore
└── 📖 README.md                         # You are here!
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://docs.docker.com/get-docker/) | 20.10+ | Container runtime |
| [Docker Compose](https://docs.docker.com/compose/) | 2.0+ | Multi-container orchestration |
| [Java](https://adoptium.net/) | 17+ | Java projects |
| [Maven](https://maven.apache.org/) | 3.9+ | Java build tool |
| [Python](https://www.python.org/) | 3.11+ | Python projects |

### Clone & Explore

```bash
# Clone the repository
git clone https://github.com/hlaff147/software-engineer.git
cd software-engineer

# Navigate to any project
cd <project-name>

# Follow project-specific README
cat README.md
```

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔃 Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** — feel free to use these examples for learning and reference.

---

<p align="center">
  <i>Built with ❤️ for learning and sharing knowledge</i>
</p>

<p align="center">
  <a href="https://github.com/hlaff147">
    <img src="https://img.shields.io/badge/GitHub-hlaff147-181717?style=flat-square&logo=github" alt="GitHub">
  </a>
</p>
