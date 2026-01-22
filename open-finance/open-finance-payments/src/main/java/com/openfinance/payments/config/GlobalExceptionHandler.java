package com.openfinance.payments.config;

import com.openfinance.payments.adapter.input.rest.dto.response.ResponseError;
import com.openfinance.payments.application.exception.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.MissingRequestHeaderException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;
import java.util.List;

@Slf4j
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ConsentNotFoundException.class)
    public ResponseEntity<ResponseError> handleConsentNotFound(ConsentNotFoundException ex) {
        log.warn("Consent not found: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.NOT_FOUND, "RECURSO_NAO_ENCONTRADO",
                "Recurso não encontrado", ex.getMessage());
    }

    @ExceptionHandler(PaymentNotFoundException.class)
    public ResponseEntity<ResponseError> handlePaymentNotFound(PaymentNotFoundException ex) {
        log.warn("Payment not found: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.NOT_FOUND, "RECURSO_NAO_ENCONTRADO",
                "Recurso não encontrado", ex.getMessage());
    }

    @ExceptionHandler(ConsentInvalidException.class)
    public ResponseEntity<ResponseError> handleConsentInvalid(ConsentInvalidException ex) {
        log.warn("Consent invalid: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.UNPROCESSABLE_ENTITY, ex.getErrorCode(),
                "Consentimento inválido", ex.getMessage());
    }

    @ExceptionHandler(PaymentCancellationNotAllowedException.class)
    public ResponseEntity<ResponseError> handleCancellationNotAllowed(PaymentCancellationNotAllowedException ex) {
        log.warn("Cancellation not allowed: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.UNPROCESSABLE_ENTITY, "PAGAMENTO_NAO_PERMITE_CANCELAMENTO",
                "Pagamento não permite cancelamento", ex.getMessage());
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ResponseError> handleValidation(MethodArgumentNotValidException ex) {
        log.warn("Validation error: {}", ex.getMessage());

        var errors = ex.getBindingResult().getFieldErrors().stream()
                .map(e -> ResponseError.ErrorItem.builder()
                        .code("PARAMETRO_INVALIDO")
                        .title("Parâmetro inválido")
                        .detail("Campo " + e.getField() + ": " + e.getDefaultMessage())
                        .build())
                .toList();

        return ResponseEntity
                .unprocessableEntity()
                .body(ResponseError.builder()
                        .errors(errors)
                        .meta(ResponseError.Meta.builder()
                                .requestDateTime(Instant.now().toString())
                                .build())
                        .build());
    }

    @ExceptionHandler(MissingRequestHeaderException.class)
    public ResponseEntity<ResponseError> handleMissingHeader(MissingRequestHeaderException ex) {
        log.warn("Missing header: {}", ex.getHeaderName());
        return buildErrorResponse(HttpStatus.BAD_REQUEST, "PARAMETRO_NAO_INFORMADO",
                "Parâmetro não informado", "Header obrigatório não informado: " + ex.getHeaderName());
    }

    @ExceptionHandler(UnsupportedOperationException.class)
    public ResponseEntity<ResponseError> handleUnsupportedOperation(UnsupportedOperationException ex) {
        log.warn("Unsupported operation: {}", ex.getMessage());
        return buildErrorResponse(HttpStatus.BAD_REQUEST, "FORMA_PAGAMENTO_INVALIDA",
                "Operação não suportada", ex.getMessage());
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ResponseError> handleGenericException(Exception ex) {
        log.error("Unexpected error", ex);
        return buildErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR, "ERRO_INTERNO",
                "Erro interno do servidor", "Ocorreu um erro inesperado. Tente novamente mais tarde.");
    }

    private ResponseEntity<ResponseError> buildErrorResponse(HttpStatus status, String code, String title,
            String detail) {
        return ResponseEntity
                .status(status)
                .body(ResponseError.builder()
                        .errors(List.of(ResponseError.ErrorItem.builder()
                                .code(code)
                                .title(title)
                                .detail(detail)
                                .build()))
                        .meta(ResponseError.Meta.builder()
                                .requestDateTime(Instant.now().toString())
                                .build())
                        .build());
    }
}
