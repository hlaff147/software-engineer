package com.openfinance.common.application.exception;

public class PaymentCancellationNotAllowedException extends RuntimeException {

    public PaymentCancellationNotAllowedException(String paymentId, String currentStatus) {
        super("Payment " + paymentId + " cannot be cancelled. Current status: " + currentStatus);
    }
}
