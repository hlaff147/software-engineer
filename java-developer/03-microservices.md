# Microservices Questions

## 21. How do you implement inter-service communication in microservices?

**Two main patterns:**

### Synchronous (HTTP/gRPC)

```java
// 1. RestTemplate (legacy)
@Bean
public RestTemplate restTemplate() {
    return new RestTemplate();
}

// 2. WebClient (reactive, preferred)
@Service
public class OrderService {
    private final WebClient webClient;
    
    public OrderService(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("http://user-service").build();
    }
    
    public Mono<User> getUser(Long id) {
        return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class);
    }
}

// 3. OpenFeign (declarative)
@FeignClient(name = "user-service")
public interface UserClient {
    @GetMapping("/users/{id}")
    User getUser(@PathVariable Long id);
}
```

### Asynchronous (Message Broker)

```java
// Kafka Producer
@Service
public class OrderEventPublisher {
    private final KafkaTemplate<String, OrderEvent> kafka;
    
    public void publishOrderCreated(Order order) {
        kafka.send("order-events", order.getId(), new OrderCreatedEvent(order));
    }
}

// Kafka Consumer
@KafkaListener(topics = "order-events", groupId = "inventory-service")
public void handleOrderEvent(OrderCreatedEvent event) {
    inventoryService.reserveStock(event.getItems());
}
```

| Pattern | Use When |
|---------|----------|
| **Sync** | Need immediate response, simple queries |
| **Async** | Fire-and-forget, event-driven, decoupling |

---

## 22. What is the difference between API Gateway and Service Mesh?

| Aspect | API Gateway | Service Mesh |
|--------|-------------|--------------|
| **Location** | Edge (north-south traffic) | Between services (east-west) |
| **Focus** | External client requests | Inter-service communication |
| **Examples** | Kong, AWS API Gateway, Spring Cloud Gateway | Istio, Linkerd, Consul Connect |
| **Features** | Auth, rate limiting, routing | mTLS, retries, circuit breaking, observability |

**API Gateway:**
```yaml
# Spring Cloud Gateway
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/users/**
          filters:
            - StripPrefix=1
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 10
```

**Service Mesh (Istio example):**
```yaml
# Istio VirtualService
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
spec:
  hosts:
    - order-service
  http:
    - retries:
        attempts: 3
        perTryTimeout: 2s
      timeout: 10s
```

**Use both:** Gateway for external, Mesh for internal.

---

## 23. How do you handle eventual consistency in distributed systems?

**Strategies:**

### 1. Saga Pattern
```java
// Choreography (event-driven)
@KafkaListener(topics = "order-created")
public void onOrderCreated(OrderCreatedEvent event) {
    try {
        paymentService.charge(event);
        kafkaTemplate.send("payment-completed", new PaymentCompletedEvent(event.orderId));
    } catch (Exception e) {
        kafkaTemplate.send("payment-failed", new PaymentFailedEvent(event.orderId));
    }
}

// Orchestration (central coordinator)
@Service
public class OrderSagaOrchestrator {
    public void execute(Order order) {
        try {
            paymentService.reserve(order);
            inventoryService.reserve(order);
            shippingService.schedule(order);
            // All succeeded - commit
        } catch (Exception e) {
            // Compensate in reverse order
            compensate(order);
        }
    }
}
```

### 2. Outbox Pattern
```java
@Transactional
public void createOrder(Order order) {
    orderRepository.save(order);
    // Write event to outbox table (same transaction)
    outboxRepository.save(new OutboxEvent("OrderCreated", order));
}

// Separate process reads outbox and publishes to Kafka
@Scheduled(fixedDelay = 1000)
public void publishEvents() {
    List<OutboxEvent> events = outboxRepository.findUnpublished();
    events.forEach(e -> {
        kafkaTemplate.send(e.getTopic(), e.getPayload());
        e.markPublished();
    });
}
```

### 3. Idempotent Consumers
```java
@KafkaListener(topics = "payments")
public void processPayment(PaymentEvent event) {
    if (processedEventRepository.exists(event.getId())) {
        return; // Already processed
    }
    // Process and mark as done
    paymentService.process(event);
    processedEventRepository.save(event.getId());
}
```

---

## 24. How do you implement rate limiting in a microservices ecosystem?

### 1. API Gateway Level (Recommended)
```yaml
# Spring Cloud Gateway + Redis
spring:
  cloud:
    gateway:
      routes:
        - id: api-route
          filters:
            - name: RequestRateLimiter
              args:
                redis-rate-limiter.replenishRate: 100  # requests/sec
                redis-rate-limiter.burstCapacity: 200
                key-resolver: "#{@userKeyResolver}"

@Bean
public KeyResolver userKeyResolver() {
    return exchange -> Mono.just(
        exchange.getRequest().getHeaders().getFirst("X-API-Key")
    );
}
```

### 2. Application Level (Resilience4j)
```java
@RateLimiter(name = "api", fallbackMethod = "rateLimitFallback")
public Response callExternalApi() {
    return externalService.call();
}

public Response rateLimitFallback(Exception e) {
    throw new TooManyRequestsException("Rate limit exceeded");
}
```

```yaml
resilience4j:
  ratelimiter:
    instances:
      api:
        limitForPeriod: 100
        limitRefreshPeriod: 1s
        timeoutDuration: 0
```

### 3. Distributed Rate Limiting (Redis)
```java
@Component
public class RedisRateLimiter {
    private final RedisTemplate<String, String> redis;
    
    public boolean isAllowed(String key, int limit, int windowSeconds) {
        String redisKey = "rate:" + key;
        Long count = redis.opsForValue().increment(redisKey);
        if (count == 1) {
            redis.expire(redisKey, windowSeconds, TimeUnit.SECONDS);
        }
        return count <= limit;
    }
}
```

**Algorithms:**
- **Fixed Window**: Simple but spike at boundaries
- **Sliding Window Log**: Accurate but memory-intensive
- **Token Bucket**: Allows bursts, common choice
- **Leaky Bucket**: Smooth output rate
