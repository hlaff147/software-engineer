package com.openfinance.consent.domain.port.output;

import com.openfinance.consent.domain.entity.Consent;

import java.util.Optional;

public interface ConsentRepositoryPort {
    Consent save(Consent consent);

    Optional<Consent> findById(String consentId);

    boolean existsByIdempotencyKey(String idempotencyKey);

    Optional<Consent> findByIdempotencyKey(String idempotencyKey);
}
