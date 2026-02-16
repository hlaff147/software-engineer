package com.hlaff.loggingx.core.logger;

import java.util.function.Consumer;

/**
 * Interface principal para emissão de logs estruturados em JSON.
 * Abstrai a implementação do logger subjacente (SLF4J/Logback).
 */
public interface StructuredLogger {
    
    /**
     * Emite log de nível INFO
     */
    void info(Consumer<LogEventBuilder> eventBuilder);
    
    /**
     * Emite log de nível WARN
     */
    void warn(Consumer<LogEventBuilder> eventBuilder);
    
    /**
     * Emite log de nível ERROR
     */
    void error(Consumer<LogEventBuilder> eventBuilder);
    
    /**
     * Emite log de nível DEBUG
     */
    void debug(Consumer<LogEventBuilder> eventBuilder);
    
    /**
     * Emite log de nível TRACE
     */
    void trace(Consumer<LogEventBuilder> eventBuilder);
}
