package com.openfinance.payments.adapter.input.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResponsePaymentConsent {
    private ConsentData data;
    private Links links;
    private Meta meta;

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class ConsentData {
        private String consentId;
        private String creationDateTime;
        private String expirationDateTime;
        private String statusUpdateDateTime;
        private String status;
        private LoggedUser loggedUser;
        private BusinessEntity businessEntity;
        private Creditor creditor;
        private Payment payment;
        private DebtorAccount debtorAccount;
        private RejectionReason rejectionReason;
    }

    @Data
    @Builder
    public static class LoggedUser {
        private Document document;
    }

    @Data
    @Builder
    public static class BusinessEntity {
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
    public static class Creditor {
        private String personType;
        private String cpfCnpj;
        private String name;
    }

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class Payment {
        private String type;
        private String purpose;
        private String date;
        private String currency;
        private String amount;
        private String ibgeTownCode;
        private Details details;
    }

    @Data
    @Builder
    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class Details {
        private String localInstrument;
        private String qrCode;
        private String proxy;
        private CreditorAccount creditorAccount;
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
    public static class Links {
        private String self;
    }

    @Data
    @Builder
    public static class Meta {
        private String requestDateTime;
    }
}
