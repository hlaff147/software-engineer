# 🏦 Open Finance Brasil — Payment Initiation Microservices

> Production-ready microservices implementation of the **Open Finance Brasil Payment Initiation API (v5.0.0-beta.1)** following the **Account Holder (Detentora de Conta)** specification.

---

## 🏗️ Microservices Architecture

The platform is decomposed into three decoupled modules:

```
┌───────────────────────────────────────────────────────────┐
│                    open-finance-common                    │
│   (Shared DTOs, Enums, Error Handlers, Domain Exceptions) │
└─────────────────────────────┬─────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    ┌───────────────────┐           ┌───────────────────┐
    │   open-finance-   │           │   open-finance-   │
    │      consent      │           │      payment      │
    │    (Port 8081)    │           │    (Port 8082)    │
    └───────────────────┘           └───────────────────┘
              ▲                               │
              │         Feign Client          │
              └───────────────────────────────┘
```

---

## 📦 Modules Description

| Module | Port | Technology | Purpose |
|--------|------|------------|---------|
| [`open-finance-common`](./open-finance-common) | Library | Java 17, Spring Boot | Shared domain models, Open Finance enums, standard RFC 7807 error responses. |
| [`open-finance-consent`](./open-finance-consent) | `8081` | Spring Boot 3, MongoDB | Manages user consent lifecycle (`AWAITING_AUTHORISATION`, `AUTHORISED`, `REJECTED`, `REVOKED`), JWT signature validation. |
| [`open-finance-payment`](./open-finance-payment) | `8082` | Spring Boot 3, Feign, MongoDB | Payment initiation endpoint (`/pix/payments`), validates consent via Feign Client with Consent service before executing PIX transfer. |

---

## 📡 API Endpoints Summary

### Consent Service (Port 8081)
- `POST /open-banking/payments/v5/consents` — Create payment consent
- `GET /open-banking/payments/v5/consents/{consentId}` — Get consent status
- `DELETE /open-banking/payments/v5/consents/{consentId}` — Revoke consent

### Payment Service (Port 8082)
- `POST /open-banking/payments/v5/pix/payments` — Initiate PIX payment
- `GET /open-banking/payments/v5/pix/payments/{paymentId}` — Query payment status

---

## 🚀 How to Build and Run

### Prerequisites
- JDK 17+
- Maven 3.9+
- MongoDB (or embedded test container)

### 1. Build and install common library
```bash
cd open-finance/open-finance-common
mvn clean install
```

### 2. Run Consent Microservice
```bash
cd ../open-finance-consent
mvn clean spring-boot:run
```

### 3. Run Payment Microservice
```bash
cd ../open-finance-payment
mvn clean spring-boot:run
```
