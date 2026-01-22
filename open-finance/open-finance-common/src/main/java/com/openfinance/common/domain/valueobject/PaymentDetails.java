package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumLocalInstrument;
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
