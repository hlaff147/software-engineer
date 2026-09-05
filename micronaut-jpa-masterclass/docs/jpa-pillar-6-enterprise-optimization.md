# 🚀 Pillar 6: Enterprise Optimization & Configuration

> JDBC Batching, Second-Level Caching, and Java 25 Synergy

---

## 1. JDBC Batching Configuration

```yaml
jpa:
  default:
    properties:
      hibernate:
        jdbc:
          batch_size: 30
        order_inserts: true
        order_updates: true
        batch_versioned_data: true
```

* `batch_size: 30`: Groups up to 30 INSERT or UPDATE statements into a single network roundtrip via `java.sql.PreparedStatement.addBatch()`.
* `order_inserts: true` & `order_updates: true`: Sorts statements by entity type to allow batching across polymorphic cascades.

---

## 2. Bulk Memory Management: `flush()` & `clear()`

When inserting thousands of rows, the First-Level Cache retains every entity in heap memory:

```java
for (int i = 0; i < totalCount; i++) {
    entityManager.persist(reading);

    if ((i + 1) % batchSize == 0) {
        entityManager.flush(); // Sends batch SQL to database buffer
        entityManager.clear(); // Evicts entities from L1 cache, reclaiming heap
    }
}
```

---

## 3. Second-Level (L2) & Query Caching

```yaml
jpa:
  default:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: true
          region:
            factory_class: org.hibernate.cache.jcache.internal.JCacheRegionFactory
```

* **L1 Cache:** Bounded to the single `EntityManager` transaction.
* **L2 Cache:** Shared across all transactions in the JVM process (managed by Ehcache/Caffeine).
* **Query Cache:** Caches the list of entity IDs returned by specific query parameter combinations.

---

## 4. Java 25 Synergy with JPA

| Java 25 Feature | Impact on JPA Performance |
| :--- | :--- |
| **Compact Object Headers (JEP 519)** | Shrinks object headers to 8 bytes. Reduces memory consumption of cached entities by **15% to 25%**. |
| **Virtual Threads (Project Loom)** | Allows thousands of concurrent JDBC calls on `@ExecuteOn(TaskExecutors.BLOCKING)` without carrier thread exhaustion. |
| **Java Records as Embeddables** | Immutable data carriers can now serve directly as `@Embeddable` value objects. |
| **Flexible Constructor Bodies (JEP 513)** | Validate domain constraints before executing `super(...)` in entity constructors. |

