# 📊 Technical Documentation

This folder contains diagrams and complementary technical material for the Wallet API.

## Files
- **[architecture.puml](architecture.puml)** – PlantUML diagram of the layered architecture

## Viewing the diagram
### Option 1: Online
1. Copy the contents of `architecture.puml`
2. Open https://www.plantuml.com/plantuml/
3. Paste the code and click *Submit*

### Option 2: VS Code
1. Install the "PlantUML" extension
2. Open `architecture.puml`
3. Press `Ctrl+Shift+P` → "PlantUML: Preview Current Diagram"

### Option 3: Local PlantUML
```bash
brew install plantuml
plantuml docs/architecture.puml     # PNG
plantuml -tsvg docs/architecture.puml  # SVG
```

### Option 4: Docker
```bash
docker run --rm -v $(pwd):/data plantuml/plantuml:latest \
  -tpng /data/docs/architecture.puml
```
The image will be saved as `architecture.png`.

## Architecture overview
The diagram depicts the main layers of the system:
1. **Controllers** – REST endpoints
2. **DTOs** – Data transfer objects
3. **Services** – Business rules
4. **Mappers** – Conversion between DTOs and models
5. **Models** – Domain entities
6. **Repositories** – Data access
7. **Enums** – Enumerated types
8. **Exceptions** – Error handling
9. **Utils** – Helper classes

## Development tools
Recommended IDE plugins:
- PlantUML
- Java Extension Pack / Spring Boot tools
- MongoDB visualization plugin

## Testing strategy
The project follows a testing pyramid with unit, integration and web tests. See [TESTING.md](../TESTING.md) for details.
