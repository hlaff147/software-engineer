package com.portfolio.fleet.controller;

import com.portfolio.fleet.domain.asset.Asset;
import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.dto.AssetSummaryDTO;
import com.portfolio.fleet.service.AssetService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.QueryValue;
import java.util.List;

@Controller("/api/assets")
public class AssetController {

    private final AssetService assetService;

    public AssetController(AssetService assetService) {
        this.assetService = assetService;
    }

    @Post("/vehicles")
    public HttpResponse<Vehicle> registerVehicle(@Body Vehicle vehicle) {
        Vehicle saved = assetService.registerVehicle(vehicle);
        return HttpResponse.created(saved);
    }

    @Get("/{id}/details")
    public HttpResponse<Asset> getAssetDetails(@PathVariable Long id) {
        return assetService.getAssetDetailed(id)
            .map(HttpResponse::ok)
            .orElseGet(HttpResponse::notFound);
    }

    @Get("/summaries")
    public HttpResponse<List<AssetSummaryDTO>> getSummaries(@QueryValue(defaultValue = "ACTIVE") AssetStatus status) {
        return HttpResponse.ok(assetService.getAssetSummaries(status));
    }

    @Get("/vehicles/high-mileage")
    public HttpResponse<List<Vehicle>> getHighMileage(
            @QueryValue(defaultValue = "ACTIVE") AssetStatus status,
            @QueryValue(defaultValue = "100000") Long minMileage) {
        return HttpResponse.ok(assetService.getHighMileageVehicles(status, minMileage));
    }
}
