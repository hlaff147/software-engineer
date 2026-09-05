package com.portfolio.fleet.pillar2;

import com.portfolio.fleet.domain.asset.Asset;
import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.domain.common.Money;
import com.portfolio.fleet.domain.operator.Operator;
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
import java.util.Optional;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 2: Declarative Fetching & Join Fetch")
class EntityGraphTest {

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
    @DisplayName("@Join(type = LEFT_FETCH): Loads entity and associations in a single SQL query")
    void testDeclarativeFetchJoin() {
        Operator operator = new Operator("FastFleet S.A.", "55.444.333/0001-22", "fleet@fastfleet.com", new Money(new BigDecimal("750000"), "BRL"));
        operatorRepository.save(operator);

        Vehicle vehicle = new Vehicle("AST-GRAPH-01", "Mercedes Actros", AssetStatus.ACTIVE, "GRP-5555", "VINACTROS001", 80000L, FuelType.DIESEL);
        vehicle.setOperator(operator);
        vehicleRepository.save(vehicle);

        entityManager.flush();
        entityManager.clear();

        // 💡 JPA TIP: findWithDetailsById uses @Join to fetch operator eagerly in 1 query
        Optional<Asset> fetched = assetRepository.findWithDetailsById(vehicle.getId());
        assertThat(fetched).isPresent();
        assertThat(fetched.get().getOperator()).isNotNull();
        assertThat(fetched.get().getOperator().getName()).isEqualTo("FastFleet S.A.");
    }
}
