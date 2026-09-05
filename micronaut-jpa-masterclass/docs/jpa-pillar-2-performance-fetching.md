# ⚡ Pillar 2: Performance, Fetching & N+1 Mitigation

> Understanding the Persistence Context, First-Level Cache, and Modern Fetch Strategies

---

## 1. 💡 JPA Tip: `findById()` Doesn't Always Hit the Database

Consider this snippet inside a `@Transactional` method:

```java
@Transactional
public void updateUserPreferences(Long id, String newTheme) {
    // 1. Database hit: Issues SQL SELECT and stores entity in Persistence Context (L1 Cache)
    User user = userRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("User not found"));

    user.setTheme(newTheme);

    // 2. Cache hit: Returns the managed instance directly from memory!
    // No second SQL SELECT is executed.
    User cachedUser = userRepository.findById(id).get();

    // 3. Dirty Checking: Hibernate detects change upon transaction commit.
    // No userRepository.save(user) required!
}
```

### What Happens Behind the Scenes:
1. **First `findById(id)`**:
   - Checks First-Level Cache → Miss.
   - Executes SQL: `SELECT ... FROM users WHERE id = ?`.
   - Entity is loaded, and a **snapshot copy** is taken for dirty checking.
   - Entity is stored in the Persistence Context map: `Map<EntityKey, Object>`.
2. **Second `findById(id)`**:
   - Checks First-Level Cache → **Hit!**
   - Returns the managed instance immediately from RAM.
   - `user == cachedUser` is **strictly true** (reference equality guaranteed).
3. **Dirty Checking on Commit**:
   - Hibernate compares current entity state against the initial snapshot.
   - Emits `UPDATE users SET theme = ? WHERE id = ?`.

---

## 2. The N+1 Query Problem & Mitigations

### The Problem:
When loading 50 `MaintenanceSchedule` entities with lazy `logs`:
1. `SELECT * FROM maintenance_schedules` (1 query)
2. For each schedule, iterating `schedule.getLogs()` triggers:
   `SELECT * FROM maintenance_logs WHERE schedule_id = ?` (50 queries!)
   Total: **51 database roundtrips**.

---

### Mitigation A: Declarative `@Join` (Micronaut Data)

Micronaut Data compiles join queries ahead-of-time:

```java
@Repository
public interface AssetRepository extends JpaRepository<Asset, Long> {

    @Join(value = "operator", type = Join.Type.LEFT_FETCH)
    @Join(value = "maintenanceSchedules", type = Join.Type.LEFT_FETCH)
    Optional<Asset> findWithDetailsById(Long id);
}
```
* **SQL Output:** Single query using `LEFT OUTER JOIN` for all requested associations.

---

### Mitigation B: JPQL `JOIN FETCH`

```java
@Query("SELECT a FROM Asset a JOIN FETCH a.operator WHERE a.operator.id = :operatorId")
List<Asset> findAllByOperatorIdWithFetch(Long operatorId);
```
* Forces Hibernate to initialize the association eagerly in the initial query.

---

### Mitigation C: Collection Batching via `@BatchSize`

```java
@Entity
@Table(name = "maintenance_schedules")
public class MaintenanceSchedule {

    @BatchSize(size = 25)
    @OneToMany(mappedBy = "schedule")
    private List<MaintenanceLog> logs;
}
```

* When accessing `schedule.getLogs()`, Hibernate checks the persistence context for up to 25 uninitialized collections and fetches them with a single `IN` query:
  ```sql
  SELECT * FROM maintenance_logs WHERE schedule_id IN (?, ?, ?, ?, ...)
  ```
* Cuts roundtrips from $N+1$ down to $1 + \lceil N / 25 \rceil$.

