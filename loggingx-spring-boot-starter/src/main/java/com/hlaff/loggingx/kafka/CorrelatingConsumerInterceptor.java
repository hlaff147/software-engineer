package com.hlaff.loggingx.kafka;

import com.hlaff.loggingx.spring.mdc.CorrelationFilter;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerInterceptor;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.OffsetAndMetadata;
import org.apache.kafka.common.TopicPartition;
import org.apache.kafka.common.header.Header;
import org.slf4j.MDC;

import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * Interceptor para Kafka Consumer que:
 * - Extrai correlationId dos headers das mensagens e adiciona no MDC
 * - Gera logs estruturados de consumo de mensagens
 */
@Slf4j
public class CorrelatingConsumerInterceptor<K, V> implements ConsumerInterceptor<K, V> {

    private static final String CORRELATION_HEADER = "X-Correlation-Id";

    @Override
    public ConsumerRecords<K, V> onConsume(ConsumerRecords<K, V> records) {
        for (ConsumerRecord<K, V> record : records) {
            // Extrai correlationId do header da mensagem e adiciona no MDC
            String correlationId = extractCorrelationId(record);
            
            if (correlationId != null) {
                MDC.put(CorrelationFilter.MDC_CORRELATION_KEY, correlationId);
            }

            // Log de consumo (se configurado)
            logConsumerReceive(record, correlationId);
        }

        return records;
    }

    @Override
    public void onCommit(Map<TopicPartition, OffsetAndMetadata> offsets) {
        // Log de commit se necessário
        logConsumerCommit(offsets);
    }

    @Override
    public void close() {
        // Cleanup if needed
    }

    @Override
    public void configure(Map<String, ?> configs) {
        // Configuration if needed
    }

    private String extractCorrelationId(ConsumerRecord<K, V> record) {
        Header correlationHeader = record.headers().lastHeader(CORRELATION_HEADER);
        
        if (correlationHeader != null && correlationHeader.value() != null) {
            return new String(correlationHeader.value(), StandardCharsets.UTF_8);
        }
        
        return null;
    }

    private void logConsumerReceive(ConsumerRecord<K, V> record, String correlationId) {
        try {
            log.debug("Kafka Consumer Receive - Topic: {}, Partition: {}, Offset: {}, Key: {}, CorrelationId: {}", 
                     record.topic(), 
                     record.partition(), 
                     record.offset(), 
                     record.key(), 
                     correlationId);
        } catch (Exception e) {
            log.trace("Erro ao logar recebimento Kafka: {}", e.getMessage());
        }
    }

    private void logConsumerCommit(Map<TopicPartition, OffsetAndMetadata> offsets) {
        try {
            log.debug("Kafka Consumer Commit - Offsets: {}", offsets.size());
        } catch (Exception e) {
            log.trace("Erro ao logar commit Kafka: {}", e.getMessage());
        }
    }
}
