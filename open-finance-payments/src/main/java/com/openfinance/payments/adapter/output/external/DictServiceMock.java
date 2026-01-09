package com.openfinance.payments.adapter.output.external;

import com.openfinance.payments.domain.port.output.DictServicePort;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class DictServiceMock implements DictServicePort {

    @Override
    public DictValidationResult validatePixKey(String pixKey) {
        log.info("[DICT MOCK] Validating Pix key: {}", pixKey);

        // Always returns success for mock purposes
        return DictValidationResult.builder()
                .valid(true)
                .accountHolderName("Mock Account Holder")
                .ispb("12345678")
                .accountNumber("1234567890")
                .accountType("CACC")
                .build();
    }
}
