package com.openfinance.payment.adapter.output.external;

import com.openfinance.payment.adapter.output.external.dto.ConsentResponse;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;

@FeignClient(name = "consent-service", url = "${consent.service.url}")
public interface ConsentServiceClient {

    @GetMapping("/consents/{consentId}")
    ConsentResponse getConsent(
            @PathVariable("consentId") String consentId,
            @RequestHeader("Authorization") String authorization,
            @RequestHeader("x-fapi-interaction-id") String interactionId);
}
