# 💳 Wallet API

A production-ready REST service for managing digital wallets. The service allows clients to create wallets, deposit funds, withdraw funds and transfer money between users while keeping a full audit trail.

![Java](https://img.shields.io/badge/Java-17+-orange.svg)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.0+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-5.0+-darkgreen.svg)
![Maven](https://img.shields.io/badge/Maven-3.6+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

## ✨ Features
- Layered architecture with services, controllers, mappers and repositories
- Full auditing of all financial operations
- Support for multiple currencies (BRL, USD, EUR)
- Comprehensive test suite (unit, integration and web)
- Interactive documentation with OpenAPI/Swagger

## 🚀 Quick Start
### Run with Docker (recommended)
```bash
./start.sh
```
The API will be available at http://localhost:8080 and Swagger UI at http://localhost:8080/swagger-ui.html.

### Local development
Requires Java 17, MongoDB 5 and Maven 3.
```bash
./mvnw spring-boot:run
```

## 🏗️ Architecture
The project follows a classic layered architecture:
```
HTTP -> Controller -> Service -> Mapper -> Repository -> MongoDB
            ↕            ↕
          DTOs          Domain
```
A sequence of ledger entries keeps an immutable history of all wallet operations, allowing historical balance queries.

## 🔧 Configuration
The default configuration is located in `src/main/resources/application.yml`. Environment variables such as `MONGODB_URI` and `SERVER_PORT` can override defaults.

## 🧪 Tests
Run the full test suite with:
```bash
./mvnw test
```

## 📖 Additional Documentation
- [Docker guide](DOCKER.md)
- [API reference](API.md)
- [cURL examples](CURL_EXAMPLES.md)
- [Project overview](PROJECT_OVERVIEW.md)
- [Testing strategy](TESTING.md)
- [Technical docs & diagrams](docs/README.md)

## 📈 Future Improvements
Planned enhancements include transactional support in MongoDB, idempotency, balance snapshots and Redis caching.

## 📝 License
Released under the [MIT License](LICENSE).
