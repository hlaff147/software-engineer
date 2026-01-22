package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumPaymentPurpose;
import com.openfinance.common.domain.enums.EnumPaymentType;
import lombok.Builder;
import lombok.Value;

import java.math.BigDecimal;
import java.time.LocalDate;

@Value
@Builder
public class PaymentInfo {
    EnumPaymentType type;
    EnumPaymentPurpose purpose;
    LocalDate date;
    String currency;
    BigDecimal amount;
    String ibgeTownCode;
    PaymentDetails details;
}
