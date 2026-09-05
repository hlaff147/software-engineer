package com.portfolio.fleet.domain.maintenance;

import com.portfolio.fleet.audit.AuditableEntity;
import com.portfolio.fleet.domain.asset.Asset;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import org.hibernate.annotations.BatchSize;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * 💡 JPA TIP: Batch Size to Kill N+1 Queries
 * @BatchSize(size = 25) tells Hibernate: when initializing the 'logs' collection
 * for one schedule, pre-fetch the collections for up to 25 other schedules in the current
 * persistence context using a single 'WHERE schedule_id IN (?, ?, ...)' query!
 */
@Entity
@Table(name = "maintenance_schedules")
public class MaintenanceSchedule extends AuditableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "asset_id", nullable = false)
    private Asset asset;

    @Column(name = "description", nullable = false, length = 500)
    private String description;

    @Column(name = "scheduled_date", nullable = false)
    private LocalDate scheduledDate;

    @Column(name = "completed_date")
    private LocalDate completedDate;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    private MaintenanceStatus status = MaintenanceStatus.SCHEDULED;

    @Enumerated(EnumType.STRING)
    @Column(name = "priority", nullable = false, length = 20)
    private MaintenancePriority priority = MaintenancePriority.MEDIUM;

    @Column(name = "estimated_cost", precision = 12, scale = 2)
    private BigDecimal estimatedCost;

    // 💡 JPA TIP: @BatchSize prevents N+1 when iterating over schedules and inspecting logs
    @BatchSize(size = 25)
    @OneToMany(mappedBy = "schedule", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<MaintenanceLog> logs = new ArrayList<>();

    public MaintenanceSchedule() {
    }

    public MaintenanceSchedule(String description, LocalDate scheduledDate, MaintenancePriority priority, BigDecimal estimatedCost) {
        this.description = description;
        this.scheduledDate = scheduledDate;
        this.priority = priority;
        this.estimatedCost = estimatedCost;
        this.status = MaintenanceStatus.SCHEDULED;
    }

    public void addLog(MaintenanceLog log) {
        this.logs.add(log);
        log.setSchedule(this);
    }

    public void removeLog(MaintenanceLog log) {
        this.logs.remove(log);
        log.setSchedule(null);
    }

    public Long getId() {
        return id;
    }

    public Asset getAsset() {
        return asset;
    }

    public void setAsset(Asset asset) {
        this.asset = asset;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDate getScheduledDate() {
        return scheduledDate;
    }

    public void setScheduledDate(LocalDate scheduledDate) {
        this.scheduledDate = scheduledDate;
    }

    public LocalDate getCompletedDate() {
        return completedDate;
    }

    public void setCompletedDate(LocalDate completedDate) {
        this.completedDate = completedDate;
    }

    public MaintenanceStatus getStatus() {
        return status;
    }

    public void setStatus(MaintenanceStatus status) {
        this.status = status;
    }

    public MaintenancePriority getPriority() {
        return priority;
    }

    public void setPriority(MaintenancePriority priority) {
        this.priority = priority;
    }

    public BigDecimal getEstimatedCost() {
        return estimatedCost;
    }

    public void setEstimatedCost(BigDecimal estimatedCost) {
        this.estimatedCost = estimatedCost;
    }

    public List<MaintenanceLog> getLogs() {
        return logs;
    }

    public void setLogs(List<MaintenanceLog> logs) {
        this.logs = logs;
    }
}
