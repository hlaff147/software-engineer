package com.openfinance.payment.strategy.impl;

import com.openfinance.payment.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.request.PatchPixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponseCreatePixPayment;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponsePaymentsList;
import com.openfinance.payment.adapter.input.rest.dto.response.ResponsePixPayment;
import com.openfinance.payment.adapter.input.rest.mapper.PaymentRestMapper;
import com.openfinance.payment.domain.port.input.*;
import com.openfinance.payment.strategy.PaymentStrategy;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;

@Slf4j
@Service("Payment_5_0_0")
@RequiredArgsConstructor
public class PaymentStrategyV5 implements PaymentStrategy {

    private final CreatePixPaymentUseCase createPixPaymentUseCase;
    private final GetPixPaymentUseCase getPixPaymentUseCase;
    private final CancelPixPaymentUseCase cancelPixPaymentUseCase;
    private final GetPaymentsByConsentUseCase getPaymentsByConsentUseCase;
    private final PaymentRestMapper mapper;

    @Override
    public ResponseCreatePixPayment createPayment(CreatePixPaymentRequest request, String idempotencyKey,
            String baseUrl) {
        log.info("[V5] Creating payment");

        var command = mapper.toCommand(request, idempotencyKey);
        var payments = createPixPaymentUseCase.execute(command);

        return mapper.toCreateResponse(payments, baseUrl);
    }

    @Override
    public ResponsePixPayment getPayment(String paymentId, String baseUrl) {
        log.info("[V5] Getting payment: {}", paymentId);

        var payment = getPixPaymentUseCase.execute(paymentId);
        return mapper.toResponse(payment, baseUrl);
    }

    @Override
    public ResponsePixPayment cancelPayment(String paymentId, PatchPixPaymentRequest request, String baseUrl) {
        log.info("[V5] Cancelling payment: {}", paymentId);

        var cancellation = mapper.toCancellation(request);
        var payment = cancelPixPaymentUseCase.execute(paymentId, cancellation);

        return mapper.toResponse(payment, baseUrl);
    }

    @Override
    public ResponsePaymentsList getPaymentsByConsent(String consentId, LocalDate startDate, LocalDate endDate,
            String baseUrl) {
        log.info("[V5] Getting payments for consent: {}", consentId);

        var payments = getPaymentsByConsentUseCase.execute(consentId, startDate, endDate);
        return mapper.toPaymentsListResponse(payments, baseUrl + "/consents/" + consentId + "/pix/payments");
    }
}
