# Testing Guide – Wallet API

## Structure
Tests are organized across several layers to ensure high coverage:
```
src/test/java/com/hlaff/wallet_api/
├── service/             # Service unit tests
├── controller/          # Web layer tests with MockMvc
├── repository/          # Integration tests using Testcontainers
└── mapper/              # Mapper unit tests
```

## Running tests
```bash
./mvnw test
```
This command runs unit, integration and web tests. Testcontainers automatically starts MongoDB for repository tests.

## Testing strategy
The project follows a classic testing pyramid:
```
        E2E tests (few)
    -------------------------
    Integration tests (some)
---------------------------------
Unit tests (many)
```
- **Unit tests** validate business logic in isolation.
- **Integration tests** check repository behaviour with MongoDB.
- **Web tests** verify controllers using MockMvc.
