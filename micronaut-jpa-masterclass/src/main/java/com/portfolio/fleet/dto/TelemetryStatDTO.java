package com.portfolio.fleet.dto;

import io.micronaut.core.annotation.Introspected;

@Introspected
public record TelemetryStatDTO(
    String sensorMac,
    Long readingCount,
    Double avgTemperature,
    Double maxSpeed,
    Double minBattery
) {}
