package com.portfolio.fleet.dto;

import com.portfolio.fleet.domain.maintenance.MaintenancePriority;
import com.portfolio.fleet.domain.maintenance.MaintenanceStatus;
import io.micronaut.core.annotation.Introspected;
import java.math.BigDecimal;
import java.time.LocalDate;

@Introspected
public record MaintenanceFilterRequest(
    Long assetId,
    MaintenanceStatus status,
    MaintenancePriority priority,
    LocalDate fromDate,
    LocalDate toDate,
    BigDecimal maxCost
) {}
