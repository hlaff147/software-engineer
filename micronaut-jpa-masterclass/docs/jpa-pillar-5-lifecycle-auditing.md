# 📝 Pillar 5: Lifecycle Auditing & Event Listeners

> Intercepting Entity State Changes with JPA Callbacks and Asynchronous Audit Logging

---

## 1. JPA Entity Lifecycle Annotations

```text
       ┌──────────────┐
       │     NEW      │
       └──────┬───────┘
              │ persist()
              ▼
       ┌──────────────┐
       │  @PrePersist │
       └──────┬───────┘
              ▼
       ┌──────────────┐
       │   MANAGED    │ ◀─── find() / @PostLoad
       └──────┬───────┘
              │ mutate field
              ▼
       ┌──────────────┐
       │  @PreUpdate  │
       └──────┬───────┘
              │ flush / commit
              ▼
       ┌──────────────┐
       │  @PostUpdate │
       └──────────────┘
```

### Registered Listener:
```java
@MappedSuperclass
@EntityListeners(AuditEntityListener.class)
public abstract class AuditableEntity { ... }

public class AuditEntityListener {
    @PrePersist
    public void onPrePersist(Object entity) {
        if (entity instanceof AuditableEntity auditable) {
            auditable.setCreatedAt(Instant.now());
            auditable.setCreatedBy("SYSTEM_AUTO");
        }
    }

    @PreUpdate
    public void onPreUpdate(Object entity) {
        if (entity instanceof AuditableEntity auditable) {
            auditable.setUpdatedAt(Instant.now());
        }
    }
}
```

---

## 2. Asynchronous Audit Ledger via Virtual Threads

To prevent audit logging from adding database latency to business transactions:
1. Business transaction completes.
2. An `AuditEvent` record is published via Micronaut event publisher.
3. `AuditEventListener` consumes the event asynchronously on a Virtual Thread (`TaskExecutors.BLOCKING`) using `REQUIRES_NEW` propagation.

