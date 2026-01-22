package com.openfinance.consent.application.usecase;

import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.consent.domain.port.input.GetConsentUseCase;
import com.openfinance.consent.domain.port.output.ConsentRepositoryPort;
import com.openfinance.common.application.exception.ConsentNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class GetConsentUseCaseImpl implements GetConsentUseCase {

    private final ConsentRepositoryPort consentRepository;

    @Override
    public Consent execute(String consentId) {
        log.info("Getting consent: {}", consentId);

        return consentRepository.findById(consentId)
                .orElseThrow(() -> new ConsentNotFoundException(consentId));
    }
}
