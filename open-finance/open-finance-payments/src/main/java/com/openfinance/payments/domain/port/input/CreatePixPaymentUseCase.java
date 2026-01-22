package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.PixPayment;
import com.openfinance.payments.domain.enums.EnumLocalInstrument;
import com.openfinance.payments.domain.valueobject.CreditorAccount;

import java.math.BigDecimal;
import java.util.List;

public interface CreatePixPaymentUseCase {

    List<PixPayment> execute(CreatePixPaymentCommand command);

    record CreatePixPaymentCommand(
            List<PaymentItem> payments,
            String idempotencyKey) {
    }

    record PaymentItem(
            String endToEndId,
            EnumLocalInstrument localInstrument,
            BigDecimal amount,
            String currency,
            CreditorAccount creditorAccount,
            String remittanceInformation,
            String qrCode,
            String proxy,
            String cnpjInitiator,
            String transactionIdentification,
            String authorisationFlow,
            String consentId) {
    }
}
