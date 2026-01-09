package com.openfinance.payments.domain.port.output;

import com.openfinance.payments.domain.entity.PixPayment;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

public interface PaymentRepositoryPort {
    PixPayment save(PixPayment payment);

    Optional<PixPayment> findById(String paymentId);

    List<PixPayment> findByConsentId(String consentId);

    List<PixPayment> findByConsentIdAndDateRange(String consentId, LocalDate startDate, LocalDate endDate);

    boolean existsByIdempotencyKey(String idempotencyKey);

    Optional<PixPayment> findByIdempotencyKey(String idempotencyKey);
}
