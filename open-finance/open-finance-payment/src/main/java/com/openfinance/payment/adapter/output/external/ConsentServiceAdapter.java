package com.openfinance.payment.adapter.output.external;

import com.openfinance.payment.adapter.output.external.dto.ConsentResponse;
import com.openfinance.payment.domain.port.output.ConsentServicePort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.UUID;

@Slf4j
@Component
@RequiredArgsConstructor
public class ConsentServiceAdapter implements ConsentServicePort {

    private final ConsentServiceClient consentClient;

    @Override
    public ConsentResponse getConsent(String consentId) {
        log.info("Fetching consent {} from consent service", consentId);

        // Using mock authorization and interaction ID for inter-service communication
        String authorization = "Bearer inter-service-token";
        String interactionId = UUID.randomUUID().toString();

        return consentClient.getConsent(consentId, authorization, interactionId);
    }
}
