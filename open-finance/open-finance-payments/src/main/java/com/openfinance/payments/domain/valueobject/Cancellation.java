package com.openfinance.payments.domain.valueobject;

import com.openfinance.payments.domain.enums.EnumCancellationFrom;
import com.openfinance.payments.domain.enums.EnumCancellationReason;
import lombok.Builder;
import lombok.Value;

import java.time.Instant;

@Value
@Builder
public class Cancellation {
    EnumCancellationReason reason;
    EnumCancellationFrom cancelledFrom;
    Instant cancelledAt;
    Document cancelledBy;
}
