# LoggingX - Exemplo de Uso Completo

Este exemplo mostra como configurar e usar o LoggingX em um microserviço Spring Boot.

## 1. Configuração (`application.yml`)

```yaml
loggingx:
  enabled: true
  service: rental-api           # Nome do seu microserviço
  env: ${ENVIRONMENT:dev}       # Ambiente (dev, qa, prod)
  version: ${APP_VERSION:1.0.0} # Versão da aplicação
  
  # Configuração de dados sensíveis
  redact-keys:
    - password
    - token
    - cpf
    - email
    - creditCard
    - authorization
  
  max-payload-length: 4096
  include-stacktrace: true
  
  # Configurações HTTP
  http:
    server:
      enabled: true
      log-body: false        # Cuidado com volume e dados sensíveis
      log-headers: false
    client:
      enabled: true
      log-body: false
      log-headers: false
  
  # Configurações Kafka
  kafka:
    enabled: true
    log-producer: true
    log-consumer: true
    log-payload: false       # Cuidado com volume
    log-headers: true
  
  # Configurações MongoDB
  mongo:
    enabled: true
    log-commands: true
    slow-queries-only: true
    slow-threshold-ms: 1000
    log-results: false
  
  # Configurações de sampling
  sampling:
    default-percent: 30      # 30% dos logs por padrão
    rules:
      - pattern: ".*Payment.*"
        percent: 100         # 100% para pagamentos
      - pattern: ".*Health.*"
        percent: 5           # 5% para health checks

# Configuração Kafka com interceptors
spring:
  kafka:
    producer:
      properties:
        interceptor.classes: com.hlaff.loggingx.kafka.CorrelatingProducerInterceptor
    consumer:
      properties:
        interceptor.classes: com.hlaff.loggingx.kafka.CorrelatingConsumerInterceptor
```

## 2. Service com Logging Automático

```java
@Loggable
@Service
@RequiredArgsConstructor
public class ReservationService {
    
    private final VehicleRepository vehicleRepository;
    private final PaymentService paymentService;
    private final NotificationService notificationService;

    // Logging automático de entrada/saída
    public ReservationResult createReservation(ReservationRequest request) {
        // Validações
        Vehicle vehicle = vehicleRepository.findById(request.getVehicleId())
            .orElseThrow(() -> new VehicleNotFoundException(request.getVehicleId()));

        // Processa pagamento
        PaymentResult payment = paymentService.processPayment(
            request.getCustomerId(), 
            request.getAmount()
        );

        // Cria reserva
        Reservation reservation = Reservation.builder()
            .customerId(request.getCustomerId())
            .vehicleId(request.getVehicleId())
            .startDate(request.getStartDate())
            .endDate(request.getEndDate())
            .amount(request.getAmount())
            .paymentId(payment.getId())
            .status(ReservationStatus.CONFIRMED)
            .build();

        reservationRepository.save(reservation);

        // Emite evento de negócio
        return emitReservationCreated(reservation, payment);
    }

    // Método sensível - não loga argumentos
    @Loggable(logArgs = false)
    public void validateCreditCard(@Sensitive String cardNumber, 
                                  @Sensitive String cvv) {
        // Validação do cartão
        // cardNumber e cvv serão mascarados como "***" nos logs
    }

    // Evento de negócio
    @BusinessEvent(type = "Rental", name = "ReservationCreated", version = 1)
    private ReservationCreatedEvent emitReservationCreated(Reservation reservation, 
                                                          PaymentResult payment) {
        return ReservationCreatedEvent.builder()
            .reservationId(reservation.getId())
            .customerId(reservation.getCustomerId())
            .vehicleId(reservation.getVehicleId())
            .amount(reservation.getAmount())
            .currency("BRL")
            .paymentId(payment.getId())
            .createdAt(Instant.now())
            .build();
    }
}
```

## 3. Service de Pagamento

```java
@Loggable
@Service
@RequiredArgsConstructor
public class PaymentService {
    
    private final PaymentGateway paymentGateway;
    private final RestTemplate restTemplate;

    public PaymentResult processPayment(String customerId, BigDecimal amount) {
        
        // Chama gateway externo - correlação automática via RestTemplate
        PaymentRequest request = PaymentRequest.builder()
            .customerId(customerId)
            .amount(amount)
            .currency("BRL")
            .build();

        PaymentResponse response = restTemplate.postForObject(
            "/api/payments", 
            request, 
            PaymentResponse.class
        );

        return PaymentResult.builder()
            .id(response.getPaymentId())
            .status(response.getStatus())
            .amount(amount)
            .build();
    }

    @BusinessEvent(type = "Payment", name = "PaymentApproved", version = 2)
    public PaymentApprovedEvent approvePayment(PaymentApprovalRequest request) {
        // Lógica de aprovação
        
        return PaymentApprovedEvent.builder()
            .paymentId(request.getPaymentId())
            .amount(request.getAmount())
            .approvedAt(Instant.now())
            .approvedBy("SYSTEM")
            .build();
    }
}
```

## 4. Configuração de Beans

```java
@Configuration
public class HttpClientConfig {
    
    // RestTemplate com interceptor LoggingX automático
    @Bean
    public RestTemplate restTemplate(LoggingXRestTemplateCustomizer customizer) {
        RestTemplate rt = new RestTemplateBuilder()
            .setConnectTimeout(Duration.ofSeconds(5))
            .setReadTimeout(Duration.ofSeconds(30))
            .build();
        
        // Aplica interceptor de correlação e logging
        customizer.customize(rt);
        return rt;
    }
    
    // WebClient com filtros LoggingX
    @Bean 
    public WebClient webClient(WebClientFilters loggingFilters) {
        return WebClient.builder()
            .baseUrl("https://api.external-service.com")
            .filter(loggingFilters.correlationAndLogging())
            .build();
    }
}
```

## 5. Consumer Kafka

```java
@Component
@RequiredArgsConstructor
public class PaymentEventConsumer {
    
    private final PaymentService paymentService;

    @KafkaListener(topics = "payment-events")
    @Loggable
    public void handlePaymentEvent(PaymentEvent event) {
        // correlationId será extraído automaticamente do header da mensagem
        
        switch (event.getType()) {
            case PAYMENT_APPROVED:
                paymentService.handleApprovedPayment(event);
                break;
            case PAYMENT_REJECTED:
                paymentService.handleRejectedPayment(event);
                break;
        }
    }
}
```

## 6. Producer Kafka

```java
@Component
@RequiredArgsConstructor
public class NotificationService {
    
    private final KafkaTemplate<String, Object> kafkaTemplate;

    @Loggable
    public void sendReservationNotification(ReservationCreatedEvent event) {
        NotificationMessage message = NotificationMessage.builder()
            .type(NotificationType.RESERVATION_CREATED)
            .customerId(event.getCustomerId())
            .reservationId(event.getReservationId())
            .build();

        // correlationId será adicionado automaticamente no header
        kafkaTemplate.send("notification-events", event.getCustomerId(), message);
    }
}
```

## 7. Repository MongoDB

```java
@Repository
public interface VehicleRepository extends MongoRepository<Vehicle, String> {
    
    // Todos os comandos MongoDB serão logados automaticamente
    // graças ao LoggingMongoCommandListener
    
    List<Vehicle> findByLocationAndAvailable(String location, boolean available);
    
    @Query("{ 'category': ?0, 'pricePerDay': { $lte: ?1 } }")
    List<Vehicle> findByCategoryAndMaxPrice(VehicleCategory category, BigDecimal maxPrice);
}
```

## 8. Execução Assíncrona com Correlação

```java
@Service
@RequiredArgsConstructor
public class AsyncNotificationService {
    
    @Async
    @Loggable
    public CompletableFuture<Void> sendEmailNotification(String customerId, String message) {
        
        // Para manter correlação em execução assíncrona
        return CompletableFuture.runAsync(CorrelationUtils.withCorrelation(() -> {
            // Sua lógica aqui
            emailService.sendEmail(customerId, message);
        }));
    }
}
```

## 9. Logs Gerados

### Log Técnico (Método)
```json
{
  "@timestamp": "2025-01-20T14:05:23.817Z",
  "level": "INFO",
  "service": "rental-api",
  "env": "prod",
  "version": "1.0.0",
  "correlationId": "c-7f1d5363",
  "component": "aop",
  "class": "ReservationService",
  "method": "createReservation",
  "args": {
    "customerId": "CUST-123",
    "vehicleId": "VEH-456",
    "amount": 299.90
  },
  "return": {
    "reservationId": "RES-789",
    "status": "CONFIRMED"
  },
  "durationMs": 234,
  "sampled": true
}
```

### Log de Negócio
```json
{
  "@timestamp": "2025-01-20T14:05:23.820Z",
  "level": "INFO",
  "service": "rental-api",
  "env": "prod",
  "correlationId": "c-7f1d5363",
  "component": "business",
  "eventType": "Rental",
  "eventName": "ReservationCreated",
  "eventVersion": 1,
  "eventPayload": {
    "reservationId": "RES-789",
    "customerId": "CUST-123",
    "vehicleId": "VEH-456",
    "amount": 299.90,
    "currency": "BRL",
    "createdAt": "2025-01-20T14:05:23.820Z"
  }
}
```

### Log HTTP Client
```json
{
  "@timestamp": "2025-01-20T14:05:24.100Z",
  "level": "INFO",
  "service": "rental-api",
  "env": "prod",
  "correlationId": "c-7f1d5363",
  "component": "http-client",
  "httpMethod": "POST",
  "httpPath": "/api/payments",
  "httpStatus": 200,
  "durationMs": 156,
  "sizeOut": 245,
  "url": "https://payment-api.com/api/payments",
  "sampled": true
}
```

### Log MongoDB
```json
{
  "@timestamp": "2025-01-20T14:05:24.200Z",
  "level": "INFO",
  "service": "rental-api",
  "env": "prod",
  "correlationId": "c-7f1d5363",
  "component": "mongo",
  "db.system": "mongodb",
  "db.op": "find",
  "collection": "vehicles",
  "durationMs": 45,
  "sampled": true
}
```

## 10. Consultas de Observabilidade

### Kibana/OpenSearch
```sql
-- Latência por método
GET logs-*/_search
{
  "aggs": {
    "by_method": {
      "terms": { "field": "method" },
      "aggs": {
        "avg_duration": { "avg": { "field": "durationMs" } }
      }
    }
  }
}

-- Erros por endpoint
GET logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "component": "http-server" } },
        { "term": { "level": "ERROR" } }
      ]
    }
  },
  "aggs": {
    "by_path": {
      "terms": { "field": "httpPath" }
    }
  }
}

-- Fluxo completo por correlationId
GET logs-*/_search
{
  "query": {
    "term": { "correlationId": "c-7f1d5363" }
  },
  "sort": [
    { "@timestamp": "asc" }
  ]
}
```

Este exemplo mostra o uso completo do LoggingX em um microserviço real, incluindo correlação ponta-a-ponta, eventos de negócio, e observabilidade estruturada.
