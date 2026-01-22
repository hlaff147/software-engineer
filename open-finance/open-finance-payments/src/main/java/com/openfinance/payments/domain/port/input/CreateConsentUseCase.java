package com.openfinance.payments.domain.port.input;

import com.openfinance.payments.domain.entity.Consent;
import com.openfinance.payments.domain.valueobject.*;

public interface CreateConsentUseCase {

    Consent execute(CreateConsentCommand command);

    record CreateConsentCommand(
            LoggedUser loggedUser,
            BusinessEntity businessEntity,
            Creditor creditor,
            PaymentInfo payment,
            DebtorAccount debtorAccount,
            String idempotencyKey) {
    }
}
