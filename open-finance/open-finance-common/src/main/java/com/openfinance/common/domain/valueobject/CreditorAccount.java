package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumAccountPaymentsType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class CreditorAccount {
    String ispb;
    String issuer;
    String number;
    EnumAccountPaymentsType accountType;
}
