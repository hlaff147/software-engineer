package com.example.openbanking.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.LocalDateTime;
import java.util.Map;

/**
 * Handler global de exceções para a API.
 * Converte exceções em respostas HTTP estruturadas.
 */
@RestControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    /**
     * Trata versões de API não suportadas.
     */
    @ExceptionHandler(UnsupportedOperationException.class)
    public ResponseEntity<?> handleUnsupportedVersion(UnsupportedOperationException ex) {
        log.warn("Versão não suportada: {}", ex.getMessage());
        
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(buildErrorResponse("VERSION_NOT_SUPPORTED", ex.getMessage()));
    }

    /**
     * Trata erros de validação de negócio.
     */
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<?> handleIllegalArgument(IllegalArgumentException ex) {
        log.warn("Erro de validação: {}", ex.getMessage());
        
        return ResponseEntity
            .status(HttpStatus.BAD_REQUEST)
            .body(buildErrorResponse("VALIDATION_ERROR", ex.getMessage()));
    }

    /**
     * Trata erros genéricos.
     */
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handleGenericError(Exception ex) {
        log.error("Erro interno: {}", ex.getMessage(), ex);
        
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(buildErrorResponse("INTERNAL_ERROR", "Ocorreu um erro interno. Tente novamente."));
    }

    private Map<String, Object> buildErrorResponse(String code, String message) {
        return Map.of(
            "timestamp", LocalDateTime.now().toString(),
            "code", code,
            "message", message
        );
    }
}
