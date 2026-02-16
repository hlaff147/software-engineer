package com.hlaff.wallet_api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;

import java.util.Map;

public record TransferRequest(
        @NotBlank(message = "fromWalletId é obrigatório")
        String fromWalletId,
        
        @NotBlank(message = "toWalletId é obrigatório")
        String toWalletId,
        
        @Positive(message = "amount deve ser positivo")
        Long amount,
        
        Map<String, String> metadata
) {}
