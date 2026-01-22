package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.Consent;

public interface GetConsentUseCase {
    Consent execute(String consentId);
}
