package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.telemetry.TelemetryReading;
import com.portfolio.fleet.dto.TelemetryStatDTO;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.time.Instant;
import java.util.List;

/**
 * 💡 JPA TIP: High-Throughput Aggregations
 * Demonstrates scalar calculations (AVG, MAX, MIN) projected directly into a DTO.
 */
@Repository
public interface TelemetryRepository extends JpaRepository<TelemetryReading, Long> {

    List<TelemetryReading> findBySensorMacOrderByTimestampDesc(String sensorMac);

    @Query("""
        SELECT new com.portfolio.fleet.dto.TelemetryStatDTO(
            t.sensorMac,
            COUNT(t.id),
            AVG(t.temperatureCelsius),
            MAX(t.speedKmh),
            MIN(t.batteryVolts)
        )
        FROM TelemetryReading t
        WHERE t.sensorMac = :sensorMac AND t.timestamp >= :since
        GROUP BY t.sensorMac
    """)
    TelemetryStatDTO getSensorStatsSince(String sensorMac, Instant since);

    @Query("SELECT COUNT(t) FROM TelemetryReading t")
    long countTotalReadings();
}
