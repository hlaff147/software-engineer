# Aprovação de Empréstimo com Motor de Risco Real-Time

![Loan Risk System Design](./images/emprestimo_pf_system_design.png)

Este sistema demonstra como separar processos críticos síncronos (decisão de crédito) de processos assíncronos (notificação e ledger), utilizando Machine Learning.

## Padrões e Técnicas Utilizadas

- **Feature Store:** Uso do Redis para armazenar variáveis pré-calculadas (consumo médio, atrasos recentes) com leitura baixíssima latência (< 5ms).
- **In-Process vs Remote ML Inference:** O Risk Engine Service consulta modelos de crédito para tomar decisões em milissegundos.
- **Transactional Outbox / Event Driven:** Uma vez aprovado, o evento é publicado no Kafka para garantir que o saldo seja movimentado e o cliente notificado.
- **Separation of Concerns:** Divisão clara entre a "Security Layer", "Síncrono Crítico" e "Assíncrono Seguro".

## Componentes e Suas Funções

### 1. Security Layer
- **API Gateway:** Faz o "Gatekeeping" (Rate Limit, Roteamento).
- **Identity Provider (Keycloak/Auth0):** Valida a identidade do usuário antes que a requisição chegue ao orquestrador.

### 2. Síncrono Crítico (Motor de Risco)
- **Loan Orchestrator:** Coordena a chamada ao motor de risco.
- **Risk Engine Service:** O componente de decisão.
    - **Redis (Feature Store):** Provê dados históricos processados assincronamente via ETL a partir de um Data Lake.
    - **Modelo de Crédito:** Modelo de ML que recebe as features e retorna o score de aprovação.

### 3. Assíncrono Seguro (Pós-Aprovação)
- **Kafka (Tópico loan approved):** Garante a entrega confiável do evento de aprovação.
- **Core Banking Ledger:** Sistema de registro oficial (Livro Razão) persistido em **Postgres** com garantias **ACID**.
- **Notification Service:** Dispara o Push Notification para o App do usuário.

## Fluxo da Requisição
1. O usuário solicita o empréstimo via App.
2. O Gateway valida o token e o **Loan Orchestrator** inicia a consulta (1).
3. O **Risk Engine** lê os dados das features no Redis em < 5ms, aplica o modelo de ML e decide pela aprovação.
4. Se aprovado, publica o evento no **Kafka** (2).
5. O sistema de Ledger consome do Kafka e **Movimenta o Saldo** (3).
6. O sistema de notificação dispara o aviso ao usuário (4).
