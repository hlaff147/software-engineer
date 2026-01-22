package com.openfinance.payment.domain.port.input;

import com.openfinance.payment.domain.entity.PixPayment;

public interface GetPixPaymentUseCase {
    PixPayment execute(String paymentId);
}
