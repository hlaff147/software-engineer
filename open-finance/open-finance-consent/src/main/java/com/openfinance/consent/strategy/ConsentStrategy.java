package com.openfinance.consent.strategy;

import com.openfinance.consent.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.consent.adapter.input.rest.dto.response.ResponsePaymentConsent;

public interface ConsentStrategy {
    ResponsePaymentConsent createConsent(CreatePaymentConsentRequest request, String idempotencyKey, String baseUrl);

    ResponsePaymentConsent getConsent(String consentId, String baseUrl);
}
