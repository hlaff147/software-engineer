package com.openfinance.payment.domain.port.output;

import com.openfinance.payment.domain.entity.PixPayment;

public interface SpiServicePort {
    SpiResult sendPayment(PixPayment payment);

    record SpiResult(boolean success, String message) {
        public boolean isSuccess() {
            return success;
        }
    }
}
