package com.hlaff.wallet_api.dto;

import com.hlaff.wallet_api.enums.Currency;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

public record CreateWalletRequest(
        @NotBlank(message = "userId é obrigatório")
        String userId,
        
        @NotNull(message = "currency é obrigatório")
        Currency currency
) {}
