package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumPaymentPersonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class Creditor {
    EnumPaymentPersonType personType;
    String cpfCnpj;
    String name;
}
