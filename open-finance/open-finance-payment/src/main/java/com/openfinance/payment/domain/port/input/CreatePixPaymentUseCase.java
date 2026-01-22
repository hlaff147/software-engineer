package com.openfinance.payment.domain.port.input;

import com.openfinance.payment.domain.entity.PixPayment;
import com.openfinance.common.domain.enums.EnumLocalInstrument;
import com.openfinance.common.domain.valueobject.CreditorAccount;

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
