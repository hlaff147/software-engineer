package com.openfinance.payments.domain.valueobject;

import lombok.Builder;
import lombok.Value;

@Value
@Builder
public class BusinessEntity {
    Document document;
}
