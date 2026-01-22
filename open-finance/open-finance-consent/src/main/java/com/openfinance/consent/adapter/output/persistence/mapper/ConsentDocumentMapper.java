package com.openfinance.consent.adapter.output.persistence.mapper;

import com.openfinance.consent.adapter.output.persistence.document.ConsentDocument;
import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.common.domain.valueobject.*;
import org.springframework.stereotype.Component;

@Component
public class ConsentDocumentMapper {

    public ConsentDocument toDocument(Consent consent, String idempotencyKey) {
        var builder = ConsentDocument.builder()
                .consentId(consent.getConsentId())
                .idempotencyKey(idempotencyKey)
                .creationDateTime(consent.getCreationDateTime())
                .expirationDateTime(consent.getExpirationDateTime())
                .statusUpdateDateTime(consent.getStatusUpdateDateTime())
                .status(consent.getStatus())
                .paymentType(consent.getPayment().getType())
                .paymentPurpose(consent.getPayment().getPurpose())
                .paymentDate(consent.getPayment().getDate())
                .currency(consent.getPayment().getCurrency())
                .amount(consent.getPayment().getAmount())
                .ibgeTownCode(consent.getPayment().getIbgeTownCode());

        // LoggedUser
        if (consent.getLoggedUser() != null && consent.getLoggedUser().getDocument() != null) {
            builder.loggedUserIdentification(consent.getLoggedUser().getDocument().getIdentification())
                    .loggedUserRel(consent.getLoggedUser().getDocument().getRel());
        }

        // BusinessEntity
        if (consent.getBusinessEntity() != null && consent.getBusinessEntity().getDocument() != null) {
            builder.businessEntityIdentification(consent.getBusinessEntity().getDocument().getIdentification())
                    .businessEntityRel(consent.getBusinessEntity().getDocument().getRel());
        }

        // Creditor
        if (consent.getCreditor() != null) {
            builder.creditorPersonType(consent.getCreditor().getPersonType())
                    .creditorCpfCnpj(consent.getCreditor().getCpfCnpj())
                    .creditorName(consent.getCreditor().getName());
        }

        // Payment Details
        if (consent.getPayment().getDetails() != null) {
            var details = consent.getPayment().getDetails();
            builder.localInstrument(details.getLocalInstrument())
                    .qrCode(details.getQrCode())
                    .proxy(details.getProxy());

            if (details.getCreditorAccount() != null) {
                builder.creditorAccountIspb(details.getCreditorAccount().getIspb())
                        .creditorAccountIssuer(details.getCreditorAccount().getIssuer())
                        .creditorAccountNumber(details.getCreditorAccount().getNumber())
                        .creditorAccountType(details.getCreditorAccount().getAccountType());
            }
        }

        // Debtor Account
        if (consent.getDebtorAccount() != null) {
            builder.debtorAccountIspb(consent.getDebtorAccount().getIspb())
                    .debtorAccountIssuer(consent.getDebtorAccount().getIssuer())
                    .debtorAccountNumber(consent.getDebtorAccount().getNumber())
                    .debtorAccountType(consent.getDebtorAccount().getAccountType());
        }

        // Rejection Reason
        if (consent.getRejectionReason() != null) {
            builder.rejectionReasonCode(consent.getRejectionReason().getCode())
                    .rejectionReasonDetail(consent.getRejectionReason().getDetail());
        }

        return builder.build();
    }

    public Consent toDomain(ConsentDocument doc) {
        return Consent.builder()
                .consentId(doc.getConsentId())
                .creationDateTime(doc.getCreationDateTime())
                .expirationDateTime(doc.getExpirationDateTime())
                .statusUpdateDateTime(doc.getStatusUpdateDateTime())
                .status(doc.getStatus())
                .loggedUser(LoggedUser.builder()
                        .document(Document.builder()
                                .identification(doc.getLoggedUserIdentification())
                                .rel(doc.getLoggedUserRel())
                                .build())
                        .build())
                .businessEntity(doc.getBusinessEntityIdentification() != null ? BusinessEntity.builder()
                        .document(Document.builder()
                                .identification(doc.getBusinessEntityIdentification())
                                .rel(doc.getBusinessEntityRel())
                                .build())
                        .build() : null)
                .creditor(Creditor.builder()
                        .personType(doc.getCreditorPersonType())
                        .cpfCnpj(doc.getCreditorCpfCnpj())
                        .name(doc.getCreditorName())
                        .build())
                .payment(PaymentInfo.builder()
                        .type(doc.getPaymentType())
                        .purpose(doc.getPaymentPurpose())
                        .date(doc.getPaymentDate())
                        .currency(doc.getCurrency())
                        .amount(doc.getAmount())
                        .ibgeTownCode(doc.getIbgeTownCode())
                        .details(PaymentDetails.builder()
                                .localInstrument(doc.getLocalInstrument())
                                .qrCode(doc.getQrCode())
                                .proxy(doc.getProxy())
                                .creditorAccount(CreditorAccount.builder()
                                        .ispb(doc.getCreditorAccountIspb())
                                        .issuer(doc.getCreditorAccountIssuer())
                                        .number(doc.getCreditorAccountNumber())
                                        .accountType(doc.getCreditorAccountType())
                                        .build())
                                .build())
                        .build())
                .debtorAccount(doc.getDebtorAccountIspb() != null ? DebtorAccount.builder()
                        .ispb(doc.getDebtorAccountIspb())
                        .issuer(doc.getDebtorAccountIssuer())
                        .number(doc.getDebtorAccountNumber())
                        .accountType(doc.getDebtorAccountType())
                        .build() : null)
                .rejectionReason(doc.getRejectionReasonCode() != null ? ConsentRejectionReason.builder()
                        .code(doc.getRejectionReasonCode())
                        .detail(doc.getRejectionReasonDetail())
                        .build() : null)
                .build();
    }
}
