package com.portfolio.fleet.dto;

import com.portfolio.fleet.domain.asset.AssetStatus;
import io.micronaut.core.annotation.Introspected;

/**
 * 💡 JPA TIP: Constructor-Expression DTO Projection
 * Used in JPQL: SELECT new com.portfolio.fleet.dto.AssetSummaryDTO(...)
 * 
 * Benefits:
 * 1. Bypasses Hibernate's First-Level Cache (persistence context overhead).
 * 2. Fetches ONLY required columns from the database, eliminating network bloat.
 * 3. Immutable Java Record guarantees thread safety.
 */
@Introspected
public record AssetSummaryDTO(
    Long id,
    String assetCode,
    String name,
    AssetStatus status,
    String operatorName
) {}
