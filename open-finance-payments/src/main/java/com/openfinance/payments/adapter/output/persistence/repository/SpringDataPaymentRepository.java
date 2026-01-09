package com.openfinance.payments.adapter.output.persistence.repository;

import com.openfinance.payments.adapter.output.persistence.document.PaymentDocument;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;

@Repository
public interface SpringDataPaymentRepository extends MongoRepository<PaymentDocument, String> {
    List<PaymentDocument> findByConsentId(String consentId);

    @Query("{'consentId': ?0, 'creationDateTime': {$gte: ?1, $lte: ?2}}")
    List<PaymentDocument> findByConsentIdAndCreationDateTimeBetween(
            String consentId, Instant startDate, Instant endDate);

    Optional<PaymentDocument> findByIdempotencyKey(String idempotencyKey);

    boolean existsByIdempotencyKey(String idempotencyKey);
}
