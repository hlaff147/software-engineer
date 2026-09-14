# 🏗️ Exemplo Prático: Pipeline Serverless de CDC na AWS

> **Implementação de Referência Orientada a Eventos**  
> *Amazon DynamoDB Streams → Amazon EventBridge Pipes → Amazon EventBridge Event Bus → Amazon SQS (com DLQ) → AWS Lambda Function.*

---

## 📌 Visão Geral

Este exemplo prático demonstra como construir um pipeline de **Change Data Capture (CDC)** serverless, desacoplado, escalável e resiliente na nuvem AWS.

A arquitetura resolve o desafio de capturar mutações transacionais em tempo real no banco operacional e propagá-las com garantias de entrega, ordenação de partição, amortecimento de carga (*backpressure*) e isolamento de mensagens corrompidas (*Dead Letter Queue*), sem necessidade de escrita dupla (*Dual-Write*) no código da aplicação.

---

## 🏛️ Topologia Arquitetural

```
[ Aplicação / API ]
        │
        │ 1. PutItem / UpdateItem / DeleteItem
        ▼
┌─────────────────────────────────┐
│        Amazon DynamoDB          │
│        (Tabela Orders)          │
│   Stream: NEW_AND_OLD_IMAGES    │
└────────────────┬────────────────┘
                 │
                 │ 2. Captura automática via Transaction Log ordenado
                 ▼
┌─────────────────────────────────┐
│     EventBridge Pipes           │
│   (Filtro: INSERT & MODIFY)     │
└────────────────┬────────────────┘
                 │
                 │ 3. Normalização e envio estruturado
                 ▼
┌─────────────────────────────────┐
│       Amazon EventBridge        │
│      (Custom Event Bus)         │
└────────────────┬────────────────┘
                 │
                 │ 4. Roteamento por Regras (Event Pattern)
                 ▼
┌─────────────────────────────────┐           3 Falhas de Execução
│           Amazon SQS            │ ─────────────────────────────────► ┌────────────────────────┐
│     (Fila de Bufferização)      │                                    │     Amazon SQS DLQ     │
└────────────────┬────────────────┘                                    │  (Dead Letter Queue)   │
                 │                                                     └────────────────────────┘
                 │ 5. Trigger em Lote (BatchSize: 10)
                 ▼
┌─────────────────────────────────┐
│           AWS Lambda            │
│   (order_processor.py)          │
│  - Deserialização de imagens    │
│  - Cálculo de deltas            │
│  - Idempotência                 │
│  - ReportBatchItemFailures      │
└─────────────────────────────────┘
```

---

## 🧩 Componentes do Pipeline

### 1. Amazon DynamoDB (`cdc-orders`)
- **Tabela Transacional**: Modela pedidos com chave de partição `orderId` e chave de ordenação `customerId`.
- **StreamSpecification**: Configurada com `StreamViewType: NEW_AND_OLD_IMAGES`. Isso faz com que cada evento do stream carregue tanto a foto anterior do item (`OldImage`) quanto a foto após a mutação (`NewImage`), viabilizando a detecção de deltas sem consultas extras.

### 2. Amazon EventBridge Pipes (`cdc-dynamodb-to-eventbridge-pipe`)
- **Conexão Nativa**: Lê diretamente o DynamoDB Stream gerenciando iteradores de shards e concorrência.
- **Filtro de Eventos Integrado**: Regra de filtragem JSON `{"eventName": ["INSERT", "MODIFY"]}`. Mutações irrelevantes são descartadas antes mesmo de serem publicadas no barramento, economizando custos e processamento.

### 3. Amazon EventBridge Custom Bus (`commerce-cdc-event-bus`)
- **Barramento de Eventos Desacoplado**: Permite que múltiplos sistemas subscrevam o mesmo fluxo de CDC (ex: faturamento, auditoria, motor de busca, BI) sem criar dependências com o banco DynamoDB.

### 4. Amazon SQS & Dead Letter Queue
- **Fila Principal (`cdc-order-events-queue`)**: Serve como amortecedor de picos (*buffer*) para proteger consumidores downstream contra saturação.
- **Fila de Letras Mortas (`cdc-order-events-dlq`)**: Configurada com `maxReceiveCount: 3`. Se um evento falhar sucessivamente por 3 vezes devido a corrupção de payload (*poison pill*), ele é isolado na DLQ sem travar os demais pedidos.

### 5. AWS Lambda (`cdc-order-processor`)
- **Processamento Parcial em Lote**: Utiliza a diretiva `ReportBatchItemFailures`. Se 1 mensagem falhar dentro de um lote de 10 mensagens da SQS, apenas a mensagem com erro é retida para nova tentativa, enquanto as outras 9 são confirmadas e removidas.
- **Idempotência**: Garante que entregas repetidas (inerentes ao padrão *at-least-once*) não causem duplicidade de ações no mundo real.

---

## 📂 Arquivos Deste Exemplo

| Arquivo | Descrição |
|:---|:---|
| [`template.yaml`](./template.yaml) | Template AWS SAM / CloudFormation com todos os recursos declarados (IaC). |
| [`src/order_processor.py`](./src/order_processor.py) | Código da função Lambda em Python com deserializador de tipos DynamoDB, cálculo de deltas e idempotência. |
| [`src/cdc_payload.json`](./src/cdc_payload.json) | Exemplos de payloads reais dos eventos `INSERT`, `MODIFY` e `REMOVE`. |

---

## 🧪 Como Testar e Executar Localmente

### Teste Rápido do Manipulador Python
Para executar o processador de eventos simulando o consumo da fila SQS localmente:

```bash
cd src
python3 order_processor.py
```

**Saída Esperada:**
```text
[INFO] [CDC INSERT] Novo registro criado: Pedido ord-10001 | Valor: R$ 199.9
[INFO] [CDC MODIFY] Pedido ord-10001 alterado. Deltas detectados: {'status': {'old': 'PENDING_PAYMENT', 'new': 'PAYMENT_CONFIRMED'}, 'updatedAt': {'old': '2026-03-14T12:00:00Z', 'new': '2026-03-14T12:05:00Z'}}
[INFO] [CDC REMOVE] Pedido ord-10001 removido. Estado final antes da exclusao: {'orderId': 'ord-10001', ...}
{
  "batchItemFailures": []
}
```

### Implantação na AWS via AWS SAM CLI (Opcional)
Caso deseje provisionar a infraestrutura na sua conta AWS:

```bash
# Validar o template
sam validate --lint

# Fazer o build dos artefatos
sam build

# Fazer o deploy guiado
sam deploy --guided
```
