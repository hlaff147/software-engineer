package com.portfolio.fleet.audit;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

/**
 * 💡 JPA TIP: Immutable Audit Entity
 * In production systems, audit logs should be write-only/append-only.
 * Notice no setters are exposed for core fields once constructed.
 */
@Entity
@Table(name = "audit_logs")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "entity_name", nullable = false)
    private String entityName;

    @Column(name = "entity_id", nullable = false)
    private String entityId;

    @Column(name = "action_type", nullable = false)
    private String actionType;

    @Column(name = "details", length = 2000)
    private String details;

    @Column(name = "performed_by")
    private String performedBy;

    @Column(name = "timestamp", nullable = false)
    private Instant timestamp;

    public AuditLog() {
    }

    public AuditLog(String entityName, String entityId, String actionType, String details, String performedBy) {
        this.entityName = entityName;
        this.entityId = entityId;
        this.actionType = actionType;
        this.details = details;
        this.performedBy = performedBy;
        this.timestamp = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public String getEntityName() {
        return entityName;
    }

    public String getEntityId() {
        return entityId;
    }

    public String getActionType() {
        return actionType;
    }

    public String getDetails() {
        return details;
    }

    public String getPerformedBy() {
        return performedBy;
    }

    public Instant getTimestamp() {
        return timestamp;
    }
}
