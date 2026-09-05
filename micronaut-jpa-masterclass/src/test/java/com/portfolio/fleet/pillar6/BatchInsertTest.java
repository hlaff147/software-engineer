package com.portfolio.fleet.pillar6;

import com.portfolio.fleet.repository.TelemetryRepository;
import com.portfolio.fleet.service.BulkOperationService;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 6: Enterprise Optimization — JDBC Batching & Memory Flush/Clear")
class BatchInsertTest {

    @Inject
    private BulkOperationService bulkOperationService;

    @Inject
    private TelemetryRepository telemetryRepository;

    @Test
    @DisplayName("JDBC Batching: Bulk inserts 200 readings with flush and clear every 25 records")
    void testBulkInsertMemoryManagement() {
        int inserted = bulkOperationService.batchInsertReadings(200, 25);
        assertThat(inserted).isEqualTo(200);

        long count = telemetryRepository.countTotalReadings();
        assertThat(count).isGreaterThanOrEqualTo(200L);
    }
}
