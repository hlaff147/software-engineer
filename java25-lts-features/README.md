# ⚡ Java 25 & Java 21 LTS Features

> **Mini projeto clean demonstrando as novidades do Java 25 (com foco no `ScopedValue`) e os destaques da versão LTS anterior (Java 21).**

---

## 📌 Principais Recursos Demonstrados

### 1. ⚡ Java 25: `ScopedValue` vs `ThreadLocal`
O `ScopedValue` substitui o antigo `ThreadLocal` com uma filosofia imutável e vinculada ao escopo de execução:

| Característica | `ThreadLocal` (Legado) | `ScopedValue` (Java 25) |
| :--- | :--- | :--- |
| **Mutabilidade** | Mutável em qualquer ponto (`set()`) | **Imutável** após o vínculo do escopo |
| **Ciclo de Vida** | Manual (Risco de *Memory Leak* se esquecer `.remove()`) | **Limpeza Automática** ao sair do bloco `run`/`call` |
| **Sub-escopos** | Altera valor global da thread | **Rebind (Shadowing)** isolado no sub-escopo |
| **Virtual Threads** | Overhead de cópia de mapa | **Leve e ultra-eficiente** |

---

### 2. 🚀 Java 25: Flexible Constructor Bodies (JEP 492)
Permite executar validações, logs e pré-processamentos de argumentos **antes** de invocar o `super(...)` ou `this(...)` no construtor de sub-classes.

---

### 3. ☕ Java 21 LTS (Versão LTS Anterior)
- **Virtual Threads (JEP 444):** Threads leves nativas da JVM para concorrência maciça.
- **Pattern Matching para `switch` & Record Patterns (JEP 440/441):** Desestruturação declarativa de records no `switch`.
- **Sequenced Collections (JEP 431):** Métodos universais `getFirst()`, `getLast()`, `reversed()` para coleções ordenadas.

---

### 4. 🧵 Estudo Aprofundado: Concorrência Estruturada (Java vs. Kotlin)
- [📖 Concorrência Estruturada na Prática: Eliminando Threads Fantasmas (Java vs. Kotlin)](./docs/STRUCTURED_CONCURRENCY_JAVA_VS_KOTLIN.md) — Análise aprofundada de alta volumetria comparando Java 21+ (`StructuredTaskScope`) e Kotlin (`coroutineScope`), tratamento de falhas rápidas (*fail-fast*) e benchmark de eficiência de recursos.

---

## 🚀 Como Compilar e Executar

### Pré-requisitos
- JDK 21+ instalado.

### 1. Execução via Maven (Recomendado)

```bash
cd java25-lts-features
mvn clean compile exec:java
```

### 2. Execução Direta via Terminal (CLI)

```bash
cd java25-lts-features
javac --enable-preview -d target/classes src/main/java/com/portfolio/java25/**/*.java src/main/java/com/portfolio/java25/*.java
java --enable-preview -cp target/classes com.portfolio.java25.Main
```
