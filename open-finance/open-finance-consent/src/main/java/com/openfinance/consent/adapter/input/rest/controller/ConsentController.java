package com.openfinance.consent.adapter.input.rest.controller;

import com.openfinance.consent.adapter.input.rest.dto.request.CreatePaymentConsentRequest;
import com.openfinance.consent.adapter.input.rest.dto.response.ResponsePaymentConsent;
import com.openfinance.consent.strategy.ConsentStrategyFactory;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@Slf4j
@RestController
@RequestMapping("/consents")
@RequiredArgsConstructor
public class ConsentController {

    private static final String VERSION = "5_0_0";

    private final ConsentStrategyFactory strategyFactory;

    @PostMapping(consumes = { MediaType.APPLICATION_JSON_VALUE,
            "application/jwt" }, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponsePaymentConsent> createConsent(
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            @RequestHeader("x-idempotency-key") String idempotencyKey,
            @Valid @RequestBody CreatePaymentConsentRequest request,
            HttpServletRequest httpRequest) {

        log.info("POST /consents - interactionId: {}", interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.createConsent(request, idempotencyKey, baseUrl);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .header("x-fapi-interaction-id", interactionId)
                .body(response);
    }

    @GetMapping(value = "/{consentId}", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<ResponsePaymentConsent> getConsent(
            @PathVariable String consentId,
            @RequestHeader("Authorization") String authorization,
            @RequestHeader(value = "x-fapi-auth-date", required = false) String fapiAuthDate,
            @RequestHeader(value = "x-fapi-customer-ip-address", required = false) String customerIpAddress,
            @RequestHeader("x-fapi-interaction-id") String interactionId,
            @RequestHeader(value = "x-customer-user-agent", required = false) String customerUserAgent,
            HttpServletRequest httpRequest) {

        log.info("GET /consents/{} - interactionId: {}", consentId, interactionId);

        var strategy = strategyFactory.getStrategy(VERSION);
        var baseUrl = getBaseUrl(httpRequest);
        var response = strategy.getConsent(consentId, baseUrl);

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
