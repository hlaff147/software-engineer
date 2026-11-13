# 📘 Guia Didático: Padrões "Aggregate" em Microserviços

> **Desmistificando os dois conceitos mais confundidos na engenharia de software distribuída:**  
> 1. **Gateway Aggregation Pattern** *(Composição assíncrona de rede no API Gateway / BFF)*  
> 2. **DDD Aggregate Pattern** *(Fronteira de consistência transacional e integridade de domínio)*  
>
> *Implementação prática e executável com FastAPI, Docker Compose, PostgreSQL 16 (database-per-service), RFC 7807 e Transactional Outbox.*

---

## 📌 1. Por Que Existem Dois Padrões Chamados "Aggregate"?

Uma das fontes mais frequentes de confusão em entrevistas de System Design e discussões de arquitetura corporativa é o uso do termo **Aggregate**. 

Dependendo do contexto da conversa, o engenheiro pode estar falando de:
- **Rede / Composição de Serviços (Gateway Aggregation)**: "Juntar várias respostas de APIs diferentes em uma única resposta JSON para economizar idas e vindas de rede (*round-trips*) no cliente mobile/web."
- **Modelagem de Domínio / Consistência Transacional (DDD Aggregate)**: "Um cluster de objetos de domínio tratados como uma unidade atômica para garantir invariantes de negócio e integridade sob concorrência."

| Dimensão | 🌐 Gateway Aggregation Pattern | 🧱 DDD Aggregate Pattern |
|:---|:---|:---|
| **Origem** | Padrões de Integração Corporativa / Microservices (Chris Richardson, Martin Fowler) | Domain-Driven Design (Eric Evans) |
| **Problema que Resolve** | Clientes com conexões lentas fazendo dezenas de chamadas HTTP sequenciais (*over-the-wire chatter*). | Dificuldade em manter regras de negócio consistentes entre entidades associadas sob mutação concorrente. |
| **Fronteira (*Boundary*)** | **Fronteira de Rede / Comunicação RPC** entre serviços. | **Fronteira Transacional ACID** dentro de um único serviço/banco de dados. |
| **Mecanismo Central** | Fan-out assíncrono não bloqueante (`asyncio.gather` / Scatter-Gather) e junção de respostas (*merge*). | Encapsulamento estrito via **Aggregate Root** que intercepta toda e qualquer alteração de estado. |
| **Lei de Desempenho** | **"A latência da resposta é aproximadamente a do serviço mais lento, e não a soma de todas as chamadas."** | **"Transações não devem cruzar múltiplos agregados. Um agregado por transação ACID."** |
| **Principais Riscos** | Falhas em cascata, conexões presas por *slow downstreams*, alto acoplamento temporal. | Contenção de banco de dados sob alta concorrência (*lock contention*), raízes inchadas (*god aggregates*). |
| **Mitigações Necessárias** | Timeouts curtos, circuit breakers, respostas parciais degradadas (*graceful fallbacks*). | Controle de Concorrência Otimista (*Optimistic Locking* via `version`), Transactional Outbox para eventos. |

---

## 🌐 2. Padrão 1: Gateway Aggregation (Scatter-Gather)

### O Problema do Cliente Móvel
Imagine que para exibir a tela de detalhes de um produto em um aplicativo móvel (4G/5G com latência de rádio), o app precisasse chamar:
1. `GET /products/42` (100ms)
2. `GET /stock/42` (150ms)
3. `GET /reviews/42` (80ms)

Se o aplicativo fizer isso sequencialmente pela rede móvel:
$$\text{Latência Total} = 100\text{ms} + 150\text{ms} + 80\text{ms} = \mathbf{330\text{ms}} + 3 \times \text{RTT de rede móvel}$$

Além do tempo somado, o cliente consome bateria extra, gasta tráfego desnecessário e precisa lidar com 3 falhas de rede diferentes.

### A Solução da Gateway Aggregator
O cliente faz **uma única chamada** para o serviço agregador:
`GET /api/v1/pages/products/42`

O agregador dispara chamadas paralelas aos três microserviços em sua rede interna de alta velocidade (backbone com baixa latência) e une as respostas em um único payload:

```python
# Disparo concorrente não-bloqueante no Gateway
(
    (prod_res, prod_ms, prod_err),
    (inv_res, inv_ms, inv_err),
    (rev_res, rev_ms, rev_err),
) = await asyncio.gather(fetch_product(), fetch_inventory(), fetch_reviews())
```

$$\text{Latência Total} \approx \max(100\text{ms}, 150\text{ms}, 80\text{ms}) \approx \mathbf{150\text{ms}}$$

### Resiliência e Degradação Graciosa (*Graceful Fallbacks*)
Um agregador ingênuo falharia a tela inteira se qualquer serviço caísse. O `gateway-aggregator` deste laboratório implementa a **política de dependências críticas vs. não-críticas**:
- **Catálogo de Produtos (`product-service`) é CRÍTICO**: Se o produto não existe (404) ou o serviço caiu (503/504), não há tela para renderizar. O agregador responde imediatamente com RFC 7807 (`504 Gateway Timeout` ou `404 Not Found`).
- **Avaliações (`reviews-service`) é NÃO-CRÍTICO**: Se o serviço de reviews expirar o timeout, o agregador preenche a seção com nota `0.0`, lista vazia de avaliações, marca `is_fallback: true` e entrega a página com `composition_status: "degraded"`. O usuário ainda pode ver o preço e comprar o item!

---

## 🧱 3. Padrão 2: DDD Aggregate (Fronteira de Consistência)

### Por Que Entidades Soltas Falham em Consistência?
Se permitirmos que controladores ou serviços de aplicação alterem diretamente uma tabela `order_items` no banco de dados via SQL solto (`INSERT INTO order_items ...`), como garantir que:
1. O valor total do pedido não ultrapasse o teto financeiro do cliente?
2. A quantidade do SKU respeite o limite de 10 unidades por pedido?
3. O pedido não seja alterado após ter sido confirmado ou pago?
4. Duas requisições simultâneas não adicionem o mesmo SKU e gerem dados inconsistentes?

### A Solução: Aggregate Root (`Order`)
No Domain-Driven Design (DDD):
- O **Agregado** é o cluster formado por `Order` (Raiz) e suas `OrderLineItem`s (Entidades internas).
- **Referências externas apontam SOMENTE para a Raiz (`Order`)**: Ninguém fora do microserviço conhece ou acessa diretamente o ID interno de uma linha de item para mutação.
- **A coleção de itens é imutável para o exterior**: `order.items` retorna uma tupla `tuple[OrderLineItem, ...]`. Não é possível fazer `order.items.append(...)` nem burlar as regras da raiz.

```
┌───────────────────────────────────────────────────────────┐
│               DDD AGGREGATE BOUNDARY                      │
│                                                           │
│   ┌───────────────────────────────────────────────────┐   │
│   │             Order (AGGREGATE ROOT)                │   │
│   │  - id: OrderId                                    │   │
│   │  - total_amount: Money (Decimal exato)            │   │
│   │  - version: int (Optimistic Concurrency)          │   │
│   │  - status: DRAFT | CONFIRMED | CANCELLED          │   │
│   │                                                   │   │
│   │  Methods:                                         │   │
│   │  + add_item(product_id, sku, price, quantity)     │   │
│   │  + update_item_quantity(sku, new_quantity)        │   │
│   │  + remove_item(sku)                               │   │
│   │  + confirm()                                      │   │
│   │  + pull_domain_events()                           │   │
│   └─────────┬───────────────────────────────┬─────────┘   │
│             │ (owns & encapsulates)         │             │
│             ▼                               ▼             │
│   ┌───────────────────┐           ┌───────────────────┐   │
│   │   OrderLineItem   │           │   OrderLineItem   │   │
│   │ - sku: Sku        │           │ - sku: Sku        │   │
│   │ - qty: Quantity   │           │ - qty: Quantity   │   │
│   │ - subtotal: Money │           │ - subtotal: Money │   │
│   └───────────────────┘           └───────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

### Invariantes de Negócio Garantidas pelo Root
1. **Precisão Monetária**: Uso de `Decimal` quantizado com arredondamento `ROUND_HALF_UP` a 2 casas decimais. Impede desvios de precisão de ponto flutuante (IEEE 754).
2. **Teto Máximo por Pedido**: O somatório das linhas nunca pode ultrapassar `$50,000.00`.
3. **Limite por Linha**: A quantidade de um SKU nunca pode ultrapassar `10` unidades.
4. **Consolidação Automática**: Ao adicionar um SKU já existente, o agregado consolida as quantidades e recalcula o subtotal atomicamente.
5. **Máquina de Estados Finita**: Um pedido confirmado (`CONFIRMED`) ou cancelado (`CANCELLED`) torna-se imutável. Tentativas de adicionar, alterar ou remover itens disparam `InvalidOrderStateError` (`409 Conflict`).

### Concorrência Otimista (*Optimistic Locking*)
Quando múltiplos clientes ou processos tentam alterar o mesmo pedido simultaneamente, o repositório executa:
```sql
UPDATE orders
SET status = :status, version = :new_version
WHERE id = :id AND version = :loaded_version;
```
Se `rowcount == 0`, outro processo alterou o pedido no meio do caminho. A transação sofre *rollback* imediato e retorna HTTP `409 Conflict` (RFC 7807), protegendo o sistema contra condições de corrida (*lost updates*).

### Transactional Outbox
Toda transição do agregado grava eventos de domínio (`OrderCreated`, `OrderItemAdded`, `OrderConfirmed`) na tabela `order_outbox_events` **na mesmíssima transação ACID** que grava o pedido. Isso elimina o anti-padrão de *Dual Write* (gravar no banco e publicar na mensageria separadamente, correndo risco de dessincronização em caso de falha de rede).

---

## 🔄 4. Como os Dois Padrões Coexistem na Arquitetura

Os padrões não são excludentes; eles operam em camadas completamente diferentes:

1. O cliente chama o **Gateway Aggregator** pedindo a tela unificada de um pedido (`GET /api/v1/pages/orders/{id}`).
2. O Gateway consulta o **Order Service**, que carrega o **DDD Order Aggregate Root** do `orders_db` com todas as suas linhas de itens consistentes.
3. Para enriquecer o pedido com nomes atualizados e estoque em tempo real, o Gateway faz o *fan-out* concorrente para `product-service` e `inventory-service` usando os `product_id`s das linhas do pedido.
4. O cliente recebe uma visualização completa, rápida e resiliente, enquanto a consistência transacional do pedido foi estritamente preservada pelo Agregado DDD.

---

## 🧪 5. Laboratório Prático: Roteiro de Experimentos

### Experimento 1: Comprovando $T_{\text{parallel}} \approx \text{slowest call}$
Suba o ambiente com `make up` (ou `docker compose up -d`) e execute:

```bash
# Execução Sequencial: 80ms + 150ms + 100ms = ~330ms
curl -s "http://localhost:8000/api/v1/pages/products/42?mode=sequential&product_delay_ms=80&inventory_delay_ms=150&reviews_delay_ms=100" | python3 -m json.tool

# Execução Paralela: max(80ms, 150ms, 100ms) = ~150ms
curl -s "http://localhost:8000/api/v1/pages/products/42?mode=parallel&product_delay_ms=80&inventory_delay_ms=150&reviews_delay_ms=100" | python3 -m json.tool
```
*Observe a chave `telemetry.latency_saved_ms` demonstrando a economia empírica de latência.*

### Experimento 2: Queda Parcial e Fallback
```bash
curl -s "http://localhost:8000/api/v1/pages/products/42?fail_reviews=true" | python3 -m json.tool
```
*Observe que a resposta retorna HTTP 200, com `composition_status: "degraded"`, nota média `0.0` e `is_fallback: true` nas avaliações.*

### Experimento 3: Violação de Invariante no Agregado DDD
Tente adicionar 12 teclados em um pedido (limite é 10):
```bash
# Crie um pedido
ORDER_ID=$(curl -s -X POST "http://localhost:8004/api/v1/orders" -H "Content-Type: application/json" -d '{"customer_id":"cust-1","currency":"USD"}' | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

# Tente adicionar 12 unidades (invariante rejeita com RFC 7807 status 422)
curl -s -X POST "http://localhost:8004/api/v1/orders/$ORDER_ID/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id":43,"sku":"ACC-KEYBOARD-43","product_name":"Keyboard","unit_price":189.50,"quantity":12}' | python3 -m json.tool
```

### Experimento 4: Confirmação e Bloqueio de Mutações
```bash
# Adicione um item válido
curl -s -X POST "http://localhost:8004/api/v1/orders/$ORDER_ID/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id":42,"sku":"TECH-LAPTOP-42","product_name":"Laptop","unit_price":2499.00,"quantity":1}'

# Confirme o pedido
curl -s -X POST "http://localhost:8004/api/v1/orders/$ORDER_ID/confirm" | python3 -m json.tool

# Tente adicionar outro item após confirmação (rejeitado com RFC 7807 status 409)
curl -s -X POST "http://localhost:8004/api/v1/orders/$ORDER_ID/items" \
  -H "Content-Type: application/json" \
  -d '{"product_id":43,"sku":"ACC-KEYBOARD-43","product_name":"Keyboard","unit_price":189.50,"quantity":1}' | python3 -m json.tool
```
