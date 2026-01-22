package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumConsentRejectionReasonType;
import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class ConsentRejectionReason {
    EnumConsentRejectionReasonType code;
    String detail;
}
