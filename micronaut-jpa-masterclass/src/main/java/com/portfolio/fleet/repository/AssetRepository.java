package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.asset.Asset;
import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.dto.AssetSummaryDTO;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.Optional;

/**
 * 💡 JPA TIP: Declarative Fetching & EntityGraph
 * Micronaut Data allows compile-time validated @Join annotations.
 * Join.Type.FETCH forces an SQL INNER JOIN FETCH, eliminating N+1 queries.
 * Join.Type.LEFT_FETCH performs a LEFT OUTER JOIN FETCH, safe for nullable associations.
 */
@Repository
public interface AssetRepository extends JpaRepository<Asset, Long> {

    Optional<Asset> findByAssetCode(String assetCode);

    // 💡 JPA TIP: Eagerly joins operator and maintenanceSchedules in a single query
    @Query("SELECT a FROM Asset a LEFT JOIN FETCH a.operator LEFT JOIN FETCH a.maintenanceSchedules WHERE a.id = :id")
    Optional<Asset> findWithDetailsById(Long id);

    // 💡 JPA TIP: Constructor-expression DTO projection directly from JPQL
    @Query("""
        SELECT new com.portfolio.fleet.dto.AssetSummaryDTO(
            a.id, a.assetCode, a.name, a.status, o.name
        )
        FROM Asset a
        LEFT JOIN a.operator o
        WHERE a.status = :status
        ORDER BY a.name ASC
    """)
    List<AssetSummaryDTO> findSummariesByStatus(AssetStatus status);

    // 💡 JPA TIP: Explicit JOIN FETCH in JPQL
    @Query("SELECT a FROM Asset a JOIN FETCH a.operator WHERE a.operator.id = :operatorId")
    List<Asset> findAllByOperatorIdWithFetch(Long operatorId);
}
