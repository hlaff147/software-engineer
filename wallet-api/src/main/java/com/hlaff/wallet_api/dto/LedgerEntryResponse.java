package com.hlaff.wallet_api.dto;

import com.hlaff.wallet_api.enums.OperationType;

import java.time.Instant;

public record LedgerEntryResponse(
        String id,
        String walletId,
        OperationType operation,
        Long amount,
        Instant occurredAt,
        Long resultingBalance
) {}
