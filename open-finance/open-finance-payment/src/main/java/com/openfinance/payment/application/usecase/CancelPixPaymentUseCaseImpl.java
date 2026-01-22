package com.openfinance.payment.application.usecase;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.payment.domain.port.input.CancelPixPaymentUseCase;
import com.openfinance.payment.domain.port.output.PaymentRepositoryPort;
import com.openfinance.common.application.exception.PaymentNotFoundException;
import com.openfinance.common.application.exception.PaymentCancellationNotAllowedException;
import com.openfinance.common.domain.valueobject.Cancellation;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
@RequiredArgsConstructor
public class CancelPixPaymentUseCaseImpl implements CancelPixPaymentUseCase {

    private final PaymentRepositoryPort paymentRepository;

    @Override
    public PixPayment execute(String paymentId, Cancellation cancellation) {
        log.info("Cancelling payment: {}", paymentId);

        var payment = paymentRepository.findById(paymentId)
                .orElseThrow(() -> new PaymentNotFoundException(paymentId));

        if (!payment.canBeCancelled()) {
            throw new PaymentCancellationNotAllowedException(
                    paymentId, payment.getStatus().name());
        }

        payment.cancel(cancellation);

        var saved = paymentRepository.save(payment);
        log.info("Payment cancelled: {}", saved.getPaymentId());

        return saved;
    }
}
