package com.example.openbanking.dto.v1;

/**
 * Request DTO para a versão 1.0.0 da API de Pagamentos.
 */
public record PaymentRequestV1(
    String amount,
    String currency,
    String description
) {}
