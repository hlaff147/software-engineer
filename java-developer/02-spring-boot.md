# Spring + Spring Boot Questions

## 11. How does dependency injection work in Spring Framework?

**Dependency Injection (DI)** inverts object creation - Spring creates and injects dependencies.

**Mechanism:**
1. Spring scans for components (`@Component`, `@Service`, `@Repository`)
2. Creates beans and stores in ApplicationContext
3. Injects dependencies via constructor, setter, or field

**Injection types:**
```java
// 1. Constructor injection (RECOMMENDED)
@Service
public class OrderService {
    private final PaymentService paymentService;
    
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}

// 2. Field injection (not recommended - hard to test)
@Service
public class OrderService {
    @Autowired
    private PaymentService paymentService;
}

// 3. Setter injection
@Service
public class OrderService {
    private PaymentService paymentService;
    
    @Autowired
    public void setPaymentService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

---

## 12. What is the role of @Configuration and @Bean annotations?

**`@Configuration`**: Marks a class as a source of bean definitions.

**`@Bean`**: Marks a method that returns an object to be managed by Spring.

```java
@Configuration
public class AppConfig {
    
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }
    
    @Bean
    @Profile("prod")  // Only in production
    public DataSource prodDataSource() {
        return new HikariDataSource(prodConfig());
    }
}
```

**Key points:**
- `@Configuration` uses CGLIB proxies to ensure singleton behavior
- `@Bean` methods can depend on other `@Bean` methods
- Useful for third-party library configuration

---

## 13. How do you configure application properties for multiple environments in Spring Boot?

**Use profile-specific property files:**

```
src/main/resources/
├── application.yml           # Common/default
├── application-dev.yml       # Development
├── application-staging.yml   # Staging
└── application-prod.yml      # Production
```

**application.yml:**
```yaml
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

server:
  port: 8080
```

**application-prod.yml:**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://prod-db:5432/app
    
logging:
  level:
    root: WARN
```

**Activate profiles:**
```bash
# Environment variable
export SPRING_PROFILES_ACTIVE=prod

# Command line
java -jar app.jar --spring.profiles.active=prod

# Kubernetes ConfigMap
env:
  - name: SPRING_PROFILES_ACTIVE
    value: "prod"
```

---

## 14. How do you secure Spring Boot REST APIs with JWT authentication?

**Implementation steps:**

```java
// 1. Add dependency
// spring-boot-starter-security + jjwt

// 2. JWT Utility
@Component
public class JwtUtil {
    @Value("${jwt.secret}")
    private String secret;
    
    public String generateToken(UserDetails user) {
        return Jwts.builder()
            .setSubject(user.getUsername())
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + 86400000))
            .signWith(Keys.hmacShaKeyFor(secret.getBytes()))
            .compact();
    }
    
    public String extractUsername(String token) {
        return Jwts.parserBuilder()
            .setSigningKey(secret.getBytes())
            .build()
            .parseClaimsJws(token)
            .getBody()
            .getSubject();
    }
}

// 3. JWT Filter
@Component
public class JwtFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
            HttpServletResponse response, FilterChain chain) {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            String token = header.substring(7);
            String username = jwtUtil.extractUsername(token);
            // Set authentication in SecurityContext
        }
        chain.doFilter(request, response);
    }
}

// 4. Security Config
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(sm -> sm.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/auth/**").permitAll()
                .anyRequest().authenticated())
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

---

## 15. Explain how Spring Boot manages embedded servers like Tomcat/Jetty.

**Auto-configuration:**
- `spring-boot-starter-web` includes Tomcat by default
- Spring Boot auto-configures and starts the server

**Switch servers:**
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <exclusions>
        <exclusion>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-tomcat</artifactId>
        </exclusion>
    </exclusions>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-jetty</artifactId>
</dependency>
```

**Customize server:**
```yaml
server:
  port: 8080
  tomcat:
    threads:
      max: 200
      min-spare: 10
    connection-timeout: 5000
    max-connections: 10000
```

```java
@Bean
public WebServerFactoryCustomizer<TomcatServletWebServerFactory> customizer() {
    return factory -> {
        factory.setPort(9090);
        factory.addConnectorCustomizers(connector -> 
            connector.setProperty("maxThreads", "500"));
    };
}
```

---

## 16. How does Spring Boot Actuator help with monitoring and metrics?

**Actuator** exposes operational endpoints for monitoring.

**Setup:**
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus,info
  endpoint:
    health:
      show-details: always
```

**Key endpoints:**

| Endpoint | Purpose |
|----------|---------|
| `/actuator/health` | Application health status |
| `/actuator/metrics` | JVM, HTTP, custom metrics |
| `/actuator/prometheus` | Prometheus-format metrics |
| `/actuator/info` | App info (version, git) |
| `/actuator/env` | Environment properties |

**Custom health indicator:**
```java
@Component
public class DatabaseHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        if (isDatabaseHealthy()) {
            return Health.up().withDetail("database", "responsive").build();
        }
        return Health.down().withDetail("error", "Connection failed").build();
    }
}
```

**Custom metrics:**
```java
@Service
public class OrderService {
    private final Counter orderCounter;
    
    public OrderService(MeterRegistry registry) {
        this.orderCounter = registry.counter("orders.created");
    }
    
    public void createOrder() {
        orderCounter.increment();
    }
}
```

---

## 17. How do you manage transaction propagation in Spring?

**`@Transactional`** propagation controls how transactions interact.

| Propagation | Behavior |
|-------------|----------|
| `REQUIRED` (default) | Join existing or create new |
| `REQUIRES_NEW` | Always create new (suspend existing) |
| `NESTED` | Nested transaction with savepoint |
| `SUPPORTS` | Use existing or run without |
| `MANDATORY` | Must have existing, else exception |
| `NOT_SUPPORTED` | Run without transaction |
| `NEVER` | Exception if transaction exists |

```java
@Service
public class OrderService {
    
    @Transactional  // REQUIRED by default
    public void processOrder(Order order) {
        saveOrder(order);
        paymentService.charge(order);  // Same transaction
    }
    
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void logAudit(String message) {
        // New transaction - commits even if parent rolls back
        auditRepository.save(new AuditLog(message));
    }
    
    @Transactional(
        propagation = Propagation.REQUIRED,
        isolation = Isolation.READ_COMMITTED,
        rollbackFor = Exception.class,
        timeout = 30
    )
    public void complexOperation() { }
}
```

---

## 18. What is the difference between @ControllerAdvice and @ExceptionHandler?

**`@ExceptionHandler`**: Handles exceptions in a single controller.

**`@ControllerAdvice`**: Global exception handling across all controllers.

```java
// Local - only for this controller
@RestController
public class UserController {
    
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<String> handleUserNotFound(UserNotFoundException ex) {
        return ResponseEntity.status(404).body(ex.getMessage());
    }
}

// Global - handles exceptions from ALL controllers
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(ResourceNotFoundException ex) {
        return ResponseEntity.status(404)
            .body(new ErrorResponse("NOT_FOUND", ex.getMessage()));
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        List<String> errors = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .toList();
        return ResponseEntity.badRequest()
            .body(new ErrorResponse("VALIDATION_ERROR", errors.toString()));
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleAll(Exception ex) {
        log.error("Unexpected error", ex);
        return ResponseEntity.status(500)
            .body(new ErrorResponse("INTERNAL_ERROR", "Something went wrong"));
    }
}
```

---

## 19. How do you enable asynchronous method execution in Spring Boot?

**Steps:**

```java
// 1. Enable async
@Configuration
@EnableAsync
public class AsyncConfig implements AsyncConfigurer {
    
    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.initialize();
        return executor;
    }
    
    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> log.error("Async error in {}", method, ex);
    }
}

// 2. Use @Async on methods
@Service
public class EmailService {
    
    @Async  // Runs in separate thread
    public void sendEmail(String to, String body) {
        // Long-running email sending
    }
    
    @Async
    public CompletableFuture<Report> generateReport(Long id) {
        Report report = // expensive operation
        return CompletableFuture.completedFuture(report);
    }
}

// 3. Call async methods
@RestController
public class ReportController {
    
    @GetMapping("/report/{id}")
    public CompletableFuture<Report> getReport(@PathVariable Long id) {
        return reportService.generateReport(id);  // Non-blocking
    }
}
```

**Note:** `@Async` only works when called from another bean (not same class).

---

## 20. How does Spring Boot integrate with cloud services (e.g., AWS S3, RDS)?

**AWS S3 Integration:**

```xml
<dependency>
    <groupId>software.amazon.awssdk</groupId>
    <artifactId>s3</artifactId>
</dependency>
```

```java
@Configuration
public class S3Config {
    @Bean
    public S3Client s3Client() {
        return S3Client.builder()
            .region(Region.US_EAST_1)
            .credentialsProvider(DefaultCredentialsProvider.create())
            .build();
    }
}

@Service
public class S3Service {
    private final S3Client s3Client;
    
    public void uploadFile(String bucket, String key, byte[] content) {
        s3Client.putObject(
            PutObjectRequest.builder().bucket(bucket).key(key).build(),
            RequestBody.fromBytes(content)
        );
    }
}
```

**AWS RDS (same as regular DB):**
```yaml
spring:
  datasource:
    url: jdbc:postgresql://mydb.xxx.rds.amazonaws.com:5432/mydb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
```

**Spring Cloud AWS:**
```yaml
# application.yml with Spring Cloud AWS
spring:
  cloud:
    aws:
      credentials:
        instance-profile: true  # Use IAM role
      region:
        static: us-east-1
      s3:
        bucket: my-bucket
```
