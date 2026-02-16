# Wallet API – Quick Guide

## Running
```bash
./mvnw spring-boot:run
```
Base URL: `http://localhost:8080`
Swagger UI: `http://localhost:8080/swagger-ui.html`

## Endpoints
### Create wallet
```bash
curl -X POST http://localhost:8080/api/v1/wallets \
  -H "Content-Type: application/json" \
  -d '{"userId":"user123","currency":"BRL"}'
```

### Get current balance
```bash
curl http://localhost:8080/api/v1/wallets/{id}/balance
```

### Get historical balance
```bash
curl http://localhost:8080/api/v1/wallets/{id}/balance?at=2024-01-15T10:30:00Z
```

### Deposit
```bash
curl -X POST http://localhost:8080/api/v1/wallets/{id}/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":10000}'
```

### Withdraw
```bash
curl -X POST http://localhost:8080/api/v1/wallets/{id}/withdraw \
  -H "Content-Type: application/json" \
  -d '{"amount":5000}'
```

### Transfer
```bash
curl -X POST http://localhost:8080/api/v1/transfers \
  -H "Content-Type: application/json" \
  -d '{"sourceWalletId":"...","targetWalletId":"...","amount":2000}'
```

### List ledger entries
```bash
curl http://localhost:8080/api/v1/wallets/{id}/ledger
```
Each response contains the resulting balance and a timestamp so balances can be reconstructed at any point in time.
