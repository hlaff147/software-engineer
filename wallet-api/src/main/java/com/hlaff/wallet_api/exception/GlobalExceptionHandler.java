package com.hlaff.wallet_api.exception;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.Map;

@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ProblemDetail> notFound(NotFoundException ex, HttpServletRequest req) {
        var pd = ProblemDetail.forStatus(HttpStatus.NOT_FOUND);
        pd.setTitle("Not Found");
        pd.setDetail(ex.getMessage());
        pd.setInstance(java.net.URI.create(req.getRequestURI()));
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(pd);
    }
    
    @ExceptionHandler(InsufficientFundsException.class)
    public ResponseEntity<ProblemDetail> insufficient(InsufficientFundsException ex, HttpServletRequest req) {
        var pd = ProblemDetail.forStatus(HttpStatus.CONFLICT);
        pd.setTitle("Insufficient funds");
        pd.setDetail(ex.getMessage());
        pd.setInstance(java.net.URI.create(req.getRequestURI()));
        return ResponseEntity.status(HttpStatus.CONFLICT).body(pd);
    }
    
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ProblemDetail> businessError(BusinessException ex, HttpServletRequest req) {
        var pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Business Error");
        pd.setDetail(ex.getMessage());
        pd.setInstance(java.net.URI.create(req.getRequestURI()));
        return ResponseEntity.badRequest().body(pd);
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ProblemDetail> badRequest(MethodArgumentNotValidException ex, HttpServletRequest req) {
        var pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Validation error");
        pd.setDetail("Invalid request content.");
        pd.setInstance(java.net.URI.create(req.getRequestURI()));
        pd.setProperty("errors", ex.getFieldErrors().stream()
                .map(e -> Map.of("field", e.getField(), "message", e.getDefaultMessage()))
                .toList());
        return ResponseEntity.badRequest().body(pd);
    }
}
