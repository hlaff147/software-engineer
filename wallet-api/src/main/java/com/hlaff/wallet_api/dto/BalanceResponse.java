package com.hlaff.wallet_api.dto;

import com.hlaff.wallet_api.enums.Currency;

import java.time.Instant;

public record BalanceResponse(
        String id,
        Currency currency,
        Long balance,
        Instant asOf
) {}
