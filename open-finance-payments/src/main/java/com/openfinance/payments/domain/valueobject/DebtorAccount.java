package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumAccountPaymentsType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class DebtorAccount {
    String ispb;
    String issuer;
    String number;
    EnumAccountPaymentsType accountType;
}
