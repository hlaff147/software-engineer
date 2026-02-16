package com.hlaff.loggingx.core.logger;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;

import java.time.Instant;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Consumer;

/**
 * Implementação do StructuredLogger usando SLF4J.
 * Emite eventos JSON estruturados conforme o padrão LoggingX.
 */
@Slf4j
@RequiredArgsConstructor
public class Slf4jStructuredLogger implements StructuredLogger {

    private final ObjectMapper mapper = new ObjectMapper();
    private final LoggingXProperties properties;

    @Override
    public void info(Consumer<LogEventBuilder> eventBuilder) {
        emit("INFO", eventBuilder, log::info);
    }

    @Override
    public void warn(Consumer<LogEventBuilder> eventBuilder) {
        emit("WARN", eventBuilder, log::warn);
    }

    @Override
    public void error(Consumer<LogEventBuilder> eventBuilder) {
        emit("ERROR", eventBuilder, log::error);
    }

    @Override
    public void debug(Consumer<LogEventBuilder> eventBuilder) {
        emit("DEBUG", eventBuilder, log::debug);
    }

    @Override
    public void trace(Consumer<LogEventBuilder> eventBuilder) {
        emit("TRACE", eventBuilder, log::trace);
    }

    private void emit(String level, Consumer<LogEventBuilder> eventBuilder, Consumer<String> logMethod) {
        Map<String, Object> eventData = createBaseEvent(level);
        
        LogEventBuilder builder = new DefaultLogEventBuilder(eventData, properties.isIncludeStacktrace());
        eventBuilder.accept(builder);
        
        try {
            String json = mapper.writeValueAsString(eventData);
            logMethod.accept(json);
        } catch (JsonProcessingException e) {
            log.warn("Falha ao serializar evento de log: {}", e.getMessage());
        }
    }

    private Map<String, Object> createBaseEvent(String level) {
        Map<String, Object> base = new LinkedHashMap<>();
        base.put("@timestamp", Instant.now().toString());
        base.put("level", level);
        base.put("service", properties.getService());
        base.put("env", properties.getEnv());
        base.put("version", properties.getVersion());
        
        // Adiciona correlationId do MDC se disponível
        String correlationId = MDC.get("correlationId");
        if (correlationId != null) {
            base.put("correlationId", correlationId);
        }
        
        // Adiciona traceId e spanId se disponíveis (OpenTelemetry)
        String traceId = MDC.get("traceId");
        if (traceId != null) {
            base.put("traceId", traceId);
        }
        
        String spanId = MDC.get("spanId");
        if (spanId != null) {
            base.put("spanId", spanId);
        }
        
        return base;
    }

    /**
     * Implementação padrão do LogEventBuilder
     */
    private static class DefaultLogEventBuilder implements LogEventBuilder {
        
        private final Map<String, Object> eventData;
        private final boolean includeStackTrace;

        public DefaultLogEventBuilder(Map<String, Object> eventData, boolean includeStackTrace) {
            this.eventData = eventData;
            this.includeStackTrace = includeStackTrace;
        }

        @Override
        public LogEventBuilder put(String key, Object value) {
            eventData.put(key, value);
            return this;
        }

        @Override
        public LogEventBuilder component(String component) {
            return put("component", component);
        }

        @Override
        public LogEventBuilder clazz(String className) {
            return put("class", className);
        }

        @Override
        public LogEventBuilder method(String methodName) {
            return put("method", methodName);
        }

        @Override
        public LogEventBuilder args(Object args) {
            return put("args", args);
        }

        @Override
        public LogEventBuilder ret(Object returnValue) {
            return put("return", returnValue);
        }

        @Override
        public LogEventBuilder durationMs(long duration) {
            return put("durationMs", duration);
        }

        @Override
        public LogEventBuilder sizeIn(long sizeIn) {
            return put("sizeIn", sizeIn);
        }

        @Override
        public LogEventBuilder sizeOut(long sizeOut) {
            return put("sizeOut", sizeOut);
        }

        @Override
        public LogEventBuilder eventType(String eventType) {
            return put("eventType", eventType);
        }

        @Override
        public LogEventBuilder eventName(String eventName) {
            return put("eventName", eventName);
        }

        @Override
        public LogEventBuilder eventVersion(int version) {
            return put("eventVersion", version);
        }

        @Override
        public LogEventBuilder eventPayload(Object payload) {
            return put("eventPayload", payload);
        }

        @Override
        public LogEventBuilder httpMethod(String method) {
            return put("httpMethod", method);
        }

        @Override
        public LogEventBuilder httpPath(String path) {
            return put("httpPath", path);
        }

        @Override
        public LogEventBuilder httpStatus(int status) {
            return put("httpStatus", status);
        }

        @Override
        public LogEventBuilder remoteIp(String remoteIp) {
            return put("remoteIp", remoteIp);
        }

        @Override
        public LogEventBuilder topic(String topic) {
            return put("topic", topic);
        }

        @Override
        public LogEventBuilder partition(int partition) {
            return put("partition", partition);
        }

        @Override
        public LogEventBuilder offset(long offset) {
            return put("offset", offset);
        }

        @Override
        public LogEventBuilder key(String key) {
            return put("key", key);
        }

        @Override
        public LogEventBuilder dbSystem(String system) {
            return put("db.system", system);
        }

        @Override
        public LogEventBuilder dbOperation(String operation) {
            return put("db.op", operation);
        }

        @Override
        public LogEventBuilder collection(String collection) {
            return put("collection", collection);
        }

        @Override
        public LogEventBuilder error(Throwable throwable) {
            errorKind(throwable.getClass().getName());
            errorMessage(throwable.getMessage());
            if (includeStackTrace) {
                errorStack(getStackTraceAsString(throwable));
            }
            return this;
        }

        @Override
        public LogEventBuilder errorKind(String kind) {
            return put("error.kind", kind);
        }

        @Override
        public LogEventBuilder errorMessage(String message) {
            return put("error.message", message);
        }

        @Override
        public LogEventBuilder errorStack(String stackTrace) {
            return put("error.stack", stackTrace);
        }

        @Override
        public LogEventBuilder sampled(boolean sampled) {
            return put("sampled", sampled);
        }

        @Override
        public LogEventBuilder truncated(boolean truncated) {
            return put("truncated", truncated);
        }

        @Override
        public LogEventBuilder redactedFields(String... fields) {
            return put("redactedFields", Arrays.asList(fields));
        }

        private String getStackTraceAsString(Throwable throwable) {
            StringBuilder sb = new StringBuilder();
            for (StackTraceElement element : throwable.getStackTrace()) {
                sb.append(element.toString()).append("\n");
            }
            return sb.toString();
        }
    }
}
