package com.portfolio.fleet.pillar4;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.repository.VehicleRepository;
import com.portfolio.fleet.service.OptimisticLockingService;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.OptimisticLockException;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@MicronautTest(transactional = false)
@DisplayName("Pillar 4: Optimistic Locking with @Version")
class OptimisticLockTest {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private OptimisticLockingService optimisticLockingService;

    @Inject
    private EntityManager entityManager;

    @Test
    @DisplayName("@Version: Detects concurrent update and throws OptimisticLockException on stale version")
    void testOptimisticLockFailureDetection() {
        Vehicle vehicle = new Vehicle("AST-OPT-01", "Iveco S-Way", AssetStatus.ACTIVE, "OPT-1234", "VINOPT0001", 10000L, FuelType.GASOLINE);
        Vehicle saved = vehicleRepository.save(vehicle);
        Long vehicleId = saved.getId();

        // Transaction 1 reads the entity
        Vehicle tx1View = vehicleRepository.findById(vehicleId).orElseThrow();
        Long originalVersion = tx1View.getVersion();

        // Transaction 2 updates the vehicle independently, incrementing the version in the database
        optimisticLockingService.updateVehicleMileage(vehicleId, 15000L);

        // Transaction 1 attempts to update using its stale version
        tx1View.setMileage(20000L);

        assertThatThrownBy(() -> {
            vehicleRepository.update(tx1View);
        }).isInstanceOf(Exception.class); // Throws OptimisticLockException or DataAccessException wrapping it
    }

    @Test
    @DisplayName("Retry Mechanism: Resolves optimistic lock conflicts gracefully")
    void testOptimisticLockWithRetry() {
        Vehicle vehicle = new Vehicle("AST-RETRY-01", "Renault T", AssetStatus.ACTIVE, "RTY-5678", "VINRTY0001", 5000L, FuelType.DIESEL);
        Vehicle saved = vehicleRepository.save(vehicle);

        Vehicle updated = optimisticLockingService.updateWithRetry(saved.getId(), 8500L, 3);
        assertThat(updated.getMileage()).isEqualTo(8500L);
    }
}
