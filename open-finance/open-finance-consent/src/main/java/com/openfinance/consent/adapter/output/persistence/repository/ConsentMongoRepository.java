package com.openfinance.consent.adapter.output.persistence.repository;

import com.openfinance.consent.adapter.output.persistence.mapper.ConsentDocumentMapper;
import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.consent.domain.port.output.ConsentRepositoryPort;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
@RequiredArgsConstructor
public class ConsentMongoRepository implements ConsentRepositoryPort {

    private final SpringDataConsentRepository springDataRepository;
    private final ConsentDocumentMapper mapper;

    private String currentIdempotencyKey;

    public void setIdempotencyKey(String idempotencyKey) {
        this.currentIdempotencyKey = idempotencyKey;
    }

    @Override
    public Consent save(Consent consent) {
        var document = mapper.toDocument(consent, currentIdempotencyKey);
        var saved = springDataRepository.save(document);
        return mapper.toDomain(saved);
    }

    @Override
    public Optional<Consent> findById(String consentId) {
        return springDataRepository.findById(consentId)
                .map(mapper::toDomain);
    }

    @Override
    public boolean existsByIdempotencyKey(String idempotencyKey) {
        return springDataRepository.existsByIdempotencyKey(idempotencyKey);
    }

    @Override
    public Optional<Consent> findByIdempotencyKey(String idempotencyKey) {
        return springDataRepository.findByIdempotencyKey(idempotencyKey)
                .map(mapper::toDomain);
    }
}
