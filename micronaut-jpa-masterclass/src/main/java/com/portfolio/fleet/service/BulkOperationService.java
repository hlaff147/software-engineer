package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.common.GpsCoordinate;
import com.portfolio.fleet.domain.telemetry.TelemetryReading;
import com.portfolio.fleet.repository.VehicleRepository;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.time.Instant;
import java.util.List;

/**
 * 💡 JPA TIP: Bulk Operations & Memory Management
 * 
 * When processing thousands of entities in a single transaction:
 * 1. The Persistence Context (First-Level Cache) retains references to ALL managed entities.
 * 2. Without intervention, this leads to heap exhaustion (OutOfMemoryError) and degraded GC performance.
 * 
 * Solution:
 * Periodically invoke:
 *   entityManager.flush(); // Sends pending SQL INSERT/UPDATE statements to the database buffer
 *   entityManager.clear(); // Evicts all managed entities from the First-Level Cache, freeing memory!
 */
@Singleton
public class BulkOperationService {

    private static final Logger log = LoggerFactory.getLogger(BulkOperationService.class);

    @PersistenceContext
    private final EntityManager entityManager;

    private final VehicleRepository vehicleRepository;

    public BulkOperationService(EntityManager entityManager, VehicleRepository vehicleRepository) {
        this.entityManager = entityManager;
        this.vehicleRepository = vehicleRepository;
    }

    /**
     * Ingests a large batch of telemetry readings with periodic flush and clear.
     */
    @Transactional
    public int batchInsertReadings(int totalCount, int batchSize) {
        log.info("Starting bulk insertion of {} records with flush batch size of {}", totalCount, batchSize);

        Instant baseTime = Instant.now();
        for (int i = 0; i < totalCount; i++) {
            TelemetryReading reading = new TelemetryReading(
                "AA:BB:CC:DD:EE:" + String.format("%02X", (i % 256)),
                baseTime.minusSeconds(totalCount - i),
                22.5 + (i % 15),
                12.4 + (i % 3) * 0.1,
                65.0 + (i % 40),
                new GpsCoordinate(-23.5505 + (i * 0.0001), -46.6333 + (i * 0.0001), 760.0)
            );

            entityManager.persist(reading);

            // 💡 JPA TIP: Flush and Clear pattern
            if ((i + 1) % batchSize == 0) {
                log.debug("Flushing and clearing persistence context at record count: {}", (i + 1));
                entityManager.flush(); // Execute SQL INSERTs via JDBC batch
                entityManager.clear(); // Empty first-level cache to reclaim JVM heap
            }
        }

        // Final flush for remaining items
        entityManager.flush();
        entityManager.clear();

        log.info("Completed bulk insertion of {} records successfully.", totalCount);
        return totalCount;
    }

    /**
     * Demonstrates JPQL Bulk Update vs Individual Entity Dirty Checking.
     * 💡 JPA TIP: JPQL bulk update directly executes SQL:
     * UPDATE vehicles SET status = ? WHERE status = ?
     * It does NOT load entities into memory, nor does it fire entity lifecycle callbacks!
     */
    @Transactional
    public int executeBulkStatusUpdate(AssetStatus newStatus, AssetStatus currentStatus) {
        log.info("Executing JPQL bulk update from {} to {}", currentStatus, newStatus);
        int rowsUpdated = vehicleRepository.updateStatusInBulk(newStatus, currentStatus);
        
        // 💡 JPA TIP: Because bulk queries bypass the Persistence Context,
        // any entities already cached in memory would have stale data.
        // Calling entityManager.clear() ensures subsequent queries read fresh data from the DB!
        entityManager.clear();

        log.info("Bulk updated {} rows directly in the database", rowsUpdated);
        return rowsUpdated;
    }
}
