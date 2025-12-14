package com.example.openbanking.dto.v2;

/**
 * Request DTO para a versão 2.0.0 da API de Pagamentos.
 * Inclui campos novos: pixKey e endToEndId.
 */
public record PaymentRequestV2(
    String amount,
    String currency,
    String description,
    String pixKey,        // NOVO na V2
    String endToEndId     // NOVO na V2
) {}
