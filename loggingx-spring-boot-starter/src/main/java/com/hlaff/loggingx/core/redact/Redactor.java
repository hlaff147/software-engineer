package com.hlaff.loggingx.core.redact;

import java.util.Map;

/**
 * Interface para redação (mascaramento) de dados sensíveis nos logs.
 * Responsável por mascarar PII, truncar payloads grandes e aplicar políticas de privacidade.
 */
public interface Redactor {
    
    /**
     * Reduz os argumentos de um método, mascarando dados sensíveis e truncando se necessário.
     * 
     * @param parameterNames nomes dos parâmetros do método
     * @param values valores dos argumentos
     * @param maxLength tamanho máximo do payload antes do truncamento
     * @return mapa com argumentos processados (mascarados/truncados)
     */
    Map<String, Object> redactArgs(String[] parameterNames, Object[] values, int maxLength);
    
    /**
     * Reduz um valor de retorno, mascarando dados sensíveis e truncando se necessário.
     * 
     * @param value valor a ser processado
     * @param maxLength tamanho máximo do payload antes do truncamento
     * @return valor processado (mascarado/truncado)
     */
    Object redactValue(Object value, int maxLength);
    
    /**
     * Reduz um objeto arbitrário, aplicando políticas de mascaramento.
     * 
     * @param value objeto a ser processado
     * @param maxLength tamanho máximo do payload antes do truncamento
     * @return objeto processado
     */
    Object redactObject(Object value, int maxLength);
    
    /**
     * Verifica se uma chave deve ser mascarada baseado nas políticas configuradas.
     * 
     * @param key chave a ser verificada
     * @return true se a chave deve ser mascarada
     */
    boolean shouldRedact(String key);
    
    /**
     * Trunca um valor se exceder o tamanho máximo permitido.
     * 
     * @param value valor a ser truncado
     * @param maxLength tamanho máximo permitido
     * @return valor truncado se necessário
     */
    Object truncate(Object value, int maxLength);
}
