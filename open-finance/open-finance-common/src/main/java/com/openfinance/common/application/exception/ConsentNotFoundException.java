package com.openfinance.common.application.exception;

public class ConsentNotFoundException extends RuntimeException {

    public ConsentNotFoundException(String consentId) {
        super("Consent not found: " + consentId);
    }
}
