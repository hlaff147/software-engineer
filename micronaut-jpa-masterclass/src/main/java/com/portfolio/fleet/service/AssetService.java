package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.asset.Asset;
import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.dto.AssetSummaryDTO;
import com.portfolio.fleet.repository.AssetRepository;
import com.portfolio.fleet.repository.VehicleRepository;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;
import java.util.Optional;

@Singleton
public class AssetService {

    private static final Logger log = LoggerFactory.getLogger(AssetService.class);

    private final AssetRepository assetRepository;
    private final VehicleRepository vehicleRepository;

    public AssetService(AssetRepository assetRepository, VehicleRepository vehicleRepository) {
        this.assetRepository = assetRepository;
        this.vehicleRepository = vehicleRepository;
    }

    @Transactional
    public Vehicle registerVehicle(Vehicle vehicle) {
        log.info("Registering new vehicle with plate: {}", vehicle.getLicensePlate());
        return vehicleRepository.save(vehicle);
    }

    @Transactional
    public Optional<Asset> getAssetDetailed(Long assetId) {
        // 💡 JPA TIP: Uses @Join (LEFT_FETCH) to load asset, operator, and maintenance schedules in 1 query
        return assetRepository.findWithDetailsById(assetId);
    }

    @Transactional
    public List<AssetSummaryDTO> getAssetSummaries(AssetStatus status) {
        // 💡 JPA TIP: Constructor-expression projection query bypassing full entity graph
        return assetRepository.findSummariesByStatus(status);
    }

    @Transactional
    public List<Vehicle> getHighMileageVehicles(AssetStatus status, Long minMileage) {
        return vehicleRepository.findByStatusAndMileageGreaterThan(status, minMileage);
    }
}
