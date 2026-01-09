package com.openfinance.payments.adapter.input.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResponsePixPayment {
    private PaymentData data;
    private Links links;
    private Meta meta;

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class PaymentData {
        private String paymentId;
        private String endToEndId;
        private String consentId;
        private String creationDateTime;
        private String statusUpdateDateTime;
        private String proxy;
        private String status;
        private RejectionReason rejectionReason;
        private String localInstrument;
        private String cnpjInitiator;
        private Payment payment;
        private String transactionIdentification;
        private String remittanceInformation;
        private CreditorAccount creditorAccount;
        private DebtorAccount debtorAccount;
        private Cancellation cancellation;
        private String authorisationFlow;
    }

    @Data
    @Builder
    public static class Payment {
        private String amount;
        private String currency;
    }

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class CreditorAccount {
        private String ispb;
        private String issuer;
        private String number;
        private String accountType;
    }

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class DebtorAccount {
        private String ispb;
        private String issuer;
        private String number;
        private String accountType;
    }

    @Data
    @Builder
    public static class RejectionReason {
        private String code;
        private String detail;
    }

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class Cancellation {
        private String reason;
        private String cancelledFrom;
        private String cancelledAt;
        private CancelledBy cancelledBy;
    }

    @Data
    @Builder
    public static class CancelledBy {
        private Document document;
    }

    @Data
    @Builder
    public static class Document {
        private String identification;
        private String rel;
    }

    @Data
    @Builder
    public static class Links {
        private String self;
    }

    @Data
    @Builder
    public static class Meta {
        private String requestDateTime;
    }
}
