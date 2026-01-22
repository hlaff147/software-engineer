package com.openfinance.payment.application.usecase;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.payment.domain.port.input.GetPixPaymentUseCase;
import com.openfinance.payment.domain.port.output.PaymentRepositoryPort;
import com.openfinance.common.application.exception.PaymentNotFoundException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class GetPixPaymentUseCaseImpl implements GetPixPaymentUseCase {

    private final PaymentRepositoryPort paymentRepository;

    @Override
    public PixPayment execute(String paymentId) {
        log.info("Getting payment: {}", paymentId);

        return paymentRepository.findById(paymentId)
                .orElseThrow(() -> new PaymentNotFoundException(paymentId));
    }
}
