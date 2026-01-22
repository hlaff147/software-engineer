package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.PixPayment;

import java.time.LocalDate;
import java.util.List;

public interface GetPaymentsByConsentUseCase {

    List<PixPayment> execute(GetPaymentsByConsentCommand command);

    record GetPaymentsByConsentCommand(
            String consentId,
            LocalDate startDate,
            LocalDate endDate) {
    }
}
