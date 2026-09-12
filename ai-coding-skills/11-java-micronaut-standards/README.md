# 🚀 Java & Micronaut 4+ Standards

> **Enforces Ahead-of-Time (AOT) compilation idioms, reflection-free dependency injection, compile-time Micronaut Data JPA, and GraalVM native image readiness.**

---

## 🎯 The Problem

When working on **Micronaut** applications, AI coding assistants routinely default to **Spring Boot habits**:
1. **Hallucinating Spring annotations**: Inadvertently importing `org.springframework.stereotype.Service`, `@Autowired`, or `@RestController`, causing compilation failures.
2. **Field Injection Anti-Pattern**: Injecting dependencies on private fields with `@Inject` instead of constructor injection, violating immutability and testability.
3. **Runtime Reflection Pitfalls**: Generating code that relies on dynamic proxies, reflection, or runtime bytecode manipulation, which completely breaks **GraalVM Native Image** compilation.
4. **N+1 Query Explosions**: Generating standard JPA entity associations without Micronaut Data's compile-time `@Join(type = Join.Type.FETCH)` directives.
5. **Event Loop Starvation**: Running blocking JDBC database calls on Netty's reactive event loop threads without offloading.

---

## ✅ The Solution

This skill guides the AI assistant to adopt **Micronaut 4 native idioms**:
- Reflection-free dependency injection with `jakarta.inject.Singleton` and explicit constructor injection.
- Ahead-of-Time (AOT) annotation processing with `micronaut-inject-java`.
- Compile-time AST-validated query methods with Micronaut Data JPA.
- Declarative `@Join` fetching to eliminate N+1 queries.
- Java Records and `@Introspected` / `@Serdeable` DTOs for zero-reflection JSON serialization.
- Java 21+ Virtual Threads integration (`thread-selection: AUTO`).

---

## ⚖️ Bad vs Good Code Examples

### 1. Spring Habits vs Micronaut Native Controller

❌ **BAD (Spring annotations in Micronaut)**
```java
package com.example.controller;

import org.springframework.web.bind.annotation.*; // ❌ Spring imports break Micronaut
import org.springframework.beans.factory.annotation.Autowired;

@RestController
@RequestMapping("/api/assets")
public class AssetController {

    @Autowired // ❌ Field injection
    private AssetService assetService;

    @PostMapping
    public Asset createAsset(@RequestBody Asset asset) {
        return assetService.save(asset);
    }
}
```

✅ **GOOD (Micronaut 4 Native Controller)**
```java
package com.example.controller;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Post;
import jakarta.validation.Valid;

@Controller("/api/assets")
public class AssetController {

    private final AssetService assetService; // ✅ final immutable dependency

    public AssetController(AssetService assetService) { // ✅ Constructor injection
        this.assetService = assetService;
    }

    @Post
    public HttpResponse<AssetDTO> createAsset(@Valid @Body CreateAssetRequest request) {
        AssetDTO created = assetService.create(request);
        return HttpResponse.created(created); // ✅ Semantic HTTP response
    }
}
```

---

### 2. N+1 Queries vs Declarative Compile-Time Fetching

❌ **BAD (N+1 queries with runtime lazy loading)**
```java
@Repository
public interface AssetRepository extends JpaRepository<Asset, Long> {
    // ❌ Accessing asset.getOperator() later triggers separate SELECT query per entity
    List<Asset> findByStatus(AssetStatus status);
}
```

✅ **GOOD (Declarative `@Join` compile-time FETCH)**
```java
@Repository
public interface AssetRepository extends JpaRepository<Asset, Long> {

    // ✅ Forces compile-time INNER JOIN FETCH in generated SQL
    @Join(value = "operator", type = Join.Type.FETCH)
    @Join(value = "maintenanceSchedules", type = Join.Type.LEFT_FETCH)
    List<Asset> findByStatus(AssetStatus status);

    // ✅ Constructor-expression projection with Java text blocks
    @Query("""
        SELECT new com.example.dto.AssetSummaryDTO(a.id, a.code, a.name, o.name)
        FROM Asset a LEFT JOIN a.operator o
        WHERE a.status = :status
    """)
    List<AssetSummaryDTO> findSummaries(AssetStatus status);
}
```

---

### 3. Reflection DTOs vs Compile-Time Introspection

❌ **BAD (POJO requiring runtime reflection for JSON)**
```java
// ❌ Jackson needs runtime reflection to serialize this, failing in GraalVM native images
public class AssetDTO {
    private Long id;
    private String name;
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

✅ **GOOD (Java Record or `@Introspected` class)**
```java
// ✅ Java Record generates compile-time reflection-free serde metadata
public record AssetDTO(Long id, String name, String code) {}

// OR for mutable classes:
@Introspected // ✅ Generates BeanIntrospection at compile time
public class MutableAssetDTO {
    private Long id;
    private String name;
    // getters/setters
}
```

---

## 📐 Anatomy of the Skill

```
11-java-micronaut-standards/
├── SKILL.md                  # Gemini / Antigravity format (.agents/skills/)
├── .cursorrules              # Cursor scoped rule (globs: ["**/*.java", "**/application*.yml"])
├── copilot-instructions.md   # GitHub Copilot format (.github/copilot-instructions.md)
└── README.md                 # This didactic guide
```

---

## 🔧 How to Install

### Option 1: In Cursor (`.cursor/rules/`)
```bash
mkdir -p .cursor/rules
cp ai-coding-skills/11-java-micronaut-standards/.cursorrules .cursor/rules/micronaut-standards.mdc
```

### Option 2: In GitHub Copilot
```bash
cat ai-coding-skills/11-java-micronaut-standards/copilot-instructions.md >> .github/copilot-instructions.md
```

### Option 3: In Windsurf (Codeium)
```bash
cat ai-coding-skills/11-java-micronaut-standards/.cursorrules >> .windsurfrules
```

### Option 4: In Gemini / Antigravity
```bash
mkdir -p .agents/skills/java-micronaut-standards
cp ai-coding-skills/11-java-micronaut-standards/SKILL.md .agents/skills/java-micronaut-standards/
```

---

## 📊 Expected Impact

| Metric | Without Skill | With Skill |
|---|---|---|
| **Build Success Rate** | ❌ Frequent compilation errors from Spring imports | ✅ 100% Micronaut 4 compile-ready code |
| **GraalVM Native Image** | ⚠️ Fails due to un-introspected reflection | ✅ 100% Native Image AOT compatible |
| **Database Performance** | ⚠️ N+1 queries on nested associations | ⚡ Zero N+1 via declarative `@Join(type = FETCH)` |
| **Event Loop Health** | ⚠️ Blocking I/O on Netty threads | 🚀 Automatically offloaded to Virtual Threads |

---

## 🔗 References

- [Micronaut Framework Official Documentation](https://docs.micronaut.io/latest/guide/)
- [Micronaut Data JPA Guide](https://micronaut-projects.github.io/micronaut-data/latest/guide/)
- [Local Project Reference: `micronaut-jpa-masterclass`](../../micronaut-jpa-masterclass/README.md) (Global fleet management masterclass mastering the 6 pillars of JPA in this repository)
