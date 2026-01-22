package com.openfinance.payment.adapter.input.rest.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

import java.util.List;

@Data
public class CreatePixPaymentRequest {

    @NotNull
    @Size(min = 1)
    @Valid
    private List<PaymentData> data;

    @Data
    public static class PaymentData {
        @NotNull
        @Pattern(regexp = "^([E])([0-9A-Z]{8})([0-9]{4})(0[1-9]|1[0-2])(0[1-9]|[1-2][0-9]|3[0-1])(2[0-3]|[01][0-9])([0-5][0-9])([a-zA-Z0-9]{11})$")
        private String endToEndId;

        @NotNull
        private String localInstrument;

        @NotNull
        @Valid
        private PaymentAmountDto payment;

        @NotNull
        @Valid
        private CreditorAccountDto creditorAccount;

        @Size(max = 140)
        private String remittanceInformation;

        @Size(max = 512)
        private String qrCode;

        @Size(max = 77)
        private String proxy;

        @NotNull
        @Pattern(regexp = "^[0-9A-Z]{12}[0-9]{2}$")
        private String cnpjInitiator;

        @Pattern(regexp = "^[a-zA-Z0-9]{1,35}$")
        private String transactionIdentification;

        private String authorisationFlow;

        @Pattern(regexp = "^urn:[a-zA-Z0-9][a-zA-Z0-9\\-]{0,31}:[a-zA-Z0-9()+,\\-.:=@;$_!*'%/?#]+$")
        private String consentId;
    }

    @Data
    public static class PaymentAmountDto {
        @NotNull
        @Pattern(regexp = "^((\\d{1,16}\\.\\d{2}))$")
        private String amount;

        @NotNull
        @Pattern(regexp = "^([A-Z]{3})$")
        private String currency;
    }

    @Data
    public static class CreditorAccountDto {
        @NotNull
        @Pattern(regexp = "^[0-9A-Z]{8}$")
        private String ispb;

        @Pattern(regexp = "^[0-9]{1,4}$")
        private String issuer;

        @NotNull
        @Pattern(regexp = "^[0-9]{1,20}$")
        private String number;

        @NotNull
        private String accountType;
    }
}
