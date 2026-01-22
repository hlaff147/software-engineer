package com.openfinance.common.domain.valueobject;

import com.openfinance.common.domain.enums.EnumCancellationFrom;
import com.openfinance.common.domain.enums.EnumCancellationReason;
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
