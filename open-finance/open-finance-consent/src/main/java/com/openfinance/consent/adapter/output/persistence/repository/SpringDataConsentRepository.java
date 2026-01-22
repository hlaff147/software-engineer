package com.openfinance.consent.adapter.output.persistence.repository;

import com.openfinance.consent.adapter.output.persistence.document.ConsentDocument;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface SpringDataConsentRepository extends MongoRepository<ConsentDocument, String> {
    Optional<ConsentDocument> findByIdempotencyKey(String idempotencyKey);

    boolean existsByIdempotencyKey(String idempotencyKey);
}
