# Java Spring Boot 3 Standards

Enforces modern Java 21+ and Spring Boot 3 idiomatic standards. Activate when writing or reviewing Java/Spring Boot code.

## 🎯 Problem
Older Java versions and outdated Spring Boot practices lead to boilerplate code, poor encapsulation, and legacy dependencies.

## ✅ Solution
Use modern language features and Spring Boot 3 constructs.

### Examples

**BAD: POJO with getters/setters**
```java
public class UserDto {
    private String name;
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}
```

**GOOD: Record**
```java
public record UserDto(String name) {}
```

**BAD: @Autowired field**
```java
@Service
public class UserService {
    @Autowired
    private UserRepository repository;
}
```

**GOOD: Constructor injection**
```java
@Service
@RequiredArgsConstructor
public class UserService {
    private final UserRepository repository;
}
```

**BAD: javax.persistence**
```java
import javax.persistence.Entity;
```

**GOOD: jakarta.persistence**
```java
import jakarta.persistence.Entity;
```

**BAD: return null**
```java
public User findUser(Long id) {
    return repository.findById(id).orElse(null);
}
```

**GOOD: return Optional.empty()**
```java
public Optional<User> findUser(Long id) {
    return repository.findById(id);
}
```

## 📐 Anatomy of the skill
This skill updates practices to Java 21 and Spring Boot 3, enforcing immutability (Records, Collections), safe dependency injection, robust error handling, modern API namespaces, and efficient concurrency (Virtual Threads).

## 🔧 How to install

### Cursor
Copy `.cursorrules` to the root of your repository.

### GitHub Copilot
Copy `copilot-instructions.md` to `.github/copilot-instructions.md`.

### Windsurf / Gemini
Use `SKILL.md` in your AI coding skills or custom instructions directory.

## 📊 Expected impact
- Reduced boilerplate
- Fewer null pointer exceptions
- Safe multithreading with virtual threads
- Seamless migration to future Spring/Java versions

## 🔗 References
- [Spring Boot Documentation](https://spring.io/projects/spring-boot)
- [cursor.directory/java-spring-boot](https://cursor.directory/)
