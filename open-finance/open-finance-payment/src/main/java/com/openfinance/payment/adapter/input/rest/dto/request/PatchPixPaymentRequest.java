package com.openfinance.payment.adapter.input.rest.dto.request;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

@Data
public class PatchPixPaymentRequest {

    @NotNull
    @Valid
    private CancellationData data;

    @Data
    public static class CancellationData {
        @NotNull
        private String status;

        private CancellationInfo cancellation;
    }

    @Data
    public static class CancellationInfo {
        @NotNull
        private String reason;

        private CancelledBy cancelledBy;
    }

    @Data
    public static class CancelledBy {
        private DocumentDto document;
    }

    @Data
    public static class DocumentDto {
        private String identification;
        private String rel;
    }
}
