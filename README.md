<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
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

| Project | Description | Key Concepts | Status |
|---------|-------------|--------------|--------|
| [🔄 kafka-consumer-groups](./kafka-consumer-groups) | Demonstrates Kafka consumer group behavior — how consumers with different group IDs independently process and acknowledge messages | Consumer Groups, Offset Management, Event Streaming | ✅ Complete |

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| [Docker](https://docs.docker.com/get-docker/) | 20.10+ | Container runtime |
| [Docker Compose](https://docs.docker.com/compose/) | 2.0+ | Multi-container orchestration |
| [Conda](https://docs.conda.io/en/latest/miniconda.html) | Latest | Python environment management |
| [Python](https://www.python.org/) | 3.11+ | Programming language |

### Clone & Navigate

```bash
# Clone the repository
git clone https://github.com/hlaff147/software-engineer.git
cd software-engineer

# Navigate to a project
cd kafka-consumer-groups

# Create conda environment
conda env create -f environment.yml
conda activate kafka-consumer-groups

# Follow project-specific README
```

---

## 📚 Topics Covered

<table>
<tr>
<td width="50%">

### 🔄 Event Streaming & Messaging
- Kafka consumer groups
- Message acknowledgment patterns
- Offset management
- Event-driven architecture

</td>
<td width="50%">

### 🌐 API Development
- FastAPI async patterns
- RESTful API design
- Request/Response models
- API documentation (OpenAPI)

</td>
</tr>
<tr>
<td width="50%">

### 🧪 Testing Strategies
- Unit testing with pytest
- Integration testing
- Mocking external services
- Test fixtures and factories

</td>
<td width="50%">

### 🐳 DevOps & Infrastructure
- Docker containerization
- Docker Compose orchestration
- Environment management
- CI/CD pipelines

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECH STACK                                │
├─────────────────────────────────────────────────────────────────┤
│  Languages      │  Python 3.11+                                 │
│  Frameworks     │  FastAPI, pytest                              │
│  Message Broker │  Apache Kafka                                 │
│  Containers     │  Docker, Docker Compose                       │
│  Environment    │  Conda, pip                                   │
│  Testing        │  pytest, pytest-asyncio, httpx                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

```
software-engineer/
├── 📂 kafka-consumer-groups/     # Kafka consumer groups demo
│   ├── 📂 app/                   # FastAPI application
│   ├── 📂 tests/                 # Test suite
│   ├── 📂 notebooks/             # Jupyter notebooks with visualizations
│   ├── 🐳 docker-compose.yml     # Kafka infrastructure
│   ├── 📋 environment.yml        # Conda environment
│   └── 📖 README.md              # Project documentation
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
