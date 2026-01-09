package com.openfinance.payments.adapter.input.rest.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import lombok.Data;

@Data
public class PatchPixPaymentRequest {

    @NotNull
    @Valid
    private PatchData data;

    @Data
    public static class PatchData {
        @NotNull
        @Pattern(regexp = "^CANC$")
        private String status;

        @NotNull
        @Valid
        private CancellationDto cancellation;
    }

    @Data
    public static class CancellationDto {
        @NotNull
        @Valid
        private CancelledByDto cancelledBy;
    }

    @Data
    public static class CancelledByDto {
        @NotNull
        @Valid
        private DocumentDto document;
    }

    @Data
    public static class DocumentDto {
        @NotNull
        @Pattern(regexp = "^\\d{11}$")
        private String identification;

        @NotNull
        @Pattern(regexp = "^[A-Z]{3}$")
        private String rel;
    }
}
