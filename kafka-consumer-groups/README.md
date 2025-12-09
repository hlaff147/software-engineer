<p align="center">
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/pytest-passing-brightgreen?style=for-the-badge" alt="Tests">
</p>

# 🔄 Kafka Consumer Groups Demo

> **Proving that Kafka consumers with different group IDs can independently acknowledge messages — one consumer's acknowledgment does NOT affect the other.**

---

## 🎯 What This Project Proves

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE KEY CONCEPT                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Same Group ID      →  Messages are PARTITIONED among consumers            │
│                          (load balancing)                                    │
│                                                                              │
│   Different Group ID →  Each consumer receives ALL messages                 │
│                          (independent processing)                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 💡 Real-World Use Case

Imagine an e-commerce system where order events need to be processed by multiple services:

| Service | Group ID | Purpose | Can Fail Independently? |
|---------|----------|---------|------------------------|
| 📧 Notification Service | `notifications` | Send order confirmation emails | ✅ Yes |
| 📊 Analytics Service | `analytics` | Track sales metrics | ✅ Yes |
| 📦 Inventory Service | `inventory` | Update stock levels | ✅ Yes |

**Each service receives ALL orders and tracks its OWN progress!**

---

## 🏗️ Architecture

```
                         ┌──────────────────────────┐
                         │      Kafka Topic         │
                         │     "demo-topic"         │
                         │                          │
                         │  [msg0][msg1][msg2]...   │
                         └────────────┬─────────────┘
                                      │
                    ┌─────────────────┴─────────────────┐
                    │         Same messages             │
                    │         to BOTH groups            │
                    ▼                                   ▼
        ┌───────────────────────┐       ┌───────────────────────┐
        │     Consumer A        │       │     Consumer B        │
        │  ┌─────────────────┐  │       │  ┌─────────────────┐  │
        │  │ group-id: "A"   │  │       │  │ group-id: "B"   │  │
        │  └─────────────────┘  │       │  └─────────────────┘  │
        │                       │       │                       │
        │  Offset: 5 ────────── │       │  Offset: 3 ────────── │
        │  (processed 5 msgs)   │       │  (processed 3 msgs)   │
        │                       │       │                       │
        │  ✅ Independent!      │       │  ✅ Independent!      │
        └───────────────────────┘       └───────────────────────┘
                    │                               │
                    ▼                               ▼
        ┌───────────────────────┐       ┌───────────────────────┐
        │  A can ACK msg 0-4    │       │  B can ACK msg 0-2    │
        │  without affecting B  │       │  without affecting A  │
        └───────────────────────┘       └───────────────────────┘
```

---

## 📁 Project Structure

```
kafka-consumer-groups/
├── 📂 app/
│   ├── __init__.py
│   ├── main.py              # 🚀 FastAPI application & endpoints
│   ├── config.py            # ⚙️  Configuration settings
│   ├── producer.py          # 📤 Kafka producer service
│   └── consumer.py          # 📥 Kafka consumer service
│
├── 📂 tests/
│   ├── conftest.py          # 🔧 Test fixtures
│   ├── test_producer.py     # ✅ Producer unit tests
│   ├── test_consumer.py     # ✅ Consumer unit tests
│   ├── test_consumer_group_isolation.py  # ⭐ KEY TESTS!
│   └── test_api.py          # ✅ API integration tests
│
├── 📂 notebooks/
│   └── consumer_groups_proof.ipynb  # 📊 Visual proof with graphs
│
├── 🐳 docker-compose.yml    # Kafka + Zookeeper + UI
├── 📋 environment.yml       # Conda environment
├── 📋 requirements.txt      # pip dependencies
├── ⚙️  pytest.ini            # pytest configuration
└── 📖 README.md             # You are here!
```

---

## 🚀 Quick Start

### 1️⃣ Start Kafka Infrastructure

```bash
docker-compose up -d
```

This starts:

| Service | Port | URL |
|---------|------|-----|
| Zookeeper | 2181 | - |
| Kafka | 9092 | `localhost:9092` |
| Kafka UI | 8080 | http://localhost:8080 |

### 2️⃣ Install Dependencies

```bash
# Create and activate conda environment
conda env create -f environment.yml
conda activate kafka-consumer-groups
```

### 3️⃣ Run the Application

```bash
uvicorn app.main:app --reload
```

📍 API available at: http://localhost:8000  
📍 Swagger docs at: http://localhost:8000/docs

### 4️⃣ Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run only the consumer group isolation tests (the proof!)
pytest tests/test_consumer_group_isolation.py -v

# Run with coverage
pytest --cov=app --cov-report=html
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | 🏥 Health check |
| `/produce` | `POST` | 📤 Send a message to Kafka |
| `/consumers/status` | `GET` | 📊 Get status of both consumer groups |
| `/consumers/{A\|B}/acknowledge` | `POST` | ✅ Acknowledge a message for a specific consumer |
| `/consumers/reset` | `POST` | 🔄 Reset both consumers' state |

---

## 🧪 Testing the Concept

### Option 1: Via API (Manual Testing)

```bash
# 1. Produce a message
curl -X POST http://localhost:8000/produce \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello Kafka!", "key": "test-1"}'

# 2. Check both consumers received it
curl http://localhost:8000/consumers/status

# 3. Acknowledge for Consumer A only
curl -X POST "http://localhost:8000/consumers/A/acknowledge?message_offset=0"

# 4. Verify Consumer B is UNAFFECTED
curl http://localhost:8000/consumers/status
# ✅ Consumer A: acknowledged = 1
# ✅ Consumer B: acknowledged = 0  (not affected!)
```

### Option 2: Via Tests (Automated Proof)

The key tests in `tests/test_consumer_group_isolation.py`:

| Test | What It Proves |
|------|----------------|
| `test_different_group_ids_maintain_separate_state` | Both consumers receive ALL messages |
| `test_acknowledge_in_one_group_does_not_affect_other` | ⭐ **THE CRITICAL TEST** |
| `test_multiple_messages_independent_acknowledgment` | Complex multi-message scenario |
| `test_reset_one_consumer_does_not_affect_other` | Reset isolation |

### Option 3: Via Jupyter Notebook (Visual Proof)

```bash
jupyter notebook notebooks/consumer_groups_proof.ipynb
```

See beautiful visualizations proving the concept! 📊

---

## 📊 Visual Proof

### Message Distribution

```
    Messages:     [0] [1] [2] [3] [4] [5] [6] [7] [8] [9]
                   │   │   │   │   │   │   │   │   │   │
    ───────────────┼───┼───┼───┼───┼───┼───┼───┼───┼───┼──── Kafka Topic
                   │   │   │   │   │   │   │   │   │   │
                   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
    Consumer A:   [0] [1] [2] [3] [4] [5] [6] [7] [8] [9]  ← ALL messages
                   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
    Consumer B:   [0] [1] [2] [3] [4] [5] [6] [7] [8] [9]  ← ALL messages
```

### Independent Acknowledgment

```
    Consumer A:   [✓] [✓] [✓] [✓] [✓] [ ] [ ] [ ] [ ] [ ]  ← ACKed 0-4
    Consumer B:   [✓] [✓] [✓] [ ] [ ] [ ] [ ] [ ] [ ] [ ]  ← ACKed 0-2
                   ↑   ↑   ↑
                   └───┴───┴── Messages 0-2 acknowledged by BOTH groups!
```

---

## 🔑 Key Takeaways

| Concept | Explanation |
|---------|-------------|
| **Group ID** | Unique identifier for offset tracking |
| **Different Group IDs** | Each group gets ALL messages |
| **Same Group ID** | Messages partitioned among consumers |
| **Offset** | Position in the topic (each group tracks its own) |
| **Acknowledgment** | Committing offset after processing |

---

## 🛠️ Tech Stack

- **Python 3.11+** — Modern Python with async support
- **FastAPI** — High-performance async web framework
- **aiokafka** — Async Kafka client for Python
- **pytest** — Testing framework with async support
- **Docker** — Containerized Kafka infrastructure

---

## 📝 License

MIT License — feel free to use for learning and reference.

---

<p align="center">
  <b>🎓 This project is part of the <a href="../README.md">Software Engineer</a> learning repository</b>
</p>
