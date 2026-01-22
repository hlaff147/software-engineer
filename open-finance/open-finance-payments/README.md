# Open Finance Payments API

## Overview
Implementação da API de Iniciação de Pagamentos do Open Finance Brasil v5.0.0-beta.1 como Detentora de Conta.

## Quick Start

### 1. Start MongoDB
```bash
docker-compose up -d
```

### 2. Run Application
```bash
./mvnw spring-boot:run
```

### 3. Access Swagger UI
Open: http://localhost:8080/open-banking/payments/v5/swagger-ui.html

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/consents` | Create consent |
| GET | `/consents/{consentId}` | Get consent |
| POST | `/pix/payments` | Create Pix payment |
| GET | `/pix/payments/{paymentId}` | Get payment |
| PATCH | `/pix/payments/{paymentId}` | Cancel payment |
| GET | `/consents/{consentId}/pix/payments` | List payments by consent |

## Test Commands

### Create Consent
```bash
curl -X POST http://localhost:8080/open-banking/payments/v5/consents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer test-token" \
  -H "x-fapi-interaction-id: $(uuidgen)" \
  -H "x-idempotency-key: test-consent-001" \
  -d '{
    "data": {
      "loggedUser": {
        "document": {"identification": "11111111111", "rel": "CPF"}
      },
      "creditor": {
        "personType": "PESSOA_NATURAL",
        "cpfCnpj": "11111111111",
        "name": "Marco Antonio"
      },
      "payment": {
        "type": "PIX",
        "date": "2026-01-10",
        "currency": "BRL",
        "amount": "100.00",
        "details": {
          "localInstrument": "DICT",
          "proxy": "11111111111",
          "creditorAccount": {
            "ispb": "12345678",
            "number": "1234567890",
            "accountType": "CACC"
          }
        }
      }
    }
  }'
```

### Get Consent
```bash
curl http://localhost:8080/open-banking/payments/v5/consents/{consentId} \
  -H "Authorization: Bearer test-token" \
  -H "x-fapi-interaction-id: $(uuidgen)"
```

## Architecture

- **Hexagonal Architecture** with domain, application, and adapter layers
- **Strategy + Factory Pattern** for API versioning
- **MongoDB** for persistence
- **Mocked external services** (DICT, SPI)
