package com.hlaff.wallet_api.dto;

import jakarta.validation.constraints.Positive;

import java.util.Map;

public record AmountRequest(
        @Positive(message = "amount deve ser positivo")
        Long amount,
        
        Map<String, String> metadata
) {}
