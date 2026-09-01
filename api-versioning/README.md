# 🔌 API Versioning with Strategy + Factory Pattern

> Demonstrating clean, URL-based REST API versioning in Spring Boot using the **Strategy and Factory design patterns** combined with Spring's dynamic `Map<String, Strategy>` bean injection.

---

## 🎯 Overview & Architecture

When APIs evolve with breaking contract changes, handling multiple active versions without duplicating boilerplate or introducing messy `if/else` checks is a major architectural challenge.

This project implements a version-routed architecture where a dynamic factory selects the appropriate strategy based on the URL path version token (`/api/v{version}/payments`).

```
                ┌────────────────────────┐
                │   PaymentController    │
                │  /api/v{version}/...   │
                └───────────┬────────────┘
                            │
                ┌───────────▼────────────┐
                │ PaymentServiceFactory  │
                │ Map<String, Strategy>  │
                └───────────┬────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    ┌───────────────┐               ┌───────────────┐
    │ PaymentV1_0_0 │               │ PaymentV2_0_0 │
    │   Strategy    │               │   Strategy    │
    └───────────────┘               └───────────────┘
```

---

## 💡 Key Design Patterns

| Pattern | Role | Implementation |
|---------|------|----------------|
| **Strategy** | Encapsulate version-specific payment business logic | `PaymentStrategy` interface with `PaymentStrategyV1` & `PaymentStrategyV2` |
| **Factory** | Resolve strategy dynamically at runtime | `PaymentServiceFactory` mapping version strings to bean names |
| **SPI (Spring Auto-Injection)** | Auto-discover strategy beans | Spring automatically injects all `PaymentStrategy` implementations into a `Map<String, PaymentStrategy>` |

```java
// Spring auto-injects all strategies into the map keyed by bean name:
@Service
public class PaymentServiceFactory {
    private final Map<String, PaymentStrategy> strategies;

    public PaymentStrategy getStrategy(String version) {
        String beanName = "Payment_" + version.replace('.', '_');
        PaymentStrategy strategy = strategies.get(beanName);
        if (strategy == null) {
            throw new UnsupportedVersionException("Version " + version + " is not supported");
        }
        return strategy;
    }
}
```

---

## 📡 API Endpoints & Request Payloads

### Version 1.0.0 (`/api/v1_0_0/payments`)
```bash
curl -X POST http://localhost:8080/api/v1_0_0/payments \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "currency": "BRL",
    "recipient": "user-123"
  }'
```

### Version 2.0.0 (`/api/v2_0_0/payments`)
Introduces mandatory idempotency key and structured payment method:
```bash
curl -X POST http://localhost:8080/api/v2_0_0/payments \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 100.50,
    "currency": "BRL",
    "recipient": "user-123",
    "idempotencyKey": "a9b8c7d6-e5f4",
    "paymentMethod": "PIX"
  }'
```

---

## 🚀 How to Build and Run

### Prerequisites
- JDK 17+
- Maven 3.9+

### Build and Run Application
```bash
cd api-versioning
mvn clean spring-boot:run
```

### Run Tests
```bash
mvn test
```
