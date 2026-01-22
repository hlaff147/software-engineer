package com.openfinance.payment.adapter.input.rest.mapper;

import com.openfinance.payment.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.request.PatchPixPaymentRequest;
import com.openfinance.payment.adapter.input.rest.dto.response.*;
import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.common.domain.enums.*;
import com.openfinance.payment.domain.port.input.CreatePixPaymentUseCase;
import com.openfinance.common.domain.valueobject.*;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;

@Component
public class PaymentRestMapper {

    public CreatePixPaymentUseCase.CreatePixPaymentCommand toCommand(CreatePixPaymentRequest request,
            String idempotencyKey) {
        var payments = request.getData().stream()
                .map(this::mapPaymentItem)
                .toList();

        return new CreatePixPaymentUseCase.CreatePixPaymentCommand(payments, idempotencyKey);
    }

    public Cancellation toCancellation(PatchPixPaymentRequest request) {
        var data = request.getData();
        var cancellation = data.getCancellation();

        Document cancelledBy = null;
        if (cancellation.getCancelledBy() != null && cancellation.getCancelledBy().getDocument() != null) {
            cancelledBy = Document.builder()
                    .identification(cancellation.getCancelledBy().getDocument().getIdentification())
                    .rel(cancellation.getCancelledBy().getDocument().getRel())
                    .build();
        }

        return Cancellation.builder()
                .reason(EnumCancellationReason.valueOf(cancellation.getReason()))
                .cancelledFrom(EnumCancellationFrom.INICIADORA)
                .cancelledAt(Instant.now())
                .cancelledBy(cancelledBy)
                .build();
    }

    public ResponsePixPayment toResponse(PixPayment payment, String baseUrl) {
        return ResponsePixPayment.builder()
                .data(mapPaymentDataResponse(payment))
                .links(ResponsePixPayment.Links.builder()
                        .self(baseUrl + "/pix/payments/" + payment.getPaymentId())
                        .build())
                .meta(ResponsePixPayment.Meta.builder()
                        .requestDateTime(formatInstant(Instant.now()))
                        .build())
                .build();
    }

    public ResponseCreatePixPayment toCreateResponse(List<PixPayment> payments, String baseUrl) {
        var paymentDataList = payments.stream()
                .map(p -> ResponseCreatePixPayment.PaymentData.builder()
                        .paymentId(p.getPaymentId())
                        .endToEndId(p.getEndToEndId())
                        .consentId(p.getConsentId())
                        .creationDateTime(formatInstant(p.getCreationDateTime()))
                        .statusUpdateDateTime(formatInstant(p.getStatusUpdateDateTime()))
                        .proxy(p.getProxy())
                        .status(p.getStatus().name())
                        .localInstrument(p.getLocalInstrument().name())
                        .cnpjInitiator(p.getCnpjInitiator())
                        .payment(ResponsePixPayment.Payment.builder()
                                .amount(p.getAmount().toPlainString())
                                .currency(p.getCurrency())
                                .build())
                        .transactionIdentification(p.getTransactionIdentification())
                        .remittanceInformation(p.getRemittanceInformation())
                        .creditorAccount(mapCreditorAccountResponse(p.getCreditorAccount()))
                        .debtorAccount(
                                p.getDebtorAccount() != null ? mapDebtorAccountPaymentResponse(p.getDebtorAccount())
                                        : null)
                        .authorisationFlow(p.getAuthorisationFlow())
                        .build())
                .toList();

        return ResponseCreatePixPayment.builder()
                .data(paymentDataList)
                .links(ResponseCreatePixPayment.Links.builder()
                        .self(baseUrl + "/pix/payments/" + (payments.isEmpty() ? "" : payments.get(0).getPaymentId()))
                        .build())
                .meta(ResponseCreatePixPayment.Meta.builder()
                        .requestDateTime(formatInstant(Instant.now()))
                        .build())
                .build();
    }

    public ResponsePaymentsList toPaymentsListResponse(List<PixPayment> payments, String baseUrl) {
        var summaries = payments.stream()
                .map(p -> ResponsePaymentsList.PaymentSummary.builder()
                        .paymentId(p.getPaymentId())
                        .endToEndId(p.getEndToEndId())
                        .statusUpdateDateTime(formatInstant(p.getStatusUpdateDateTime()))
                        .status(p.getStatus().name())
                        .build())
                .toList();

        return ResponsePaymentsList.builder()
                .data(summaries)
                .links(ResponsePaymentsList.Links.builder()
                        .self(baseUrl)
                        .build())
                .meta(ResponsePaymentsList.Meta.builder()
                        .requestDateTime(formatInstant(Instant.now()))
                        .build())
                .build();
    }

    private CreatePixPaymentUseCase.PaymentItem mapPaymentItem(CreatePixPaymentRequest.PaymentData dto) {
        return new CreatePixPaymentUseCase.PaymentItem(
                dto.getEndToEndId(),
                EnumLocalInstrument.valueOf(dto.getLocalInstrument()),
                new BigDecimal(dto.getPayment().getAmount()),
                dto.getPayment().getCurrency(),
                CreditorAccount.builder()
                        .ispb(dto.getCreditorAccount().getIspb())
                        .issuer(dto.getCreditorAccount().getIssuer())
                        .number(dto.getCreditorAccount().getNumber())
                        .accountType(EnumAccountPaymentsType.valueOf(dto.getCreditorAccount().getAccountType()))
                        .build(),
                dto.getRemittanceInformation(),
                dto.getQrCode(),
                dto.getProxy(),
                dto.getCnpjInitiator(),
                dto.getTransactionIdentification(),
                dto.getAuthorisationFlow(),
                dto.getConsentId());
    }

    private ResponsePixPayment.PaymentData mapPaymentDataResponse(PixPayment p) {
        return ResponsePixPayment.PaymentData.builder()
                .paymentId(p.getPaymentId())
                .endToEndId(p.getEndToEndId())
                .consentId(p.getConsentId())
                .creationDateTime(formatInstant(p.getCreationDateTime()))
                .statusUpdateDateTime(formatInstant(p.getStatusUpdateDateTime()))
                .proxy(p.getProxy())
                .status(p.getStatus().name())
                .rejectionReason(p.getRejectionReason() != null ? ResponsePixPayment.RejectionReason.builder()
                        .code(p.getRejectionReason().getCode().name())
                        .detail(p.getRejectionReason().getDetail())
                        .build() : null)
                .localInstrument(p.getLocalInstrument().name())
                .cnpjInitiator(p.getCnpjInitiator())
                .payment(ResponsePixPayment.Payment.builder()
                        .amount(p.getAmount().toPlainString())
                        .currency(p.getCurrency())
                        .build())
                .transactionIdentification(p.getTransactionIdentification())
                .remittanceInformation(p.getRemittanceInformation())
                .creditorAccount(mapCreditorAccountResponse(p.getCreditorAccount()))
                .debtorAccount(
                        p.getDebtorAccount() != null ? mapDebtorAccountPaymentResponse(p.getDebtorAccount()) : null)
                .cancellation(p.getCancellation() != null ? ResponsePixPayment.Cancellation.builder()
                        .reason(p.getCancellation().getReason().name())
                        .cancelledFrom(p.getCancellation().getCancelledFrom().name())
                        .cancelledAt(formatInstant(p.getCancellation().getCancelledAt()))
                        .cancelledBy(p.getCancellation().getCancelledBy() != null ? ResponsePixPayment.CancelledBy
                                .builder()
                                .document(ResponsePixPayment.Document.builder()
                                        .identification(p.getCancellation().getCancelledBy().getIdentification())
                                        .rel(p.getCancellation().getCancelledBy().getRel())
                                        .build())
                                .build() : null)
                        .build() : null)
                .authorisationFlow(p.getAuthorisationFlow())
                .build();
    }

    private ResponsePixPayment.CreditorAccount mapCreditorAccountResponse(CreditorAccount ca) {
        return ResponsePixPayment.CreditorAccount.builder()
                .ispb(ca.getIspb())
                .issuer(ca.getIssuer())
                .number(ca.getNumber())
                .accountType(ca.getAccountType().name())
                .build();
    }

    private ResponsePixPayment.DebtorAccount mapDebtorAccountPaymentResponse(DebtorAccount da) {
        return ResponsePixPayment.DebtorAccount.builder()
                .ispb(da.getIspb())
                .issuer(da.getIssuer())
                .number(da.getNumber())
                .accountType(da.getAccountType().name())
                .build();
    }

    private String formatInstant(Instant instant) {
        return instant != null ? instant.toString() : null;
    }
}
