<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Java-17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java">
  <img src="https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

# 🛠️ Software & AI Engineer

> A curated collection of hands-on projects exploring software engineering, AI/ML, and modern technologies.

---

## 🎯 About This Repository

This repository serves as a **learning lab** and **reference** for software and AI engineering topics. Each project is:

- ✅ **Self-contained** — Independent setup and documentation
- ✅ **Well-tested** — Comprehensive test suites
- ✅ **Production-ready patterns** — Real-world best practices
- ✅ **Fully documented** — Clear explanations and examples

---

## 📚 Study Guides

| Guide | Description |
|-------|-------------|
| [🤖 AI Engineer Study Guide](./AI_ENGINEER_STUDY_GUIDE.md) | Comprehensive documentation on AI agent patterns, architectures, and LLM applications |
| [☕ Java Developer Guide](./java-developer) | Interview preparation guide for Java backend developers |
| [💼 PicPay Interview Study](./pic_pay_estudo_entrevista) | SOLID, CAP/ACID, Design Patterns, Microservices |

---

## 📂 Projects

### 🤖 AI & Machine Learning

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [🤖 hedge-fund-bot](./hedge_fund_bot) | Multi-agent AI system for automated stock analysis with self-correcting verification | LangGraph, LangChain, Groq, Llama 3.3 | ✅ Complete |

### 🔌 API & Backend Development

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [💳 api-versioning](./api-versioning) | URL-based API versioning using Strategy Pattern with Spring's Map injection | Java 17, Spring Boot 3 | ✅ Complete |
| [🏦 open-finance-payments](./open-finance-payments) | Open Finance Brazil Payment Initiation API v5.0.0-beta.1 (Detentora) | Java 17, Spring Boot, MongoDB | ✅ Complete |

### 🔄 Event Streaming & Messaging

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [🔄 kafka-consumer-groups](./kafka-consumer-groups) | Demonstrates Kafka consumer group behavior and message acknowledgment | Python, FastAPI, Kafka | ✅ Complete |
| [☁️ servicebus-poc](./servicebus-poc) | Azure Service Bus connection management and memory leak prevention | Java 17, Spring Boot, Azure | ✅ Complete |

### 🗄️ Database & Infrastructure

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [🗄️ mongodb-objectid-proof](./mongodb-objectid-proof) | Proves MongoDB ObjectIds contain embedded timestamps for chronological ordering | Python, FastAPI, MongoDB | ✅ Complete |

### 🔒 Security & Analysis

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [🛡️ vuln-analyzer-agent](./vuln-analyzer-agent) | Python agent for vulnerability analysis in Java Spring projects (OWASP, NVD, Mend) | Python, OWASP, NVD | ✅ Complete |

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
| [Conda](https://docs.conda.io/en/latest/miniconda.html) | Latest | Python environment management |

### Clone & Navigate

```bash
# Clone the repository
git clone https://github.com/hlaff147/software-engineer.git
cd software-engineer

# Navigate to a project
cd <project-name>

# Follow project-specific README
```

---

## 📚 Topics Covered

<table>
<tr>
<td width="50%">

### 🤖 AI & LLM Engineering
- Multi-agent systems (LangGraph)
- Tool Use, ReAct patterns
- Meta-Controller routing
- PEV (Plan, Execute, Verify)

</td>
<td width="50%">

### 🔄 Event Streaming & Messaging
- Kafka consumer groups
- Azure Service Bus
- Message acknowledgment patterns
- Event-driven architecture

</td>
</tr>
<tr>
<td width="50%">

### 🎨 Design Patterns
- Strategy Pattern
- Factory Pattern
- Hexagonal Architecture
- Dependency Injection

</td>
<td width="50%">

### 🌐 API Development
- FastAPI async patterns
- Spring Boot REST APIs
- URL-based versioning
- Open Finance Brazil

</td>
</tr>
<tr>
<td width="50%">

### 🗄️ Databases
- MongoDB ObjectId internals
- Connection pooling
- Document databases

</td>
<td width="50%">

### 🔒 Security & DevOps
- Vulnerability scanning
- OWASP Dependency-Check
- Docker containerization
- Makefile automation

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECH STACK                               │
├─────────────────────────────────────────────────────────────────┤
│  Languages      │  Python 3.11+, Java 17+                       │
│  AI/ML          │  LangChain, LangGraph, Groq, Llama 3.3        │
│  Frameworks     │  FastAPI, Spring Boot 3, pytest, JUnit        │
│  Message Broker │  Apache Kafka, Azure Service Bus              │
│  Databases      │  MongoDB                                      │
│  Containers     │  Docker, Docker Compose                       │
│  Security       │  OWASP, NVD, Mend.io                          │
│  Build Tools    │  Maven, pip, Conda                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
software-engineer/
│
├── 📚 Study Guides
│   ├── 📖 AI_ENGINEER_STUDY_GUIDE.md    # AI agent patterns and architectures
│   ├── 📂 java-developer/               # Java interview preparation
│   └── 📂 pic_pay_estudo_entrevista/    # SOLID, CAP/ACID, patterns
│
├── 🤖 AI & Machine Learning
│   └── 📂 hedge_fund_bot/               # Multi-agent stock analysis (LangGraph)
│
├── 🔌 API & Backend
│   ├── 📂 api-versioning/               # Strategy Pattern versioning
│   └── 📂 open-finance-payments/        # Open Finance Brazil API
│
├── 🔄 Event Streaming
│   ├── 📂 kafka-consumer-groups/        # Kafka consumer groups demo
│   └── 📂 servicebus-poc/               # Azure Service Bus POC
│
├── 🗄️ Database
│   └── 📂 mongodb-objectid-proof/       # ObjectId timestamp proof
│
├── 🔒 Security
│   └── 📂 vuln-analyzer-agent/          # Vulnerability analysis agent
│
├── 📄 .gitignore
└── 📖 README.md
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
