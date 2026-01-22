package com.openfinance.payment.domain.port.input;

import com.openfinance.payment.domain.entity.PixPayment;

import java.time.LocalDate;
import java.util.List;

public interface GetPaymentsByConsentUseCase {
    List<PixPayment> execute(String consentId, LocalDate startDate, LocalDate endDate);
}
