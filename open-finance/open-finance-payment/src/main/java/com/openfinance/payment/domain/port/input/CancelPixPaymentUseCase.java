package com.openfinance.payment.domain.port.input;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.common.domain.valueobject.Cancellation;

public interface CancelPixPaymentUseCase {
    PixPayment execute(String paymentId, Cancellation cancellation);
}
