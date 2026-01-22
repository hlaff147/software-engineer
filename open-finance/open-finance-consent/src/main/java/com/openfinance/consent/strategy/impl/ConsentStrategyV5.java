package com.openfinance.consent.strategy.impl;

import com.openfinance.consent.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.consent.adapter.input.rest.dto.response.ResponsePaymentConsent;
import com.openfinance.consent.adapter.input.rest.mapper.ConsentRestMapper;
import com.openfinance.consent.domain.port.input.CreateConsentUseCase;
import com.openfinance.consent.domain.port.input.GetConsentUseCase;
import com.openfinance.consent.strategy.ConsentStrategy;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service("Consent_5_0_0")
@RequiredArgsConstructor
public class ConsentStrategyV5 implements ConsentStrategy {

    private final CreateConsentUseCase createConsentUseCase;
    private final GetConsentUseCase getConsentUseCase;
    private final ConsentRestMapper mapper;

    @Override
    public ResponsePaymentConsent createConsent(CreatePaymentConsentRequest request, String idempotencyKey,
            String baseUrl) {
        log.info("[V5] Creating consent");

        var command = mapper.toCommand(request, idempotencyKey);
        var consent = createConsentUseCase.execute(command);

        return mapper.toResponse(consent, baseUrl);
    }

    @Override
    public ResponsePaymentConsent getConsent(String consentId, String baseUrl) {
        log.info("[V5] Getting consent: {}", consentId);

        var consent = getConsentUseCase.execute(consentId);
        return mapper.toResponse(consent, baseUrl);
    }
}
