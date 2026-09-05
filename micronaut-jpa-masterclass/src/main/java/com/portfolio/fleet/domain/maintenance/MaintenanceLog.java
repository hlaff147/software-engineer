package com.portfolio.fleet.domain.maintenance;

import com.portfolio.fleet.audit.AuditableEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import java.time.Instant;

/**
 * 💡 JPA TIP: Child Entity in 1:N Relationship
 * Defines @ManyToOne with FetchType.LAZY.
 * Default in JPA for @ManyToOne is EAGER, which is an N+1 trap. Always make it LAZY!
 */
@Entity
@Table(name = "maintenance_logs")
public class MaintenanceLog extends AuditableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "schedule_id", nullable = false)
    private MaintenanceSchedule schedule;

    @Column(name = "log_message", nullable = false, length = 1000)
    private String logMessage;

    @Column(name = "technician_notes", length = 2000)
    private String technicianNotes;

    @Column(name = "logged_at", nullable = false)
    private Instant loggedAt;

    @Column(name = "parts_replaced", length = 500)
    private String partsReplaced;

    public MaintenanceLog() {
    }

    public MaintenanceLog(String logMessage, String technicianNotes, String partsReplaced) {
        this.logMessage = logMessage;
        this.technicianNotes = technicianNotes;
        this.partsReplaced = partsReplaced;
        this.loggedAt = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public MaintenanceSchedule getSchedule() {
        return schedule;
    }

    public void setSchedule(MaintenanceSchedule schedule) {
        this.schedule = schedule;
    }

    public String getLogMessage() {
        return logMessage;
    }

    public void setLogMessage(String logMessage) {
        this.logMessage = logMessage;
    }

    public String getTechnicianNotes() {
        return technicianNotes;
    }

    public void setTechnicianNotes(String technicianNotes) {
        this.technicianNotes = technicianNotes;
    }

    public Instant getLoggedAt() {
        return loggedAt;
    }

    public void setLoggedAt(Instant loggedAt) {
        this.loggedAt = loggedAt;
    }

    public String getPartsReplaced() {
        return partsReplaced;
    }

    public void setPartsReplaced(String partsReplaced) {
        this.partsReplaced = partsReplaced;
    }
}
