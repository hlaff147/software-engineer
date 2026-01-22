package com.openfinance.consent.strategy;

import org.springframework.stereotype.Component;

import java.util.Map;
import java.util.Set;

@Component
public class ConsentStrategyFactory {

    private final Map<String, ConsentStrategy> strategies;

    public ConsentStrategyFactory(Map<String, ConsentStrategy> strategies) {
        this.strategies = strategies;
    }

    public ConsentStrategy getStrategy(String version) {
        String beanName = "Consent_" + version;

        ConsentStrategy strategy = strategies.get(beanName);

        if (strategy == null) {
            throw new UnsupportedOperationException(
                    "API version not supported: " + version +
                            ". Available versions: " + getAvailableVersions());
        }

        return strategy;
    }

    public boolean isVersionSupported(String version) {
        return strategies.containsKey("Consent_" + version);
    }

    public Set<String> getAvailableVersions() {
        return strategies.keySet();
    }
}
