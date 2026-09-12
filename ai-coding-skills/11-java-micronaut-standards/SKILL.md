---
name: java-micronaut-standards
description: >-
  Enforces modern Java 21+ and Micronaut 4+ idiomatic standards, Ahead-of-Time (AOT) compilation,
  reflection-free dependency injection, compile-time Micronaut Data repositories, GraalVM native
  readiness, and @MicronautTest patterns. Activate when writing, reviewing, or generating Micronaut code.
---

# 🚀 Java & Micronaut 4+ Standards

Enforces Ahead-of-Time (AOT) compilation idioms, reflection-free dependency injection, compile-time Micronaut Data JPA practices, and GraalVM native image compatibility.

---

## 🚫 Critical Negative Constraints (Anti-Patterns)

- **NEVER import Spring Framework classes**: Ban `org.springframework.*` (`@Service`, `@Autowired`, `@Component`, `@RestController`).
- **NEVER use field injection**: Ban `@Inject` or `@Autowired` on private instance variables.
- **NEVER use legacy Java EE namespaces**: Ban `javax.*` imports — use `jakarta.*` (`jakarta.inject.*`, `jakarta.persistence.*`, `jakarta.validation.*`).
- **NEVER block the Netty event loop**: Offload blocking I/O (JDBC, HTTP calls) with `@ExecuteOn(TaskExecutors.BLOCKING)` or Java 21+ Virtual Threads.
- **NEVER use dynamic reflection or runtime bytecode generation**: Ban runtime reflection, `java.lang.reflect.Proxy`, or CGLIB-style proxies. Everything must be discoverable at compile-time for GraalVM Native Image compatibility.
- **NEVER return `null` for query results**: Return `Optional<T>` for single entities or immutable collections (`List.of()`, `Set.of()`).

---

## 🧩 1. Dependency Injection & Ahead-of-Time (AOT) Architecture

- **Constructor Injection**: Inject dependencies exclusively via explicit constructors with `final` fields.
  ```java
  @Singleton
  public class FleetService {
      private final AssetRepository assetRepository;

      public FleetService(AssetRepository assetRepository) {
          this.assetRepository = assetRepository;
      }
  }
  ```
- **Jakarta Scopes**: Use `jakarta.inject.Singleton` as default bean scope. Use `@Prototype` or `@RequestScope` only when state dictates.
- **Factory Beans**: Use `@Factory` classes with `@Singleton` producer methods for external library beans.
- **Conditional Beans**: Use `@Requires(property = "feature.enabled", value = "true")` or `@Requires(env = "dev")` for conditional wiring.

---

## 🌐 2. HTTP Controllers & Routing

- **Controller Definition**: Use `@Controller("/api/v1/resource")` from `io.micronaut.http.annotation.Controller`.
- **HTTP Responses**: Return `io.micronaut.http.HttpResponse<T>` with explicit status codes (`HttpResponse.ok()`, `HttpResponse.created()`, `HttpResponse.noContent()`).
  ```java
  @Controller("/api/assets")
  public class AssetController {
      private final AssetService assetService;

      public AssetController(AssetService assetService) {
          this.assetService = assetService;
      }

      @Post("/vehicles")
      public HttpResponse<VehicleDTO> registerVehicle(@Valid @Body CreateVehicleRequest request) {
          VehicleDTO created = assetService.create(request);
          return HttpResponse.created(created);
      }

      @Get("/{id}")
      public HttpResponse<AssetDTO> getById(@PathVariable Long id) {
          return assetService.findById(id)
              .map(HttpResponse::ok)
              .orElseGet(HttpResponse::notFound);
      }
  }
  ```
- **DTOs & Serialization**: Use Java Records for DTOs. For POJOs, annotate with `@Introspected` or `@Serdeable` to generate compile-time reflection-free serializers.
- **Input Validation**: Annotate request payloads with `@Valid` and Jakarta validation annotations (`@NotNull`, `@Size`, `@NotBlank`, `@Positive`).

---

## 🗄️ 3. Micronaut Data JPA & Repository Layer

- **Declarative Interfaces**: Extend `io.micronaut.data.jpa.repository.JpaRepository<Entity, ID>` or `CrudRepository<Entity, ID>` annotated with `@Repository`.
- **Compile-Time Queries**: Leverage method name conventions (`findByStatusAndCreatedAtAfter`) which are validated during `javac` compilation.
- **N+1 Prevention with Declarative Fetching**: Use `@Join` annotations instead of runtime entity graphs:
  ```java
  @Repository
  public interface AssetRepository extends JpaRepository<Asset, Long> {

      // Prevents N+1 by forcing compile-time INNER JOIN FETCH
      @Join(value = "operator", type = Join.Type.FETCH)
      @Join(value = "maintenanceSchedules", type = Join.Type.LEFT_FETCH)
      Optional<Asset> findWithDetailsById(Long id);

      // Constructor-expression projection with Java text blocks
      @Query("""
          SELECT new com.portfolio.fleet.dto.AssetSummaryDTO(
              a.id, a.assetCode, a.name, a.status, o.name
          )
          FROM Asset a
          LEFT JOIN a.operator o
          WHERE a.status = :status
      """)
      List<AssetSummaryDTO> findSummariesByStatus(AssetStatus status);
  }
  ```
- **Transactions**: Annotate methods or classes with `jakarta.transaction.Transactional`. Use `@Transactional(readOnly = true)` on query methods.

---

## ⚡ 4. Virtual Threads & Concurrency (Java 21+)

- **Virtual Thread Offloading**: In Micronaut 4+, configure virtual threads or annotate blocking controllers/services with `@ExecuteOn(TaskExecutors.BLOCKING)`.
- **Application Configuration (`application.yml`)**:
  ```yaml
  micronaut:
    application:
      name: fleet-management
    server:
      port: 8080
      thread-selection: AUTO # Enables Virtual Threads when running on Java 21+
  ```

---

## 🧪 5. Testing with `@MicronautTest`

- **Test Harness**: Use `@MicronautTest` from `io.micronaut.test.extensions.junit5.annotation.MicronautTest`.
- **Injection in Tests**: Inject beans directly into test constructor, test method arguments, or test fields with `@Inject`.
- **Assertion Standards**: Use AssertJ (`assertThat(...)`).
  ```java
  @MicronautTest
  class AssetControllerTest {

      @Inject
      @Client("/api/assets")
      HttpClient client;

      @Test
      void should_ReturnCreated_When_VehicleRequestIsValid() {
          var request = HttpRequest.POST("/vehicles", new CreateVehicleRequest("TRK-01", "Volvo FH"));
          var response = client.toBlocking().exchange(request, VehicleDTO.class);

          assertThat(response.getStatus()).isEqualTo(HttpStatus.CREATED);
          assertThat(response.body()).isNotNull();
          assertThat(response.body().assetCode()).isEqualTo("TRK-01");
      }
  }
  ```

---

## 🔄 Verification Commands

Before completing tasks on a Micronaut project, verify:
- **Compile & AOT check**: `./gradlew compileJava` or `mvn compile` (verifies annotation processors pass)
- **Unit & Integration tests**: `./gradlew test` or `mvn test`
- **Check for banned imports**:
  ```bash
  ! grep -rn "org.springframework" src/
  ! grep -rn "javax.persistence" src/
  ```
