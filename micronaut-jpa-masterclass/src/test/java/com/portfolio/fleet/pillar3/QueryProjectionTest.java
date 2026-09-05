package com.portfolio.fleet.pillar3;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.domain.common.Money;
import com.portfolio.fleet.domain.operator.Operator;
import com.portfolio.fleet.dto.AssetSummaryDTO;
import com.portfolio.fleet.dto.OperatorDashboardDTO;
import com.portfolio.fleet.repository.AssetRepository;
import com.portfolio.fleet.repository.OperatorRepository;
import com.portfolio.fleet.repository.VehicleRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.util.List;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 3: Advanced Querying & Projections")
class QueryProjectionTest {

    @Inject
    private AssetRepository assetRepository;

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private OperatorRepository operatorRepository;

    @Inject
    private EntityManager entityManager;

    @Test
    @Transactional
    @DisplayName("Constructor-Expression DTO Projection: Fetching read-only DTO records directly from JPQL")
    void testConstructorExpressionDtoProjection() {
        Operator operator = new Operator("Nexus Transport", "33.222.111/0001-99", "ops@nexus.com", new Money(new BigDecimal("900000"), "BRL"));
        operatorRepository.save(operator);

        Vehicle vehicle = new Vehicle("AST-PROJ-01", "Scania Super 560", AssetStatus.ACTIVE, "PRJ-1001", "VINPROJ0001", 30000L, FuelType.DIESEL);
        vehicle.setOperator(operator);
        vehicleRepository.save(vehicle);

        entityManager.flush();
        entityManager.clear();

        List<AssetSummaryDTO> summaries = assetRepository.findSummariesByStatus(AssetStatus.ACTIVE);
        assertThat(summaries).isNotEmpty();

        AssetSummaryDTO summary = summaries.stream()
            .filter(s -> "AST-PROJ-01".equals(s.assetCode()))
            .findFirst()
            .orElseThrow();

        assertThat(summary.name()).isEqualTo("Scania Super 560");
        assertThat(summary.operatorName()).isEqualTo("Nexus Transport");
    }

    @Test
    @Transactional
    @DisplayName("Aggregate Projection: GROUP BY with COUNT and SUM projected into OperatorDashboardDTO")
    void testAggregateProjection() {
        Operator operator = new Operator("LogiPrime", "77.888.999/0001-33", "prime@logiprime.com", new Money(new BigDecimal("2500000"), "USD"));
        operatorRepository.save(operator);

        Vehicle v1 = new Vehicle("AST-AGGR-01", "Delivery Van 1", AssetStatus.ACTIVE, "AGR-1001", "VINAGR001", 20000L, FuelType.ELECTRIC);
        v1.setOperator(operator);
        vehicleRepository.save(v1);

        Vehicle v2 = new Vehicle("AST-AGGR-02", "Delivery Van 2", AssetStatus.ACTIVE, "AGR-1002", "VINAGR002", 35000L, FuelType.ELECTRIC);
        v2.setOperator(operator);
        vehicleRepository.save(v2);

        entityManager.flush();
        entityManager.clear();

        List<OperatorDashboardDTO> dashboard = operatorRepository.getOperatorDashboardStats();
        assertThat(dashboard).isNotEmpty();

        OperatorDashboardDTO stats = dashboard.stream()
            .filter(d -> "LogiPrime".equals(d.operatorName()))
            .findFirst()
            .orElseThrow();

        assertThat(stats.vehicleCount()).isGreaterThanOrEqualTo(2L);
        assertThat(stats.totalMileage()).isGreaterThanOrEqualTo(55000L);
    }

    @Test
    @Transactional
    @DisplayName("Native SQL Query: Scalar projection using raw database SQL")
    void testNativeQueryScalarProjection() {
        List<Object[]> results = operatorRepository.getOperatorAssetCountsNative();
        assertThat(results).isNotNull();
    }
}
