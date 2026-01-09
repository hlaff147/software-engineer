package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumPaymentRejectionReasonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class PaymentRejectionReason {
    EnumPaymentRejectionReasonType code;
    String detail;
}
