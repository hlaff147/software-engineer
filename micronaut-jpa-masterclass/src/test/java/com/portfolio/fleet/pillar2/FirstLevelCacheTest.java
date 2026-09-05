package com.portfolio.fleet.pillar2;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.repository.VehicleRepository;
import com.portfolio.fleet.service.PersistenceContextDemoService;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 2: First-Level Cache & Dirty Checking Mechanics")
class FirstLevelCacheTest {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private PersistenceContextDemoService demoService;

    @Inject
    private EntityManager entityManager;

    private Long savedVehicleId;

    @BeforeEach
    void setUp() {
        Vehicle vehicle = new Vehicle(
            "AST-CACHE-01", "Scania R450", AssetStatus.ACTIVE, 
            "L1-CACHE", "VINL1TEST0001", 100000L, FuelType.DIESEL
        );
        Vehicle saved = vehicleRepository.save(vehicle);
        savedVehicleId = saved.getId();
    }

    @Test
    @Transactional
    @DisplayName("💡 JPA TIP: findById() doesn't always hit DB — L1 Cache returns identical object instance")
    void testFirstLevelCacheHitAndObjectIdentity() {
        // 1. First findById(): Database hit (SELECT SQL executed and entity registered in L1 Cache)
        Vehicle firstCall = vehicleRepository.findById(savedVehicleId).orElseThrow();

        // 2. Second findById(): First-Level Cache hit! No second SQL SELECT is executed.
        Vehicle secondCall = vehicleRepository.findById(savedVehicleId).orElseThrow();

        // 💡 IDENTITY GUARANTEE: In the same persistence context, Hibernate guarantees that
        // repeated queries for the same entity primary key return the EXACT SAME memory reference!
        assertThat(firstCall).isSameAs(secondCall);
        assertThat(firstCall == secondCall).isTrue();

        // Entity is currently managed
        assertThat(entityManager.contains(firstCall)).isTrue();
    }

    @Test
    @DisplayName("Verified via PersistenceContextDemoService")
    void testServiceFirstLevelCacheVerification() {
        boolean cacheHitGuaranteed = demoService.verifyFirstLevelCacheHit(savedVehicleId);
        assertThat(cacheHitGuaranteed).isTrue();
    }

    @Test
    @DisplayName("💡 JPA TIP: Dirty Checking automatically persists changes without explicit save()")
    void testDirtyCheckingMechanism() {
        Long addedMileage = 500L;
        Long expectedMileage = 100000L + addedMileage;

        // Execute service method where NO repository.save() or update() is called
        Long newMileage = demoService.demonstrateDirtyChecking(savedVehicleId, addedMileage);
        assertThat(newMileage).isEqualTo(expectedMileage);

        // Verify the database state in a fresh transaction
        Vehicle reloaded = vehicleRepository.findById(savedVehicleId).orElseThrow();
        assertThat(reloaded.getMileage()).isEqualTo(expectedMileage);
    }
}
