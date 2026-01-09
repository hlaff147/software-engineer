package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.valueobject.Document;

public interface CancelPixPaymentUseCase {

    PixPayment execute(CancelPixPaymentCommand command);

    record CancelPixPaymentCommand(
            String paymentId,
            Document cancelledBy) {
    }
}
