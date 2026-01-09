package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumConsentRejectionReasonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class ConsentRejectionReason {
    EnumConsentRejectionReasonType code;
    String detail;
}
