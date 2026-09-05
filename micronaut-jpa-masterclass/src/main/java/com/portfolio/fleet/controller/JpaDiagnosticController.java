package com.portfolio.fleet.controller;

import com.portfolio.fleet.service.JpaDiagnosticService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.Post;
import java.util.Map;

/**
 * 🔬 JPA DIAGNOSTIC & WORKSHOP CONTROLLER
 * 
 * Exposes REST endpoints to trigger and verify JPA behaviors in real time:
 * - /api/diagnostic/seed              : Initialize sample data for diagnostics
 * - /api/diagnostic/l1-cache          : Verify First-Level Cache hit and object identity
 * - /api/diagnostic/dirty-checking    : Verify automatic snapshot comparison and flush
 * - /api/diagnostic/detach-lifecycle  : Demonstrate MANAGED -> DETACHED -> MANAGED transitions
 * - /api/diagnostic/n-plus-1          : Demonstrate N+1 problem & @BatchSize mitigation
 * - /api/diagnostic/optimistic-lock   : Simulate concurrent version conflict (@Version)
 * - /api/diagnostic/statistics        : Retrieve real-time Hibernate execution statistics
 */
@Controller("/api/diagnostic")
public class JpaDiagnosticController {

    private final JpaDiagnosticService diagnosticService;

    public JpaDiagnosticController(JpaDiagnosticService diagnosticService) {
        this.diagnosticService = diagnosticService;
    }

    @Post("/seed")
    public HttpResponse<Map<String, Object>> seedTestData() {
        return HttpResponse.ok(diagnosticService.seedTestData());
    }

    @Get("/l1-cache")
    public HttpResponse<Map<String, Object>> demonstrateFirstLevelCache() {
        return HttpResponse.ok(diagnosticService.demonstrateFirstLevelCache());
    }

    @Post("/dirty-checking")
    public HttpResponse<Map<String, Object>> demonstrateDirtyChecking() {
        return HttpResponse.ok(diagnosticService.demonstrateDirtyChecking());
    }

    @Post("/detach-lifecycle")
    public HttpResponse<Map<String, Object>> demonstrateDetachLifecycle() {
        return HttpResponse.ok(diagnosticService.demonstrateDetachAndReattach());
    }

    @Get("/n-plus-1")
    public HttpResponse<Map<String, Object>> demonstrateNPlus1() {
        return HttpResponse.ok(diagnosticService.demonstrateNPlus1Problem());
    }

    @Post("/optimistic-lock")
    public HttpResponse<Map<String, Object>> demonstrateOptimisticLock() {
        return HttpResponse.ok(diagnosticService.demonstrateOptimisticLockConflict());
    }

    @Get("/statistics")
    public HttpResponse<Map<String, Object>> captureStatistics() {
        return HttpResponse.ok(diagnosticService.captureHibernateStatistics());
    }
}
