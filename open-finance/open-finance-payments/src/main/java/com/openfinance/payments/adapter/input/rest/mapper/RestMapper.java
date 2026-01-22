package com.openfinance.payments.adapter.input.rest.mapper;

import com.openfinance.payments.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.payments.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payments.adapter.input.rest.dto.response.*;
import com.openfinance.payments.domain.entity.Consent;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.enums.*;
import com.openfinance.payments.domain.port.input.CreateConsentUseCase;
import com.openfinance.payments.domain.port.input.CreatePixPaymentUseCase;
import com.openfinance.payments.domain.valueobject.*;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

@Component
public class RestMapper {

    private static final DateTimeFormatter ISO_INSTANT = DateTimeFormatter.ISO_INSTANT;
    private static final DateTimeFormatter ISO_DATE = DateTimeFormatter.ISO_LOCAL_DATE;

    public CreateConsentUseCase.CreateConsentCommand toCommand(CreatePaymentConsentRequest request,
            String idempotencyKey) {
        var data = request.getData();

        return new CreateConsentUseCase.CreateConsentCommand(
                mapLoggedUser(data.getLoggedUser()),
                data.getBusinessEntity() != null ? mapBusinessEntity(data.getBusinessEntity()) : null,
                mapCreditor(data.getCreditor()),
                mapPaymentInfo(data.getPayment()),
                data.getDebtorAccount() != null ? mapDebtorAccount(data.getDebtorAccount()) : null,
                idempotencyKey);
    }

    public CreatePixPaymentUseCase.CreatePixPaymentCommand toCommand(CreatePixPaymentRequest request,
            String idempotencyKey) {
        var payments = request.getData().stream()
                .map(this::mapPaymentItem)
                .toList();

        return new CreatePixPaymentUseCase.CreatePixPaymentCommand(payments, idempotencyKey);
    }

    public ResponsePaymentConsent toResponse(Consent consent, String baseUrl) {
        return ResponsePaymentConsent.builder()
                .data(ResponsePaymentConsent.ConsentData.builder()
                        .consentId(consent.getConsentId())
                        .creationDateTime(formatInstant(consent.getCreationDateTime()))
                        .expirationDateTime(formatInstant(consent.getExpirationDateTime()))
                        .statusUpdateDateTime(formatInstant(consent.getStatusUpdateDateTime()))
                        .status(consent.getStatus().name())
                        .loggedUser(mapLoggedUserResponse(consent.getLoggedUser()))
                        .businessEntity(consent.getBusinessEntity() != null
                                ? mapBusinessEntityResponse(consent.getBusinessEntity())
                                : null)
                        .creditor(mapCreditorResponse(consent.getCreditor()))
                        .payment(mapPaymentResponse(consent.getPayment()))
                        .debtorAccount(consent.getDebtorAccount() != null
                                ? mapDebtorAccountResponse(consent.getDebtorAccount())
                                : null)
                        .rejectionReason(consent.getRejectionReason() != null
                                ? mapRejectionReasonResponse(consent.getRejectionReason())
                                : null)
                        .build())
                .links(ResponsePaymentConsent.Links.builder()
                        .self(baseUrl + "/consents/" + consent.getConsentId())
                        .build())
                .meta(ResponsePaymentConsent.Meta.builder()
                        .requestDateTime(formatInstant(Instant.now()))
                        .build())
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

    // Private mapping methods

    private LoggedUser mapLoggedUser(CreatePaymentConsentRequest.LoggedUserDto dto) {
        return LoggedUser.builder()
                .document(Document.builder()
                        .identification(dto.getDocument().getIdentification())
                        .rel(dto.getDocument().getRel())
                        .build())
                .build();
    }

    private BusinessEntity mapBusinessEntity(CreatePaymentConsentRequest.BusinessEntityDto dto) {
        if (dto.getDocument() == null)
            return null;
        return BusinessEntity.builder()
                .document(Document.builder()
                        .identification(dto.getDocument().getIdentification())
                        .rel(dto.getDocument().getRel())
                        .build())
                .build();
    }

    private Creditor mapCreditor(CreatePaymentConsentRequest.CreditorDto dto) {
        return Creditor.builder()
                .personType(EnumPaymentPersonType.valueOf(dto.getPersonType()))
                .cpfCnpj(dto.getCpfCnpj())
                .name(dto.getName())
                .build();
    }

    private PaymentInfo mapPaymentInfo(CreatePaymentConsentRequest.PaymentDto dto) {
        return PaymentInfo.builder()
                .type(EnumPaymentType.valueOf(dto.getType()))
                .purpose(dto.getPurpose() != null ? EnumPaymentPurpose.valueOf(dto.getPurpose()) : null)
                .date(dto.getDate() != null ? LocalDate.parse(dto.getDate()) : null)
                .currency(dto.getCurrency())
                .amount(new BigDecimal(dto.getAmount()))
                .ibgeTownCode(dto.getIbgeTownCode())
                .details(mapPaymentDetails(dto.getDetails()))
                .build();
    }

    private PaymentDetails mapPaymentDetails(CreatePaymentConsentRequest.DetailsDto dto) {
        return PaymentDetails.builder()
                .localInstrument(EnumLocalInstrument.valueOf(dto.getLocalInstrument()))
                .qrCode(dto.getQrCode())
                .proxy(dto.getProxy())
                .creditorAccount(mapCreditorAccount(dto.getCreditorAccount()))
                .build();
    }

    private CreditorAccount mapCreditorAccount(CreatePaymentConsentRequest.CreditorAccountDto dto) {
        return CreditorAccount.builder()
                .ispb(dto.getIspb())
                .issuer(dto.getIssuer())
                .number(dto.getNumber())
                .accountType(EnumAccountPaymentsType.valueOf(dto.getAccountType()))
                .build();
    }

    private DebtorAccount mapDebtorAccount(CreatePaymentConsentRequest.DebtorAccountDto dto) {
        return DebtorAccount.builder()
                .ispb(dto.getIspb())
                .issuer(dto.getIssuer())
                .number(dto.getNumber())
                .accountType(EnumAccountPaymentsType.valueOf(dto.getAccountType()))
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

    // Response mapping methods

    private ResponsePaymentConsent.LoggedUser mapLoggedUserResponse(LoggedUser lu) {
        return ResponsePaymentConsent.LoggedUser.builder()
                .document(ResponsePaymentConsent.Document.builder()
                        .identification(lu.getDocument().getIdentification())
                        .rel(lu.getDocument().getRel())
                        .build())
                .build();
    }

    private ResponsePaymentConsent.BusinessEntity mapBusinessEntityResponse(BusinessEntity be) {
        return ResponsePaymentConsent.BusinessEntity.builder()
                .document(ResponsePaymentConsent.Document.builder()
                        .identification(be.getDocument().getIdentification())
                        .rel(be.getDocument().getRel())
                        .build())
                .build();
    }

    private ResponsePaymentConsent.Creditor mapCreditorResponse(Creditor c) {
        return ResponsePaymentConsent.Creditor.builder()
                .personType(c.getPersonType().name())
                .cpfCnpj(c.getCpfCnpj())
                .name(c.getName())
                .build();
    }

    private ResponsePaymentConsent.Payment mapPaymentResponse(PaymentInfo p) {
        return ResponsePaymentConsent.Payment.builder()
                .type(p.getType().name())
                .purpose(p.getPurpose() != null ? p.getPurpose().name() : null)
                .date(p.getDate() != null ? p.getDate().format(ISO_DATE) : null)
                .currency(p.getCurrency())
                .amount(p.getAmount().toPlainString())
                .ibgeTownCode(p.getIbgeTownCode())
                .details(ResponsePaymentConsent.Details.builder()
                        .localInstrument(p.getDetails().getLocalInstrument().name())
                        .qrCode(p.getDetails().getQrCode())
                        .proxy(p.getDetails().getProxy())
                        .creditorAccount(ResponsePaymentConsent.CreditorAccount.builder()
                                .ispb(p.getDetails().getCreditorAccount().getIspb())
                                .issuer(p.getDetails().getCreditorAccount().getIssuer())
                                .number(p.getDetails().getCreditorAccount().getNumber())
                                .accountType(p.getDetails().getCreditorAccount().getAccountType().name())
                                .build())
                        .build())
                .build();
    }

    private ResponsePaymentConsent.DebtorAccount mapDebtorAccountResponse(DebtorAccount da) {
        return ResponsePaymentConsent.DebtorAccount.builder()
                .ispb(da.getIspb())
                .issuer(da.getIssuer())
                .number(da.getNumber())
                .accountType(da.getAccountType().name())
                .build();
    }

    private ResponsePaymentConsent.RejectionReason mapRejectionReasonResponse(ConsentRejectionReason rr) {
        return ResponsePaymentConsent.RejectionReason.builder()
                .code(rr.getCode().name())
                .detail(rr.getDetail())
                .build();
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
