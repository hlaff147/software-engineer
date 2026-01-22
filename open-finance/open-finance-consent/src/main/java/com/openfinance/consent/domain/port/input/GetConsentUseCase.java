package com.openfinance.consent.domain.port.input;

import com.openfinance.consent.domain.entity.Consent;

public interface GetConsentUseCase {
    Consent execute(String consentId);
}
