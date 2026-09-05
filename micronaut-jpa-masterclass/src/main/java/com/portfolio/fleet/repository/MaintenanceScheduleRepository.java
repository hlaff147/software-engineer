package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.maintenance.MaintenancePriority;
import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.domain.maintenance.MaintenanceStatus;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface MaintenanceScheduleRepository extends JpaRepository<MaintenanceSchedule, Long> {

    @Query("SELECT s FROM MaintenanceSchedule s JOIN FETCH s.asset LEFT JOIN FETCH s.logs WHERE s.id = :id")
    Optional<MaintenanceSchedule> findWithLogsById(Long id);

    List<MaintenanceSchedule> findByStatus(MaintenanceStatus status);

    List<MaintenanceSchedule> findByPriority(MaintenancePriority priority);

    List<MaintenanceSchedule> findByScheduledDateBetween(LocalDate start, LocalDate end);
}
