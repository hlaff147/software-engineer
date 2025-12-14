<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Java-17+-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white" alt="Java">
  <img src="https://img.shields.io/badge/Spring%20Boot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white" alt="Spring Boot">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
</p>

# 🛠️ Software Engineer

> A curated collection of hands-on projects exploring software engineering concepts, patterns, and modern technologies.

---

## 🎯 About This Repository

This repository serves as a **learning lab** and **reference** for software engineering topics. Each project is:

- ✅ **Self-contained** — Independent setup and documentation
- ✅ **Well-tested** — Comprehensive test suites
- ✅ **Production-ready patterns** — Real-world best practices
- ✅ **Fully documented** — Clear explanations and examples

---

## 📂 Projects

| Project | Description | Tech Stack | Status |
|---------|-------------|------------|--------|
| [🔄 kafka-consumer-groups](./kafka-consumer-groups) | Demonstrates Kafka consumer group behavior — how consumers with different group IDs independently process and acknowledge messages | Python, FastAPI, Kafka | ✅ Complete |
| [💳 api-versioning](./api-versioning) | URL-based API versioning using Strategy Pattern with Spring's Map injection for dynamic strategy resolution | Java 17, Spring Boot 3 | ✅ Complete |
| [🗄️ mongodb-objectid-proof](./mongodb-objectid-proof) | Proves that MongoDB ObjectIds contain embedded timestamps for chronological ordering | Python, FastAPI, MongoDB | ✅ Complete |
| [☁️ servicebus-poc](./servicebus-poc) | Demonstrates proper vs improper connection management with Azure Service Bus — memory leak prevention | Java 17, Spring Boot, Azure | ✅ Complete |
| [📚 java-developer](./java-developer) | Comprehensive interview preparation guide for Java backend developers | Markdown | ✅ Complete |

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

### 🔄 Event Streaming & Messaging
- Kafka consumer groups
- Azure Service Bus
- Message acknowledgment patterns
- Event-driven architecture

</td>
<td width="50%">

### 🎨 Design Patterns
- Strategy Pattern
- Factory Pattern
- Singleton (Spring Beans)
- Dependency Injection

</td>
</tr>
<tr>
<td width="50%">

### 🌐 API Development
- FastAPI async patterns
- Spring Boot REST APIs
- URL-based API versioning
- OpenAPI documentation

</td>
<td width="50%">

### 🗄️ Databases
- MongoDB ObjectId internals
- Timestamp extraction from ObjectId
- Connection pooling best practices

</td>
</tr>
<tr>
<td width="50%">

### 🧪 Testing Strategies
- Unit testing (pytest, JUnit)
- Integration testing
- Load testing (k6)
- Mocking external services

</td>
<td width="50%">

### 🐳 DevOps & Infrastructure
- Docker containerization
- Docker Compose orchestration
- Azure Service Bus Emulator
- Makefile automation

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECH STACK                                │
├─────────────────────────────────────────────────────────────────┤
│  Languages      │  Python 3.11+, Java 17+                       │
│  Frameworks     │  FastAPI, Spring Boot 3, pytest, JUnit        │
│  Message Broker │  Apache Kafka, Azure Service Bus              │
│  Databases      │  MongoDB                                      │
│  Containers     │  Docker, Docker Compose                       │
│  Testing        │  pytest, JUnit, k6 (load testing)             │
│  Build Tools    │  Maven, pip, Conda                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
software-engineer/
├── 📂 api-versioning/            # Spring Boot API versioning with Strategy Pattern
│   ├── 📂 src/main/java/         # Java source code
│   ├── 🐳 pom.xml                # Maven configuration
│   └── 📖 README.md              # Project documentation
│
├── 📂 kafka-consumer-groups/     # Kafka consumer groups demo
│   ├── 📂 app/                   # FastAPI application
│   ├── 📂 tests/                 # Test suite
│   ├── 📂 notebooks/             # Jupyter notebooks
│   ├── 🐳 docker-compose.yml     # Kafka infrastructure
│   └── 📖 README.md              # Project documentation
│
├── � mongodb-objectid-proof/    # MongoDB ObjectId timestamp proof
│   ├── 📂 app/                   # FastAPI application
│   ├── 📂 notebooks/             # Analysis notebook
│   ├── 🐳 docker-compose.yml     # MongoDB container
│   └── 📖 README.md              # Project documentation
│
├── 📂 servicebus-poc/            # Azure Service Bus connection management
│   ├── 📂 src/                   # Spring Boot source
│   ├── 📂 k6/                    # Load test scripts
│   ├── 📂 analysis/              # Jupyter analysis notebooks
│   ├── 🐳 docker-compose.yml     # Azure emulator
│   └── 📖 README.md              # Project documentation
│
├── 📂 java-developer/            # Java interview preparation guide
│   ├── 📄 01-java-core.md        # Java fundamentals
│   ├── 📄 02-spring-boot.md      # Spring Boot concepts
│   ├── 📄 03-microservices.md    # Microservices patterns
│   ├── 📄 04-coding-questions.md # Coding challenges
│   └── 📄 05-others.md           # Kafka, K8s, Docker, SQL
│
├── 📄 .gitignore                 # Git ignore rules
└── 📖 README.md                  # This file
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
