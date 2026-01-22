package com.openfinance.payment.adapter.output.external.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ConsentResponse {
    private ConsentData data;

    @Data
    public static class ConsentData {
        private String consentId;
        private String creationDateTime;
        private String expirationDateTime;
        private String statusUpdateDateTime;
        private String status;
        private LoggedUser loggedUser;
        private Creditor creditor;
        private Payment payment;
        private DebtorAccount debtorAccount;
    }

    @Data
    public static class LoggedUser {
        private Document document;
    }

    @Data
    public static class Document {
        private String identification;
        private String rel;
    }

    @Data
    public static class Creditor {
        private String personType;
        private String cpfCnpj;
        private String name;
    }

    @Data
    public static class Payment {
        private String type;
        private String currency;
        private String amount;
        private Details details;
    }

    @Data
    public static class Details {
        private String localInstrument;
        private String proxy;
        private CreditorAccount creditorAccount;
    }

    @Data
    public static class CreditorAccount {
        private String ispb;
        private String issuer;
        private String number;
        private String accountType;
    }

    @Data
    public static class DebtorAccount {
        private String ispb;
        private String issuer;
        private String number;
        private String accountType;
    }
}
