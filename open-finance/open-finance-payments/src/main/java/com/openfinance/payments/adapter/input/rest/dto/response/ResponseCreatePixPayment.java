package com.openfinance.payments.adapter.input.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResponseCreatePixPayment {
    private List<PaymentData> data;
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
        private ResponsePixPayment.RejectionReason rejectionReason;
        private String localInstrument;
        private String cnpjInitiator;
        private ResponsePixPayment.Payment payment;
        private String transactionIdentification;
        private String remittanceInformation;
        private ResponsePixPayment.CreditorAccount creditorAccount;
        private ResponsePixPayment.DebtorAccount debtorAccount;
        private String authorisationFlow;
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
