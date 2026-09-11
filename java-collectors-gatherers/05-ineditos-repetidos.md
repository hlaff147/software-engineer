# Caso Completo: Inéditos vs Repetidos

Este é o módulo central do guia — aqui reunimos tudo que aprendemos sobre Collectors e Gatherers
aplicados a um problema real de refatoração.

---

## 📋 O Problema

Dado um `List<AlgumObjeto>`, onde cada objeto possui uma `key()`, queremos:

1. **Inéditos**: o primeiro objeto que aparece com cada chave distinta
2. **Repetidos**: todos os objetos que aparecem com uma chave já vista

```java
// record AlgumObjeto(String key, ...) {}
Set<AlgumObjeto> detectaInvalidos(List<AlgumObjeto> todosObjetos) {
    Set<AlgumObjeto> invalidos = new HashSet<>();
    Set<String> chavesValidas = new HashSet<>();

    for (final var o: todosObjetos) {
        final var k = o.key();
        if (!chavesValidas.add(k)) {
            invalidos.add(o);
        }
    }

    return invalidos;
}

List<AlgumObjeto> todosObjetos = ...;
Set<AlgumObjeto> invalidos = detectaInvalidos(todosObjetos);

// log dos invalidos

List<AlgumObjeto> validos = new ArrayList<>(todosObjetos);
validos.removeAll(invalidos);

return validos;
```

A pergunta que originou o artigo: **será que a gente consegue transformar isso em um coletor?**

---

## 🎯 Assinatura Desejada

O coletor deve ter a seguinte assinatura:

```java
Collector<T, ?, List<T>>
```

Onde:
- `T` = o elemento que chega e é processado
- `?` = estado intermediário (irrelevante para o chamador)
- `List<T>` = resultado final

Além disso, precisamos de um **discriminador** — a função que extrai a chave:

```java
Function<T, K> classifier
```

---

## 1️⃣ Inéditos com Collectors Compostos

### Abordagem Imperativa

```java
List<T> elementos = ...;
Function<T, K> classifier = ...;

final var grupos = elementos.stream().collect(Collectors.groupingBy(classifier));

return grupos.values()
    .stream()
    .map(List::getFirst)
    .toList();
```

### Usando `collectingAndThen`

```java
final var resultado = elementos.stream()
    .collect(
        Collectors.collectingAndThen(
            Collectors.groupingBy(classifier),
            grupos -> grupos.values()
                            .stream()
                            .map(List::getFirst)
                            .toList()
        )
    );
```

### Usando `groupingBy` com downstream `first()`

Ao invés de coletar listas inteiras e pegar o primeiro, podemos usar um collector
`first()` como downstream do `groupingBy`:

```java
<T, K> Collector<T, ?, List<T>> firstFromKind(Function<T, K> classifier) {
    return Collectors.collectingAndThen(
        Collectors.groupingBy(classifier, first()),
        grupos -> List.copyOf(grupos.values())
    );
}
```

> Para a implementação do `first()` com a sealed interface `Achei`, veja o
> [módulo 02](./02-composing-collectors.md).

---

## 2️⃣ Inéditos com Collector Próprio (from scratch)

Usando `LinkedHashMap` diretamente como acumulador:

```java
<T, K> Collector<T, ?, List<T>> firstFromKind(Function<T, K> classifier) {
    return Collector.of(
        LinkedHashMap<K, T>::new,
        (a, t) -> a.putIfAbsent(classifier.apply(t), t),
        (x, y) -> {
            for (final var es: y.entrySet()) {
                x.putIfAbsent(es.getKey(), es.getValue());
            }
            return x;
        },
        a -> List.copyOf(a.values())
    );
}
```

**Por que funciona?**
- `LinkedHashMap` preserva a ordem de inserção
- `putIfAbsent` só insere se a chave ainda não existir → captura o primeiro de cada tipo
- O `finisher` apenas extrai os valores em ordem

> Para mais detalhes, veja o [módulo 03](./03-custom-collector-from-scratch.md).

---

## 3️⃣ Repetidos com Collectors

### Evolução da Solução

**Tentativa 1 — SubList:**
```java
Collectors.collectingAndThen(
    Collectors.groupingBy(classifier),
    grupos -> grupos.values()
        .stream()
        .map(l -> l.subList(1, l.size()))
        .toList()
);
```
❌ Problema: `subList(1, l.size())` falha se a lista estiver vazia.

**Tentativa 2 — Filter + SubList:**
```java
Collectors.collectingAndThen(
    Collectors.groupingBy(classifier),
    grupos -> grupos.values()
        .stream()
        .filter(Predicate.not(List::isEmpty))
        .map(l -> l.subList(1, l.size()))
        .toList()
);
```
✅ Funciona, mas retorna `List<List<T>>` — precisa aplainar.

**Tentativa 3 — Filter + SubList + FlatMap:**
```java
Collectors.collectingAndThen(
    Collectors.groupingBy(classifier),
    grupos -> grupos.values()
        .stream()
        .filter(Predicate.not(List::isEmpty))
        .map(l -> l.subList(1, l.size()))
        .flatMap(List::stream)
        .toList()
);
```
✅ Funciona! Mas pode ser simplificado...

**Solução Final — skip(1):**
```java
Collectors.collectingAndThen(
    Collectors.groupingBy(classifier),
    grupos -> grupos.values()
        .stream()
        .flatMap(l -> l.stream().skip(1))
        .toList()
);
```
✅ Elegante! O `skip(1)` em uma stream vazia não causa erro, eliminando a necessidade
do filtro e da sublista.

### Por que o collector próprio é mais difícil para repetidos?

Ao tentar criar um collector from scratch para repetidos, seria necessário manter o
primeiro elemento de cada chave (para o combiner saber o que descartar), tornando a
lógica bem complicada. Por isso, a abordagem com `groupingBy` + `stream().skip(1)` é
a **canônica** para repetidos.

---

## 4️⃣ Inéditos com Gatherer

Usando Gatherers (Java 24+), podemos tratar isso como operação intermediária:

```java
<T, K> Gatherer<T, ?, T> ineditos(Function<T, K> classifier) {
    return Gatherer.ofSequential(
        HashSet<K>::new,
        Gatherer.Integrator.ofGreedy((state, element, ds) -> {
            final var k = classifier.apply(element);
            if (state.add(k)) {
                return ds.push(element);
            }
            return !ds.isRejecting();
        })
    );
}
```

**Teste:**
```java
List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    .stream()
    .gather(ineditos(i -> i % 3))
    .toList();
// Resultado: [1, 2, 3]
```

**Vantagem**: o resultado continua como stream, permitindo mais operações downstream!

---

## 5️⃣ Repetidos com Gatherer

A versão para repetidos é simétrica — inverte a lógica do `if`:

```java
<T, K> Gatherer<T, ?, T> repetidos(Function<T, K> classifier) {
    return Gatherer.ofSequential(
        HashSet<K>::new,
        Gatherer.Integrator.ofGreedy((state, element, ds) -> {
            final var k = classifier.apply(element);
            if (state.add(k)) {
                return !ds.isRejecting();
            }
            return ds.push(element);
        })
    );
}
```

**Teste:**
```java
List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    .stream()
    .gather(repetidos(i -> i % 3))
    .toList();
// Resultado: [4, 5, 6, 7, 8, 9, 10, 11, 12]
```

---

## 🔍 A Beleza da Simetria

Compare o código imperativo original com o gatherer de repetidos:

### Imperativo

```java
Set<String> chavesValidas = new HashSet<>();   // estado criado fora do laço
for (final var o: todosObjetos) {
    final var k = o.key();
    if (!chavesValidas.add(k)) {               // se NÃO adicionou (já existia)
        invalidos.add(o);                      // coleta o elemento
    }
}
```

### Gatherer

```java
(state, element, ds) -> {
    final var k = classifier.apply(element);
    if (state.add(k)) {                        // se adicionou (inédito)
        return !ds.isRejecting();              // ignora (não empurra)
    }
    return ds.push(element);                   // empurra (repetido)
}
```

> A estrutura muda um pouco, mas a **essência é idêntica**:
> - Estado externo alimentado dentro do laço → `state` do gatherer
> - Decisão baseada em `set.add()` → mesma lógica
> - Coletar vs ignorar → `ds.push()` vs `!ds.isRejecting()`
>
> A única adição no gatherer é verificar se o downstream parou de aceitar
> (`isRejecting`), algo impossível na iteração tradicional.

---

## 📊 Resumo Comparativo

| Abordagem | Tipo | Retorna | Complexidade | Para Inéditos | Para Repetidos |
|-----------|------|---------|--------------|:---:|:---:|
| Imperativa (loop) | — | `Set<T>` / `List<T>` | Baixa | ✅ | ✅ |
| `groupingBy` + `collectingAndThen` | Collector | `List<T>` | Média | ✅ | ✅ |
| `groupingBy` + `first()` | Collector | `List<T>` | Média-alta | ✅ | ❌ |
| `LinkedHashMap` from scratch | Collector | `List<T>` | Média | ✅ | ❌ (complexo) |
| `Gatherer.ofSequential` | Gatherer | `Stream<T>` | Baixa | ✅ | ✅ |

> **Takeaway**: Gatherers oferecem a solução mais natural e simétrica. Para collectors,
> a composição com `groupingBy` é mais pragmática que construir from scratch, especialmente
> para o caso dos repetidos.

---

## 🔗 Referências

- [Collector API](./01-collector-api-anatomy.md) — Módulo 01
- [Composing Collectors](./02-composing-collectors.md) — Módulo 02
- [Custom Collectors](./03-custom-collector-from-scratch.md) — Módulo 03
- [Gatherer API](./04-gatherer-api-anatomy.md) — Módulo 04
