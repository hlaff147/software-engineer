# Sistema de Transferência de Pagamentos e Idempotência

![Payment Idempotency System](./images/payment_system_picpay_payment_example.png)

Garantir que uma transferência de dinheiro ocorra exatamente uma vez, mesmo em caso de retentativas de rede, é o desafio central deste design.

## Padrões e Técnicas Utilizadas

- **Idempotency Key:** Uso de uma chave única enviada pelo cliente e verificada no Redis para evitar o processamento duplicado da mesma transação.
- **Pessimistic Locking (Lock Pessimista):** Bloqueio do registro do saldo no banco de dados (SELECT FOR UPDATE) durante a transação para evitar condições de corrida em carteiras com mutações simultâneas.
- **Fan-out Pattern:** O evento `transfer.success` é publicado no Kafka e consumido por múltiplos serviços independentes (Notificação, Auditoria, BI).
- **Synchronous Anti-Fraud:** Checagem de fraude realizada antes da movimentação financeira para evitar estornos custosos.

## Componentes e Suas Funções

### 1. Edge Layer (Filtro de Entrada)
- **API Gateway:**
    - **Auth Service:** Valida o JWT do usuário.
    - **Redis (Idempotency Keys):** Armazena chaves de transação por um tempo determinado. Se a chave já existir, o Gateway retorna o resultado cacheado sem reprocessar.

### 2. Core Domain (Execução)
- **Transaction Service:** Orquestra a validação e execução.
- **User Service:** Verifica se pagador e recebedor estão ativos e aptos.
- **Anti-Fraud Service:** Avalia o risco da transação em tempo real.
- **Wallet Core Service:** O componente mais crítico. Realiza o débito e crédito no **Postgres (Ledger/Wallets)** garantindo atomicidade.

### 3. Async Processing (Efeitos Colaterais)
- **Kafka:** Desacopla tarefas que não precisam ser feitas no tempo da requisição HTTP.
- **Data Lake Ingestion:** Alimenta o sistema de analytics para relatórios futuros.
- **Audit Service:** Registra a transação para conformidade regulatória.

## Fluxo da Operação
1. O usuário envia o pagamento com uma `x-idempotency-key`.
2. O Gateway verifica no Redis se essa chave já foi processada.
3. O **Transaction Service** valida os usuários (1) e a fraude (2).
4. O **Wallet Core** aplica um **Lock Pessimista** no Postgres, altera os saldos e libera o lock (3).
5. Um evento de sucesso é disparado para o **Kafka** (4).
6. O usuário recebedor recebe uma notificação de "Dinheiro Recebido".
