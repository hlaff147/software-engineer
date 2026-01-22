package com.openfinance.payments.strategy.payment.impl;

import com.openfinance.payments.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payments.adapter.input.rest.dto.request.PatchPixPaymentRequest;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponseCreatePixPayment;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePaymentsList;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePixPayment;
import com.openfinance.payments.adapter.input.rest.mapper.RestMapper;
import com.openfinance.payments.domain.port.input.CancelPixPaymentUseCase;
import com.openfinance.payments.domain.port.input.CreatePixPaymentUseCase;
import com.openfinance.payments.domain.port.input.GetPaymentsByConsentUseCase;
import com.openfinance.payments.domain.port.input.GetPixPaymentUseCase;
import com.openfinance.payments.domain.valueobject.Document;
import com.openfinance.payments.strategy.payment.PaymentStrategy;
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
    private final RestMapper mapper;

    @Override
    public ResponseCreatePixPayment createPayment(CreatePixPaymentRequest request, String idempotencyKey,
            String baseUrl) {
        log.info("[V5] Creating payment(s)");

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

        var cancelledBy = Document.builder()
                .identification(request.getData().getCancellation().getCancelledBy().getDocument().getIdentification())
                .rel(request.getData().getCancellation().getCancelledBy().getDocument().getRel())
                .build();

        var command = new CancelPixPaymentUseCase.CancelPixPaymentCommand(paymentId, cancelledBy);
        var payment = cancelPixPaymentUseCase.execute(command);

        return mapper.toResponse(payment, baseUrl);
    }

    @Override
    public ResponsePaymentsList getPaymentsByConsent(String consentId, LocalDate startDate, LocalDate endDate,
            String baseUrl) {
        log.info("[V5] Getting payments for consent: {}", consentId);

        var command = new GetPaymentsByConsentUseCase.GetPaymentsByConsentCommand(consentId, startDate, endDate);
        var payments = getPaymentsByConsentUseCase.execute(command);

        return mapper.toPaymentsListResponse(payments, baseUrl);
    }
}
