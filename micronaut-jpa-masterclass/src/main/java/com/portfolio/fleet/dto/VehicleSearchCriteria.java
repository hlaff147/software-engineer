package com.portfolio.fleet.dto;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import io.micronaut.core.annotation.Introspected;

/**
 * 💡 Criteria API Filter Object
 * Encapsulates dynamic query filter parameters.
 */
@Introspected
public record VehicleSearchCriteria(
    String assetCode,
    String licensePlate,
    AssetStatus status,
    FuelType fuelType,
    Long minMileage,
    Long maxMileage,
    String operatorName
) {}
