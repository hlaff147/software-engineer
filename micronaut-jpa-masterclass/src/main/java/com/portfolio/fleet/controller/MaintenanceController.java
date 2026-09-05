package com.portfolio.fleet.controller;

import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.dto.MaintenanceFilterRequest;
import com.portfolio.fleet.service.MaintenanceQueryService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import io.micronaut.http.annotation.QueryValue;
import java.util.List;
import java.util.Map;

@Controller("/api/maintenance")
public class MaintenanceController {

    private final MaintenanceQueryService maintenanceService;

    public MaintenanceController(MaintenanceQueryService maintenanceService) {
        this.maintenanceService = maintenanceService;
    }

    @Post
    public HttpResponse<MaintenanceSchedule> createSchedule(@Body MaintenanceSchedule schedule) {
        return HttpResponse.created(maintenanceService.scheduleMaintenance(schedule));
    }

    @Get("/{id}")
    public HttpResponse<MaintenanceSchedule> getSchedule(@PathVariable Long id) {
        return maintenanceService.getScheduleWithLogs(id)
            .map(HttpResponse::ok)
            .orElseGet(HttpResponse::notFound);
    }

    @Post("/search")
    public HttpResponse<Map<String, Object>> searchDynamic(
            @Body MaintenanceFilterRequest filter,
            @QueryValue(defaultValue = "0") Integer page,
            @QueryValue(defaultValue = "10") Integer size) {

        List<MaintenanceSchedule> results = maintenanceService.searchSchedules(filter, page, size);
        long total = maintenanceService.countSchedules(filter);

        return HttpResponse.ok(Map.of(
            "content", results,
            "totalElements", total,
            "page", page,
            "size", size
        ));
    }
}
