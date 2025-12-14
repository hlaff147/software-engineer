package com.example.openbanking.strategy;

/**
 * Contrato para todas as implementações de estratégia de pagamento.
 * Cada versão de API deve implementar esta interface.
 */
public interface PaymentStrategy {
    
    /**
     * Retorna o identificador da versão (ex: "1_0_0").
     * Usado para logs e validação.
     */
    String getVersion();
    
    /**
     * Processa a criação de um pagamento.
     * @param payload DTO específico da versão
     * @return Response DTO específico da versão
     */
    Object createPayment(Object payload);
    
    /**
     * Recupera detalhes de um pagamento.
     * @param id Identificador do pagamento
     * @return Response DTO específico da versão
     */
    Object getPayment(String id);
}
