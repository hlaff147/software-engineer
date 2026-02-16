package com.hlaff.wallet_api.util;

import java.util.UUID;

public class CorrelationId {
    
    private static final String CORRELATION_ID_HEADER = "X-Correlation-ID";
    private static final ThreadLocal<String> correlationIdHolder = new ThreadLocal<>();
    
    public static String getHeaderName() {
        return CORRELATION_ID_HEADER;
    }
    
    public static String get() {
        String correlationId = correlationIdHolder.get();
        if (correlationId == null) {
            correlationId = generate();
            set(correlationId);
        }
        return correlationId;
    }
    
    public static void set(String correlationId) {
        correlationIdHolder.set(correlationId);
    }
    
    public static void clear() {
        correlationIdHolder.remove();
    }
    
    public static String generate() {
        return UUID.randomUUID().toString();
    }
}
