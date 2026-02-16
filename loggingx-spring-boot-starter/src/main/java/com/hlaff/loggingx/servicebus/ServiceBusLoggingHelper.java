package com.hlaff.loggingx.servicebus;

import com.azure.messaging.servicebus.ServiceBusErrorContext;
import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusReceivedMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

/**
 * Helper para logging estruturado de eventos do Azure Service Bus.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class ServiceBusLoggingHelper {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    /**
     * Loga envio de mensagem pelo Service Bus Sender.
     */
    public void logProducerSend(ServiceBusSenderClient sender, ServiceBusMessage message) {
        if (!properties.getServicebus().isLogProducer()) {
            return;
        }

        try {
            structuredLogger.info(event -> {
                event.component("servicebus-producer")
                     .topic(sender.getEntityPath())
                     .put("messageId", message.getMessageId())
                     .put("correlationId", message.getCorrelationId());

                if (properties.getServicebus().isLogPayload() && message.getBody() != null) {
                    event.put("payload", message.getBody().toString());
                }

                if (properties.getServicebus().isLogApplicationProperties() &&
                    message.getApplicationProperties() != null && !message.getApplicationProperties().isEmpty()) {
                    event.put("applicationProperties", message.getApplicationProperties());
                }

                event.sampled(true);
            });
        } catch (Exception e) {
            log.debug("Erro ao logar envio Service Bus: {}", e.getMessage());
        }
    }

    /**
     * Loga recebimento de mensagem pelo Service Bus.
     */
    public void logConsumerReceive(String entity, ServiceBusReceivedMessage message) {
        if (!properties.getServicebus().isLogConsumer()) {
            return;
        }

        try {
            structuredLogger.info(event -> {
                event.component("servicebus-consumer")
                     .topic(entity)
                     .put("messageId", message.getMessageId())
                     .put("correlationId", message.getCorrelationId());

                if (properties.getServicebus().isLogPayload() && message.getBody() != null) {
                    event.put("payload", message.getBody().toString());
                }

                if (properties.getServicebus().isLogApplicationProperties() &&
                    message.getApplicationProperties() != null && !message.getApplicationProperties().isEmpty()) {
                    event.put("applicationProperties", message.getApplicationProperties());
                }

                event.sampled(true);
            });
        } catch (Exception e) {
            log.debug("Erro ao logar recebimento Service Bus: {}", e.getMessage());
        }
    }

    /**
     * Loga erros de processamento do Service Bus.
     */
    public void logProcessError(ServiceBusErrorContext context) {
        try {
            structuredLogger.error(event -> {
                event.component("servicebus")
                     .topic(context.getEntityPath())
                     .errorKind(context.getException().getClass().getSimpleName())
                     .errorMessage(context.getException().getMessage());

                if (properties.isIncludeStacktrace()) {
                    event.error(context.getException());
                }

                event.sampled(true);
            });
        } catch (Exception e) {
            log.debug("Erro ao logar erro Service Bus: {}", e.getMessage());
        }
    }
}

