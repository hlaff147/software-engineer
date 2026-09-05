package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.repository.VehicleRepository;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManager;
import jakarta.persistence.OptimisticLockException;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 💡 JPA TIP: Optimistic Locking with @Version
 * 
 * In high-concurrency systems where conflict frequency is relatively low,
 * optimistic locking provides maximum throughput because transactions do NOT lock
 * database rows with exclusive locks.
 * 
 * Instead, Hibernate appends the version check to the UPDATE statement:
 * UPDATE assets SET version = version + 1 WHERE id = ? AND version = ?
 * 
 * If another transaction committed an update in the meantime, the WHERE clause finds 0 rows,
 * and Hibernate throws an OptimisticLockException.
 */
@Singleton
public class OptimisticLockingService {

    private static final Logger log = LoggerFactory.getLogger(OptimisticLockingService.class);

    private final VehicleRepository vehicleRepository;

    @PersistenceContext
    private final EntityManager entityManager;

    public OptimisticLockingService(VehicleRepository vehicleRepository, EntityManager entityManager) {
        this.vehicleRepository = vehicleRepository;
        this.entityManager = entityManager;
    }

    /**
     * Standard update utilizing @Version.
     */
    @Transactional
    public Vehicle updateVehicleMileage(Long vehicleId, Long newMileage) {
        Vehicle vehicle = vehicleRepository.findById(vehicleId)
            .orElseThrow(() -> new IllegalArgumentException("Vehicle not found: " + vehicleId));

        log.info("Updating vehicle ID {} with current version {}", vehicleId, vehicle.getVersion());
        vehicle.setMileage(newMileage);
        // Dirty checking commits the update with incremented version
        return vehicle;
    }

    /**
     * Executes update with resilient retry loop upon optimistic locking conflict.
     */
    public Vehicle updateWithRetry(Long vehicleId, Long newMileage, int maxRetries) {
        int attempts = 0;
        while (attempts < maxRetries) {
            attempts++;
            try {
                return executeUpdateInTransaction(vehicleId, newMileage);
            } catch (OptimisticLockException | org.hibernate.StaleObjectStateException ex) {
                log.warn("Optimistic locking conflict on attempt {} for vehicle {}. Retrying...", attempts, vehicleId);
                if (attempts >= maxRetries) {
                    throw new IllegalStateException("Failed to update vehicle after " + maxRetries + " attempts due to concurrent modifications", ex);
                }
                try {
                    Thread.sleep(50L * attempts); // Exponential jitter backoff
                } catch (InterruptedException ie) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException("Retry interrupted", ie);
                }
            }
        }
        throw new IllegalStateException("Max retries exceeded");
    }

    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public Vehicle executeUpdateInTransaction(Long vehicleId, Long newMileage) {
        Vehicle vehicle = vehicleRepository.findById(vehicleId)
            .orElseThrow(() -> new IllegalArgumentException("Vehicle not found: " + vehicleId));
        vehicle.setMileage(newMileage);
        entityManager.flush(); // Force immediate SQL execution to trigger version check
        return vehicle;
    }
}
