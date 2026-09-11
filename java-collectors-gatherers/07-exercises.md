# Exercícios Práticos

> Exercícios para fixação dos conceitos de Collectors, Gatherers e programação funcional
> com Streams em Java.

---

## 📋 Instruções

- Cada exercício pode ser resolvido no [dev.java Playground](https://dev.java/playground/)
- Exercícios 1-4 requerem Java 8+, exercícios 5-7 requerem Java 24+ (Gatherers)
- Tente resolver sozinho antes de consultar as dicas!

---

## Exercício 1: Collector `last()`

Implemente um `Collector<T, ?, T>` chamado `last()` que retorna o **último** elemento
de uma stream. É o simétrico do `first()` visto no [módulo 02](./02-composing-collectors.md).

```java
<T> Collector<T, ?, T> last() {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = List.of("a", "b", "c", "d")
    .stream()
    .collect(last());
// Esperado: "d"
```

<details>
<summary>💡 Dica</summary>

O acumulador é bem mais simples que o `first()` — basta sempre substituir o valor
armazenado pelo novo elemento. Não precisa da `sealed interface Achei`.

Considere usar um array de tamanho 1 como container mutável: `new Object[]{null}`.
</details>

---

## Exercício 2: Collector de Contagem por Chave

Implemente um Collector que agrupa elementos por uma chave e conta quantas vezes
cada chave aparece, retornando `Map<K, Long>`.

```java
<T, K> Collector<T, ?, Map<K, Long>> countByKey(Function<T, K> classifier) {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = List.of("a", "bb", "c", "dd", "eee", "f")
    .stream()
    .collect(countByKey(String::length));
// Esperado: {1=3, 2=2, 3=1}
```

<details>
<summary>💡 Dica</summary>

Você pode resolver de duas formas:
1. **Composição**: `Collectors.groupingBy(classifier, Collectors.counting())`
2. **From scratch**: use `HashMap<K, long[]>` como acumulador e incremente

Tente ambas!
</details>

---

## Exercício 3: Gatherer `distinctBy`

Implemente um Gatherer que filtra elementos mantendo apenas o primeiro com cada
valor distinto de uma propriedade extraída pela função `classifier`.

```java
<T, K> Gatherer<T, ?, T> distinctBy(Function<T, K> classifier) {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = Stream.of("apple", "ant", "banana", "bat", "cherry")
    .gather(distinctBy(s -> s.charAt(0)))
    .toList();
// Esperado: ["apple", "banana", "cherry"]
```

<details>
<summary>💡 Dica</summary>

Muito similar ao gatherer `ineditos()` do [módulo 05](./05-ineditos-repetidos.md).
Use `HashSet<K>` como estado e `state.add(classifier.apply(element))` para decidir.
</details>

---

## Exercício 4: Collector para Particionamento Customizado

Implemente um Collector que separa elementos em dois grupos baseado em um predicado,
retornando um `record Partition<T>(List<T> matching, List<T> notMatching)`.

```java
record Partition<T>(List<T> matching, List<T> notMatching) {}

<T> Collector<T, ?, Partition<T>> partitionBy(Predicate<T> predicate) {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = List.of(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    .stream()
    .collect(partitionBy(n -> n % 2 == 0));
// Esperado: Partition[matching=[2, 4, 6, 8, 10], notMatching=[1, 3, 5, 7, 9]]
```

<details>
<summary>💡 Dica</summary>

O acumulador pode ser uma classe interna com duas listas. O `finisher` cria o record
`Partition` a partir delas. Compare com `Collectors.partitioningBy()`.
</details>

---

## Exercício 5: Gatherer `windowFixed`

Implemente um Gatherer que agrupa elementos em sub-listas (janelas) de tamanho fixo `N`.
A última janela pode ter menos de `N` elementos.

```java
<T> Gatherer<T, ?, List<T>> windowFixed(int size) {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = Stream.of(1, 2, 3, 4, 5, 6, 7)
    .gather(windowFixed(3))
    .toList();
// Esperado: [[1, 2, 3], [4, 5, 6], [7]]
```

<details>
<summary>💡 Dica</summary>

Use `ArrayList<T>` como estado. No integrator, adicione o elemento à lista.
Quando a lista atingir `size`, faça `ds.push(List.copyOf(state))`, limpe o estado,
e continue. No `finisher`, empurre os elementos restantes se houver.
</details>

---

## Exercício 6: Gatherer `flatMap`

Reimplemente a operação `flatMap` como um Gatherer. Ela recebe uma função que mapeia
cada elemento para uma Stream e aplaina o resultado.

```java
<T, R> Gatherer<T, ?, R> flatMap(Function<T, Stream<R>> mapper) {
    // Sua implementação aqui
}
```

**Teste:**
```java
var resultado = Stream.of("hello world", "foo bar baz")
    .gather(flatMap(s -> Stream.of(s.split(" "))))
    .toList();
// Esperado: ["hello", "world", "foo", "bar", "baz"]
```

<details>
<summary>💡 Dica</summary>

É um gatherer stateless — não precisa de `initializer`. No integrator, aplique a
função ao elemento, itere sobre a Stream resultante e faça `push` de cada sub-elemento.
Atenção: verifique `ds.isRejecting()` após cada push!
</details>

---

## Exercício 7: Caso Real — Detecção de Transações Duplicadas

Dado um fluxo de transações financeiras, use collectors e/ou gatherers para:

1. Separar transações com IDs únicos (válidas) das duplicadas
2. Para as duplicadas, contar quantas vezes cada ID apareceu
3. Retornar um `TransactionReport` com os resultados

```java
record Transaction(String id, double amount, String status) {}

record TransactionReport(
    List<Transaction> valid,
    List<Transaction> duplicates,
    Map<String, Long> duplicateCountById
) {}

TransactionReport analyzeTransactions(List<Transaction> transactions) {
    // Sua implementação aqui usando collectors/gatherers
}
```

**Dados de teste:**
```java
var transactions = List.of(
    new Transaction("TX001", 100.0, "APPROVED"),
    new Transaction("TX002", 200.0, "APPROVED"),
    new Transaction("TX001", 150.0, "PENDING"),    // duplicada
    new Transaction("TX003", 300.0, "APPROVED"),
    new Transaction("TX002", 250.0, "REJECTED"),   // duplicada
    new Transaction("TX001", 175.0, "APPROVED"),   // duplicada
    new Transaction("TX004", 400.0, "APPROVED")
);
```

**Resultado esperado:**
```
valid:      [TX001(100.0), TX002(200.0), TX003(300.0), TX004(400.0)]
duplicates: [TX001(150.0), TX002(250.0), TX001(175.0)]
duplicateCountById: {TX001=2, TX002=1}
```

<details>
<summary>💡 Dica</summary>

Combine os conceitos dos módulos 02, 03 e 05:
- Use `groupingBy(Transaction::id)` para agrupar por ID
- Use `collectingAndThen` para extrair inéditos (primeiro de cada grupo)
- Use `flatMap(l -> l.stream().skip(1))` para os repetidos
- Use `Collectors.counting()` para a contagem

Ou, se preferir a abordagem moderna, combine os gatherers `ineditos()` e `repetidos()`
com operações adicionais de stream.
</details>

---

## 🏆 Desafio Bônus: Pipeline Completa

Combine **pelo menos 3 técnicas** diferentes deste guia para resolver o seguinte:

Dado um log de eventos `record Event(String userId, String action, Instant timestamp)`:

1. Usando um **gatherer**: filtre apenas os eventos das últimas 24h
2. Usando um **collector composto**: agrupe por `userId` e pegue apenas a **primeira** ação de cada usuário
3. Usando um **collector from scratch**: construa um `Map<String, List<String>>` onde a chave é a ação e o valor é a lista de userIds que fizeram aquela ação primeiro
4. O resultado final deve preservar a ordem cronológica dos eventos

---

## 📊 Checklist de Auto-Avaliação

| Conceito | Exercício | Dominei? |
|----------|:---------:|:--------:|
| `Collector.of()` com tipos genéricos | 1, 2, 4 | ☐ |
| Composição com `groupingBy` + `collectingAndThen` | 2, 7 | ☐ |
| `sealed interface` para estado do collector | 1 | ☐ |
| `Gatherer.ofSequential` com estado | 3, 5 | ☐ |
| `Gatherer.Integrator.ofGreedy` | 3, 5, 6 | ☐ |
| `finisher` no Gatherer | 5 | ☐ |
| `Downstream.push()` e `isRejecting()` | 3, 5, 6 | ☐ |
| Combinar collectors + gatherers em pipeline real | 7, Bônus | ☐ |

---

## 🔗 Referências

- [01 - Collector API Anatomy](./01-collector-api-anatomy.md)
- [02 - Composing Collectors](./02-composing-collectors.md)
- [03 - Custom Collector from Scratch](./03-custom-collector-from-scratch.md)
- [04 - Gatherer API Anatomy](./04-gatherer-api-anatomy.md)
- [05 - Inéditos vs Repetidos](./05-ineditos-repetidos.md)
- [06 - Streams from Scratch](./06-streams-from-scratch.md)
- [dev.java Playground](https://dev.java/playground/)
