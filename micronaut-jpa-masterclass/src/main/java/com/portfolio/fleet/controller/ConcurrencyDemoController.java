package com.portfolio.fleet.controller;

import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.service.OptimisticLockingService;
import com.portfolio.fleet.service.PessimisticLockingService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.QueryValue;
import java.math.BigDecimal;
import java.util.Map;

@Controller("/api/demo/concurrency")
public class ConcurrencyDemoController {

    private final OptimisticLockingService optimisticService;
    private final PessimisticLockingService pessimisticService;

    public ConcurrencyDemoController(OptimisticLockingService optimisticService, 
                                     PessimisticLockingService pessimisticService) {
        this.optimisticService = optimisticService;
        this.pessimisticService = pessimisticService;
    }

    /**
     * Demonstrates Optimistic Locking with automatic retry
     */
    @Post("/optimistic-lock/{vehicleId}")
    public HttpResponse<Map<String, Object>> updateWithOptimisticLock(
            @PathVariable Long vehicleId, 
            @QueryValue Long newMileage) {

        Vehicle updated = optimisticService.updateWithRetry(vehicleId, newMileage, 3);
        return HttpResponse.ok(Map.of(
            "vehicleId", updated.getId(),
            "newMileage", updated.getMileage(),
            "version", updated.getVersion(),
            "lockingStrategy", "OPTIMISTIC (@Version)"
        ));
    }

    /**
     * Demonstrates Pessimistic Locking (SELECT FOR UPDATE)
     */
    @Post("/pessimistic-lock/{operatorId}/deduct")
    public HttpResponse<Map<String, Object>> deductBudget(
            @PathVariable Long operatorId, 
            @QueryValue BigDecimal amount) {

        BigDecimal remaining = pessimisticService.deductBudgetWithPessimisticLock(operatorId, amount);
        return HttpResponse.ok(Map.of(
            "operatorId", operatorId,
            "deductedAmount", amount,
            "remainingBudget", remaining,
            "lockingStrategy", "PESSIMISTIC_WRITE (SELECT FOR UPDATE)"
        ));
    }
}
