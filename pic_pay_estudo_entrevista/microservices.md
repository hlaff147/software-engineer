# Arquitetura de Microserviços — Perguntas comuns

## 1) Como definir o “limite” de um microserviço?

**Resposta curta:** por **capacidade de negócio** (bounded context), com dados e regras de domínio coesos.

**Gatilhos:** DDD, ownership, mudanças independentes, reduzir chatty calls.

---

## 2) Microserviços x monólito: quando escolher?

**Resposta curta:** microserviços quando precisa de autonomia de deploy/escala e múltiplos times; monólito para começar rápido e reduzir overhead.

**Gatilhos:** complexidade operacional, observabilidade, CI/CD, custo de rede, latência, consistência distribuída.

---

## 3) Cada microserviço deve ter seu próprio banco?

**Resposta curta:** idealmente sim (data ownership). Compartilhar banco acopla deploy e quebra autonomia.

**Gatilhos:** schema coupling, migrações independentes, integração via APIs/eventos.

---

## 4) Como lidar com transações distribuídas?

**Resposta curta:** evitar 2PC; usar **Sagas** (orquestração ou coreografia) com compensações e idempotência.

**Gatilhos:** eventual consistency, outbox pattern, retries, deduplicação.

---

## 5) Comunicação síncrona x assíncrona?

**Resposta curta:** síncrona para consulta/fluxo simples; assíncrona para desacoplamento, resiliência e integração entre domínios.

**Gatilhos:** HTTP/gRPC vs eventos, backpressure, *at-least-once*, ordenação.

---

## 6) Como versionar APIs sem quebrar consumidores?

**Resposta curta:** evoluir de forma compatível; versionar quando necessário e preferir mudança aditiva.

**Gatilhos:** contratos, OpenAPI, compatibilidade, depreciação, API gateway.

---

## 7) O que é Observabilidade (de verdade)?

**Resposta curta:** capacidade de entender o sistema por logs, métricas e traces correlacionados.

**Gatilhos:** trace id, OpenTelemetry, SLI/SLO, alertas orientados a sintomas.

---

## 8) Como projetar para resiliência?

**Resposta curta:** tratar falhas como norma: timeouts, retries com jitter, circuit breaker, bulkhead.

**Gatilhos:** Resilience4j, limites, fallback (com cuidado), idempotência.
