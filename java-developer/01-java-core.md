# Java Core Questions

## 1. What are the benefits of sealed classes introduced in Java 17?

**Sealed classes** restrict which classes can extend or implement them.

**Benefits:**
- **Controlled inheritance**: Define a closed set of permitted subclasses
- **Exhaustive pattern matching**: Compiler knows all subtypes, enabling complete `switch` expressions without `default`
- **Better API design**: Express domain models more precisely
- **Enhanced security**: Prevent unauthorized extensions

```java
public sealed class Shape permits Circle, Rectangle, Triangle {
}

public final class Circle extends Shape { }
public final class Rectangle extends Shape { }
public non-sealed class Triangle extends Shape { } // allows further extension
```

---

## 2. How do virtual threads in Java 21 improve request handling in high-load systems?

**Virtual threads** are lightweight threads managed by the JVM, not the OS.

**Improvements:**
- **Massive scalability**: Create millions of threads (vs thousands with platform threads)
- **Reduced memory**: ~1KB per virtual thread vs ~1MB for platform threads
- **Simplified code**: Write blocking code that scales like async code
- **No thread pool tuning**: No need to optimize pool sizes

```java
// Create 1 million virtual threads easily
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 1_000_000).forEach(i -> 
        executor.submit(() -> handleRequest(i))
    );
}
```

**Use case**: Handle 100K+ concurrent HTTP requests without complex reactive programming.

---

## 3. What is the difference between Optional.map() and Optional.flatMap()?

| Aspect | `map()` | `flatMap()` |
|--------|---------|-------------|
| **Return type** | Wraps result in Optional | Expects function to return Optional |
| **Use when** | Transformation returns a value | Transformation returns Optional |
| **Nesting** | Can cause `Optional<Optional<T>>` | Flattens nested Optionals |

```java
Optional<String> name = Optional.of("John");

// map() - function returns String
Optional<Integer> length = name.map(String::length); // Optional<Integer>

// flatMap() - function returns Optional<String>
Optional<String> upper = name.flatMap(n -> Optional.of(n.toUpperCase())); // Optional<String>

// Problem with map() when function returns Optional
Optional<Optional<String>> nested = name.map(n -> Optional.of(n.toUpperCase())); // Nested!
```

---

## 4. How does garbage collection differ in Serial, Parallel, and G1 collectors?

| Collector | Threads | Best For | Pause Behavior |
|-----------|---------|----------|----------------|
| **Serial** | Single | Small heaps, single-core | Stop-the-world, simple |
| **Parallel** | Multiple | Throughput-focused apps | Stop-the-world, faster |
| **G1** | Multiple | Large heaps (4GB+), low latency | Incremental, predictable pauses |

**Serial GC** (`-XX:+UseSerialGC`):
- Single-threaded, simple mark-sweep-compact
- Good for containers with limited CPU

**Parallel GC** (`-XX:+UseParallelGC`):
- Multi-threaded young and old generation collection
- Maximizes throughput, longer pauses acceptable

**G1 GC** (`-XX:+UseG1GC`) - Default since Java 9:
- Divides heap into regions
- Collects regions with most garbage first
- Target pause time: `-XX:MaxGCPauseMillis=200`

---

## 5. How does var help with type inference in Java?

`var` allows local variable type inference - compiler determines the type.

**Benefits:**
- Reduces verbosity
- Improves readability for complex generic types
- Type is still statically checked

```java
// Before
Map<String, List<Employee>> employeesByDept = new HashMap<>();

// After
var employeesByDept = new HashMap<String, List<Employee>>();

// Works with loops
for (var entry : map.entrySet()) { }

// Works with try-with-resources
try (var stream = Files.lines(path)) { }
```

**Restrictions:**
- Only for local variables with initializers
- Cannot use for method parameters, return types, or fields
- Cannot initialize with `null`

---

## 6. Explain the difference between CopyOnWriteArrayList and ArrayList.

| Aspect | ArrayList | CopyOnWriteArrayList |
|--------|-----------|----------------------|
| **Thread-safety** | Not thread-safe | Thread-safe |
| **Write operation** | Modifies in place | Creates new copy |
| **Read performance** | Fast | Fast (no locking) |
| **Write performance** | Fast | Slow (copies array) |
| **Iterator** | Fail-fast | Snapshot (never throws ConcurrentModificationException) |

```java
// ArrayList - needs external synchronization
List<String> list = Collections.synchronizedList(new ArrayList<>());

// CopyOnWriteArrayList - inherently thread-safe
List<String> cowList = new CopyOnWriteArrayList<>();
```

**Use CopyOnWriteArrayList when:**
- Reads vastly outnumber writes
- Need to iterate without locking
- Example: listener lists, configuration caches

---

## 7. What is the purpose of CompletableFuture in asynchronous programming?

`CompletableFuture` enables non-blocking async operations with composable callbacks.

**Key features:**
- Chain async operations
- Combine multiple futures
- Handle exceptions elegantly
- Transform results

```java
CompletableFuture.supplyAsync(() -> fetchUser(userId))      // async call
    .thenApplyAsync(user -> fetchOrders(user))              // chain
    .thenAcceptAsync(orders -> sendEmail(orders))           // consume
    .exceptionally(ex -> { log.error(ex); return null; });  // error handling

// Combine multiple futures
CompletableFuture.allOf(future1, future2, future3)
    .thenRun(() -> System.out.println("All done!"));

// Get first completed
CompletableFuture.anyOf(future1, future2)
    .thenAccept(result -> process(result));
```

---

## 8. How does pattern matching for switch improve readability in Java 17+?

Pattern matching eliminates verbose `instanceof` checks and casting.

**Before (verbose):**
```java
if (obj instanceof String) {
    String s = (String) obj;
    System.out.println(s.length());
} else if (obj instanceof Integer) {
    Integer i = (Integer) obj;
    System.out.println(i * 2);
}
```

**After (clean):**
```java
switch (obj) {
    case String s  -> System.out.println(s.length());
    case Integer i -> System.out.println(i * 2);
    case null      -> System.out.println("null");
    default        -> System.out.println("unknown");
}

// With guards (Java 21)
switch (obj) {
    case String s when s.length() > 5 -> "long string";
    case String s                      -> "short string";
    case Integer i when i > 0          -> "positive";
    default                            -> "other";
}
```

---

## 9. What are text blocks, and how do they simplify working with JSON/XML?

**Text blocks** (Java 15+) are multi-line string literals using `"""`.

**Benefits:**
- No escape characters for quotes
- Preserves formatting
- Automatic indentation stripping

```java
// Before - escaped quotes, concatenation
String json = "{\n" +
    "  \"name\": \"John\",\n" +
    "  \"age\": 30\n" +
    "}";

// After - clean and readable
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;

// SQL queries
String sql = """
    SELECT u.name, o.total
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE o.status = 'ACTIVE'
    """;

// With interpolation (formatted)
String html = """
    <html>
      <body>%s</body>
    </html>
    """.formatted(content);
```

---

## 10. Explain immutability and how to enforce it in Java.

**Immutability** means an object's state cannot change after creation.

**Benefits:**
- Thread-safe by default
- Safe to share/cache
- Easier to reason about
- Good hash keys

**How to enforce:**

```java
// 1. Use final class (prevent subclassing)
public final class Person {
    
    // 2. Make fields private and final
    private final String name;
    private final List<String> hobbies;
    
    // 3. No setters, only constructor
    public Person(String name, List<String> hobbies) {
        this.name = name;
        // 4. Defensive copy of mutable objects
        this.hobbies = List.copyOf(hobbies);
    }
    
    // 5. Return copies of mutable fields
    public List<String> getHobbies() {
        return List.copyOf(hobbies);
    }
}

// Easier way - use records (Java 16+)
public record Person(String name, List<String> hobbies) {
    public Person {
        hobbies = List.copyOf(hobbies); // defensive copy in compact constructor
    }
}
```
