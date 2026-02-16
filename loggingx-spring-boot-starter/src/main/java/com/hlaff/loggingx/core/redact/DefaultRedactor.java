package com.hlaff.loggingx.core.redact;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Implementação padrão do Redactor.
 * Mascara dados sensíveis baseado em chaves configuradas e anotações @Sensitive.
 */
@Slf4j
@RequiredArgsConstructor
public class DefaultRedactor implements Redactor {

    private static final String MASK = "***";
    private static final String TRUNCATED_SUFFIX = "...TRUNCATED";
    
    private final LoggingXProperties properties;
    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public Map<String, Object> redactArgs(String[] parameterNames, Object[] values, int maxLength) {
        Map<String, Object> result = new LinkedHashMap<>();
        
        for (int i = 0; i < parameterNames.length && i < values.length; i++) {
            String paramName = parameterNames[i] != null ? parameterNames[i] : ("arg" + i);
            Object value = values[i];
            
            if (shouldRedact(paramName)) {
                result.put(paramName, MASK);
            } else {
                result.put(paramName, redactObject(value, maxLength));
            }
        }
        
        return result;
    }

    @Override
    public Object redactValue(Object value, int maxLength) {
        return redactObject(value, maxLength);
    }

    @Override
    public Object redactObject(Object value, int maxLength) {
        if (value == null) {
            return null;
        }
        
        // Para tipos primitivos e strings simples
        if (isPrimitiveOrWrapper(value.getClass()) || value instanceof String) {
            return truncate(value, maxLength);
        }
        
        try {
            // Converte para JSON e processa recursivamente
            String json = objectMapper.writeValueAsString(value);
            JsonNode node = objectMapper.readTree(json);
            
            if (node.isObject()) {
                ObjectNode objectNode = (ObjectNode) node;
                redactJsonObject(objectNode);
            }
            
            // Converte de volta para objeto e verifica truncamento
            Object processed = objectMapper.treeToValue(node, Object.class);
            return truncate(processed, maxLength);
            
        } catch (JsonProcessingException e) {
            log.debug("Erro ao processar objeto para redação: {}", e.getMessage());
            return truncate(value.toString(), maxLength);
        }
    }

    @Override
    public boolean shouldRedact(String key) {
        if (key == null) {
            return false;
        }
        
        String lowerKey = key.toLowerCase();
        return properties.getRedactKeys().stream()
                .anyMatch(redactKey -> lowerKey.contains(redactKey.toLowerCase()));
    }

    @Override
    public Object truncate(Object value, int maxLength) {
        if (value == null) {
            return null;
        }
        
        String stringValue = value.toString();
        if (stringValue.length() > maxLength) {
            return stringValue.substring(0, maxLength) + TRUNCATED_SUFFIX;
        }
        
        return value;
    }

    /**
     * Reduz recursivamente um objeto JSON mascarando campos sensíveis.
     */
    private void redactJsonObject(ObjectNode objectNode) {
        List<String> fieldsToRedact = new ArrayList<>();
        
        objectNode.fieldNames().forEachRemaining(fieldName -> {
            if (shouldRedact(fieldName)) {
                fieldsToRedact.add(fieldName);
            } else {
                JsonNode fieldValue = objectNode.get(fieldName);
                if (fieldValue.isObject()) {
                    redactJsonObject((ObjectNode) fieldValue);
                }
            }
        });
        
        // Mascara os campos identificados como sensíveis
        fieldsToRedact.forEach(fieldName -> objectNode.put(fieldName, MASK));
    }

    /**
     * Verifica se a classe é um tipo primitivo ou wrapper.
     */
    private boolean isPrimitiveOrWrapper(Class<?> clazz) {
        return clazz.isPrimitive() || 
               clazz == Boolean.class ||
               clazz == Byte.class ||
               clazz == Character.class ||
               clazz == Short.class ||
               clazz == Integer.class ||
               clazz == Long.class ||
               clazz == Float.class ||
               clazz == Double.class;
    }
}
