package com.openfinance.payments.domain.port.output;

import lombok.Builder;
import lombok.Value;

public interface DictServicePort {

    DictValidationResult validatePixKey(String pixKey);

    @Value
    @Builder
    class DictValidationResult {
        boolean valid;
        String accountHolderName;
        String ispb;
        String accountNumber;
        String accountType;
    }
}
