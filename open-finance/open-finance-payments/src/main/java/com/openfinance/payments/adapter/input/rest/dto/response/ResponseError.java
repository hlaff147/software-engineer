package com.openfinance.payments.adapter.input.rest.dto.response;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Builder;
import lombok.Data;

import java.util.List;

@Data
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ResponseError {
    private List<ErrorItem> errors;
    private Meta meta;

    @Data
    @Builder
    public static class ErrorItem {
        private String code;
        private String title;
        private String detail;
    }

    @Data
    @Builder
    public static class Meta {
        private String requestDateTime;
    }
}
