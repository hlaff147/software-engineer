package com.example.openbanking.strategy.impl;

import com.example.openbanking.dto.v1.PaymentRequestV1;
import com.example.openbanking.dto.v1.PaymentResponseV1;
import com.example.openbanking.strategy.PaymentStrategy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/**
 * Implementação base para a versão 1.0.0 da API de Pagamentos.
 * 
 * IMPORTANTE: O nome do Bean "Payment_1_0_0" será usado como chave
 * para localização dinâmica via PaymentServiceFactory.
 */
@Service("Payment_1_0_0")
public class PaymentStrategyV1 implements PaymentStrategy {

    private static final Logger log = LoggerFactory.getLogger(PaymentStrategyV1.class);

    @Override
    public String getVersion() {
        return "1_0_0";
    }

    @Override
    public Object createPayment(Object payload) {
        // Cast seguro - o Controller já converteu para o DTO correto
        PaymentRequestV1 request = (PaymentRequestV1) payload;
        
        log.info("[V1] Processando pagamento: amount={}, currency={}", 
            request.amount(), request.currency());
        
        // Aqui você colocaria a lógica real:
        // - Validações de negócio
        // - Chamadas a repositórios
        // - Integrações externas
        
        String generatedId = "v1-" + System.currentTimeMillis();
        return new PaymentResponseV1(generatedId, "PROCESSING");
    }

    @Override
    public Object getPayment(String id) {
        log.info("[V1] Buscando pagamento: id={}", id);
        
        // Aqui você buscaria no banco de dados
        return new PaymentResponseV1(id, "COMPLETED");
    }
}
