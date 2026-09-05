package com.portfolio.fleet.repository.custom;

import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.dto.MaintenanceFilterRequest;
import java.util.List;

public interface CustomMaintenanceRepository {

    /**
     * 💡 JPA TIP: Dynamic Queries with Criteria API
     * Builds type-safe SQL dynamically based on non-null parameters.
     */
    List<MaintenanceSchedule> findSchedulesByDynamicCriteria(
        MaintenanceFilterRequest filter, 
        int page, 
        int pageSize
    );

    long countSchedulesByDynamicCriteria(MaintenanceFilterRequest filter);
}
