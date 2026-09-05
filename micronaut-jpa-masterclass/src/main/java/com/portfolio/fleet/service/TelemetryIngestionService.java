package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.telemetry.TelemetryReading;
import com.portfolio.fleet.dto.TelemetryStatDTO;
import com.portfolio.fleet.repository.TelemetryRepository;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import java.time.Instant;
import java.util.List;

@Singleton
public class TelemetryIngestionService {

    private final TelemetryRepository telemetryRepository;

    public TelemetryIngestionService(TelemetryRepository telemetryRepository) {
        this.telemetryRepository = telemetryRepository;
    }

    @Transactional
    public TelemetryReading ingestReading(TelemetryReading reading) {
        return telemetryRepository.save(reading);
    }

    @Transactional
    public List<TelemetryReading> getRecentReadings(String sensorMac) {
        return telemetryRepository.findBySensorMacOrderByTimestampDesc(sensorMac);
    }

    @Transactional
    public TelemetryStatDTO getSensorStatistics(String sensorMac, Instant since) {
        return telemetryRepository.getSensorStatsSince(sensorMac, since);
    }
}
