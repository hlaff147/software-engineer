package com.portfolio.fleet.pillar2;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.domain.maintenance.MaintenanceLog;
import com.portfolio.fleet.domain.maintenance.MaintenancePriority;
import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.repository.MaintenanceScheduleRepository;
import com.portfolio.fleet.repository.VehicleRepository;
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
@DisplayName("Pillar 2: N+1 Problem Mitigation via @BatchSize")
class NPlus1Test {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private MaintenanceScheduleRepository scheduleRepository;

    @Inject
    private EntityManager entityManager;

    @Test
    @Transactional
    @DisplayName("@BatchSize(size = 25): Eliminates N+1 when accessing child collections")
    void testBatchSizeEliminatesNPlus1() {
        Vehicle vehicle = new Vehicle("AST-BATCH-01", "MAN TGX", AssetStatus.ACTIVE, "BAT-0001", "VINMAN0001", 120000L, FuelType.DIESEL);
        vehicleRepository.save(vehicle);

        // Create 5 schedules, each with 2 logs
        for (int i = 1; i <= 5; i++) {
            MaintenanceSchedule schedule = new MaintenanceSchedule(
                "Periodic Inspection #" + i, LocalDate.now().plusMonths(i), MaintenancePriority.HIGH, new BigDecimal("1200.00")
            );
            schedule.setAsset(vehicle);
            schedule.addLog(new MaintenanceLog("Inspection check A" + i, "Passed oil test", "Oil filter"));
            schedule.addLog(new MaintenanceLog("Inspection check B" + i, "Brake pad replacement", "Brake pads"));
            scheduleRepository.save(schedule);
        }

        entityManager.flush();
        entityManager.clear();

        // Query all schedules
        List<MaintenanceSchedule> schedules = scheduleRepository.findAll();
        assertThat(schedules).hasSize(5);

        // 💡 JPA TIP: Without @BatchSize, iterating over 5 schedules would execute 5 separate queries.
        // With @BatchSize(size = 25), Hibernate batches the collection fetch into a single query:
        // WHERE schedule_id IN (?, ?, ?, ?, ?)
        int totalLogs = 0;
        for (MaintenanceSchedule s : schedules) {
            totalLogs += s.getLogs().size();
        }
        assertThat(totalLogs).isEqualTo(10);
    }
}
