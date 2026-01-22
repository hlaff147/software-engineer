package com.openfinance.payments.application.usecase.payment;

import com.openfinance.payments.application.exception.PaymentNotFoundException;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.port.input.GetPixPaymentUseCase;
import com.openfinance.payments.domain.port.output.PaymentRepositoryPort;
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
