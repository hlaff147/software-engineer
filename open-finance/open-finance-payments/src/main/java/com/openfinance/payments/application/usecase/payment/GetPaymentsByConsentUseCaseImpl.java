package com.openfinance.payments.application.usecase.payment;

import com.openfinance.payments.application.exception.ConsentNotFoundException;
import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.port.input.GetPaymentsByConsentUseCase;
import com.openfinance.payments.domain.port.output.ConsentRepositoryPort;
import com.openfinance.payments.domain.port.output.PaymentRepositoryPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GetPaymentsByConsentUseCaseImpl implements GetPaymentsByConsentUseCase {

    private final PaymentRepositoryPort paymentRepository;
    private final ConsentRepositoryPort consentRepository;

    @Override
    public List<PixPayment> execute(GetPaymentsByConsentCommand command) {
        log.info("Getting payments for consent: {}", command.consentId());

        // Validate consent exists
        if (!consentRepository.findById(command.consentId()).isPresent()) {
            throw new ConsentNotFoundException(command.consentId());
        }

        if (command.startDate() != null && command.endDate() != null) {
            return paymentRepository.findByConsentIdAndDateRange(
                    command.consentId(),
                    command.startDate(),
                    command.endDate());
        }

        return paymentRepository.findByConsentId(command.consentId());
    }
}
