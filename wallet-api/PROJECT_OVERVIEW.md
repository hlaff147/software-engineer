# 🎯 Project Overview – Wallet API

## Summary
The Wallet API is a Java Spring Boot application for managing digital wallets. It provides a layered architecture, full audit logging, extensive tests and ready-to-use Docker support.

## Repository structure
```
wallet-api/
├── README.md             # Main documentation
├── DOCKER.md             # Docker guide
├── CURL_EXAMPLES.md      # cURL usage examples
├── PROJECT_OVERVIEW.md   # This file
├── TESTING.md            # Testing guide
├── API.md                # API quick reference
├── docs/                 # Technical docs and diagrams
├── docker-compose.yml
├── Dockerfile
├── start.sh / stop.sh
└── src/                  # Application source code
```

## Main technologies
- Java 17
- Spring Boot 3
- MongoDB 5
- Maven
- Docker / Docker Compose

## Key capabilities
- Create wallets for users
- Deposit, withdraw and transfer funds
- Retrieve current or historical balances
- Full ledger of operations for audit purposes

For setup and detailed instructions see [README.md](README.md).
