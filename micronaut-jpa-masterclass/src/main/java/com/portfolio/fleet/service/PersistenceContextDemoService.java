package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.repository.VehicleRepository;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 💡 MASTERCLASS: Persistence Context, First-Level Cache & Dirty Checking
 * 
 * 💡 JPA Tip: findById() doesn't always hit the database!
 * 
 * Inside the same @Transactional boundary:
 * 1. The first repository.findById(id) issues a SELECT SQL query to the database,
 *    materializes the entity, and registers it in the Persistence Context (First-Level Cache).
 * 2. The second repository.findById(id) finds the managed entity inside the First-Level Cache
 *    and returns the EXACT SAME Java object instance immediately in memory. NO SECOND SQL SELECT!
 * 3. Dirty Checking: When you modify a setter on a managed entity (e.g. vehicle.setMileage(...)),
 *    Hibernate's snapshot comparison mechanism automatically detects the change upon transaction
 *    commit. It generates and executes the SQL UPDATE statement automatically.
 *    No explicit repository.update(entity) is required!
 */
@Singleton
public class PersistenceContextDemoService {

    private static final Logger log = LoggerFactory.getLogger(PersistenceContextDemoService.class);

    private final VehicleRepository vehicleRepository;

    @PersistenceContext
    private final EntityManager entityManager;

    public PersistenceContextDemoService(VehicleRepository vehicleRepository, EntityManager entityManager) {
        this.vehicleRepository = vehicleRepository;
        this.entityManager = entityManager;
    }

    /**
     * Demonstrates First-Level Cache hit and object identity guarantee.
     */
    @Transactional
    public boolean verifyFirstLevelCacheHit(Long vehicleId) {
        log.info("─── Step 1: First findById() -> Expected: Database hit (SELECT SQL) ───");
        Vehicle firstFetch = vehicleRepository.findById(vehicleId)
            .orElseThrow(() -> new IllegalArgumentException("Vehicle not found with ID: " + vehicleId));

        log.info("─── Step 2: Second findById() -> Expected: First-Level Cache hit (NO SQL) ───");
        Vehicle secondFetch = vehicleRepository.findById(vehicleId)
            .orElseThrow(() -> new IllegalArgumentException("Vehicle not found with ID: " + vehicleId));

        // 💡 JPA TIP: Object Identity Guarantee
        // In the same persistence context, findById for the same primary key returns
        // the EXACT SAME reference in memory: firstFetch == secondFetch is TRUE!
        boolean isSameInstance = (firstFetch == secondFetch);
        log.info("Is firstFetch == secondFetch identical reference? {}", isSameInstance);

        // Also true via EntityManager.contains
        boolean isManaged = entityManager.contains(firstFetch);
        log.info("Is entity in MANAGED state in Persistence Context? {}", isManaged);

        return isSameInstance;
    }

    /**
     * Demonstrates Dirty Checking without calling save() or update().
     */
    @Transactional
    public Long demonstrateDirtyChecking(Long vehicleId, Long addedMileage) {
        log.info("─── Step 1: Fetching vehicle (managed by Persistence Context) ───");
        Vehicle vehicle = vehicleRepository.findById(vehicleId)
            .orElseThrow(() -> new IllegalArgumentException("Vehicle not found"));

        Long oldMileage = vehicle.getMileage() != null ? vehicle.getMileage() : 0L;
        Long newMileage = oldMileage + addedMileage;

        log.info("─── Step 2: Mutating property in memory (from {} to {}) ───", oldMileage, newMileage);
        vehicle.setMileage(newMileage);

        // 💡 JPA TIP: NO call to vehicleRepository.update(vehicle) or save(vehicle)!
        // When the transaction commits, Hibernate's flush cycle:
        // 1. Compares current entity state against the baseline snapshot taken during loading.
        // 2. Detects 'mileage' was modified.
        // 3. Emits: UPDATE vehicles SET mileage=?, version=version+1 WHERE id=? AND version=?
        log.info("─── Step 3: Transaction about to commit -> Hibernate automatically triggers UPDATE ───");
        return newMileage;
    }

    /**
     * Demonstrates EntityManager.detach() and what happens when an entity is no longer managed.
     */
    @Transactional
    public void demonstrateDetachedEntity(Long vehicleId) {
        Vehicle vehicle = vehicleRepository.findById(vehicleId).orElseThrow();
        log.info("Entity is currently managed: {}", entityManager.contains(vehicle));

        // 💡 JPA TIP: Detaching removes the entity from the Persistence Context
        entityManager.detach(vehicle);
        log.info("After detach(), is entity still managed? {}", entityManager.contains(vehicle));

        // Modifying detached entity will NOT trigger dirty checking!
        vehicle.setStatus(AssetStatus.DECOMMISSIONED);
        log.info("Modified detached entity. Upon transaction commit, NO UPDATE will occur for this change!");
    }
}
