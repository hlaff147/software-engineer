package com.example.openbanking.dto.v1;

/**
 * Response DTO para a versão 1.0.0 da API de Pagamentos.
 */
public record PaymentResponseV1(
    String id,
    String status
) {}
