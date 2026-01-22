package com.openfinance.payments.domain.valueobject;

import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class Document {
    String identification;
    String rel;
}
