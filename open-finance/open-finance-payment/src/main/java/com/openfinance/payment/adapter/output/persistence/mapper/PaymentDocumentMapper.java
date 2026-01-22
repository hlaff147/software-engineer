package com.openfinance.payment.adapter.output.persistence.mapper;

import com.openfinance.payment.adapter.output.persistence.document.PaymentDocument;
import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.common.domain.valueobject.*;
import org.springframework.stereotype.Component;

@Component
public class PaymentDocumentMapper {

    public PaymentDocument toDocument(PixPayment payment, String idempotencyKey) {
        var builder = PaymentDocument.builder()
                .paymentId(payment.getPaymentId())
                .consentId(payment.getConsentId())
                .idempotencyKey(idempotencyKey)
                .endToEndId(payment.getEndToEndId())
                .creationDateTime(payment.getCreationDateTime())
                .statusUpdateDateTime(payment.getStatusUpdateDateTime())
                .proxy(payment.getProxy())
                .status(payment.getStatus())
                .localInstrument(payment.getLocalInstrument())
                .cnpjInitiator(payment.getCnpjInitiator())
                .amount(payment.getAmount())
                .currency(payment.getCurrency())
                .transactionIdentification(payment.getTransactionIdentification())
                .remittanceInformation(payment.getRemittanceInformation())
                .authorisationFlow(payment.getAuthorisationFlow());

        // Creditor Account
        if (payment.getCreditorAccount() != null) {
            builder.creditorAccountIspb(payment.getCreditorAccount().getIspb())
                    .creditorAccountIssuer(payment.getCreditorAccount().getIssuer())
                    .creditorAccountNumber(payment.getCreditorAccount().getNumber())
                    .creditorAccountType(payment.getCreditorAccount().getAccountType());
        }

        // Debtor Account
        if (payment.getDebtorAccount() != null) {
            builder.debtorAccountIspb(payment.getDebtorAccount().getIspb())
                    .debtorAccountIssuer(payment.getDebtorAccount().getIssuer())
                    .debtorAccountNumber(payment.getDebtorAccount().getNumber())
                    .debtorAccountType(payment.getDebtorAccount().getAccountType());
        }

        // Rejection Reason
        if (payment.getRejectionReason() != null) {
            builder.rejectionReasonCode(payment.getRejectionReason().getCode())
                    .rejectionReasonDetail(payment.getRejectionReason().getDetail());
        }

        // Cancellation
        if (payment.getCancellation() != null) {
            builder.cancellationReason(payment.getCancellation().getReason())
                    .cancellationFrom(payment.getCancellation().getCancelledFrom())
                    .cancellationAt(payment.getCancellation().getCancelledAt());
            if (payment.getCancellation().getCancelledBy() != null) {
                builder.cancellationByIdentification(payment.getCancellation().getCancelledBy().getIdentification())
                        .cancellationByRel(payment.getCancellation().getCancelledBy().getRel());
            }
        }

        return builder.build();
    }

    public PixPayment toDomain(PaymentDocument doc) {
        return PixPayment.builder()
                .paymentId(doc.getPaymentId())
                .consentId(doc.getConsentId())
                .endToEndId(doc.getEndToEndId())
                .creationDateTime(doc.getCreationDateTime())
                .statusUpdateDateTime(doc.getStatusUpdateDateTime())
                .proxy(doc.getProxy())
                .status(doc.getStatus())
                .localInstrument(doc.getLocalInstrument())
                .cnpjInitiator(doc.getCnpjInitiator())
                .amount(doc.getAmount())
                .currency(doc.getCurrency())
                .transactionIdentification(doc.getTransactionIdentification())
                .remittanceInformation(doc.getRemittanceInformation())
                .authorisationFlow(doc.getAuthorisationFlow())
                .creditorAccount(CreditorAccount.builder()
                        .ispb(doc.getCreditorAccountIspb())
                        .issuer(doc.getCreditorAccountIssuer())
                        .number(doc.getCreditorAccountNumber())
                        .accountType(doc.getCreditorAccountType())
                        .build())
                .debtorAccount(doc.getDebtorAccountIspb() != null ? DebtorAccount.builder()
                        .ispb(doc.getDebtorAccountIspb())
                        .issuer(doc.getDebtorAccountIssuer())
                        .number(doc.getDebtorAccountNumber())
                        .accountType(doc.getDebtorAccountType())
                        .build() : null)
                .rejectionReason(doc.getRejectionReasonCode() != null ? PaymentRejectionReason.builder()
                        .code(doc.getRejectionReasonCode())
                        .detail(doc.getRejectionReasonDetail())
                        .build() : null)
                .cancellation(doc.getCancellationReason() != null ? Cancellation.builder()
                        .reason(doc.getCancellationReason())
                        .cancelledFrom(doc.getCancellationFrom())
                        .cancelledAt(doc.getCancellationAt())
                        .cancelledBy(doc.getCancellationByIdentification() != null ? Document.builder()
                                .identification(doc.getCancellationByIdentification())
                                .rel(doc.getCancellationByRel())
                                .build() : null)
                        .build() : null)
                .build();
    }
}
