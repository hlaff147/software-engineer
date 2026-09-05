# 🚛 Global Fleet & Asset Management System — Micronaut Data JPA Masterclass

[![Java 25](https://img.shields.io/badge/Java-25%20LTS-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)](https://openjdk.org/)
[![Micronaut 4](https://img.shields.io/badge/Micronaut-4.4.4-black?style=for-the-badge&logo=micronaut&logoColor=white)](https://micronaut.io/)
[![Hibernate ORM](https://img.shields.io/badge/Hibernate-6%2F7-59666C?style=for-the-badge&logo=hibernate&logoColor=white)](https://hibernate.org/)
[![Jakarta Persistence](https://img.shields.io/badge/Jakarta%20JPA-3.2-EE0000?style=for-the-badge&logo=jakarta&logoColor=white)](https://jakarta.ee/specifications/persistence/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Gradle](https://img.shields.io/badge/Gradle-8.12-02303A?style=for-the-badge&logo=gradle&logoColor=white)](https://gradle.org/)

> 📘 **Architectural Deep-Dive**: For an in-depth exploration of the Persistence Context state machine, snapshot dirty checking, flush timing, AST compilation, and locking mechanics, read the [JPA Behind the Scenes Architecture Guide](./docs/jpa-behind-the-scenes.md).


---

## 📌 Overview & Business Domain

A production-grade, enterprise backend system designed to master **every advanced utility, pattern, and edge case of Jakarta Persistence (JPA) and Hibernate** using **Java 25** and **Micronaut Data JPA**.

The project models a **Global Fleet & Asset Management System** managing heavy/light assets, IoT telemetries, maintenance lifecycles, multi-tenant fleet operators, and append-only audit trails.

### 💡 Core Focus: Mastering the Persistence Context
A common misconception in JPA is that every repository call executes a database query.
This codebase demonstrates that `findById()` does **not** always hit the database:
within the same transaction (`@Transactional`), Hibernate uses its **First-Level Cache** to return the managed entity in memory without emitting another `SELECT` query, while **Dirty Checking** automatically flushes changes to the database on commit without calling `.save()` or `.update()`.

---

## 🏗️ System Architecture & Entity Relationships

```text
                               ┌────────────────────────────────┐
                               │       AuditableEntity          │
                               │ (createdAt, updatedAt, audit)  │
                               └───────────────┬────────────────┘
                                               │ extends
                               ┌───────────────▼────────────────┐
                               │             Asset              │
                               │  (Joined Table Inheritance)    │
                               │  - id (PK)                     │
                               │  - version (@Version)          │
                               │  - location (@Embedded GPS)    │
                               │  - tags (@ElementCollection)   │
                               └───┬────────────────────────┬───┘
                                   │                        │
                    ┌──────────────▼──────────┐  ┌──────────▼──────────────┐
                    │         Vehicle         │  │        IoTSensor        │
                    │ - license_plate (UNIQUE)│  │ - mac_address (UNIQUE)  │
                    │ - mileage, fuel_type    │  │ - firmware, battery     │
                    └──────────────┬──────────┘  └─────────────────────────┘
                                   │
                                   │ @OneToMany (cascade = ALL, orphanRemoval = true)
                                   ▼
                    ┌─────────────────────────┐
                    │   MaintenanceSchedule   │
                    │ - @BatchSize(size = 25) │
                    └──────────────┬──────────┘
                                   │ @OneToMany
                                   ▼
                    ┌─────────────────────────┐
                    │     MaintenanceLog      │
                    └─────────────────────────┘
```

---

## 🏛️ The 6 JPA Pillars Matrix

| Pillar | Focus Area | Key Concepts Demonstrated | Detailed Guide |
| :--- | :--- | :--- | :---: |
| **1** | **Advanced Entity Mappings** | Joined Table (`Vehicle`, `IoTSensor`) vs Single Table (`Equipment`), Value Objects (`@Embeddable GpsCoordinate`, `Address`, `Money`), `@ElementCollection Tag`, Cascading (`CascadeType.ALL`, `orphanRemoval = true`), `@ManyToMany` | [Read Guide](./docs/jpa-pillar-1-entity-mappings.md) |
| **2** | **Performance & Fetching** | First-Level Cache hit mechanics, Object Identity guarantee, Dirty Checking, N+1 problem mitigation via `@BatchSize(size = 25)`, Declarative `@Join(FETCH)` | [Read Guide](./docs/jpa-pillar-2-performance-fetching.md) |
| **3** | **Querying & Projections** | Constructor-expression DTO records (`SELECT new ...`), Native SQL scalar projections, Type-safe dynamic queries via **Criteria API** with `EntityManager` | [Read Guide](./docs/jpa-pillar-3-querying-projections.md) |
| **4** | **Concurrency & Locking** | Optimistic Locking (`@Version`) with retry loop, Pessimistic Locking (`LockModeType.PESSIMISTIC_WRITE`), lock timeouts, and race condition defense | [Read Guide](./docs/jpa-pillar-4-concurrency-locking.md) |
| **5** | **Lifecycle Auditing** | JPA lifecycle callbacks (`@PrePersist`, `@PreUpdate`, `@PostLoad`), Asynchronous audit event publishing via Virtual Threads | [Read Guide](./docs/jpa-pillar-5-lifecycle-auditing.md) |
| **6** | **Enterprise Optimization** | JDBC Batching (`batch_size = 30`, `order_inserts`), Memory management (`flush()` / `clear()`), Hibernate Second-Level Cache (JCache + Ehcache), Java 25 Compact Headers | [Read Guide](./docs/jpa-pillar-6-enterprise-optimization.md) |

---

## ☕ Java 25 & Micronaut Synergy

* **Compact Object Headers (JEP 519):** Reduces cached entity heap consumption by 15%–25%.
* **Virtual Threads (Project Loom):** Safe execution of blocking JDBC database calls on `@ExecuteOn(TaskExecutors.BLOCKING)`.
* **Java Records as Embeddables & DTOs:** Zero-reflection immutable projection carriers compiled Ahead-of-Time by Micronaut Data.

---

## 🛠️ Tech Stack

* **Language:** Java 25 (OpenJDK 25+)
* **Framework:** Micronaut Framework 4.4.4
* **Persistence Layer:** Micronaut Data JPA + Hibernate ORM
* **Caching:** JCache (JSR-107) + Ehcache 3
* **Databases:** PostgreSQL 16 (Docker) / H2 (In-Memory default for unit tests)
* **Connection Pool:** HikariCP
* **Containerization:** Multi-stage Dockerfile + Docker Compose (PostgreSQL 16 Alpine)
* **Developer Automation:** GNU Makefile (13 automated targets)
* **Build Tool:** Gradle 8.12+ (Kotlin DSL)
* **Testing:** JUnit 5, Micronaut Test, AssertJ

---

## 🐳 Containerized Execution & Developer Automation

A production-grade GNU `Makefile` unifies local development, test execution, container orchestration, and JPA diagnostic benchmarks:

```bash
# Display all available targets
make help
```

### Key Makefile Targets

| Target | Command Executed | Description |
|:---|:---|:---|
| `make workshop` | `make up && make verify-jpa && make bench` | 🚀 **One-command full demo**: starts containers, executes all 6 JPA diagnostics, and runs benchmark |
| `make up` | `docker compose up --build -d` | Build multi-stage Docker image and start PostgreSQL 16 + Micronaut stack |
| `make down` | `docker compose down` | Gracefully stop containers and remove bridge network |
| `make clean` | `docker compose down -v ...` | Full cleanup: stops containers, destroys database volumes, and cleans Gradle build cache |
| `make logs` | `docker compose logs -f app` | Tail live application logs showing Hibernate SQL, bound parameters, and cache metrics |
| `make logs-db` | `docker compose logs -f postgres` | Tail live PostgreSQL database logs |
| `make psql` | `docker compose exec postgres psql ...` | Connect directly to PostgreSQL interactive terminal (`fleet_admin`) |
| `make verify-jpa` | Automated `curl` pipeline | Run the 6-stage JPA diagnostic test suite against the running stack |
| `make bench` | `curl ... /api/telemetry/bulk-seed` | Execute bulk ingestion benchmark (1,000 records with periodic `flush()`/`clear()`) |
| `make test` | `./gradlew test` | Execute local JUnit 5 test suite across all 6 JPA pillars |
| `make run` | `./gradlew run` | Launch application locally using in-memory H2 database |


---

## 🔬 Automated JPA Diagnostic Workshop

The application includes a specialized `JpaDiagnosticService` and `JpaDiagnosticController` designed to verify and demystify JPA/Hibernate behaviors in real time:

```bash
# 1. Start the containerized environment
make up

# 2. Run the complete diagnostic suite
make verify-jpa
```

### Diagnostic Endpoints

| Endpoint | Method | JPA Concept Verified | Description |
|:---|:---:|:---|:---|
| `/api/diagnostic/seed` | `POST` | Entity Lifecycle & Cascading | Seeds an Operator, Vehicle, and Maintenance Schedule with value objects |
| `/api/diagnostic/l1-cache` | `GET` | First-Level Cache (L1) Hit | Proves that consecutive `findById` calls issue 1 SELECT and return identical memory references (`v1 == v2`) |
| `/api/diagnostic/dirty-checking` | `POST` | Automatic Dirty Checking | Mutates an entity in memory without calling `.save()` and confirms Hibernate triggers `UPDATE` on commit |
| `/api/diagnostic/detach-lifecycle` | `POST` | Detached Entity Lifecycle | Demonstrates `MANAGED -> DETACHED -> MANAGED` state transitions and `merge()` behavior |
| `/api/diagnostic/n-plus-1` | `GET` | N+1 Trap vs `@BatchSize` | Compares un-batched lazy collection traversal against Hibernate `@BatchSize(size = 25)` |
| `/api/diagnostic/optimistic-lock` | `POST` | Optimistic Locking (`@Version`) | Simulates concurrent version conflict and catches `OptimisticLockException` |
| `/api/diagnostic/statistics` | `GET` | Hibernate Metrics & Cache Ratios | Returns live statistics (L1/L2 hits, entity loads, queries executed, transaction counts) |

---

## 📡 Sample cURL Requests

### 1. Verify First-Level Cache (No second SQL executed)
```bash
curl -X GET http://localhost:8080/api/diagnostic/l1-cache
```
**Response:**
```json
{
  "diagnostic": "First-Level Cache (L1) Verification",
  "vehicleId": 1,
  "firstQueryExecutedSql": true,
  "secondQueryHitL1Cache": true,
  "referenceEqualityGuaranteed": true,
  "persistenceContextManaged": true,
  "explanation": "Inside a @Transactional method, Hibernate's First-Level Cache intercepts subsequent findById calls for the same entity ID. It returns the exact same object reference in memory without issuing a second SQL SELECT."
}
```

### 2. Demonstrate Dirty Checking (Auto UPDATE without save())
```bash
curl -X POST http://localhost:8080/api/diagnostic/dirty-checking
```
**Response:**
```json
{
  "diagnostic": "Dirty Checking & Automatic Flush",
  "vehicleId": 1,
  "oldMileage": 120000,
  "newMileage": 120350,
  "explicitSaveCalled": false,
  "dirtyCheckingTriggered": true,
  "explanation": "Hibernate takes a snapshot of the entity when it is loaded. At flush time (commit), it compares the current state with the snapshot. Because 'mileage' changed, Hibernate emits: UPDATE vehicles SET mileage=?, version=version+1 WHERE id=? AND version=?"
}
```

### 3. Dynamic Search with Criteria API
```bash
curl -X POST http://localhost:8080/api/maintenance/search \
  -H "Content-Type: application/json" \
  -d '{
    "status": "IN_PROGRESS",
    "priority": "CRITICAL"
  }'
```

### 4. Bulk Telemetry Ingestion Benchmark
```bash
curl -X POST "http://localhost:8080/api/telemetry/bulk-seed?total=1000&batchSize=50"
```

---

## 📄 License
This project is open-sourced under the MIT License.

