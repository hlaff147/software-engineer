# Arquitetura de Saga Orquestrada com Message Broker

![Saga Orchestrator Architecture](./images/Saga1-2025-12-27-235823.png)

Esta imagem apresenta a visão infraestrutural do padrão Saga, destacando o papel do Broker de mensagens e do Coordenador de Execução.

## Padrões e Técnicas Utilizadas

- **SEC (Saga Execution Coordinator):** O componente dentro do `Order Service` que detém a lógica do fluxo de negócio e o estado da máquina de estados.
- **Message Broker (RabbitMQ/Kafka):** Utilizado para desacoplar o orquestrador dos executores. O orquestrador envia "Comandos" e ouve "Eventos".
- **Asynchronous Messaging:** Toda a comunicação entre o Domínio de Pedidos, Estoque e Pagamento ocorre de forma não-bloqueante via filas.
- **Saga State DB:** Banco de dados dedicado para persistir o progresso da Saga, garantindo que se o orquestrador cair, ele possa retomar de onde parou.

## Componentes e Suas Funções

### 1. Domínio de Pedidos (O Orquestrador)
- **Order Service / SEC:** Decide qual comando enviar a seguir (Reservar, Cobrar ou Compensar).
- **Saga State DB:** Garante a durabilidade do estado da transação distribuída.

### 2. Message Broker (O Meio de Transporte)
- Atua como o barramento de comunicação.
- **Comandos:** Instruções específicas enviadas pelo SEC (ex: "Reserve este item").
- **Eventos:** Respostas dos serviços (ex: "Estoque Reservado" ou "Falha no Pagamento").

### 3. Domínios Executores (Estoque e Pagamento)
- **Stock Service:** Escuta comandos de reserva, interage com seu próprio **Stock DB** e emite eventos de sucesso ou necessidade de liberação.
- **Payment Service:** Valida o saldo no **Payment DB** e reporta o sucesso ou falha da transação financeira.

## Fluxo de Mensageria
1. O SEC envia o **Comando 1 (Reservar)** para o Broker.
2. O **Stock Service** consome, executa e devolve o **Evento (Reservado)** para o Broker.
3. O SEC lê o evento de sucesso e envia o **Comando 2 (Processar Pagto)**.
4. Se o **Payment Service** devolver um evento de **FALHA**, o SEC lê e dispara o **Comando 3 (COMPENSAR)** para desfazer a reserva de estoque.
