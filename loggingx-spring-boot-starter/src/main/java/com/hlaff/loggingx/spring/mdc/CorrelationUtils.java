package com.hlaff.loggingx.spring.mdc;

import org.slf4j.MDC;

import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.Callable;
import java.util.function.Supplier;

/**
 * Utilitários para gerenciamento de correlationId em contextos síncronos e assíncronos.
 */
public final class CorrelationUtils {

    private CorrelationUtils() {
        // Utility class
    }

    /**
     * Obtém o correlationId atual do MDC.
     */
    public static Optional<String> getCurrentCorrelationId() {
        return Optional.ofNullable(MDC.get(CorrelationFilter.MDC_CORRELATION_KEY));
    }

    /**
     * Define um correlationId no MDC.
     */
    public static void setCorrelationId(String correlationId) {
        if (correlationId != null && !correlationId.trim().isEmpty()) {
            MDC.put(CorrelationFilter.MDC_CORRELATION_KEY, correlationId);
        }
    }

    /**
     * Gera e define um novo correlationId no MDC.
     */
    public static String generateAndSetCorrelationId() {
        String correlationId = UUID.randomUUID().toString();
        setCorrelationId(correlationId);
        return correlationId;
    }

    /**
     * Remove o correlationId do MDC.
     */
    public static void clearCorrelationId() {
        MDC.remove(CorrelationFilter.MDC_CORRELATION_KEY);
    }

    /**
     * Executa um Runnable propagando o correlationId atual.
     */
    public static Runnable withCorrelation(Runnable runnable) {
        String correlationId = getCurrentCorrelationId().orElse(null);
        
        return () -> {
            String previousCorrelationId = getCurrentCorrelationId().orElse(null);
            try {
                if (correlationId != null) {
                    setCorrelationId(correlationId);
                }
                runnable.run();
            } finally {
                if (previousCorrelationId != null) {
                    setCorrelationId(previousCorrelationId);
                } else {
                    clearCorrelationId();
                }
            }
        };
    }

    /**
     * Executa um Callable propagando o correlationId atual.
     */
    public static <T> Callable<T> withCorrelation(Callable<T> callable) {
        String correlationId = getCurrentCorrelationId().orElse(null);
        
        return () -> {
            String previousCorrelationId = getCurrentCorrelationId().orElse(null);
            try {
                if (correlationId != null) {
                    setCorrelationId(correlationId);
                }
                return callable.call();
            } finally {
                if (previousCorrelationId != null) {
                    setCorrelationId(previousCorrelationId);
                } else {
                    clearCorrelationId();
                }
            }
        };
    }

    /**
     * Executa um Supplier propagando o correlationId atual.
     */
    public static <T> Supplier<T> withCorrelation(Supplier<T> supplier) {
        String correlationId = getCurrentCorrelationId().orElse(null);
        
        return () -> {
            String previousCorrelationId = getCurrentCorrelationId().orElse(null);
            try {
                if (correlationId != null) {
                    setCorrelationId(correlationId);
                }
                return supplier.get();
            } finally {
                if (previousCorrelationId != null) {
                    setCorrelationId(previousCorrelationId);
                } else {
                    clearCorrelationId();
                }
            }
        };
    }
}
