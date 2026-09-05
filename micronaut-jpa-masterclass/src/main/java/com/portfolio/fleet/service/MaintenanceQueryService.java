package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.dto.MaintenanceFilterRequest;
import com.portfolio.fleet.repository.MaintenanceScheduleRepository;
import com.portfolio.fleet.repository.custom.CustomMaintenanceRepository;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import java.util.List;
import java.util.Optional;

@Singleton
public class MaintenanceQueryService {

    private final MaintenanceScheduleRepository scheduleRepository;
    private final CustomMaintenanceRepository customRepository;

    public MaintenanceQueryService(MaintenanceScheduleRepository scheduleRepository, 
                                   CustomMaintenanceRepository customRepository) {
        this.scheduleRepository = scheduleRepository;
        this.customRepository = customRepository;
    }

    @Transactional
    public MaintenanceSchedule scheduleMaintenance(MaintenanceSchedule schedule) {
        return scheduleRepository.save(schedule);
    }

    @Transactional
    public Optional<MaintenanceSchedule> getScheduleWithLogs(Long id) {
        return scheduleRepository.findWithLogsById(id);
    }

    @Transactional
    public List<MaintenanceSchedule> searchSchedules(MaintenanceFilterRequest filter, int page, int pageSize) {
        return customRepository.findSchedulesByDynamicCriteria(filter, page, pageSize);
    }

    @Transactional
    public long countSchedules(MaintenanceFilterRequest filter) {
        return customRepository.countSchedulesByDynamicCriteria(filter);
    }
}
