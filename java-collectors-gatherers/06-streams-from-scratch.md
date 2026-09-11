# Reinventando Streams do Zero

Este módulo resume como as Streams do Java funcionam por dentro, reimplementando-as
do zero a partir de `Iterable<T>`, emulando a semântica da Stream API em cenários de runtime restrito.

---

## 📋 Contexto: Java 7 e as Limitações

No mundo do Java 7:
- ❌ Não existiam Streams
- ❌ Não existiam lambdas (classes anônimas eram a alternativa, mas muito verbosas)
- ❌ Não existiam métodos `default` em interfaces
- ❌ Não existiam métodos estáticos em interfaces
- ✅ Interfaces funcionais do Java 8 (`Supplier`, `Consumer`, `Function`) eram acessíveis via [Retrolambda](https://github.com/luontola/retrolambda)

**Objetivo**: Criar uma API stream-like que pudesse ser usada com lambdas no Java 7.

---

## 🏗️ A Base: `Iterable<T>` e `Iterator<T>`

Tudo começa com o `Iterable<T>`, que tem um único método: `iterator()` retornando um `Iterator<T>`.

O `Iterator<T>` é uma estrutura **mutável** com dois métodos:
- `hasNext()` — indica se existe um próximo elemento
- `next()` — retorna o elemento atual e avança o ponteiro

```java
public class Stream<T> {
    private final Iterable<T> it;

    public Stream(Iterable<T> it) {
        this.it = it;
    }

    // intermediate operations

    // terminal operations

    // factories
}
```

---

## ⚡ Operações Terminais

### `forEach`

A operação mais simples — apenas consome cada elemento:

```java
public void forEach(Consumer<T> action) {
    for (T t: it) {
        action.accept(t);
    }
}
```

### `reduce`

Redução com valor inicial e operador binário:

```java
public T reduce(T identity, BinaryOperator<T> accumulator) {
    T result = identity;
    for (T t: it) {
        result = accumulator.apply(result, t);
    }
    return result;
}
```

### `collect`

A operação terminal que conecta com Collectors:

```java
public <R, A> R collect(Collector<T, A, R> collector) {
    A container = collector.supplier().get();
    for (T t: it) {
        collector.accumulator().accept(container, t);
    }
    return collector.finisher().apply(container);
}
```

> **Nota**: Esta é a versão sequencial. A versão paralela usaria o `combiner` para
> juntar containers de diferentes threads.

---

## 🔀 Operações Intermediárias

### `map` — Transformação de tipo

O `map` cria uma nova Stream com um novo `Iterable` que aplica a função de transformação:

```java
public <R> Stream<R> map(Function<T, R> mapper) {
    return new Stream<>(() -> new Iterator<>() {
        private final Iterator<T> innerIterator = it.iterator();

        @Override
        public boolean hasNext() {
            return innerIterator.hasNext();
        }

        @Override
        public R next() {
            final T el = innerIterator.next();
            return mapper.apply(el);
        }
    });
}
```

**Características**:
- ✅ Lazy — nenhum elemento é processado até uma operação terminal ser chamada
- ✅ Preserva a quantidade de elementos (1:1)
- ✅ Pode mudar o tipo (`Stream<T>` → `Stream<R>`)

**Teste**:
```java
new Stream<>(List.of(1, 2, 3))
    .map(x -> 2 * x)
    .forEach(System.out::println);
// Saída: 2, 4, 6
```

### `filter` — Seleção condicional

O filtro é mais complexo porque muda a quantidade de elementos. Usamos pre-fetch:

```java
public Stream<T> filter(Predicate<T> predicate) {
    return new Stream<>(() -> new Iterator<>() {
        private final Iterator<T> innerIterator = it.iterator();
        private boolean _hasNext;
        private T _next;

        {
            advance();
        }

        private void advance() {
            while (innerIterator.hasNext()) {
                T candidate = innerIterator.next();
                if (predicate.test(candidate)) {
                    _next = candidate;
                    _hasNext = true;
                    return;
                }
            }
            _hasNext = false;
        }

        @Override
        public boolean hasNext() {
            return _hasNext;
        }

        @Override
        public T next() {
            T result = _next;
            advance();
            return result;
        }
    });
}
```

**Características**:
- ✅ Lazy
- ⚠️ Altera a quantidade de elementos
- ✅ Mantém o tipo (`Stream<T>` → `Stream<T>`)
- Usa **pre-fetch**: ao construir o iterador, já busca o primeiro elemento válido

---

## 🎯 Collectors Reimplementados

### `toList` e `toSet`

Casos especiais de `toCollection`:

```java
static <T> Collector<T, ?, List<T>> toList() {
    return toCollection(ArrayList::new);
}

static <T> Collector<T, ?, Set<T>> toSet() {
    return toCollection(HashSet::new);
}

static <T, C extends Collection<T>> Collector<T, ?, C> toCollection(
        Supplier<C> collectionFactory) {
    return Collector.of(
        collectionFactory,
        Collection::add,
        (left, right) -> { left.addAll(right); return left; }
    );
}
```

### `groupingBy`

Agrupa elementos por uma chave classificadora:

```java
static <T, K> Collector<T, ?, Map<K, List<T>>> groupingBy(
        Function<T, K> classifier) {
    return Collector.of(
        HashMap::new,
        (map, element) -> map
            .computeIfAbsent(classifier.apply(element), k -> new ArrayList<>())
            .add(element),
        (left, right) -> {
            right.forEach((key, value) ->
                left.merge(key, value, (l1, l2) -> {
                    l1.addAll(l2);
                    return l1;
                })
            );
            return left;
        }
    );
}
```

---

## 🔑 Conceitos Fundamentais

### Lazy Evaluation

As operações intermediárias (`map`, `filter`) **não processam nada** imediatamente.
Elas apenas criam novos objetos `Stream` com novos `Iterable` que encadeiam a lógica.
O processamento só acontece quando uma operação terminal (`forEach`, `collect`, `reduce`)
é chamada.

```
Stream(dados)          ← Iterable original
  .map(f)              ← novo Iterable que aplica f ao original
  .filter(p)           ← novo Iterable que filtra o resultado do map
  .forEach(action)     ← AGORA processa tudo de uma vez!
```

### Encadeamento sem Materialização

Cada operação intermediária cria um novo `Iterator` que referencia o anterior.
Não há listas intermediárias sendo criadas — cada elemento flui por toda a pipeline.

### A Conexão com Collectors

O `Collector` é a interface que permite que `collect` seja genérico:

```
Collector<T, A, R>
    ├── supplier()     → cria A (container vazio)
    ├── accumulator()  → adiciona T em A
    ├── combiner()     → junta dois A's (paralelismo)
    └── finisher()     → transforma A em R
```

Este é exatamente o conceito aprofundado no [módulo 01](./01-collector-api-anatomy.md).

---

## 📊 Resumo das Implementações

| Operação | Tipo | Estado | Muda quantidade? | Muda tipo? |
|----------|------|--------|:-:|:-:|
| `forEach` | Terminal | — | — | — |
| `reduce` | Terminal | — | — | — |
| `collect` | Terminal | — | — | — |
| `map` | Intermediária | Stateless | ❌ | ✅ |
| `filter` | Intermediária | Stateless* | ✅ | ❌ |
| `flatMap` | Intermediária | Stateless | ✅ | ✅ |

\* Filter usa pre-fetch mas não mantém estado entre chamadas no sentido de stateful.

---

## 🔗 Referências

- [Functional Toolbox (open-source)](https://gitlab.com/geosales-open-source/totalcross-functional-toolbox)
- [Iterable JavaDoc](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/Iterable.html)
- [Iterator JavaDoc](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/Iterator.html)
