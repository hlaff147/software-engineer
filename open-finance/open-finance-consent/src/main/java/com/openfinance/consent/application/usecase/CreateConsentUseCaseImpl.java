package com.openfinance.consent.application.usecase;

import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.common.domain.enums.EnumAuthorisationStatusType;
import com.openfinance.consent.domain.port.input.CreateConsentUseCase;
import com.openfinance.consent.domain.port.output.ConsentRepositoryPort;
import com.openfinance.consent.adapter.output.persistence.repository.ConsentMongoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class CreateConsentUseCaseImpl implements CreateConsentUseCase {

    private final ConsentRepositoryPort consentRepository;

    @Value("${app.consent.expiration-minutes:5}")
    private int expirationMinutes;

    @Override
    public Consent execute(CreateConsentCommand command) {
        log.info("Creating consent for user: {}", command.loggedUser().getDocument().getIdentification());

        // Check idempotency
        if (consentRepository.existsByIdempotencyKey(command.idempotencyKey())) {
            log.info("Consent already exists for idempotency key: {}", command.idempotencyKey());
            return consentRepository.findByIdempotencyKey(command.idempotencyKey()).orElseThrow();
        }

        // Set idempotency key for repository
        if (consentRepository instanceof ConsentMongoRepository mongoRepo) {
            mongoRepo.setIdempotencyKey(command.idempotencyKey());
        }

        var now = Instant.now();
        var consent = Consent.builder()
                .consentId(generateConsentId())
                .creationDateTime(now)
                .expirationDateTime(now.plusSeconds((long) expirationMinutes * 60))
                .statusUpdateDateTime(now)
                .status(EnumAuthorisationStatusType.AWAITING_AUTHORISATION)
                .loggedUser(command.loggedUser())
                .businessEntity(command.businessEntity())
                .creditor(command.creditor())
                .payment(command.payment())
                .debtorAccount(command.debtorAccount())
                .build();

        var saved = consentRepository.save(consent);
        log.info("Consent created: {}", saved.getConsentId());

        return saved;
    }

    private String generateConsentId() {
        return "urn:openfinance:" + UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
    }
}
