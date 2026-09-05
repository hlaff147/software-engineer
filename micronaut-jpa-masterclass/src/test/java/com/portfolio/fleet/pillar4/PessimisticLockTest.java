package com.portfolio.fleet.pillar4;

import com.portfolio.fleet.domain.common.Money;
import com.portfolio.fleet.domain.operator.Operator;
import com.portfolio.fleet.repository.OperatorRepository;
import com.portfolio.fleet.service.PessimisticLockingService;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

@MicronautTest(transactional = false)
@DisplayName("Pillar 4: Pessimistic Locking (SELECT FOR UPDATE)")
class PessimisticLockTest {

    @Inject
    private OperatorRepository operatorRepository;

    @Inject
    private PessimisticLockingService pessimisticLockingService;

    @Test
    @DisplayName("PESSIMISTIC_WRITE: Acquires exclusive lock and safely decrements budget")
    void testPessimisticWriteBudgetDeduction() {
        Operator operator = new Operator("Global Freight Inc.", "44.555.666/0001-77", "finance@globalfreight.com", new Money(new BigDecimal("10000.00"), "USD"));
        Operator saved = operatorRepository.save(operator);

        BigDecimal remaining = pessimisticLockingService.deductBudgetWithPessimisticLock(saved.getId(), new BigDecimal("2500.00"));
        assertThat(remaining).isEqualByComparingTo(new BigDecimal("7500.00"));

        // Verify insufficient funds exception under lock
        assertThatThrownBy(() -> {
            pessimisticLockingService.deductBudgetWithPessimisticLock(saved.getId(), new BigDecimal("8000.00"));
        }).isInstanceOf(IllegalStateException.class)
          .hasMessageContaining("Insufficient operational budget");
    }
}
