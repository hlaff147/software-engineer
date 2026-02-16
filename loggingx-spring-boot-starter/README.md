# LoggingX Spring Boot Starter

[![Java](https://img.shields.io/badge/Java-17+-blue.svg)](https://openjdk.java.net/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.5+-green.svg)](https://spring.io/projects/spring-boot)
[![Maven Central](https://img.shields.io/badge/Maven%20Central-0.0.1--SNAPSHOT-orange.svg)](https://search.maven.org/)

**LoggingX** é uma biblioteca plug-and-play para padronizar logs técnicos e de negócio em microserviços Java Spring, com correlação ponta-a-ponta, redação de dados sensíveis e baixa sobrecarga.

## 🚀 Características Principais

- **Logs Estruturados JSON**: Todos os logs são emitidos em formato JSON para fácil ingestão em plataformas de observabilidade
- **Correlação Ponta-a-Ponta**: Propagação automática de `correlationId` através de HTTP, Kafka, MongoDB, JDBC, Service Bus e outros
- **AOP Automático**: Logging transparente com anotações `@Loggable` e `@BusinessEvent`
- **Redação de PII**: Mascaramento automático de dados sensíveis baseado em configuração
- **Conectores Plug-and-Play**: Suporte automático para HTTP, Kafka, MongoDB, JDBC e Azure Service Bus conforme dependências no classpath
- **Performance**: Overhead <2% CPU com sampling inteligente e appenders assíncronos

## 📦 Instalação

### Maven

```xml
<dependency>
    <groupId>com.hlaff</groupId>
    <artifactId>loggingx-spring-boot-starter</artifactId>
    <version>0.0.1-SNAPSHOT</version>
</dependency>
```

### Gradle

```kotlin
dependencies {
    implementation("com.hlaff:loggingx-spring-boot-starter:0.0.1-SNAPSHOT")
}
```

## 🔧 Configuração Básica

### application.yml

```yaml
loggingx:
  service: meu-microservico     # OBRIGATÓRIO: nome do serviço
  env: prod                     # Ambiente (dev, qa, prod)
  version: ${APP_VERSION:1.0.0} # Versão da aplicação
  
  # Chaves a serem mascaradas
  redact-keys: 
    - password
    - token 
    - cpf
    - email
    - secret
    
  # Configurações HTTP
  http:
    server:
      enabled: true
      log-body: false    # Cuidado com dados sensíveis
    client: 
      enabled: true
      log-body: false
      
  # Configurações Kafka  
  kafka:
    enabled: true
    log-payload: false   # Cuidado com volume
    
  # Configurações MongoDB
  mongo:
    enabled: true
    slow-queries-only: true
    slow-threshold-ms: 1000

  # Configurações Azure Service Bus
  servicebus:
    enabled: true
    log-payload: false

  # Configurações JDBC
  jdbc:
    enabled: false
    slow-queries-only: true
    slow-threshold-ms: 500
```

## 📝 Uso Básico

### 1. Logging Automático de Métodos

```java
@Loggable
@Service
public class PaymentService {
    
    // Loga entrada/saída automaticamente
    public PaymentResult processPayment(PaymentRequest request) {
        // sua lógica aqui
        return result;
    }
    
    // Não loga argumentos sensíveis
    @Loggable(logArgs = false)
    public void authenticate(@Sensitive String password) {
        // password será mascarado como "***"
    }
}
```

### 2. Eventos de Negócio

```java
@Service
public class ReservationService {
    
    @BusinessEvent(type = "Rental", name = "ReservationCreated", version = 1)
    public ReservationResult createReservation(ReservationRequest request) {
        // ... lógica de negócio
        return result; // será usado como payload do evento
    }
}
```

### 3. HTTP Client com Correlação

```java
@Configuration
public class HttpConfig {
    
    @Bean 
    public RestTemplate restTemplate(LoggingXRestTemplateCustomizer customizer) {
        RestTemplate rt = new RestTemplateBuilder().build();
        customizer.customize(rt); // adiciona interceptor de correlação
        return rt;
    }
    
    @Bean
    public WebClient webClient(WebClientFilters filters) {
        return WebClient.builder()
            .filter(filters.correlationAndLogging())
            .build();
    }
}
```

### 4. Kafka com Correlação

```yaml
spring:
  kafka:
    producer:
      properties:
        interceptor.classes: com.hlaff.loggingx.kafka.CorrelatingProducerInterceptor
    consumer:
      properties:
        interceptor.classes: com.hlaff.loggingx.kafka.CorrelatingConsumerInterceptor
```

## 📊 Exemplo de Log Gerado

### Log Técnico (Saída de Método)

```json
{
  "@timestamp": "2025-01-20T14:05:23.817Z",
  "level": "INFO",
  "service": "rental-api",
  "env": "prod", 
  "version": "1.12.3",
  "correlationId": "c-7f1d5363",
  "component": "aop",
  "class": "PaymentService",
  "method": "processPayment",
  "args": {"customerId": "***", "amount": 299.90},
  "return": {"paymentId": "P-9021", "status": "APPROVED"},
  "durationMs": 123,
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
  "eventType": "Payment",
  "eventName": "PaymentApproved", 
  "eventVersion": 1,
  "eventPayload": {"paymentId": "P-9021", "amount": 299.90, "currency": "BRL"}
}
```

## 🎛️ Configuração Avançada

### Sampling por Padrão

```yaml
loggingx:
  sampling:
    default-percent: 20  # 20% dos logs por padrão
    rules:
      - pattern: "com.acme.payment.*"
        percent: 100      # 100% para pagamentos
      - pattern: ".*HealthCheck.*" 
        percent: 5        # 5% para health checks
```

### Encoder JSON Recomendado (logback-spring.xml)

```xml
<configuration>
  <appender name="ASYNC" class="ch.qos.logback.classic.AsyncAppender">
    <discardingThreshold>0</discardingThreshold>
    <queueSize>10240</queueSize>
    <appender-ref ref="STDOUT_JSON"/>
  </appender>

  <appender name="STDOUT_JSON" class="ch.qos.logback.core.ConsoleAppender">
    <encoder class="net.logstash.logback.encoder.LogstashEncoder">
      <customFields>{"service":"${loggingx.service:-unknown}"}</customFields>
    </encoder>
  </appender>

  <root level="INFO">
    <appender-ref ref="ASYNC"/>
  </root>
</configuration>
```

## 🔍 Conectores Disponíveis

| Conector | Dependência Necessária | Auto-Habilitado |
|----------|------------------------|-----------------|
| HTTP Server | `spring-boot-starter-web` | ✅ |
| HTTP Client | `RestTemplate` / `WebClient` | ✅ |
| Kafka | `kafka-clients` | ✅ |
| MongoDB | `mongodb-driver-core` | ✅ |
| JDBC | `datasource-proxy` | ⚠️ Manual |

## 📈 Performance

- **Overhead típico**: <2% CPU em carga normal
- **Sempre usar**: `AsyncAppender` no Logback
- **Sampling**: Configure para reduzir volume em produção
- **Payloads grandes**: Serão truncados automaticamente

## 🛡️ Segurança

- **PII automático**: Campos como `password`, `token`, `cpf` são mascarados
- **Anotação `@Sensitive`**: Para mascaramento específico
- **Configurável**: Liste suas próprias chaves em `redact-keys`

## 🔧 Troubleshooting

### Logs não aparecem

1. Verifique se `loggingx.enabled=true`
2. Confirme configuração do `service` name
3. Verifique se classes estão anotadas com `@Loggable`

### Correlação não funciona

1. Certifique-se que `CorrelationFilter` está ativo
2. Para Kafka, configure interceptors nas properties
3. Para calls assíncronos, use `CorrelationUtils.withCorrelation()`

### Performance impacto

1. Desabilite `log-body` em produção
2. Configure sampling adequado
3. Use `AsyncAppender` sempre
4. Monitore tamanho dos logs

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Amazing Feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/hlaff/loggingx-spring-boot-starter/issues)
- **Documentação**: [Wiki](https://github.com/hlaff/loggingx-spring-boot-starter/wiki)
- **Email**: suporte@hlaff.com

---

**LoggingX** - Observabilidade padronizada para o ecossistema Java Spring 🚀
