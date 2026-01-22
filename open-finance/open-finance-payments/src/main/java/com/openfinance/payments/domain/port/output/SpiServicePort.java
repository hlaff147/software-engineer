package com.openfinance.payments.domain.port.output;

import com.openfinance.payments.domain.entity.PixPayment;
import lombok.Builder;
import lombok.Value;

public interface SpiServicePort {

    SpiResult sendPayment(PixPayment payment);

    @Value
    @Builder
    class SpiResult {
        boolean success;
        String endToEndId;
        String errorCode;
        String errorMessage;
    }
}
