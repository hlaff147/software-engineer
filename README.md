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
| **🤖 AI/ML** | 1 project | LangGraph, LangChain, Groq, Llama 3.3 |
| **🔌 Backend APIs** | 5 projects | Spring Boot, Kotlin, Hexagonal Architecture, Strategy Pattern |
| **🏦 Open Finance** | 3 microservices | Spring Boot, Feign Client, MongoDB, Microservices |
| **📨 Event Streaming** | 2 projects | Kafka, Azure Service Bus |
| **🗄️ Database** | 1 project | MongoDB ObjectId internals |
| **🔒 Security** | 2 projects | OWASP, NVD, Incognia, Vulnerability Analysis |
| **📐 Observability** | 1 library | Spring Boot Starter, AOP, Logback, Kafka, MongoDB |
| **📚 Study Guides** | 4 guides | AI Patterns, Java Core, System Design, Interview Prep |

---

## 📚 Study Guides & Documentation

| Guide | Description | Topics |
|-------|-------------|--------|
| [🤖 AI Engineer Study Guide](./AI_ENGINEER_STUDY_GUIDE.md) | Comprehensive AI agent patterns and architectures | 17 patterns: Reflection, ReAct, Multi-Agent, PEV, Meta-Controller |
| [☕ Java Developer Guide](./java-developer) | Backend interview preparation | Java Core, Spring Boot, Microservices, Kafka, K8s |
| [💼 PicPay Interview Study](./study_interview_system_design) | Quick reference for interviews | SOLID, CAP/ACID, Design Patterns, LeetCode |
| [🏛️ System Design Diagrams](./system-design) | Visual system design references | Payment systems, Saga patterns, CAP theorem |

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
| **Strategy** | api-versioning, open-finance | Encapsulate varying behavior |
| **Factory** | api-versioning, open-finance | Dynamic object creation |
| **Hexagonal** | open-finance | Ports & Adapters architecture |
| **Microservices** | open-finance | Service decomposition |
| **Layered** | wallet-api, userApi | Controller → Service → Repository |
| **Multi-Agent** | hedge_fund_bot | Specialized collaborating agents |
| **PEV** | hedge_fund_bot | Plan, Execute, Verify with retry |
| **Meta-Controller** | hedge_fund_bot | Intelligent routing |
| **Multiton** | incognia-api-java | One instance per credential pair |
| **Builder** | incognia-api-java | Fluent API construction |
| **AOP** | loggingx-spring-boot-starter | Cross-cutting logging concerns |
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
│                                         │                                │
│  💰 Digital Wallets                     │  📐 Observability              │
│  ├─ Ledger-based auditing              │  ├─ Structured JSON logging   │
│  ├─ Multi-currency support             │  ├─ End-to-end correlation    │
│  └─ Immutable transaction history      │  └─ PII redaction             │
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
│  Languages        │  Python 3.11+, Java 17+, Kotlin                      │
│                   │                                                      │
│  AI/ML            │  LangGraph, LangChain, Groq, Llama 3.3 70B          │
│                   │                                                      │
│  Backend          │  Spring Boot 3, FastAPI                              │
│                   │                                                      │
│  Message Brokers  │  Apache Kafka, Azure Service Bus                     │
│                   │                                                      │
│  Databases        │  MongoDB, H2                                         │
│                   │                                                      │
│  Security         │  OWASP Dependency-Check, NVD, Mend.io, Incognia     │
│                   │                                                      │
│  Observability    │  LoggingX, Logback, Structured JSON, AOP            │
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
│   ├── 📂 study_interview_system_design/ # SOLID, CAP/ACID, patterns
│   └── 📂 system-design/                # System design diagrams
│
├── 🤖 AI & Machine Learning
│   └── 📂 hedge_fund_bot/               # LangGraph multi-agent system
│       ├── src/agents/                  # 5 specialized agents
│       ├── src/tools/                   # yfinance, search tools
│       └── docs/                        # Architecture diagrams
│
├── 🔌 API & Backend
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
├── 🔒 Security
│   ├── 📂 vuln-analyzer-agent/          # Vulnerability scanner
│   └── 📂 incognia-api-java/            # Location identity API client
│
├── 📐 Observability
│   └── 📂 loggingx-spring-boot-starter/ # Structured logging library
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
