package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumPaymentRejectionReasonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class PaymentRejectionReason {
    EnumPaymentRejectionReasonType code;
    String detail;
}
