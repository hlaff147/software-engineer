# 🔄 Change Data Capture (CDC) — Guia de Arquitetura e Estudo Prático

> **Resumo de Estudo Pessoal & Referência Arquitetural**  
> *Conceitos fundamentais, funcionamento de baixo nível em transaction logs, comparações com abordagens tradicionais, casos de uso no mundo real e arquitetura serverless orientada a eventos na nuvem AWS.*

---

## 📌 Sumário

1. [O que é Change Data Capture (CDC)?](#-o-que-é-change-data-capture-cdc)
2. [O Problema do Dual-Write Anti-Pattern](#-o-problema-do-dual-write-anti-pattern)
3. [Como o CDC Funciona por Baixo dos Panos](#-como-o-cdc-funciona-por-baixo-dos-panos)
   - [O Papel do Transaction Log](#o-papel-do-transaction-log)
   - [Mapeamento nos Principais Bancos de Dados](#mapeamento-nos-principais-bancos-de-dados)
   - [Snapshot Inicial e Backfill](#snapshot-inicial-e-backfill)
   - [Log Sequence Numbers (LSN) e Offsets](#log-sequence-numbers-lsn-e-offsets)
4. [Diferenças Cruciais & Comparações](#-diferenças-cruciais--comparações)
   - [CDC vs ETL Tradicional](#1-cdc-vs-etl-tradicional)
   - [CDC vs SCD (Slowly Changing Dimensions)](#2-cdc-vs-scd-slowly-changing-dimensions)
   - [CDC vs HTAP (Hybrid Transactional/Analytical Processing)](#3-cdc-vs-htap-hybrid-transactionalanalytical-processing)
   - [CDC vs Consultas Federadas / Tabelas Externas](#4-cdc-vs-consultas-federadas--tabelas-externas)
5. [Benefícios e Vantagens Arquiteturais](#-benefícios-e-vantagens-arquiteturais)
6. [9 Casos de Uso Práticos no Mundo Real](#-9-casos-de-uso-práticos-no-mundo-real)
7. [Arquitetura Prática na AWS: DynamoDB, EventBridge, SQS e Lambda](#-arquitetura-prática-na-aws-dynamodb-eventbridge-sqs-e-lambda)
   - [Visão Geral da Topologia](#visão-geral-da-topologia)
   - [Diagrama de Arquitetura](#diagrama-de-arquitetura)
   - [Fluxo de Execução Passo a Passo](#fluxo-de-execução-passo-a-passo)
   - [Anatomia do Evento CDC (DynamoDB Streams)](#anatomia-do-evento-cdc-dynamodb-streams)
   - [Padrões de Resiliência: Idempotência e DLQ](#padrões-de-resiliência-idempotência-e-dlq)
8. [Estrutura do Módulo & Código Executável](#-estrutura-do-módulo--código-executável)

---

## 🎯 O que é Change Data Capture (CDC)?

**Change Data Capture (CDC)** é um padrão arquitetural de integração e engenharia de dados cujo objetivo é identificar, capturar e propagar de maneira confiável e em tempo quase real (*near real-time*) todas as modificações de dados (`INSERT`, `UPDATE`, `DELETE`) ocorridas em um sistema transacional de origem (*System of Record* / OLTP) para um ou mais destinos heterogêneos.

Em vez de sobrecarregar o banco de dados operacional executando queries periódicas e custosas (como varreduras completas de tabelas ou consultas baseadas em timestamps `WHERE updated_at > :last_sync`), o CDC opera interceptando as mutações no momento exato em que elas ocorrem, convertendo-as em um fluxo contínuo de eventos de domínio (*stream of change events*).

```
┌─────────────────┐       Commit Transacional       ┌────────────────────────┐
│  Aplicação /    │ ──────────────────────────────► │ Banco de Dados (OLTP)  │
│  Serviço OLTP   │                                 │ (Tabelas + Commit Log) │
└─────────────────┘                                 └───────────┬────────────┘
                                                                │
                                                  Leitura Assíncrona do Log (CDC)
                                                                │
                                                                ▼
                                                    ┌───────────────────────┐
                                                    │ Motor / Stream de CDC │
                                                    └───────────┬───────────┘
                                                                │
                     ┌──────────────────────────────────────────┼──────────────────────────────────────────┐
                     ▼                                          ▼                                          ▼
           ┌───────────────────┐                      ┌───────────────────┐                      ┌───────────────────┐
           │ Cache Distribuído │                      │ Índice de Busca   │                      │ Data Warehouse    │
           │ (Redis / Memcached│                      │ (Elasticsearch)   │                      │ (Redshift/BigQuery│
           └───────────────────┘                      └───────────────────┘                      └───────────────────┘
```

---

## ⚠️ O Problema do Dual-Write Anti-Pattern

Em arquiteturas tradicionais que não utilizam CDC, engenheiros frequentemente caem na armadilha do **Dual-Write**: a aplicação tenta, em um mesmo fluxo de negócio, salvar o dado no banco relacional e, logo em seguida, publicar uma mensagem num broker de mensageria ou atualizar um cache.

```
[Aplicação]
   ├── 1. db.save(order) ──────► [PostgreSQL] (Sucesso!)
   └── 2. kafka.send(event) ───► [Kafka]      (FALHA DE REDE / CRASH!)
```

### Por que o Dual-Write falha?
1. **Falta de Atomicidade Distribuída**: Sem o protocolo pesado de *Two-Phase Commit (2PC)* — que degrada brutalmente o throughput —, não há garantia atômica entre o banco de dados e o broker externo. Se a gravação no banco tiver sucesso mas a publicação no broker falhar (por timeout de rede, falta de memória ou crash da aplicação), o sistema entra em inconsistência permanente de dados.
2. **Race Conditions e Ordem Invertida**: Se duas threads atualizarem o mesmo registro quase simultaneamente, a thread A pode gravar no banco antes da thread B, mas a mensagem da thread B pode chegar ao broker antes da thread A. O cache ou os consumidores downstream ficarão com dados desatualizados (*stale data*).

**Como o CDC resolve isso?**  
A aplicação escreve exclusivamente no banco de dados operacional sob uma transação local ACID garantida. O mecanismo de CDC lê diretamente o log do banco e publica os eventos downstream com garantia de ordenação e durabilidade, eliminando por completo o anti-pattern de escrita dupla.

---

## ⚙️ Como o CDC Funciona por Baixo dos Panos

### O Papel do Transaction Log
Todos os bancos de dados relacionais e transacionais modernos utilizam internamente um **Transaction Log** append-only de escrita sequencial. Antes que qualquer modificação seja persistida nas páginas de dados em disco ou índices das tabelas, a mutação bruta é gravada de forma síncrona no log. Esse mecanismo existe primariamente para garantir as propriedades ACID de durabilidade (*Durability*) e recuperação contra falhas (*Crash Recovery*).

O CDC moderno **não executa queries SQL** contra as tabelas operacionais. Ele atua como um leitor passivo e não-intrusivo desse transaction log, deserializando as entradas de log em eventos estruturados contendo:
- Metadados da transação (ID da transação, timestamp, identificador do registro).
- Tipo de operação (`INSERT`, `UPDATE`, `DELETE`).
- **Old Image**: Estado dos atributos antes da mutação.
- **New Image**: Estado dos atributos após a mutação.

### Mapeamento nos Principais Bancos de Dados

| Banco de Dados | Mecanismo Interno do Transaction Log | Como o CDC Captura |
|:---|:---|:---|
| **PostgreSQL** | *Write-Ahead Log (WAL)* | Leitura via *Logical Decoding* e *Replication Slots* |
| **MySQL / MariaDB** | *Binary Log (Binlog)* | O motor de CDC se registra como uma réplica conectada lendo o binlog |
| **Oracle** | *Redo Log* & *Archive Log* | Leitura via *Oracle LogMiner* ou captura de streaming nativa |
| **SQL Server** | *Transaction Log (.ldf)* | CDC nativo baseado em tabelas de captura e log reader agent |
| **Amazon DynamoDB** | *DynamoDB Streams* | Buffer de 24 horas contendo shards ordenados com imagens antes/depois |

### Snapshot Inicial e Backfill
Para bancos de dados operacionais que já possuem milhões de registros existentes, apenas ler o transaction log a partir do momento atual deixaria o destino incompleto (sem os dados prévios). O padrão da indústria para resolver isso é o **Snapshot + Streaming**:

1. **Snapshot Consistente**: O motor de CDC obtém uma fotografia (*consistent snapshot*) do banco de dados na transação $T_0$, capturando o estado de todas as linhas sem travar escritas concorrentes.
2. **Marcação de Posição**: O motor registra o identificador exato da transação ou posição do log correspondente ao snapshot ($LSN_0$).
3. **Carga em Massa (Backfill)**: Os dados históricos são transmitidos e carregados no sistema de destino.
4. **Streaming Incremental**: Concluído o snapshot, o motor inicia a leitura contínua das mutações a partir de $LSN_0$. Mutações que ocorreram durante o snapshot são processadas de forma idempotente, sincronizando perfeitamente o destino com a origem.

### Log Sequence Numbers (LSN) e Offsets
Para rastrear exatamente até onde os eventos foram processados e garantir resiliência contra quedas:
- **LSN (Log Sequence Number)** / **SCN (System Change Number)** / **Binlog Position**: São identificadores monotônicos que representam a coordenada exata de uma entrada no log.
- **Armazenamento de Offset / Checkpoint**: O motor de CDC armazena periodicamente o último LSN processado com sucesso. Caso o conector ou serviço reinicie após uma falha, ele retoma o streaming exatamente desse checkpoint, evitando a perda de eventos e permitindo entrega do tipo *at-least-once*.

---

## ⚖️ Diferenças Cruciais & Comparações

### 1. CDC vs ETL Tradicional
- **ETL Tradicional (Batch)**: Executado em intervalos programados (geralmente horários noturnos ou a cada X horas). Realiza queries pesadas no banco operacional, extraindo massas volumosas de dados. Gera alto consumo de CPU/I/O no OLTP e sofre de alta latência (dados disponíveis apenas no dia seguinte ou horas depois).
- **CDC (Event-Driven Streaming)**: Extrai incrementalmente cada linha alterada em milissegundos a partir do transaction log. Impacto praticamente nulo no desempenho do OLTP e entrega dados *near real-time*.

### 2. CDC vs SCD (Slowly Changing Dimensions)
- **CDC**: É a técnica de **transporte e captura** eficiente das mutações no sistema de origem.
- **SCD (Dimensões de Mudança Lenta - Tipo 1, 2, 3)**: É a técnica de **modelagem e armazenamento** aplicada no Data Warehouse de destino para decidir como guardar o histórico (por exemplo, SCD Tipo 2 cria uma nova linha com colunas `start_date`, `end_date` e `is_current`). O CDC é o veículo que alimenta o pipeline que implementa SCD no destino.

### 3. CDC vs HTAP (Hybrid Transactional/Analytical Processing)
- **HTAP**: Bancos unificados que tentam rodar queries analíticas complexas (OLAP) e transações (OLTP) no mesmo cluster de dados sob o mesmo motor. Pode ser complexo e custoso de escalar verticalmente para grandes volumes.
- **CDC**: Abraça o princípio da especialização (*polyglot persistence*), permitindo que o sistema operacional use a melhor ferramenta para escrita (ex: PostgreSQL ou DynamoDB) enquanto projeta e sincroniza os dados continuamente para a melhor ferramenta de análise ou busca (ex: BigQuery ou Elasticsearch).

### 4. CDC vs Consultas Federadas / Tabelas Externas
- **Consultas Federadas**: Um mecanismo de query analítico lê dados diretamente do banco OLTP no momento da consulta (*on-demand query*).
- **Desvantagem da Federação**: Consultas complexas com múltiplos joins degradam violentamente o banco de produção. O CDC evita isso desacoplando totalmente as consultas analíticas do banco operacional.

---

## 💎 Benefícios e Vantagens Arquiteturais

```
┌────────────────────────────────────────────────────────────────────────┐
│                      BENEFÍCIOS DO CDC                                 │
├──────────────────────────┬─────────────────────────────────────────────┤
│ ⚡ Baixíssima Latência   │ Mudanças replicadas em milissegundos.       │
│ 🛡️ Zero Overhead OLTP   │ Leitura não-intrusiva do log binário.       │
│ 🔌 Desacoplamento Total  │ Produtores e consumidores sem dependência.  │
│ 🔄 Fim do Dual-Write     │ Consistência transacional garantida.        │
│ 📜 Trilha Completa       │ Captura antes e depois (Old & New Images).  │
│ 📈 Escalabilidade Linear │ Suporte a múltiplos destinos assíncronos.   │
└──────────────────────────┴─────────────────────────────────────────────┘
```

1. **Consistência de Dados entre Sistemas Heterogêneos**: Garante que índices de busca, caches e bancos de leitura reflitam a verdade do banco transacional sem defasagem de dados (*data drift*).
2. **Movimentação Eficiente e Econômica de I/O**: Em vez de fazer *full table scans* periódicos, transmite apenas a diferença (*delta*), poupando banda de rede e processamento.
3. **Resiliência e Recuperação Simplificada**: Como todo evento possui um offset sequencial no log, em caso de indisponibilidade de um consumidor downstream, o fluxo pode ser congelado e retomado do último ponto seguro sem perda de dados.
4. **Habilitação de Arquiteturas Reativas e Event-Driven**: Transforma bancos de dados tradicionais em fontes produtoras de eventos de primeira classe (*event streams*).

---

## 🚀 9 Casos de Uso Práticos no Mundo Real

### 1. Invalidação e Atualização Reativa de Caches (Cache-Aside / Event-Driven Cache)
- **Cenário**: Aplicações de alto tráfego utilizam caches em memória (Redis, Memcached) para acelerar leituras.
- **Problema Tradicional**: Caches dependem de TTL (Time to Live) arbitrário, resultando em dados obsoletos até a expiração, ou a aplicação precisa invalidar o cache manualmente arriscando inconsistências em caso de erro.
- **Com CDC**: Qualquer `UPDATE` na tabela de produtos emite um evento CDC. Uma função serverless intercepta a mudança e atualiza a chave no Redis ou invalida a entrada imediatamente. Leituras subsequentes sempre encontram dados consistentes.

### 2. Sincronização Contínua de Motores de Busca Textual (Elasticsearch / OpenSearch)
- **Cenário**: Bancos relacionais não são otimizados para busca textual com operadores fonéticos, autocompletar e filtros multifacetados complexos.
- **Com CDC**: Os dados relacionais são modelados em tabelas normalizadas. O fluxo de CDC extrai mutações, desnormaliza os dados em documentos JSON agregados e indexa no Elasticsearch em tempo quase real, permitindo pesquisas instantâneas sem sobrecarregar o OLTP.

### 3. Carga Contínua e Streaming para Data Warehouse e Data Lake
- **Cenário**: Engenharia de dados e times de Business Intelligence (BI) necessitam de dados frescos para tomada de decisão e relatórios operacionais.
- **Com CDC**: Elimina jobs de batch noturno lentos e frágeis. Mutações são enviadas continuamente para tabelas em plataformas de Data Warehouse (Amazon Redshift, Google BigQuery, Snowflake) ou formatos de tabela aberta em Data Lakes (Apache Iceberg, Delta Lake).

### 4. Sincronização On-Premises para Cloud & Migrações Zero-Downtime
- **Cenário**: Modernização de infraestrutura legada transferindo dados de datacenters on-premises para a nuvem pública.
- **Com CDC**: Realiza-se a carga inicial do banco local para o banco na nuvem. Em seguida, o CDC mantém ambos os bancos em sincronia bidirecional ou unidirecional contínua. Quando a aplicação na nuvem estiver pronta, a virada de chave (*cutover*) é feita em segundos com tempo de indisponibilidade nulo (*zero-downtime*).

### 5. Atualização de Materialized Views e Implementação do Padrão CQRS
- **Cenário**: Em microsserviços aplicando **Command Query Responsibility Segregation (CQRS)**, o modelo de escrita (*Write Model*) é otimizado para comandos e regras de negócio, enquanto o modelo de leitura (*Read Model*) necessita de visões materializadas preparadas para queries de baixa latência.
- **Com CDC**: Toda mutação no Write Model gera um evento de CDC que projeta e atualiza assincronamente as Materialized Views do Read Model, eliminando junções (*joins*) dispendiosas em tempo de requisição.

### 6. Comunicação Transacional Segura entre Microsserviços com Outbox Pattern
- **Cenário**: Um microsserviço de pedidos precisa criar uma ordem e notificar o microsserviço de faturamento e o de estoque.
- **Implementação com CDC**: O microsserviço de pedidos grava a ordem e um registro na tabela `outbox` na mesma transação de banco de dados. O CDC monitora especificamente a tabela `outbox`, lê os registros inseridos e publica os eventos no broker de mensageria. Após a publicação bem-sucedida, o evento é marcado como processado. Isso garante entrega garantida de eventos sem escrita dupla (*Dual-Write*).

### 7. Disseminação de Informações em Tempo Real (Dashboards & Notificações Reativas)
- **Cenário**: Plataformas de monitoramento financeiro, telemetria de frotas ou e-commerce precisam refletir alterações na tela do usuário instantaneamente.
- **Com CDC**: Modificações no banco geram eventos processados por mecanismos de stream processing (como Apache Flink ou funções serverless), que empurram os dados purificados para conexões WebSockets abertas ou atualizam dashboards de monitoramento ao vivo.

### 8. Construção de Trilha de Auditoria Imutável (Audit Trail & Compliance)
- **Cenário**: Setores regulados (bancário, saúde, seguros) exigem rastreabilidade completa de quem alterou qual dado e qual era o valor anterior.
- **Com CDC**: Como o CDC captura o estado anterior (`OldImage`) e o estado novo (`NewImage`) juntamente com o carimbo de data/hora e metadados de transação, é possível persistir esse fluxo em um armazenamento append-only e imutável (como Amazon S3 com Object Lock), criando uma trilha de auditoria completa que permite reconstruir o histórico de qualquer registro em qualquer ponto no tempo (*time-travel analysis*).

### 9. Alimentação Contínua de Feature Stores para IA e Machine Learning
- **Cenário**: Modelos preditivos de detecção de fraudes, sistemas de recomendação e precificação dinâmica requerem features comportamentais atualizadas em tempo real.
- **Com CDC**: Mutações em transações de usuários alimentam continuamente a Feature Store online em milissegundos, garantindo que as inferências do modelo de Machine Learning utilizem o comportamento mais recente do usuário.

---

## ☁️ Arquitetura Prática na AWS: DynamoDB, EventBridge, SQS e Lambda

Para demonstrar o funcionamento prático de um pipeline de CDC serverless resiliente e de alta performance, projetamos uma arquitetura orientada a eventos utilizando exclusivamente serviços nativos da **AWS**.

### Visão Geral da Topologia

1. **Amazon DynamoDB**: Atua como o banco de dados operacional transacional (OLTP). A funcionalidade **DynamoDB Streams** fica habilitada com o tipo de visualização `NEW_AND_OLD_IMAGES`.
2. **Amazon EventBridge Pipes**: Conecta-se diretamente ao DynamoDB Stream como consumidor gerenciado de baixo nível. Executa filtragem de eventos (*Event Filtering*) na origem, evitando invocações desnecessárias.
3. **Amazon EventBridge Event Bus**: Barramento central de eventos que recebe mutações filtradas e as distribui para múltiplos consumidores desacoplados através de regras de roteamento (*Rules*).
4. **Amazon SQS (Simple Queue Service)**: Fila intermediária que atua como amortecedor de vazão (*buffer / backpressure*) para proteger os serviços downstream e garantir controle de taxa de execução. Possui uma **Dead Letter Queue (DLQ)** associada para isolar mensagens venenosas (*poison pills*).
5. **AWS Lambda**: Função de processamento de eventos que consome as mensagens da fila SQS, deserializa o payload de CDC do DynamoDB, calcula a diferença entre o estado antigo e novo, atualiza downstream (como caches ou índices) e reporta falhas parciais de lote (*Batch Item Failures*).

---

### Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                ARQUITETURA SERVERLESS DE CDC NA AWS                                    │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 [ Aplicação Cliente ]
          │
          │ 1. PutItem / UpdateItem (Transação Atômica)
          ▼
┌───────────────────┐
│  Amazon DynamoDB  │
│  (Tabela Orders)  │
└─────────┬─────────┘
          │ 2. Captura contínua no log (24h buffer ordenado)
          ▼
┌───────────────────┐
│ DynamoDB Streams  │  (View: NEW_AND_OLD_IMAGES)
└─────────┬─────────┘
          │ 3. Polling nativo gerenciado + Event Pattern Filter
          ▼
┌───────────────────┐
│ EventBridge Pipes │
└─────────┬─────────┘
          │ 4. Publicação estruturada no barramento
          ▼
┌───────────────────┐
│    EventBridge    │
│  Custom Event Bus │
└─────────┬─────────┘
          │ 5. Roteamento baseado em regras (Rules)
          ▼
┌───────────────────┐               Falhas após 3 retentativas
│    Amazon SQS     │ ──────────────────────────────────────────► ┌─────────────────────────┐
│ (Orders FIFO/Std) │                                             │ Amazon SQS DLQ          │
└─────────┬─────────┘                                             │ (Dead Letter Queue)     │
          │ 6. Batch Trigger (BatchSize: 10)                      └─────────────────────────┘
          ▼
┌───────────────────┐
│    AWS Lambda     │ ────► Atualiza Cache Redis / Envia Notificação
│ (Order Processor) │ ────► Reporta falhas parciais (batchItemFailures)
└───────────────────┘
```

---

### Fluxo de Execução Passo a Passo

1. **Escrita no OLTP**: A aplicação de negócio executa um comando de inserção ou atualização no DynamoDB (ex: transição de status de pedido de `PENDING` para `CONFIRMED`).
2. **Emissão no Stream**: O DynamoDB Streams grava um registro imutável no shard correspondente contendo a chave de partição, o evento (`INSERT`, `MODIFY` ou `REMOVE`), e as duas fotos do item: `OldImage` e `NewImage`.
3. **Interceptação com EventBridge Pipes**: O Pipes lê o stream de forma gerenciada. Aplicamos um filtro de evento (*Event Filter Pattern*) para que apenas mutações relevantes (por exemplo, pedidos aprovados ou modificações de endereço) sejam propagadas para o barramento.
4. **Distribuição via Event Bus**: O barramento recebe o evento padronizado e avalia as regras cadastradas. Múltiplos sistemas podem subscrever o mesmo evento sem interferir no banco de dados de origem.
5. **Amortecimento com SQS**: A fila SQS recebe a mensagem, garantindo tolerância a picos de tráfego (*bursts*) e permitindo que o consumidor processe os itens no seu próprio ritmo (*rate limiting*).
6. **Consumo no Lambda**: A função Lambda é acionada recebendo um lote de eventos. O código valida a chave de idempotência, executa as ações de downstream e reporta à SQS apenas as mensagens que falharam, reaproveitando a fila sem reprocessar mensagens que já tiveram sucesso.

---

### Anatomia do Evento CDC (DynamoDB Streams)

Um evento típico capturado pelo DynamoDB Streams possui a seguinte estrutura JSON:

```json
{
  "eventID": "c4ca4238a0b923820dcc509a6f75849b",
  "eventName": "MODIFY",
  "eventVersion": "1.1",
  "eventSource": "aws:dynamodb",
  "awsRegion": "us-east-1",
  "dynamodb": {
    "ApproximateCreationDateTime": 1773446400,
    "Keys": {
      "orderId": { "S": "ord-88921" },
      "customerId": { "S": "cust-4410" }
    },
    "OldImage": {
      "orderId": { "S": "ord-88921" },
      "customerId": { "S": "cust-4410" },
      "status": { "S": "PENDING_PAYMENT" },
      "totalAmount": { "N": "350.00" },
      "updatedAt": { "S": "2026-03-14T10:00:00Z" }
    },
    "NewImage": {
      "orderId": { "S": "ord-88921" },
      "customerId": { "S": "cust-4410" },
      "status": { "S": "PAYMENT_CONFIRMED" },
      "totalAmount": { "N": "350.00" },
      "updatedAt": { "S": "2026-03-14T10:02:15Z" }
    },
    "SequenceNumber": "4958000000000000000000001",
    "SizeBytes": 284,
    "StreamViewType": "NEW_AND_OLD_IMAGES"
  }
}
```

#### Vantagens de utilizar `NEW_AND_OLD_IMAGES`:
- Permite calcular o delta exato: identificar quais campos sofreram mutação (`status` alterado de `PENDING_PAYMENT` para `PAYMENT_CONFIRMED`).
- Evita consultas adicionais ao banco para saber o valor prévio.
- Suporta idempotência e validação de versão sem race conditions.

---

### Padrões de Resiliência: Idempotência e DLQ

1. **Garantia At-Least-Once e Idempotência**:
   - Mecanismos de mensageria distribuída (DynamoDB Streams, EventBridge, SQS) garantem entrega **pelo menos uma vez** (*at-least-once delivery*). Em cenários de timeout de rede ou reinicialização, o mesmo evento pode ser entregue mais de uma vez.
   - O consumidor Lambda deve ser rigorosamente **idempotente**. Utiliza-se a combinação de `orderId` + `SequenceNumber` (ou um campo de versão/hash) como chave de idempotência para garantir que reprocessamentos acidentais não gerem efeitos colaterais.

2. **Isolamento de Poison Pills com Dead Letter Queue (DLQ)**:
   - Uma mensagem malformada ou com dados corrompidos (*poison pill*) que cause erro não tratado repetidamente na função Lambda acionará a política de retentativa da SQS (`maxReceiveCount: 3`).
   - Após atingir o limite, a mensagem é automaticamente movida para a DLQ, liberando a fila principal para processar o fluxo normalmente sem travar o pipeline.

3. **Falhas Parciais em Lote (Report Batch Item Failures)**:
   - Ao processar um lote de 10 mensagens vindas da SQS, se apenas 1 mensagem falhar, o Lambda retorna o identificador específico dessa mensagem no objeto `batchItemFailures`. Apenas a mensagem com falha retorna para a fila para retentativa; as 9 mensagens bem-sucedidas são confirmadas e excluídas da fila.

---

## 📁 Estrutura do Módulo & Código Executável

Todo o código de exemplo e infraestrutura como código (IaC) deste estudo está estruturado na pasta [`examples/aws-serverless-cdc/`](./examples/aws-serverless-cdc):

- [`template.yaml`](./examples/aws-serverless-cdc/template.yaml): Template completo em AWS SAM / CloudFormation definindo a tabela DynamoDB com Stream, EventBridge Pipe, SQS com DLQ e função Lambda.
- [`src/order_processor.py`](./examples/aws-serverless-cdc/src/order_processor.py): Handler Lambda em Python demonstrando deserialização de CDC, cálculo de delta entre `OldImage` e `NewImage`, validação de idempotência e retorno de `batchItemFailures`.
- [`src/cdc_payload.json`](./examples/aws-serverless-cdc/src/cdc_payload.json): Arquivo de exemplo com payloads de `INSERT`, `MODIFY` e `REMOVE` para testes locais e simulação de eventos.
- [`examples/aws-serverless-cdc/README.md`](./examples/aws-serverless-cdc/README.md): Instruções detalhadas de implantação, testes locais e verificação.
