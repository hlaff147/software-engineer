package com.openfinance.payments.adapter.input.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResponsePaymentsList {
    private List<PaymentSummary> data;
    private Links links;
    private Meta meta;

    @Data
    @Builder
    public static class PaymentSummary {
        private String paymentId;
        private String endToEndId;
        private String statusUpdateDateTime;
        private String status;
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
