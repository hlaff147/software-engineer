# Java & Micronaut 4+ Standards for GitHub Copilot

Apply these architectural and coding standards to all Java and Micronaut development tasks:

## Core Architectural Guardrails
- **Ahead-of-Time (AOT) Focus**: Micronaut relies on compile-time annotation processing (`micronaut-inject-java`), eliminating runtime reflection and runtime bytecode generation. Code must be GraalVM Native Image friendly.
- **Zero Spring Framework**: NEVER generate Spring annotations (`@Service`, `@Autowired`, `@Component`, `@RestController`). Use Micronaut and Jakarta annotations.
- **Constructor Injection Only**: NEVER use field injection (`@Inject private Service s;`). Always generate explicit constructor injection with `final` fields.
- **Jakarta Namespace**: Use `jakarta.*` packages (`jakarta.inject.Singleton`, `jakarta.persistence.*`, `jakarta.transaction.Transactional`, `jakarta.validation.*`). Never import `javax.*`.

## HTTP Controllers & Serialization
- Use `@Controller("/path")` from `io.micronaut.http.annotation.Controller`.
- Return `io.micronaut.http.HttpResponse<T>` with semantic factory methods (`HttpResponse.ok()`, `HttpResponse.created()`, `HttpResponse.notFound()`, `HttpResponse.noContent()`).
- Use Java Records for DTOs. If creating class DTOs, annotate with `@Introspected` or `@Serdeable` for reflection-free JSON serialization.
- Validate request bodies with `jakarta.validation.Valid` alongside `@NotNull`, `@NotBlank`, `@Size`.

## Micronaut Data JPA
- Repositories must extend `io.micronaut.data.jpa.repository.JpaRepository<T, ID>` and be annotated with `@Repository`.
- Derive queries using method naming conventions which Micronaut compiles to SQL at build time.
- Prevent N+1 queries using declarative `@Join(value = "field", type = Join.Type.FETCH)` annotations.
- Write JPQL queries with Java Text Blocks (`"""`) using constructor-expression DTO projections.
- Apply `@Transactional(readOnly = true)` for read-only operations and `@Transactional` for state modifications.

## Concurrency & Virtual Threads
- Offload blocking operations with `@ExecuteOn(TaskExecutors.BLOCKING)`.
- Configure `micronaut.server.thread-selection: AUTO` to leverage Java 21+ Virtual Threads on Netty.
- Never block the Netty event loop directly with blocking database or network calls.

## Testing Guidelines
- Use `@MicronautTest` on JUnit 5 test classes.
- Use declarative HTTP client tests via `@Client("/api/...") HttpClient client`.
- Write assertions with AssertJ (`assertThat(...)`).

## Verification
- Always ensure generated code compiles with `./gradlew compileJava` or `mvn compile`.
- Ensure no `org.springframework.*` or `javax.*` imports are present.
