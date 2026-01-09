package com.openfinance.payments.application.usecase.payment;

import com.openfinance.payments.application.exception.PaymentCancellationNotAllowedException;
import com.openfinance.payments.application.exception.PaymentNotFoundException;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.enums.EnumCancellationFrom;
import com.openfinance.payments.domain.enums.EnumCancellationReason;
import com.openfinance.payments.domain.enums.EnumPaymentStatusType;
import com.openfinance.payments.domain.port.input.CancelPixPaymentUseCase;
import com.openfinance.payments.domain.port.output.PaymentRepositoryPort;
import com.openfinance.payments.domain.valueobject.Cancellation;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.Instant;

@Slf4j
@Service
@RequiredArgsConstructor
public class CancelPixPaymentUseCaseImpl implements CancelPixPaymentUseCase {

    private final PaymentRepositoryPort paymentRepository;

    @Override
    public PixPayment execute(CancelPixPaymentCommand command) {
        log.info("Cancelling payment: {}", command.paymentId());

        var payment = paymentRepository.findById(command.paymentId())
                .orElseThrow(() -> new PaymentNotFoundException(command.paymentId()));

        if (!payment.canBeCancelled()) {
            throw new PaymentCancellationNotAllowedException(
                    command.paymentId(),
                    payment.getStatus().name());
        }

        var cancellationReason = determineCancellationReason(payment.getStatus());

        var cancellation = Cancellation.builder()
                .reason(cancellationReason)
                .cancelledFrom(EnumCancellationFrom.INICIADORA)
                .cancelledAt(Instant.now())
                .cancelledBy(command.cancelledBy())
                .build();

        payment.cancel(cancellation);
        var saved = paymentRepository.save(payment);

        log.info("Payment cancelled: {}", saved.getPaymentId());
        return saved;
    }

    private EnumCancellationReason determineCancellationReason(EnumPaymentStatusType status) {
        return switch (status) {
            case PDNG -> EnumCancellationReason.CANCELADO_PENDENCIA;
            case SCHD -> EnumCancellationReason.CANCELADO_AGENDAMENTO;
            default -> EnumCancellationReason.CANCELADO_PENDENCIA;
        };
    }
}
