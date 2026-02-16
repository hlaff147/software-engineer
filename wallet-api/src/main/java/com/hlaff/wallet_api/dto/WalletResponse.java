package com.hlaff.wallet_api.dto;

import com.hlaff.wallet_api.enums.Currency;
import com.hlaff.wallet_api.enums.WalletStatus;

public record WalletResponse(
        String id,
        String userId,
        Currency currency,
        WalletStatus status,
        Long balance
) {}
