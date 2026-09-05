package com.portfolio.fleet.domain.asset;

import com.portfolio.fleet.audit.AuditableEntity;
import com.portfolio.fleet.domain.common.Address;
import com.portfolio.fleet.domain.common.GpsCoordinate;
import com.portfolio.fleet.domain.common.Tag;
import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.domain.operator.Operator;
import jakarta.persistence.CascadeType;
import jakarta.persistence.CollectionTable;
import jakarta.persistence.Column;
import jakarta.persistence.ElementCollection;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Inheritance;
import jakarta.persistence.InheritanceType;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.persistence.Version;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * 💡 JPA TIP: Joined Table Inheritance Strategy
 * - @Inheritance(strategy = InheritanceType.JOINED):
 *   Each class in the hierarchy maps to its own distinct database table.
 *   Subclasses (e.g. Vehicle, IoTSensor) contain foreign keys back to 'assets.id'.
 *   Polymorphic queries perform an SQL INNER JOIN or LEFT OUTER JOIN across subclass tables.
 * 
 * 💡 JPA TIP: @Version (Optimistic Locking)
 *   Hibernate automatically checks this column during UPDATE statements:
 *   WHERE id = ? AND version = ?
 *   If another transaction updated the row concurrently, Hibernate throws OptimisticLockException.
 * 
 * 💡 JPA TIP: @ElementCollection
 *   Stores value objects in an auxiliary table without requiring a dedicated Entity class.
 */
@Entity
@Table(name = "assets")
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Asset extends AuditableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Version
    @Column(name = "version")
    private Long version;

    @Column(name = "asset_code", nullable = false, unique = true, length = 50)
    private String assetCode;

    @Column(name = "name", nullable = false, length = 150)
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "status", nullable = false, length = 30)
    private AssetStatus status = AssetStatus.ACTIVE;

    @Embedded
    private GpsCoordinate lastKnownLocation;

    @Embedded
    private Address registrationAddress;

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(name = "asset_tags", joinColumns = @JoinColumn(name = "asset_id"))
    private Set<Tag> tags = new HashSet<>();

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "operator_id")
    private Operator operator;

    @OneToMany(mappedBy = "asset", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<MaintenanceSchedule> maintenanceSchedules = new ArrayList<>();

    public Asset() {
    }

    public Asset(String assetCode, String name, AssetStatus status) {
        this.assetCode = assetCode;
        this.name = name;
        this.status = status;
    }

    public void addMaintenanceSchedule(MaintenanceSchedule schedule) {
        this.maintenanceSchedules.add(schedule);
        schedule.setAsset(this);
    }

    public void removeMaintenanceSchedule(MaintenanceSchedule schedule) {
        this.maintenanceSchedules.remove(schedule);
        schedule.setAsset(null);
    }

    public Long getId() {
        return id;
    }

    public Long getVersion() {
        return version;
    }

    public String getAssetCode() {
        return assetCode;
    }

    public void setAssetCode(String assetCode) {
        this.assetCode = assetCode;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public AssetStatus getStatus() {
        return status;
    }

    public void setStatus(AssetStatus status) {
        this.status = status;
    }

    public GpsCoordinate getLastKnownLocation() {
        return lastKnownLocation;
    }

    public void setLastKnownLocation(GpsCoordinate lastKnownLocation) {
        this.lastKnownLocation = lastKnownLocation;
    }

    public Address getRegistrationAddress() {
        return registrationAddress;
    }

    public void setRegistrationAddress(Address registrationAddress) {
        this.registrationAddress = registrationAddress;
    }

    public Set<Tag> getTags() {
        return tags;
    }

    public void setTags(Set<Tag> tags) {
        this.tags = tags;
    }

    public Operator getOperator() {
        return operator;
    }

    public void setOperator(Operator operator) {
        this.operator = operator;
    }

    public List<MaintenanceSchedule> getMaintenanceSchedules() {
        return maintenanceSchedules;
    }

    public void setMaintenanceSchedules(List<MaintenanceSchedule> maintenanceSchedules) {
        this.maintenanceSchedules = maintenanceSchedules;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Asset asset)) return false;
        return Objects.equals(assetCode, asset.assetCode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(assetCode);
    }
}
