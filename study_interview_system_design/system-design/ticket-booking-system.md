# Sistema de Venda de Ingressos de Alta Demanda (Ticket Booking System)

![Ticket Booking System](./images/Untitled diagram-2025-12-27-061426.png)

Este sistema foi projetado para lidar com picos massivos de tráfego, comuns em vendas de ingressos para grandes eventos.

## Padrões e Técnicas Utilizadas

- **Virtual Waiting Room (Fila de Espera Virtual):** Controla o fluxo de usuários antes que eles atinjam os serviços centrais, liberando o acesso em lotes.
- **Distributed Locking (Bloqueio Distribuído):** Utiliza Redis para garantir que o mesmo assento não seja reservado por dois usuários simultaneamente (Race Condition).
- **Event-Driven Architecture:** Comunicação assíncrona entre o serviço de pagamento e o serviço de tickets via RabbitMQ.
- **Edge Computing/Caching:** Uso de CDN (Cloudflare) para servir conteúdo estático e mitigar ataques básicos.

## Componentes e Suas Funções

### 1. Camada de Edge & Controle de Fluxo
- **CDN (Cloudflare):** Primeira linha de defesa e cache de conteúdo estático.
- **Fila Virtual / Waiting Room:** Protege a infraestrutura interna de sobrecarga, retendo usuários em uma fila controlada e liberando-os gradualmente.
- **Load Balancer (LB):** Distribui as requisições liberadas entre as instâncias do API Gateway.

### 2. Zona de Compra
- **API Gateway:** Centraliza as chamadas de API, realizando autenticação e roteamento para os microserviços.
- **Ticket Service:** Gerencia o ciclo de vida da reserva e venda do ticket.
    - **Redis (Lock Temporário):** Bloqueia o assento por um curto período enquanto o pagamento é processado.
    - **Postgres (Assentos):** Banco de dados relacional para garantir consistência (ACID) no estado final dos assentos.
- **Payment Service:** Interface com gateways de pagamento externos e publicação de eventos de sucesso/falha.

### 3. Zona de Pagamento
- **Gateway Pagamento Externo:** Processa a transação financeira real.
- **RabbitMQ (Eventos):** Broker de mensagens que transporta o evento `PagamentoOK` de volta para o Ticket Service.

## Fluxo de Reserva (Happy Path)
1. O usuário passa pela fila virtual e chega ao **Ticket Service**.
2. O sistema tenta criar um **Lock Temporário no Redis** (1). Se conseguir, o assento fica "preso".
3. O sistema **Consulta o Mapa no Postgres** (2) para confirmar a disponibilidade oficial.
4. O usuário é direcionado ao **Payment Service** para pagar.
5. Após o pagamento bem-sucedido, o **RabbitMQ** notifica o Ticket Service.
6. O Ticket Service **Persiste a Venda Final no Postgres** (3) e **Remove o Lock no Redis** (4).
