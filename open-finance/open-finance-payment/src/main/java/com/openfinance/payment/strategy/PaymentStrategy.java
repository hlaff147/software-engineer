package com.openfinance.payment.strategy;

import com.openfinance.payment.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.request.PatchPixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponseCreatePixPayment;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponsePaymentsList;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponsePixPayment;

import java.time.LocalDate;

public interface PaymentStrategy {
    ResponseCreatePixPayment createPayment(CreatePixPaymentRequest request, String idempotencyKey, String baseUrl);

    ResponsePixPayment getPayment(String paymentId, String baseUrl);

    ResponsePixPayment cancelPayment(String paymentId, PatchPixPaymentRequest request, String baseUrl);

    ResponsePaymentsList getPaymentsByConsent(String consentId, LocalDate startDate, LocalDate endDate, String baseUrl);
}
