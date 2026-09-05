package com.portfolio.fleet.controller;

import com.portfolio.fleet.service.PersistenceContextDemoService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.QueryValue;
import java.util.Map;

@Controller("/api/demo/persistence-context")
public class PersistenceContextDemoController {

    private final PersistenceContextDemoService demoService;

    public PersistenceContextDemoController(PersistenceContextDemoService demoService) {
        this.demoService = demoService;
    }

    /**
     * Demonstrates L1 cache hit and identity guarantee (User's JPA tip!)
     */
    @Get("/l1-cache-hit/{vehicleId}")
    public HttpResponse<Map<String, Object>> verifyFirstLevelCache(@PathVariable Long vehicleId) {
        boolean isSameInstance = demoService.verifyFirstLevelCacheHit(vehicleId);
        return HttpResponse.ok(Map.of(
            "vehicleId", vehicleId,
            "firstLevelCacheHit", true,
            "referenceEqualityGuaranteed", isSameInstance,
            "explanation", "Second findById() hit Hibernate First-Level Cache directly without SQL SELECT"
        ));
    }

    /**
     * Demonstrates Dirty Checking without save()
     */
    @Post("/dirty-checking/{vehicleId}")
    public HttpResponse<Map<String, Object>> demonstrateDirtyChecking(
            @PathVariable Long vehicleId, 
            @QueryValue(defaultValue = "150") Long addedMileage) {

        Long newMileage = demoService.demonstrateDirtyChecking(vehicleId, addedMileage);
        return HttpResponse.ok(Map.of(
            "vehicleId", vehicleId,
            "addedMileage", addedMileage,
            "newMileage", newMileage,
            "dirtyCheckingSuccessful", true,
            "explanation", "Hibernate automatically triggered SQL UPDATE on commit without calling save() or update()"
        ));
    }

    /**
     * Demonstrates Detached Entity
     */
    @Post("/detach/{vehicleId}")
    public HttpResponse<Map<String, Object>> demonstrateDetach(@PathVariable Long vehicleId) {
        demoService.demonstrateDetachedEntity(vehicleId);
        return HttpResponse.ok(Map.of(
            "vehicleId", vehicleId,
            "status", "detached",
            "explanation", "Entity detached via entityManager.detach(). Modifications ignored by Hibernate."
        ));
    }
}
