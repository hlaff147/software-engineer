package com.hlaff.loggingx.spring.aop;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.core.redact.Redactor;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;

/**
 * Aspecto responsável por interceptar métodos anotados com @BusinessEvent
 * e emitir eventos de negócio estruturados.
 */
@Aspect
@Slf4j
@RequiredArgsConstructor
public class BusinessEventAspect {

    private final StructuredLogger structuredLogger;
    private final Redactor redactor;
    private final LoggingXProperties properties;

    /**
     * Pointcut para métodos anotados com @BusinessEvent
     */
    @Pointcut("@annotation(businessEvent)")
    public void businessEventMethod(BusinessEvent businessEvent) {}

    /**
     * Advice executado após retorno bem-sucedido de métodos com @BusinessEvent
     */
    @AfterReturning(pointcut = "businessEventMethod(businessEvent)", returning = "returnValue", argNames = "businessEvent,returnValue")
    public void emitBusinessEvent(BusinessEvent businessEvent, Object returnValue) {
        
        if (!properties.isEnabled()) {
            return;
        }

        try {
            // Processa payload se necessário
            Object payload = null;
            if (businessEvent.useReturnAsPayload() && returnValue != null) {
                if (businessEvent.redactPayload()) {
                    payload = redactor.redactObject(returnValue, properties.getMaxPayloadLength());
                } else {
                    payload = returnValue;
                }
            }

            // Emite o evento de negócio
            emitEvent(businessEvent, payload);

        } catch (Exception e) {
            log.warn("Erro ao emitir evento de negócio {}.{}: {}", 
                    businessEvent.type(), businessEvent.name(), e.getMessage());
        }
    }

    private void emitEvent(BusinessEvent businessEvent, Object payload) {
        
        switch (businessEvent.level()) {
            case TRACE -> structuredLogger.trace(event -> buildBusinessEvent(event, businessEvent, payload));
            case DEBUG -> structuredLogger.debug(event -> buildBusinessEvent(event, businessEvent, payload));
            case WARN -> structuredLogger.warn(event -> buildBusinessEvent(event, businessEvent, payload));
            case ERROR -> structuredLogger.error(event -> buildBusinessEvent(event, businessEvent, payload));
            default -> structuredLogger.info(event -> buildBusinessEvent(event, businessEvent, payload));
        }
    }

    private void buildBusinessEvent(com.hlaff.loggingx.core.logger.LogEventBuilder event, 
                                   BusinessEvent businessEvent, Object payload) {
        
        event.component("business")
             .eventType(businessEvent.type())
             .eventName(businessEvent.name())
             .eventVersion(businessEvent.version());

        if (payload != null) {
            event.eventPayload(payload);
        }

        event.sampled(true);
    }
}
