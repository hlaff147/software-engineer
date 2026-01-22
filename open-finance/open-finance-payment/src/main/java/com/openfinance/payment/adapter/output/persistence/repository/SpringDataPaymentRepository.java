package com.openfinance.payment.adapter.output.persistence.repository;

import com.openfinance.payment.adapter.output.persistence.document.PaymentDocument;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface SpringDataPaymentRepository extends MongoRepository<PaymentDocument, String> {
    List<PaymentDocument> findByConsentId(String consentId);

    List<PaymentDocument> findByConsentIdAndCreationDateTimeBetween(
            String consentId, Instant startDateTime, Instant endDateTime);

    Optional<PaymentDocument> findByIdempotencyKey(String idempotencyKey);

    boolean existsByIdempotencyKey(String idempotencyKey);
}
