package com.portfolio.fleet.audit;

import jakarta.persistence.PostLoad;
import jakarta.persistence.PostPersist;
import jakarta.persistence.PostRemove;
import jakarta.persistence.PostUpdate;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreRemove;
import jakarta.persistence.PreUpdate;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.time.Instant;

/**
 * 💡 JPA TIP: Lifecycle Callbacks
 * JPA standard defines 7 entity lifecycle annotations:
 * - @PrePersist: Executed before EntityManager.persist() commits/flushes.
 * - @PostPersist: Executed immediately after INSERT SQL execution.
 * - @PreUpdate: Executed before UPDATE SQL is sent to the database.
 * - @PostUpdate: Executed immediately after UPDATE SQL execution.
 * - @PreRemove: Executed before DELETE SQL is executed.
 * - @PostRemove: Executed immediately after DELETE SQL is executed.
 * - @PostLoad: Executed whenever an entity is loaded from the DB into the Persistence Context!
 * 
 * Notice: @PostLoad will NOT fire if the entity is already present in Hibernate's First-Level Cache.
 */
public class AuditEntityListener {

    private static final Logger log = LoggerFactory.getLogger(AuditEntityListener.class);

    @PrePersist
    public void onPrePersist(Object entity) {
        if (entity instanceof AuditableEntity auditable) {
            Instant now = Instant.now();
            if (auditable.getCreatedAt() == null) {
                auditable.setCreatedAt(now);
            }
            if (auditable.getCreatedBy() == null) {
                auditable.setCreatedBy("SYSTEM_AUTO");
            }
        }
        log.info("[JPA LIFECYCLE: @PrePersist] Prepared entity for persist: {}", entity.getClass().getSimpleName());
    }

    @PreUpdate
    public void onPreUpdate(Object entity) {
        if (entity instanceof AuditableEntity auditable) {
            auditable.setUpdatedAt(Instant.now());
            if (auditable.getLastModifiedBy() == null) {
                auditable.setLastModifiedBy("SYSTEM_UPDATE");
            }
        }
        log.info("[JPA LIFECYCLE: @PreUpdate] Prepared entity for update: {}", entity.getClass().getSimpleName());
    }

    @PostPersist
    public void onPostPersist(Object entity) {
        log.info("[JPA LIFECYCLE: @PostPersist] Persisted entity to DB: {}", entity.getClass().getSimpleName());
    }

    @PostUpdate
    public void onPostUpdate(Object entity) {
        log.info("[JPA LIFECYCLE: @PostUpdate] Updated entity in DB: {}", entity.getClass().getSimpleName());
    }

    @PreRemove
    public void onPreRemove(Object entity) {
        log.warn("[JPA LIFECYCLE: @PreRemove] About to delete entity: {}", entity.getClass().getSimpleName());
    }

    @PostRemove
    public void onPostRemove(Object entity) {
        log.warn("[JPA LIFECYCLE: @PostRemove] Deleted entity from DB: {}", entity.getClass().getSimpleName());
    }

    @PostLoad
    public void onPostLoad(Object entity) {
        // JPA TIP: This fires only when materialized from the DB, NOT when retrieved from L1 Cache!
        log.debug("[JPA LIFECYCLE: @PostLoad] Materialized from DB into Persistence Context: {}", entity.getClass().getSimpleName());
    }
}
