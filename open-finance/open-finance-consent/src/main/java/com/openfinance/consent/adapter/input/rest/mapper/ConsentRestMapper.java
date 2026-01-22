package com.openfinance.consent.adapter.input.rest.mapper;

import com.openfinance.consent.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.consent.adapter.input.rest.dto.response.ResponsePaymentConsent;
import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.common.domain.enums.*;
import com.openfinance.consent.domain.port.input.CreateConsentUseCase;
import com.openfinance.common.domain.valueobject.*;
import org.springframework.stereotype.Component;

import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

@Component
public class ConsentRestMapper {

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

    private String formatInstant(Instant instant) {
        return instant != null ? instant.toString() : null;
    }
}
