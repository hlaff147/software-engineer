package com.portfolio.fleet.audit;

import io.micronaut.data.annotation.DateCreated;
import io.micronaut.data.annotation.DateUpdated;
import jakarta.persistence.Column;
import jakarta.persistence.EntityListeners;
import jakarta.persistence.MappedSuperclass;
import java.time.Instant;

/**
 * 💡 JPA TIP: @MappedSuperclass
 * A mapped superclass has no table of its own. Its mapped properties are inherited
 * by concrete entity subclasses and persisted into their respective tables.
 * 
 * 💡 JPA TIP: @EntityListeners
 * Registers a dedicated listener class to intercept entity lifecycle state changes
 * (such as @PrePersist and @PreUpdate) without cluttering domain logic.
 */
@MappedSuperclass
@EntityListeners(AuditEntityListener.class)
public abstract class AuditableEntity {

    @DateCreated
    @Column(name = "created_at", nullable = false, updatable = false)
    private Instant createdAt;

    @DateUpdated
    @Column(name = "updated_at")
    private Instant updatedAt;

    @Column(name = "created_by", updatable = false)
    private String createdBy;

    @Column(name = "last_modified_by")
    private String lastModifiedBy;

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public String getLastModifiedBy() {
        return lastModifiedBy;
    }

    public void setLastModifiedBy(String lastModifiedBy) {
        this.lastModifiedBy = lastModifiedBy;
    }
}
