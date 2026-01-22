package com.openfinance.consent.domain.port.input;

import com.openfinance.consent.domain.entity.Consent;
import com.openfinance.common.domain.valueobject.*;

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
