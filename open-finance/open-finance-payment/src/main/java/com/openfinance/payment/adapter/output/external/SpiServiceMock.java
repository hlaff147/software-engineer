package com.openfinance.payment.adapter.output.external;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.payment.domain.port.output.SpiServicePort;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SpiServiceMock implements SpiServicePort {

    @Override
    public SpiResult sendPayment(PixPayment payment) {
        log.info("[MOCK] Sending payment {} to SPI", payment.getPaymentId());
        // Mock implementation - always succeeds
        // In production, this would call the real SPI service
        return new SpiResult(true, "Payment processed successfully");
    }
}
