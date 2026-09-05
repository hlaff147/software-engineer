package com.portfolio.fleet.service;

import com.portfolio.fleet.domain.operator.Operator;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManager;
import jakarta.persistence.LockModeType;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.math.BigDecimal;
import java.util.Map;

/**
 * 💡 JPA TIP: Pessimistic Locking (SELECT ... FOR UPDATE)
 * 
 * For critical financial and inventory allocations where conflicts are frequent or catastrophic,
 * pessimistic locking directly instructs the database engine to acquire an exclusive row-level lock.
 * 
 * LockModeType.PESSIMISTIC_WRITE translates to:
 * SELECT ... FROM operators WHERE id = ? FOR UPDATE
 * 
 * Other transactions attempting to acquire the lock will wait until the first transaction commits
 * or until the timeout specified via 'jakarta.persistence.lock.timeout' expires.
 */
@Singleton
public class PessimisticLockingService {

    private static final Logger log = LoggerFactory.getLogger(PessimisticLockingService.class);

    @PersistenceContext
    private final EntityManager entityManager;

    public PessimisticLockingService(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    /**
     * Allocates operational budget safely under high concurrency.
     */
    @Transactional
    public BigDecimal deductBudgetWithPessimisticLock(Long operatorId, BigDecimal deductionAmount) {
        log.info("Acquiring PESSIMISTIC_WRITE lock on Operator ID {}", operatorId);

        // 💡 JPA TIP: Passing lock timeout hint to prevent indefinite thread blockage
        Map<String, Object> hints = Map.of("jakarta.persistence.lock.timeout", 3000);

        Operator operator = entityManager.find(
            Operator.class, 
            operatorId, 
            LockModeType.PESSIMISTIC_WRITE, 
            hints
        );

        if (operator == null) {
            throw new IllegalArgumentException("Operator not found with ID: " + operatorId);
        }

        BigDecimal currentBudget = operator.getOperationalBudget() != null && operator.getOperationalBudget().getAmount() != null
            ? operator.getOperationalBudget().getAmount()
            : BigDecimal.ZERO;

        if (currentBudget.compareTo(deductionAmount) < 0) {
            throw new IllegalStateException("Insufficient operational budget: current=" + currentBudget + ", requested=" + deductionAmount);
        }

        BigDecimal newBudget = currentBudget.subtract(deductionAmount);
        operator.getOperationalBudget().setAmount(newBudget);

        log.info("Successfully deducted {} under lock. New budget: {}", deductionAmount, newBudget);
        return newBudget;
    }

    /**
     * Reads with PESSIMISTIC_READ (shared lock: SELECT ... FOR SHARE / LOCK IN SHARE MODE).
     * Guarantees no other transaction can modify the record while this transaction inspects it.
     */
    @Transactional
    public BigDecimal getBudgetWithSharedLock(Long operatorId) {
        Operator operator = entityManager.find(
            Operator.class, 
            operatorId, 
            LockModeType.PESSIMISTIC_READ
        );
        if (operator == null) {
            throw new IllegalArgumentException("Operator not found");
        }
        return operator.getOperationalBudget() != null ? operator.getOperationalBudget().getAmount() : BigDecimal.ZERO;
    }
}
