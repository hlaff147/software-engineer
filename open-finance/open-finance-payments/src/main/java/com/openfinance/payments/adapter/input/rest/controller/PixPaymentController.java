package com.openfinance.payments.adapter.input.rest.controller;

import com.openfinance.payments.adapter.input.rest.dto.request.CreatePixPaymentRequest;
import com.openfinance.payments.adapter.input.rest.dto.request.PatchPixPaymentRequest;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponseCreatePixPayment;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePaymentsList;
import com.openfinance.payments.adapter.input.rest.dto.response.ResponsePixPayment;
import com.openfinance.payments.strategy.payment.PaymentStrategyFactory;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;

@Slf4j
@RestController
@RequiredArgsConstructor
public class PixPaymentController {

    private static final String VERSION = "5_0_0";

    private final PaymentStrategyFactory strategyFactory;

    @PostMapping(value = "/pix/payments", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/jwt" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponseCreatePixPayment> createPayment(
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            @RequestHeader("x-idempotency-key") String idempotencyKey,
            @Valid @RequestBody CreatePixPaymentRequest request,
            HttpServletRequest httpRequest) {

        log.info("POST /pix/payments - interactionId: {}", interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.createPayment(request, idempotencyKey, baseUrl);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .header("x-fapi-interaction-id", interactionId)
                .body(response);
    }

    @GetMapping(value = "/pix/payments/{paymentId}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponsePixPayment> getPayment(
            @PathVariable String paymentId,
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            HttpServletRequest httpRequest) {

        log.info("GET /pix/payments/{} - interactionId: {}", paymentId, interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.getPayment(paymentId, baseUrl);

        return ResponseEntity
                .ok()
                .header("x-fapi-interaction-id", interactionId)
                .body(response);
    }

    @PatchMapping(value = "/pix/payments/{paymentId}", consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/jwt" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponsePixPayment> cancelPayment(
            @PathVariable String paymentId,
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            @RequestHeader("x-idempotency-key") String idempotencyKey,
            @Valid @RequestBody PatchPixPaymentRequest request,
            HttpServletRequest httpRequest) {

        log.info("PATCH /pix/payments/{} - interactionId: {}", paymentId, interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.cancelPayment(paymentId, request, baseUrl);

        return ResponseEntity
                .ok()
                .header("x-fapi-interaction-id", interactionId)
                .body(response);
    }

    @GetMapping(value = "/consents/{consentId}/pix/payments", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponsePaymentsList> getPaymentsByConsent(
            @PathVariable String consentId,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate startDate,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE) LocalDate endDate,
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            HttpServletRequest httpRequest) {

        log.info("GET /consents/{}/pix/payments - interactionId: {}", consentId, interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.getPaymentsByConsent(consentId, startDate, endDate, baseUrl);

        return ResponseEntity
                .ok()
                .header("x-fapi-interaction-id", interactionId)
                .body(response);
    }

    private String getBaseUrl(HttpServletRequest request) {
        return request.getScheme() + "://" + request.getServerName() +
                (request.getServerPort() != 80 && request.getServerPort() != 443 ? ":" + request.getServerPort() : "") +
                request.getContextPath();
    }
}
