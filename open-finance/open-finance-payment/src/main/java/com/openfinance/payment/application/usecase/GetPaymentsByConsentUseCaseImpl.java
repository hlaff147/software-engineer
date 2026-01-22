package com.openfinance.payment.application.usecase;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.payment.domain.port.input.GetPaymentsByConsentUseCase;
import com.openfinance.payment.domain.port.output.PaymentRepositoryPort;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.time.LocalDate;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class GetPaymentsByConsentUseCaseImpl implements GetPaymentsByConsentUseCase {

    private final PaymentRepositoryPort paymentRepository;

    @Override
    public List<PixPayment> execute(String consentId, LocalDate startDate, LocalDate endDate) {
        log.info("Getting payments for consent: {}", consentId);

        if (startDate != null && endDate != null) {
            return paymentRepository.findByConsentIdAndDateRange(consentId, startDate, endDate);
        }

        return paymentRepository.findByConsentId(consentId);
    }
}
