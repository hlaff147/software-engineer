package com.portfolio.fleet.pillar3;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.domain.maintenance.MaintenancePriority;
import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.domain.maintenance.MaintenanceStatus;
import com.portfolio.fleet.dto.MaintenanceFilterRequest;
import com.portfolio.fleet.repository.MaintenanceScheduleRepository;
import com.portfolio.fleet.repository.VehicleRepository;
import com.portfolio.fleet.repository.custom.CustomMaintenanceRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 3: Type-Safe Dynamic Criteria API")
class CriteriaApiTest {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private MaintenanceScheduleRepository scheduleRepository;

    @Inject
    private CustomMaintenanceRepository customRepository;

    @Inject
    private EntityManager entityManager;

    @Test
    @Transactional
    @DisplayName("Criteria API: Multi-predicate dynamic filtering by priority, status, and cost")
    void testDynamicCriteriaFiltering() {
        Vehicle vehicle = new Vehicle("AST-CRIT-01", "DAF XF", AssetStatus.ACTIVE, "CRT-9000", "VINCRIT0001", 60000L, FuelType.DIESEL);
        vehicleRepository.save(vehicle);

        MaintenanceSchedule s1 = new MaintenanceSchedule("Routine check", LocalDate.now().plusDays(5), MaintenancePriority.LOW, new BigDecimal("400.00"));
        s1.setAsset(vehicle);
        s1.setStatus(MaintenanceStatus.SCHEDULED);

        MaintenanceSchedule s2 = new MaintenanceSchedule("Engine Overhaul", LocalDate.now().plusDays(10), MaintenancePriority.CRITICAL, new BigDecimal("5500.00"));
        s2.setAsset(vehicle);
        s2.setStatus(MaintenanceStatus.IN_PROGRESS);

        scheduleRepository.save(s1);
        scheduleRepository.save(s2);

        entityManager.flush();
        entityManager.clear();

        // Query with dynamic filter: only CRITICAL priority with status IN_PROGRESS
        MaintenanceFilterRequest filter = new MaintenanceFilterRequest(
            vehicle.getId(), 
            MaintenanceStatus.IN_PROGRESS, 
            MaintenancePriority.CRITICAL, 
            null, 
            null, 
            null
        );

        List<MaintenanceSchedule> results = customRepository.findSchedulesByDynamicCriteria(filter, 0, 10);
        long count = customRepository.countSchedulesByDynamicCriteria(filter);

        assertThat(results).hasSize(1);
        assertThat(count).isEqualTo(1L);
        assertThat(results.get(0).getDescription()).isEqualTo("Engine Overhaul");
    }
}
