package com.openfinance.payment.domain.port.output;

import com.openfinance.payment.adapter.output.external.dto.ConsentResponse;

public interface ConsentServicePort {
    ConsentResponse getConsent(String consentId);
}
