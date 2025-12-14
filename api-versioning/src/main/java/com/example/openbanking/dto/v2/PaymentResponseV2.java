package com.example.openbanking.dto.v2;

import java.time.LocalDateTime;

/**
 * Response DTO para a versão 2.0.0 da API de Pagamentos.
 * Inclui campo novo: transactionDate.
 */
public record PaymentResponseV2(
    String id,
    String status,
    LocalDateTime transactionDate  // NOVO na V2
) {}
