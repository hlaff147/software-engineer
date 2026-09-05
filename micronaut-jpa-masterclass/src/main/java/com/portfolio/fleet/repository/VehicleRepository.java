package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.model.Page;
import io.micronaut.data.model.Pageable;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

/**
 * 💡 JPA TIP: Micronaut Query Derivation
 * Micronaut Data parses method names at compile-time and synthesizes JPQL/SQL.
 * E.g., findByStatusAndMileageGreaterThan -> WHERE status = ? AND mileage > ?
 */
@Repository
public interface VehicleRepository extends JpaRepository<Vehicle, Long> {

    Optional<Vehicle> findByLicensePlate(String licensePlate);

    Optional<Vehicle> findByVin(String vin);

    @Join(value = "operator", type = Join.Type.LEFT_FETCH)
    List<Vehicle> findByStatusAndMileageGreaterThan(AssetStatus status, Long minMileage);

    List<Vehicle> findByFuelType(FuelType fuelType);

    Page<Vehicle> findByStatus(AssetStatus status, Pageable pageable);

    // 💡 JPA TIP: Bulk UPDATE query in JPQL
    // Modifies records directly in database without loading entities into Persistence Context.
    @Query("UPDATE Vehicle v SET v.status = :newStatus WHERE v.status = :currentStatus")
    int updateStatusInBulk(AssetStatus newStatus, AssetStatus currentStatus);
}
