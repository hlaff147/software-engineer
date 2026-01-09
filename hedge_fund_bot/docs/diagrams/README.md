# UML Diagrams

This folder contains UML diagrams for the Autonomous Hedge Fund Bot architecture.

## Diagrams

| File | Type | Description |
|------|------|-------------|
| `state_diagram.png` | State Machine | Workflow states and transitions |
| `component_diagram.png` | Component Diagram | System components and connections |
| `activity_diagram.png` | Activity Diagram | Decision flow and activities |

### State Diagram
![State Diagram](state_diagram.png)

### Component Diagram
![Component Diagram](component_diagram.png)

### Activity Diagram
![Activity Diagram](activity_diagram.png)

## Regenerating Diagrams

The `.puml` source files are included. To regenerate PNG images:

```bash
# Install PlantUML
brew install plantuml  # macOS

# Generate PNG images
plantuml *.puml
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User Input → Supervisor → [Researcher|Chartist|Analyst]   │
│                    ↑                    │                    │
│                    └────────────────────┘                    │
│                                                              │
│   Supervisor: Routes workflow based on completed analysis    │
│   Researcher: Gathers news and sentiment data                │
│   Chartist:   Performs technical analysis (RSI, MACD, SMA)   │
│   Analyst:    Synthesizes final investment recommendation    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Patterns

1. **Supervisor Pattern**: Central orchestrator routes tasks to specialized agents
2. **State Machine**: Workflow follows defined state transitions
3. **Tool Augmentation**: Agents use specialized tools (yFinance, DuckDuckGo)
4. **Message Passing**: Agents communicate through shared state messages
