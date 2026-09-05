package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.operator.Operator;
import com.portfolio.fleet.dto.OperatorDashboardDTO;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

/**
 * 💡 JPA TIP: Projections & Native Queries
 * Demonstrates JPQL aggregate projections into DTO records alongside native SQL queries.
 */
@Repository
public interface OperatorRepository extends JpaRepository<Operator, Long> {

    Optional<Operator> findByTaxId(String taxId);

    Optional<Operator> findByEmail(String email);

    @Query("SELECT o FROM Operator o LEFT JOIN FETCH o.license LEFT JOIN FETCH o.certifications WHERE o.id = :id")
    Optional<Operator> findDetailedById(Long id);

    // 💡 JPA TIP: Aggregate constructor projection across joined tables
    @Query("""
        SELECT new com.portfolio.fleet.dto.OperatorDashboardDTO(
            o.name,
            o.taxId,
            COUNT(DISTINCT v.id),
            COALESCE(SUM(v.mileage), 0L),
            o.operationalBudget.amount,
            o.operationalBudget.currency
        )
        FROM Operator o
        LEFT JOIN o.assets a
        LEFT JOIN Vehicle v ON v.id = a.id
        GROUP BY o.name, o.taxId, o.operationalBudget.amount, o.operationalBudget.currency
        ORDER BY o.name ASC
    """)
    List<OperatorDashboardDTO> getOperatorDashboardStats();

    // 💡 JPA TIP: Native SQL Query with Scalar Projection
    @Query(value = """
        SELECT o.name AS operator_name, COUNT(a.id) AS asset_count
        FROM operators o
        LEFT JOIN assets a ON a.operator_id = o.id
        GROUP BY o.name
        ORDER BY asset_count DESC
    """, nativeQuery = true)
    List<Object[]> getOperatorAssetCountsNative();
}
