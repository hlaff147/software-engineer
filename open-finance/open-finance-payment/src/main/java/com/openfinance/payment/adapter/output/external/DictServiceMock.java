package com.openfinance.payment.adapter.output.external;

import com.openfinance.payment.domain.port.output.DictServicePort;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class DictServiceMock implements DictServicePort {

    @Override
    public void validatePixKey(String pixKey) {
        log.info("[MOCK] Validating Pix key: {}", pixKey);
        // Mock implementation - always succeeds
        // In production, this would call the real DICT service
    }
}
