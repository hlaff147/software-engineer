# 🌐 Wallet API – cURL Examples

All examples assume the API is running on `http://localhost:8080`.

## Check health
```bash
curl http://localhost:8080/actuator/health
```

## Create wallet
```bash
curl -X POST http://localhost:8080/api/v1/wallets \
  -H "Content-Type: application/json" \
  -d '{"userId":"user123","currency":"BRL"}'
```

## Deposit
```bash
curl -X POST http://localhost:8080/api/v1/wallets/{id}/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":1000,"metadata":{"source":"PIX"}}'
```

## Withdraw
```bash
curl -X POST http://localhost:8080/api/v1/wallets/{id}/withdraw \
  -H "Content-Type: application/json" \
  -d '{"amount":500}'
```

## Transfer
```bash
curl -X POST http://localhost:8080/api/v1/transfers \
  -H "Content-Type: application/json" \
  -d '{"sourceWalletId":"ID1","targetWalletId":"ID2","amount":200}'
```

## Get ledger
```bash
curl http://localhost:8080/api/v1/wallets/{id}/ledger
```

## Error example – insufficient funds
```bash
curl -i -X POST http://localhost:8080/api/v1/wallets/{id}/withdraw \
  -H "Content-Type: application/json" \
  -d '{"amount":999999}'
```
