package com.openfinance.payments.strategy.consent;

import com.openfinance.payments.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePaymentConsent;

public interface ConsentStrategy {
    ResponsePaymentConsent createConsent(CreatePaymentConsentRequest request, String idempotencyKey, String baseUrl);

    ResponsePaymentConsent getConsent(String consentId, String baseUrl);
}
