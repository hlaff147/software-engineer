package com.openfinance.payments.adapter.output.external;

import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.port.output.SpiServicePort;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SpiServiceMock implements SpiServicePort {

    @Override
    public SpiResult sendPayment(PixPayment payment) {
        log.info("[SPI MOCK] Sending payment to SPI: paymentId={}, endToEndId={}, amount={}",
                payment.getPaymentId(), payment.getEndToEndId(), payment.getAmount());

        // Always returns success for mock purposes
        return SpiResult.builder()
                .success(true)
                .endToEndId(payment.getEndToEndId())
                .build();
    }
}
