<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Java-17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java">
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
| **🤖 AI/ML** | 1 project | LangGraph, LangChain, Groq, Llama 3.3 |
| **🔌 Backend APIs** | 2 projects | Spring Boot, Hexagonal Architecture, Strategy Pattern |
| **📨 Event Streaming** | 2 projects | Kafka, Azure Service Bus |
| **🗄️ Database** | 1 project | MongoDB ObjectId internals |
| **🔒 Security** | 1 project | OWASP, NVD, Vulnerability Analysis |
| **📚 Study Guides** | 3 guides | AI Patterns, Java Core, Interview Prep |

---

## 📚 Study Guides & Documentation

| Guide | Description | Topics |
|-------|-------------|--------|
| [🤖 AI Engineer Study Guide](./AI_ENGINEER_STUDY_GUIDE.md) | Comprehensive AI agent patterns and architectures | 17 patterns: Reflection, ReAct, Multi-Agent, PEV, Meta-Controller |
| [☕ Java Developer Guide](./java-developer) | Backend interview preparation | Java Core, Spring Boot, Microservices, Kafka, K8s |
| [💼 PicPay Interview Study](./pic_pay_estudo_entrevista) | Quick reference for interviews | SOLID, CAP/ACID, Design Patterns, LeetCode |

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

## 🔌 API & Backend Projects

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

### [Open Finance Payments API](./open-finance-payments)

Implementation of **Open Finance Brazil Payment Initiation API v5.0.0-beta.1** as Account Holder (Detentora).

<table>
<tr>
<td width="50%">

**🏗️ Hexagonal Architecture**
```
┌─────────────────────────────────────────┐
│             Adapter Layer               │
│  ┌─────────────┐    ┌────────────────┐  │
│  │ REST Input  │    │ MongoDB Output │  │
│  │ Controllers │    │  Repositories  │  │
│  └──────┬──────┘    └───────▲────────┘  │
└─────────┼───────────────────┼───────────┘
          │                   │
┌─────────▼───────────────────▼───────────┐
│           Application Layer             │
│  ┌──────────────────────────────────┐   │
│  │      Use Cases / Services        │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────┐
│             Domain Layer                │
│  ┌──────────┐  ┌────────┐  ┌────────┐   │
│  │ Consent  │  │ Payment│  │ Rules  │   │
│  └──────────┘  └────────┘  └────────┘   │
└─────────────────────────────────────────┘
```

</td>
<td width="50%">

**📡 API Endpoints**
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/consents` | Create consent |
| GET | `/consents/{id}` | Get consent |
| POST | `/pix/payments` | Create Pix |
| GET | `/pix/payments/{id}` | Get payment |
| PATCH | `/pix/payments/{id}` | Cancel |

**🎨 Patterns**
- Hexagonal Architecture
- Strategy + Factory (versioning)
- Mocked external services (DICT, SPI)

</td>
</tr>
</table>

**Tech Stack:** `Java 17` `Spring Boot 3` `MongoDB` `Docker` `Swagger/OpenAPI`

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

## 🔒 Security & Analysis Projects

### [Vulnerability Analyzer Agent](./vuln-analyzer-agent)

Python CLI agent for **vulnerability analysis in Java Spring projects** with auto-fix capabilities.

<table>
<tr>
<td width="50%">

**🔍 Data Sources**
| Source | Type |
|--------|------|
| OWASP Dependency-Check | Offline analysis |
| NVD (National Vulnerability Database) | Direct API queries |
| Mend.io (optional) | Proprietary "WS-" vulns |

**📊 Output Formats**
- Console (colored terminal)
- HTML report
- JSON (machine-readable)

</td>
<td width="50%">

**⚡ Commands**
```bash
# Scan project
vuln-analyzer scan /path/to/project

# With Mend integration
vuln-analyzer scan /path --mend

# Auto-fix vulnerabilities
vuln-analyzer fix /path --apply

# Dry-run (preview fixes)
vuln-analyzer fix /path --dry-run
```

</td>
</tr>
</table>

**Tech Stack:** `Python 3.11+` `Click CLI` `OWASP` `NVD API` `Mend.io`

---

## 🏛️ Architecture & Design Patterns Summary

### Patterns Demonstrated Across Projects

| Pattern | Project | Description |
|---------|---------|-------------|
| **Strategy** | api-versioning, open-finance | Encapsulate varying behavior |
| **Factory** | api-versioning, open-finance | Dynamic object creation |
| **Hexagonal** | open-finance-payments | Ports & Adapters architecture |
| **Multi-Agent** | hedge_fund_bot | Specialized collaborating agents |
| **PEV** | hedge_fund_bot | Plan, Execute, Verify with retry |
| **Meta-Controller** | hedge_fund_bot | Intelligent routing |
| **Singleton** | servicebus-poc | Connection reuse |
| **Observer** | kafka-consumer-groups | Event-driven messaging |

### System Design Concepts

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CONCEPTS COVERED                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  🔄 Event-Driven Architecture          │  🏗️ Hexagonal Architecture    │
│  ├─ Kafka consumer groups              │  ├─ Ports & Adapters          │
│  ├─ Message acknowledgment             │  ├─ Domain isolation          │
│  └─ Independent offset tracking        │  └─ Testable design           │
│                                         │                                │
│  🔌 API Versioning                      │  🤖 AI Agent Architectures    │
│  ├─ URL-based versioning               │  ├─ Multi-agent systems       │
│  ├─ Strategy pattern routing           │  ├─ Tool use patterns         │
│  └─ Backward compatibility             │  └─ Self-correcting loops     │
│                                         │                                │
│  💾 Connection Management               │  🔒 Security Analysis         │
│  ├─ Singleton vs per-request           │  ├─ Dependency scanning       │
│  ├─ Memory leak prevention             │  ├─ CVE detection             │
│  └─ Resource pooling                   │  └─ Auto-remediation          │
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
│  Languages        │  Python 3.11+, Java 17+                              │
│                   │                                                      │
│  AI/ML            │  LangGraph, LangChain, Groq, Llama 3.3 70B          │
│                   │                                                      │
│  Backend          │  Spring Boot 3, FastAPI                              │
│                   │                                                      │
│  Message Brokers  │  Apache Kafka, Azure Service Bus                     │
│                   │                                                      │
│  Databases        │  MongoDB                                             │
│                   │                                                      │
│  Security         │  OWASP Dependency-Check, NVD, Mend.io               │
│                   │                                                      │
│  Testing          │  pytest, JUnit, k6 (load testing)                   │
│                   │                                                      │
│  DevOps           │  Docker, Docker Compose, Makefile                   │
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
├── 📚 Study Guides
│   ├── 📖 AI_ENGINEER_STUDY_GUIDE.md    # 17 AI agent patterns
│   ├── 📂 java-developer/               # Java interview prep (5 modules)
│   └── 📂 pic_pay_estudo_entrevista/    # SOLID, CAP/ACID, patterns
│
├── 🤖 AI & Machine Learning
│   └── 📂 hedge_fund_bot/               # LangGraph multi-agent system
│       ├── src/agents/                  # 5 specialized agents
│       ├── src/tools/                   # yfinance, search tools
│       └── docs/                        # Architecture diagrams
│
├── 🔌 API & Backend
│   ├── 📂 api-versioning/               # Strategy + Factory pattern
│   │   └── src/.../strategy/            # PaymentStrategy implementations
│   └── 📂 open-finance-payments/        # Open Finance Brazil API
│       └── src/.../                     # Hexagonal architecture
│
├── 📨 Event Streaming
│   ├── 📂 kafka-consumer-groups/        # Consumer group isolation proof
│   │   ├── app/                         # FastAPI application
│   │   └── tests/                       # Isolation tests
│   └── 📂 servicebus-poc/               # Connection management PoC
│       ├── src/.../controller/          # Good vs Bad producers
│       └── k6/                          # Load test scripts
│
├── 🗄️ Database
│   └── 📂 mongodb-objectid-proof/       # ObjectId timestamp extraction
│       ├── app/                         # FastAPI + PyMongo
│       └── notebooks/                   # Analysis notebook
│
├── 🔒 Security
│   └── 📂 vuln-analyzer-agent/          # Vulnerability scanner
│       ├── src/vuln_analyzer/           # Analyzers, fixers, reporters
│       └── test-projects/               # Vulnerable test projects
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
