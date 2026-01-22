package com.openfinance.payment.strategy;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Set;

@Component
public class PaymentStrategyFactory {

    private final Map<String, PaymentStrategy> strategies;

    public PaymentStrategyFactory(Map<String, PaymentStrategy> strategies) {
        this.strategies = strategies;
    }

    public PaymentStrategy getStrategy(String version) {
        String beanName = "Payment_" + version;

        PaymentStrategy strategy = strategies.get(beanName);

        if (strategy == null) {
            throw new UnsupportedOperationException(
                    "API version not supported: " + version +
                            ". Available versions: " + getAvailableVersions());
        }

        return strategy;
    }

    public boolean isVersionSupported(String version) {
        return strategies.containsKey("Payment_" + version);
    }

    public Set<String> getAvailableVersions() {
        return strategies.keySet();
    }
}
