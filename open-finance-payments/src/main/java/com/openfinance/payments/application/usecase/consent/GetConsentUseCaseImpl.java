package com.openfinance.payments.application.usecase.consent;

import com.openfinance.payments.domain.entity.Consent;
import com.openfinance.payments.domain.port.input.GetConsentUseCase;
import com.openfinance.payments.domain.port.output.ConsentRepositoryPort;
import com.openfinance.payments.application.exception.ConsentNotFoundException;
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
