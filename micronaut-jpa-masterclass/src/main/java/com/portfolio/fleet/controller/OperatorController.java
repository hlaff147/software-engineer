package com.portfolio.fleet.controller;

import com.portfolio.fleet.domain.operator.Operator;
import com.portfolio.fleet.dto.OperatorDashboardDTO;
import com.portfolio.fleet.repository.OperatorRepository;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Body;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.annotation.Post;
import java.util.List;

@Controller("/api/operators")
public class OperatorController {

    private final OperatorRepository operatorRepository;

    public OperatorController(OperatorRepository operatorRepository) {
        this.operatorRepository = operatorRepository;
    }

    @Post
    public HttpResponse<Operator> createOperator(@Body Operator operator) {
        return HttpResponse.created(operatorRepository.save(operator));
    }

    @Get("/{id}")
    public HttpResponse<Operator> getOperator(@PathVariable Long id) {
        return operatorRepository.findDetailedById(id)
            .map(HttpResponse::ok)
            .orElseGet(HttpResponse::notFound);
    }

    @Get("/dashboard")
    public HttpResponse<List<OperatorDashboardDTO>> getDashboard() {
        return HttpResponse.ok(operatorRepository.getOperatorDashboardStats());
    }

    @Get("/stats/native")
    public HttpResponse<List<Object[]>> getNativeStats() {
        return HttpResponse.ok(operatorRepository.getOperatorAssetCountsNative());
    }
}
