package com.example.openbanking.strategy;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Set;

/**
 * Fábrica que resolve dinamicamente qual estratégia usar
 * baseado na versão recebida na URL.
 * 
 * O Spring popula o Map automaticamente com:
 * - Chave: Nome do Bean (@Service("Payment_1_0_0"))
 * - Valor: Instância da classe
 */
@Component
public class PaymentServiceFactory {

    private final Map<String, PaymentStrategy> strategies;

    // Injeção via construtor (recomendado)
    public PaymentServiceFactory(Map<String, PaymentStrategy> strategies) {
        this.strategies = strategies;
    }

    /**
     * Retorna a estratégia correspondente à versão.
     * 
     * @param version Versão da URL (ex: "1_0_0")
     * @return PaymentStrategy correspondente
     * @throws UnsupportedOperationException se versão não existir
     */
    public PaymentStrategy getStrategy(String version) {
        // Convenção: prefixo + versão
        String beanName = "Payment_" + version;
        
        PaymentStrategy strategy = strategies.get(beanName);
        
        if (strategy == null) {
            throw new UnsupportedOperationException(
                "Versão de API não suportada: " + version + 
                ". Versões disponíveis: " + getAvailableVersions()
            );
        }
        
        return strategy;
    }
    
    /**
     * Verifica se uma versão é suportada.
     */
    public boolean isVersionSupported(String version) {
        return strategies.containsKey("Payment_" + version);
    }
    
    /**
     * Retorna todas as versões disponíveis.
     */
    public Set<String> getAvailableVersions() {
        return strategies.keySet();
    }
}
