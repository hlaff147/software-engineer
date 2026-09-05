package com.portfolio.fleet.dto;

import io.micronaut.core.annotation.Introspected;
import java.math.BigDecimal;

/**
 * 💡 JPA TIP: Aggregation Projection
 * Combines JOIN with GROUP BY and aggregate functions (COUNT, SUM, AVG)
 * directly in the database engine.
 */
@Introspected
public record OperatorDashboardDTO(
    String operatorName,
    String taxId,
    Long vehicleCount,
    Long totalMileage,
    BigDecimal budgetAmount,
    String budgetCurrency
) {}
