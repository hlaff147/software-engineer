package com.portfolio.fleet.controller;

import com.portfolio.fleet.domain.telemetry.TelemetryReading;
import com.portfolio.fleet.dto.TelemetryStatDTO;
import com.portfolio.fleet.service.BulkOperationService;
import com.portfolio.fleet.service.TelemetryIngestionService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.QueryValue;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.List;
import java.util.Map;

@Controller("/api/telemetry")
public class TelemetryController {

    private final TelemetryIngestionService telemetryService;
    private final BulkOperationService bulkService;

    public TelemetryController(TelemetryIngestionService telemetryService, BulkOperationService bulkService) {
        this.telemetryService = telemetryService;
        this.bulkService = bulkService;
    }

    @Post
    public HttpResponse<TelemetryReading> recordReading(@Body TelemetryReading reading) {
        return HttpResponse.created(telemetryService.ingestReading(reading));
    }

    @Get("/{mac}/recent")
    public HttpResponse<List<TelemetryReading>> getRecent(@PathVariable String mac) {
        return HttpResponse.ok(telemetryService.getRecentReadings(mac));
    }

    @Get("/{mac}/stats")
    public HttpResponse<TelemetryStatDTO> getStats(
            @PathVariable String mac,
            @QueryValue(defaultValue = "24") Integer hours) {
        Instant since = Instant.now().minus(hours, ChronoUnit.HOURS);
        return HttpResponse.ok(telemetryService.getSensorStatistics(mac, since));
    }

    @Post("/bulk-seed")
    public HttpResponse<Map<String, Object>> bulkSeed(
            @QueryValue(defaultValue = "1000") Integer total,
            @QueryValue(defaultValue = "50") Integer batchSize) {
        int inserted = bulkService.batchInsertReadings(total, batchSize);
        return HttpResponse.ok(Map.of(
            "totalInserted", inserted,
            "batchFlushSize", batchSize,
            "status", "completed"
        ));
    }
}
