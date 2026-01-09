# Java — Perguntas comuns (respostas curtas)

## 1) O que é imutabilidade e por que importa?

**Resposta curta:** objeto imutável não muda estado após criado; reduz bugs, facilita concorrência e caching.

**Gatilhos (o que mencionar):**
- `final`: referência/campo não pode apontar pra outro objeto (mas o objeto pode ser mutável se ele expõe estado).
- Sem setters + campos privados: estado só é definido no construtor/factory; invariantes ficam fáceis de manter.
- Coleções defensivas: ao receber/retornar `List/Map`, copiar ou retornar versões imutáveis para não “vazarem” mutabilidade.
- *Thread-safety*: se o objeto não muda, ele pode ser compartilhado entre threads sem sincronização.
- *Value object*: igualdade baseada em valores (ex.: `Money`, `Email`), ótimo para domínio e para usar como chave de `Map`.

**Quando citar:** `String`, `LocalDate`, DTOs, chaves de `Map`.

---

## 2) `equals` e `hashCode`: qual contrato?

**Resposta curta:** objetos “iguais” por `equals` devem ter o mesmo `hashCode`; `hashCode` otimiza buckets, `equals` confirma igualdade.

**Gatilhos (o que mencionar):**
- Consistência: se nada mudou no objeto, chamadas repetidas de `equals/hashCode` devem dar o mesmo resultado.
- Reflexivo/simétrico/transitivo: `a.equals(a)`; `a.equals(b) == b.equals(a)`; e se `a==b` e `b==c` então `a==c`.
- Nulos: `a.equals(null)` deve ser `false`.
- Campos mutáveis em chaves: se `hashCode` depende de um campo que muda, o objeto “some” do bucket do `HashMap/HashSet`.

**Armadilhas:** alterar campo usado no `hashCode` após inserir em `HashMap`.

---

## 3) `HashMap` vs `ConcurrentHashMap`?

**Resposta curta:** `HashMap` não é seguro em concorrência; `ConcurrentHashMap` fornece operações thread-safe com melhor escalabilidade.

**Gatilhos (o que mencionar):**
- *Read-heavy*: `ConcurrentHashMap` escala melhor quando há muitas leituras e algumas escritas concorrentes.
- `computeIfAbsent`: forma segura/atômica de “criar se não existir” sem condição de corrida.
- Locks internos: evita um lock global único; operações comuns (ex.: `get`) têm baixa contenção.
- Evitar `Collections.synchronizedMap`: funciona, mas geralmente vira gargalo por serializar tudo num lock só.

---

## 4) O que é GC e o que costuma cair em entrevista?

**Resposta curta:** Garbage Collector gerencia memória no heap; você precisa entender *allocation*, *pausas* e como evitar “lixo” desnecessário.

**Gatilhos (o que mencionar):**
- Heap vs stack: objetos vivem no heap; stack guarda frames/referências (e influencia no escopo/vida das referências).
- *Stop-the-world*: pausas acontecem; o que importa é entender impacto em latência (p99) e como reduzir “churn”.
- Muitos objetos temporários: alta taxa de alocação gera pressão no GC (ex.: streams mal usadas, concatenação de `String`).
- `StringBuilder`: preferir em loops/concatenação repetida para reduzir lixo.
- Pools com cautela: pool pode piorar (retenção, complexidade); só vale quando há motivo (objetos caros/escassos) e medição.

---

## 5) Checked vs unchecked exceptions: quando usar?

**Resposta curta:** checked para condições esperadas e recuperáveis (com parcimônia); unchecked para erros de programação/violação de contrato.

**Gatilhos (o que mencionar):**
- Ergonomia de API: checked “força” tratamento/propagação; pode poluir assinaturas quando a recuperação real não é possível.
- “Exceção como fluxo”: evitar usar exception para controle normal (ex.: parse/validação em massa) — preferir retorno/`Optional`/resultado.
- Domínio vs infraestrutura: domínio pode ter exceções específicas (ex.: `SaldoInsuficiente`), infraestrutura vira `RuntimeException`/wrapping e vira erro 5xx.

---

## 6) O que é *idempotência* e por que é relevante em microserviços?

**Resposta curta:** repetir a mesma requisição não pode gerar efeitos colaterais adicionais; essencial para retries e eventos.

**Gatilhos (o que mencionar):**
- `idempotency-key`: cliente manda uma chave única por tentativa lógica; servidor guarda resultado e devolve o mesmo em retries.
- Deduplicação: store de “request id / event id” + status para garantir “processar uma vez” do ponto de vista do negócio.
- *At-least-once*: brokers e retries tendem a entregar/processar mais de uma vez; idempotência evita efeitos duplicados.
- *Outbox*: grava estado + evento na mesma transação; depois publica com reprocessamento seguro (evita perder evento e reduz duplicidade).
