package com.hlaff.loggingx.kafka;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.apache.kafka.common.header.Header;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Helper para logging estruturado de eventos Kafka.
 * Centraliza a lógica de geração de logs para producers e consumers.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class KafkaLoggingHelper {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    /**
     * Loga envio de mensagem pelo producer
     */
    public void logProducerSend(ProducerRecord<?, ?> record) {
        if (!properties.getKafka().isLogProducer()) {
            return;
        }

        try {
            structuredLogger.info(event -> {
                event.component("kafka-producer")
                     .topic(record.topic())
                     .key(record.key() != null ? record.key().toString() : null);

                if (record.partition() != null) {
                    event.partition(record.partition());
                }

                if (properties.getKafka().isLogPayload() && record.value() != null) {
                    event.put("payload", record.value().toString());
                }

                if (properties.getKafka().isLogHeaders() && record.headers() != null) {
                    event.put("headers", extractHeaders(record.headers()));
                }

                event.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar envio Kafka: {}", e.getMessage());
        }
    }

    /**
     * Loga confirmação de envio pelo producer
     */
    public void logProducerAck(RecordMetadata metadata, Exception exception) {
        if (!properties.getKafka().isLogProducer()) {
            return;
        }

        try {
            if (exception != null) {
                structuredLogger.error(event -> {
                    event.component("kafka-producer")
                         .topic(metadata != null ? metadata.topic() : "unknown")
                         .error(exception);

                    if (metadata != null) {
                        event.partition(metadata.partition())
                             .offset(metadata.offset());
                    }

                    event.sampled(true);
                });
            } else {
                structuredLogger.debug(event -> {
                    event.component("kafka-producer")
                         .topic(metadata.topic())
                         .partition(metadata.partition())
                         .offset(metadata.offset());

                    event.sampled(true);
                });
            }

        } catch (Exception e) {
            log.debug("Erro ao logar ACK Kafka: {}", e.getMessage());
        }
    }

    /**
     * Loga recebimento de mensagem pelo consumer
     */
    public void logConsumerReceive(ConsumerRecord<?, ?> record) {
        if (!properties.getKafka().isLogConsumer()) {
            return;
        }

        try {
            structuredLogger.info(event -> {
                event.component("kafka-consumer")
                     .topic(record.topic())
                     .partition(record.partition())
                     .offset(record.offset())
                     .key(record.key() != null ? record.key().toString() : null);

                if (properties.getKafka().isLogPayload() && record.value() != null) {
                    event.put("payload", record.value().toString());
                }

                if (properties.getKafka().isLogHeaders() && record.headers() != null) {
                    event.put("headers", extractHeaders(record.headers()));
                }

                // Calcula lag se possível
                long currentTime = System.currentTimeMillis();
                if (record.timestamp() > 0) {
                    long lag = currentTime - record.timestamp();
                    event.put("lagMs", lag);
                }

                event.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar recebimento Kafka: {}", e.getMessage());
        }
    }

    /**
     * Extrai headers da mensagem Kafka para logging
     */
    private Map<String, String> extractHeaders(Iterable<Header> headers) {
        Map<String, String> headerMap = new LinkedHashMap<>();
        
        for (Header header : headers) {
            if (header.value() != null) {
                String value = new String(header.value(), StandardCharsets.UTF_8);
                headerMap.put(header.key(), value);
            }
        }
        
        return headerMap;
    }
}
