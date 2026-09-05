package com.portfolio.fleet.pillar5;

import com.portfolio.fleet.audit.AuditLog;
import com.portfolio.fleet.repository.AuditLogRepository;
import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.repository.VehicleRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 5: Lifecycle Auditing & Entity Listeners")
class AuditLifecycleTest {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private AuditLogRepository auditLogRepository;

    @Inject
    private EntityManager entityManager;

    @Test
    @Transactional
    @DisplayName("@PrePersist & @PreUpdate: Automatically sets createdAt, createdBy, and updatedAt")
    void testAuditTimestampsPopulation() {
        Vehicle vehicle = new Vehicle("AST-AUDIT-01", "Scania G410", AssetStatus.ACTIVE, "AUD-0001", "VINAUDIT001", 1000L, FuelType.DIESEL);

        Vehicle saved = vehicleRepository.save(vehicle);
        assertThat(saved.getCreatedAt()).isNotNull();
        assertThat(saved.getCreatedBy()).isEqualTo("SYSTEM_AUTO");

        entityManager.flush();
        entityManager.clear();

        Vehicle loaded = vehicleRepository.findById(saved.getId()).orElseThrow();
        loaded.setMileage(2000L);

        Vehicle updated = vehicleRepository.update(loaded);
        entityManager.flush();

        assertThat(updated.getUpdatedAt()).isNotNull();
    }

    @Test
    @Transactional
    @DisplayName("AuditLog: Verifies append-only audit trail logging")
    void testAuditLogPersistence() {
        AuditLog log = new AuditLog("Vehicle", "AST-AUDIT-01", "UPDATE_MILEAGE", "Mileage updated from 1000 to 2000", "admin_user");
        auditLogRepository.save(log);

        List<AuditLog> logs = auditLogRepository.findByEntityNameAndEntityIdOrderByTimestampDesc("Vehicle", "AST-AUDIT-01");
        assertThat(logs).isNotEmpty();
        assertThat(logs.get(0).getActionType()).isEqualTo("UPDATE_MILEAGE");
    }
}
