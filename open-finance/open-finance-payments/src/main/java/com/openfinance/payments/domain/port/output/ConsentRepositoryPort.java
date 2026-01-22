package com.openfinance.payments.domain.port.output;

import com.openfinance.payments.domain.entity.Consent;

import java.util.Optional;

public interface ConsentRepositoryPort {
    Consent save(Consent consent);

    Optional<Consent> findById(String consentId);

    boolean existsByIdempotencyKey(String idempotencyKey);

    Optional<Consent> findByIdempotencyKey(String idempotencyKey);
}
