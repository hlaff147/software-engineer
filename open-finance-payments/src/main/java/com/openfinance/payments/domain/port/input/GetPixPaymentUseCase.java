package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.PixPayment;

public interface GetPixPaymentUseCase {
    PixPayment execute(String paymentId);
}
