package com.example.openbanking.strategy.impl;

import com.example.openbanking.dto.v2.PaymentRequestV2;
import com.example.openbanking.dto.v2.PaymentResponseV2;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

/**
 * Implementação para a versão 2.0.0 da API de Pagamentos.
 * 
 * Esta versão ESTENDE a V1 para reaproveitar lógica comum.
 * Apenas os métodos que mudaram são sobrescritos.
 * 
 * Novas funcionalidades em V2:
 * - Campo obrigatório pixKey
 * - Campo opcional endToEndId
 * - Response inclui transactionDate
 */
@Service("Payment_2_0_0")
public class PaymentStrategyV2 extends PaymentStrategyV1 {

    private static final Logger log = LoggerFactory.getLogger(PaymentStrategyV2.class);

    @Override
    public String getVersion() {
        return "2_0_0";
    }

    @Override
    public Object createPayment(Object payload) {
        PaymentRequestV2 request = (PaymentRequestV2) payload;

        // ========================================
        // NOVA REGRA DE NEGÓCIO EXCLUSIVA DA V2
        // ========================================
        if (request.pixKey() == null || request.pixKey().isBlank()) {
            throw new IllegalArgumentException("[V2] Campo 'pixKey' é obrigatório na versão 2.0.0");
        }

        log.info("[V2] Processando pagamento PIX: pixKey={}, amount={}", 
            request.pixKey(), request.amount());

        // OPÇÃO A: Reutilizar lógica da V1 (se core for compatível)
        // Em um caso real, você poderia chamar:
        // return super.createPayment(convertToV1(request));
        
        // OPÇÃO B: Implementar lógica específica da V2
        String generatedId = "v2-" + System.currentTimeMillis();
        return new PaymentResponseV2(
            generatedId, 
            "PROCESSING",
            LocalDateTime.now()  // Novo campo na V2
        );
    }
    
    @Override
    public Object getPayment(String id) {
        log.info("[V2] Buscando pagamento (formato V2): id={}", id);
        
        // V2 retorna o novo formato com transactionDate
        return new PaymentResponseV2(id, "COMPLETED", LocalDateTime.now());
    }
}
