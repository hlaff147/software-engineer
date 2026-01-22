package com.openfinance.consent.adapter.input.rest.dto.request;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.Data;

import java.math.BigDecimal;

@Data
public class CreatePaymentConsentRequest {

    @NotNull
    @Valid
    private ConsentData data;

    @Data
    public static class ConsentData {
        @NotNull
        @Valid
        private LoggedUserDto loggedUser;

        @Valid
        private BusinessEntityDto businessEntity;

        @NotNull
        @Valid
        private CreditorDto creditor;

        @NotNull
        @Valid
        private PaymentDto payment;

        @Valid
        private DebtorAccountDto debtorAccount;
    }

    @Data
    public static class LoggedUserDto {
        @NotNull
        @Valid
        private DocumentDto document;
    }

    @Data
    public static class BusinessEntityDto {
        @Valid
        private DocumentDto document;
    }

    @Data
    public static class DocumentDto {
        @NotNull
        @Pattern(regexp = "^\\d{11}$|^[0-9A-Z]{12}[0-9]{2}$")
        private String identification;

        @NotNull
        @Pattern(regexp = "^[A-Z]{3,4}$")
        private String rel;
    }

    @Data
    public static class CreditorDto {
        @NotNull
        private String personType;

        @NotNull
        @Pattern(regexp = "^([0-9]{11})$|^([0-9A-Z]{12}[0-9]{2})$")
        private String cpfCnpj;

        @NotNull
        @Size(max = 150)
        private String name;
    }

    @Data
    public static class PaymentDto {
        @NotNull
        private String type;

        private String purpose;

        @Pattern(regexp = "^(\\d{4})-(1[0-2]|0?[1-9])-(3[01]|[12][0-9]|0?[1-9])$")
        private String date;

        @NotNull
        @Pattern(regexp = "^([A-Z]{3})$")
        private String currency;

        @NotNull
        @Pattern(regexp = "^((\\d{1,16}\\.\\d{2}))$")
        private String amount;

        @Pattern(regexp = "^\\d{7}$")
        private String ibgeTownCode;

        @NotNull
        @Valid
        private DetailsDto details;
    }

    @Data
    public static class DetailsDto {
        @NotNull
        private String localInstrument;

        @Size(max = 512)
        private String qrCode;

        @Size(max = 77)
        private String proxy;

        @NotNull
        @Valid
        private CreditorAccountDto creditorAccount;
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

    @Data
    public static class DebtorAccountDto {
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
