package com.openfinance.payments.strategy.consent.impl;

import com.openfinance.payments.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePaymentConsent;
import com.openfinance.payments.adapter.input.rest.mapper.RestMapper;
import com.openfinance.payments.domain.port.input.CreateConsentUseCase;
import com.openfinance.payments.domain.port.input.GetConsentUseCase;
import com.openfinance.payments.strategy.consent.ConsentStrategy;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service("Consent_5_0_0")
@RequiredArgsConstructor
public class ConsentStrategyV5 implements ConsentStrategy {

    private final CreateConsentUseCase createConsentUseCase;
    private final GetConsentUseCase getConsentUseCase;
    private final RestMapper mapper;

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
