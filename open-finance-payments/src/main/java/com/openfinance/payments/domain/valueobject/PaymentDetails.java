package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumLocalInstrument;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class PaymentDetails {
    EnumLocalInstrument localInstrument;
    String qrCode;
    String proxy;
    CreditorAccount creditorAccount;
}
