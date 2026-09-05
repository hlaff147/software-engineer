# 🔒 Pillar 4: Concurrency & Transactional Integrity

> Optimistic vs. Pessimistic Locking, Isolation Levels, and Race Condition Mitigation

---

## 1. Optimistic Locking (`@Version`)

Optimistic locking assumes that conflicts are infrequent. It uses a version column auto-incremented by Hibernate on every UPDATE:

```java
@Entity
@Table(name = "assets")
public abstract class Asset {
    @Version
    @Column(name = "version")
    private Long version;
}
```

### Generated SQL:
```sql
UPDATE assets 
SET mileage = ?, version = version + 1 
WHERE id = ? AND version = ?
```

### If row was modified concurrently:
* Hibernate finds 0 updated rows and throws `OptimisticLockException`.
* The application can retry using an exponential backoff loop:

```java
public Vehicle updateWithRetry(Long vehicleId, Long newMileage, int maxRetries) {
    for (int attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return executeUpdateInTransaction(vehicleId, newMileage);
        } catch (OptimisticLockException ex) {
            Thread.sleep(50L * attempt); // Backoff jitter
        }
    }
    throw new IllegalStateException("Max retries exceeded");
}
```

---

## 2. Pessimistic Locking (`PESSIMISTIC_WRITE`)

For critical balance decrements and inventory allocation, acquiring a database exclusive lock prevents any race conditions:

```java
Map<String, Object> hints = Map.of("jakarta.persistence.lock.timeout", 3000);

Operator operator = entityManager.find(
    Operator.class, 
    operatorId, 
    LockModeType.PESSIMISTIC_WRITE, 
    hints
);
```

### Generated SQL:
```sql
SELECT * FROM operators WHERE id = ? FOR UPDATE
```

* Other concurrent transactions attempting to read or write will queue until the lock is released upon transaction commit or until the timeout (3,000 ms) expires.

