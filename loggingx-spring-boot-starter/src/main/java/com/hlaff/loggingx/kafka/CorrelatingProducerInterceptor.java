package com.hlaff.loggingx.kafka;

import com.hlaff.loggingx.spring.mdc.CorrelationFilter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.producer.ProducerInterceptor;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.clients.producer.RecordMetadata;
import org.slf4j.MDC;

import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * Interceptor para Kafka Producer que:
 * - Adiciona correlationId nos headers das mensagens
 * - Gera logs estruturados de produção de mensagens
 */
@Slf4j
public class CorrelatingProducerInterceptor<K, V> implements ProducerInterceptor<K, V> {

    private static final String CORRELATION_HEADER = "X-Correlation-Id";

    @Override
    public ProducerRecord<K, V> onSend(ProducerRecord<K, V> record) {
        // Adiciona correlationId do MDC nos headers da mensagem
        String correlationId = MDC.get(CorrelationFilter.MDC_CORRELATION_KEY);
        
        if (correlationId != null) {
            record.headers().add(CORRELATION_HEADER, correlationId.getBytes(StandardCharsets.UTF_8));
        }

        // Log de envio (se configurado)
        logProducerSend(record, correlationId);

        return record;
    }

    @Override
    public void onAcknowledgement(RecordMetadata metadata, Exception exception) {
        if (exception != null) {
            logProducerError(metadata, exception);
        } else {
            logProducerSuccess(metadata);
        }
    }

    @Override
    public void close() {
        // Cleanup if needed
    }

    @Override
    public void configure(Map<String, ?> configs) {
        // Configuration if needed
    }

    private void logProducerSend(ProducerRecord<K, V> record, String correlationId) {
        try {
            log.debug("Kafka Producer Send - Topic: {}, Partition: {}, Key: {}, CorrelationId: {}", 
                     record.topic(), 
                     record.partition(), 
                     record.key(), 
                     correlationId);
        } catch (Exception e) {
            log.trace("Erro ao logar envio Kafka: {}", e.getMessage());
        }
    }

    private void logProducerSuccess(RecordMetadata metadata) {
        try {
            log.debug("Kafka Producer Success - Topic: {}, Partition: {}, Offset: {}", 
                     metadata.topic(), 
                     metadata.partition(), 
                     metadata.offset());
        } catch (Exception e) {
            log.trace("Erro ao logar sucesso Kafka: {}", e.getMessage());
        }
    }

    private void logProducerError(RecordMetadata metadata, Exception exception) {
        try {
            String topic = metadata != null ? metadata.topic() : "unknown";
            log.error("Kafka Producer Error - Topic: {}, Error: {}", topic, exception.getMessage());
        } catch (Exception e) {
            log.trace("Erro ao logar erro Kafka: {}", e.getMessage());
        }
    }
}
