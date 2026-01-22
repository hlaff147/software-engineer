# MongoDB vs PostgreSQL — Perguntas comuns

> Para uma visão técnica consolidada sobre fundamentos, veja: [CAP, ACID e Locks](cap-acid-locks.md)

## 1) Quando usar PostgreSQL?

**Resposta curta:** quando você precisa de **consistência forte**, transações ricas, joins, relatórios e modelo relacional bem definido.

**Gatilhos:** ACID, integridade referencial, constraints, queries complexas, BI/reporting.

**Exemplos típicos:** contas/ledger, pedidos/pagamentos, inventário, relatórios.

---

## Contexto adicional: ACID em detalhe

**Atomicidade:** garante que um conjunto de operações dentro de uma transação é tratado como uma única unidade — ou tudo é aplicado, ou nada. Ex.: transferência bancária deve debitar e creditar ou reverter tudo.

**Consistência (ACID):** significa que transações preservam restrições do banco (FKs, constraints, triggers). Não confundir com "consistência" do CAP (consistência de réplica).

**Isolamento:** níveis comuns:
- `Read Uncommitted` — leituras sujas possíveis;
- `Read Committed` — leituras só de dados confirmados (padrão em muitos DBs);
- `Repeatable Read` — leituras repetidas veem os mesmos dados dentro da tx;
- `Serializable` — nível mais forte que evita anomalias de concorrência.

**Durabilidade:** uma vez confirmada, a transação persiste (WAL, fsync). Em produção, configurar políticas de flush/replication é crítico.

**Exemplo prático (PostgreSQL):** um sistema financeiro configura `SERIALIZABLE` ou implementa controlos de aplicação com `SELECT ... FOR UPDATE` para evitar condições de corrida.

---

## 2) Quando usar MongoDB?

**Resposta curta:** quando o modelo é **documental**, com schema flexível, leitura por agregados, e você quer evoluir campos rapidamente.

**Gatilhos:** documento como agregado, menos joins, denormalização, alto volume de escrita, JSON natural.

**Exemplos típicos:** perfil do usuário, catálogos flexíveis, eventos, logs.

---

## Quando escolher Mongo vs PostgreSQL — checklist prático
- Se precisar de transações complexas, integridade referencial e isolamento forte: inclinar para **PostgreSQL**.
- Se o domínio é documento/agregado, com campos que evoluem rápido e leitura orientada a um único documento: **MongoDB** pode ser mais produtivo.
- Se precisa de geoespacial rico e análises espaciais: **PostGIS** (PostgreSQL) normalmente vence.
- Para busca textual e pesquisa em código (full search) em larga escala considere engines dedicadas (Elasticsearch/OpenSearch, Zoekt, Sourcegraph) — ver seção abaixo.

---

## 3) “Mongo não tem transação?” (mais detalhes)

Hoje o MongoDB suporta transações multi-documento com ACID quando usado em replica sets e clusters. Pontos a considerar:
- Transações têm custo em latência e uso de recursos — prefira modelagem por agregado quando possível.
- Use `readConcern` e `writeConcern` para ajustar consistência/replicação.
- Para workloads de alto volume de escrita, modelar para operações dentro de um único documento (atomicidade implícita) é mais eficiente.

---

## 4) Como escolher entre normalização e denormalização?

## 3) “Mongo não tem transação?”

**Resposta curta:** tem transações multi-documento (há anos), mas o custo/uso deve ser avaliado; o modelo ideal ainda é orientar por documento/agregado.

**Gatilhos:** trade-off de performance, desenho do schema.

---

## 4) Como escolher entre normalização e denormalização?

**Resposta curta:** no relacional, normalizar para integridade e reduzir inconsistências; em documento, denormalizar para leitura rápida e reduzir joins.

**Gatilhos:** padrões de acesso, consistência, custo de atualização, tamanho do documento.

**Exemplos práticos:**
- E-commerce: catálogo de produto geralmente denormalizado no Mongo (preço, atributos, imagens) para leitura rápida; pedidos (ordens) em Postgres para integridade e histórico financeiro.
- Catálogo multivariado: se variantes mudam independentemente, normalize (Postgres) ou mantenha referência e materialize views.

---

## 5) Consistência eventual vs forte: explicar com exemplos

**Consistência forte:** após confirmação, leituras retornam o valor mais recente. Ex.: saldo bancário deve ser fortemente consistente — leitura depois de commit mostra o novo saldo.

**Consistência eventual:** réplicas podem estar atrasadas; ideal quando disponibilidade e latência são mais importantes que ver o valor imediatamente. Ex.: timeline de redes sociais — pequenos atrasos aceitáveis.

**Aplicação prática (Mongo/Postgres):**
- Mongo: pode fornecer leituras de réplicas com maior latência para consistência; `readPreference` controla comportamento.
- Postgres: em configuração primária-secundária, leituras em réplicas podem ser eventualmente consistentes; soluções de replicação síncrona (sync replication) aumentam latência mas garantem forte consistência.

---

## 5) Consistência eventual vs forte: como explicar?

**Resposta curta:** forte garante leitura do valor mais recente após confirmação; eventual permite atrasos, mas melhora disponibilidade/latência em sistemas distribuídos.

**Gatilhos:** CAP na prática, replicação, leitura de réplicas, caches.

---

## 6) O que olhar na modelagem (checklist rápido)?

**Resposta curta:** comece pelos casos de uso e queries.

**Gatilhos:**
- chaves e índices (cardinalidade)
- crescimento (TTL/arquivamento)
- concorrência e lock/contention
- estratégia de migração de schema

---

## 7) Casos de uso detalhados — PostgreSQL

- **Financeiro / Ledger:** transações bancárias, contabilidade — exige ACID, constraints, auditoria. Use `SERIALIZABLE` ou patterns de aplicação com `SELECT ... FOR UPDATE`.
- **E-commerce / pedidos:** integridade de estoque, pagamentos; combina transações com índices compósitos e FK.
- **Relatórios e BI:** consultas analíticas complexas, joins e agregações; materialized views e `EXPLAIN` para otimização.
- **Time-series:** com `TimescaleDB` (extensão) para métricas, particionamento por chunk e compressão.
- **Geo-spatial / mapas:** com `PostGIS` para geometria, rotas, buffers e índices espaciais GiST/SP-GiST.
- **Full-text Search (moderado):** `tsvector` + GIN index para pesquisa textual integrada; bom para busca em conteúdo de aplicação.

Observações: PostgreSQL tem ecossistema rico (extensões, FDW, stored procedures, tipos JSONB) permitindo soluções híbridas.

---

## 8) Casos de uso detalhados — MongoDB

- **Perfis de usuário / Preferências:** esquemas que mudam com frequência; perfis com campos opcionais e histórico.
- **Catálogo de produtos flexível:** atributos variáveis por categoria; documentos aninhados para reviews, imagens, variantes.
- **Eventos / logs de alta ingestão:** escrita intensiva, agregação posterior; TTL para expurgo automático.
- **CMS / conteúdo:** modelos heterogêneos, publicação rápida de campos novos.
- **Sessões e caches:** documentos pequenas e de acesso rápido.

Observações: para consultas complexas ou joins pesados, reavalie se denormalização ou pipelines de agregação resolvem; use transações apenas quando necessidade de multi-documento for explícita.

---

## 9) PostGIS — por que e quando usar

**O que é:** extensão do PostgreSQL para dados espaciais (vetor e raster), adicionando tipos (`GEOMETRY`, `GEOGRAPHY`) e centenas de funções (`ST_Intersects`, `ST_Distance`, `ST_Buffer`).

**Recursos chave:**
- Índices espaciais (GiST, SP-GiST) para consultas rápidas;
- Operadores topológicos e métricas (interseção, sobreposição, distância);
- Suporte a SRIDs e transformação entre projeções;
- Integração com `pgrouting` para rotas.

**Casos de uso:** logística (áreas de cobertura, roteamento), mapas (tiles), geofencing, análise de proximidade, armazenar trilhas GPS.

**Dica de performance:** indexe geometria com GiST e use consultas bounding-box (`&&`) antes de operações caras.

---

## 10) Full-text e busca em código ("full search") — cenário: buscar a palavra X em muitos repositórios/branches

**Desafio:** pesquisar texto (ou código) em dezenas de milhões de arquivos, múltiplos branches e repositórios, com filtros por linguagem, path e contexto.

**Componentes de arquitetura comuns:**
- **Crawler / Ingestor:** clona ou recebe eventos (push/commit), extrai arquivos relevantes e diffs;
- **Tokenizer / Normalizer:** quebra código em tokens; trata linguagens diferentes, remove binários, normaliza paths;
- **Indexer (inverted index):** mapeia termos → postings (arquivo, repo, commit, location);
- **Storage / Sharding:** índice particionado por repo/namespace; replicas para disponibilidade;
- **Query Service:** aceita consultas (palavra, regex, structural search), combina resultados, aplica ranking;
- **Updater:** ingestão incremental de commits/branches para manter frescor.

**Ferramentas e projetos:** Sourcegraph (arquitetura para código), Zoekt (indexador focado em código), OpenGrok, soluções baseadas em Elasticsearch/Lucene para texto geral.

**Ranking e features:** contar ocorrências, proximidade, correspondência exata, reconhecimento de símbolos/AST para "structural search".

**Trade-offs:**
- *Frescura vs custo:* indexar cada commit em tempo real consome recursos; muitos sistemas optam por latência de minutos/hours.
- *Armazenamento:* índices invertidos crescem rápido; compressão e deduplicação são importantes.
- *Complexidade da query:* regex e structural search são mais lentos — pré-indexar tokens ou AST ajuda.

**Exemplo simples com Elasticsearch (arquivos de código):**
- Indexar documentos com campos: `repo`, `branch`, `path`, `content` (analisador custom para código), `lang`.
- Usar shard por `repo` ou por `namespace` para distribuir carga;
- Para buscas por palavra X: consulta `match` sobre `content` ordenada por `repo`/`path` relevância.

**Exemplo com Postgres (menor escala):**
- Criar coluna `tsv` com `to_tsvector('simple', content)` e índice GIN;
- Pesquisar com `to_tsquery('X')` ou `plainto_tsquery` e filtros por `repo`/`branch`.
- Limitação: Postgres funciona bem até certa escala; para dezenas/milhares de repositórios com histórico extenso preferir engine dedicada.

---

## 11) Recomendações rápidas

- Use **PostgreSQL + PostGIS** para workloads que exigem integridade, consultas espaciais e análises complexas.
- Use **MongoDB** quando o domínio favorece documentos flexíveis, alta ingestão e evolução rápida do schema.
- Para **busca em código/full search** em larga escala, prefira uma engine dedicada (Zoekt/Sourcegraph/Elasticsearch) com pipeline de ingestão e indexação incremental.

---

Se quiser, aplico ajustes no tom (mais técnico ou mais didático), adiciono exemplos de DDL/queries (`tsvector`, `GIN`, `ST_Intersects`) ou insiro referências para projetos (Sourcegraph, Zoekt).
