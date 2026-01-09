package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumPaymentPersonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class Creditor {
    EnumPaymentPersonType personType;
    String cpfCnpj;
    String name;
}
