package com.hlaff.loggingx.core.logger;

/**
 * Builder para construção fluent de eventos de log estruturados.
 * Permite adicionar campos específicos de forma tipada.
 */
public interface LogEventBuilder {
    
    /**
     * Adiciona um campo customizado ao evento
     */
    LogEventBuilder put(String key, Object value);
    
    /**
     * Define o componente que está gerando o log (ex: "aop", "http-client", "kafka-producer")
     */
    LogEventBuilder component(String component);
    
    /**
     * Define a classe que está sendo instrumentada
     */
    LogEventBuilder clazz(String className);
    
    /**
     * Define o método que está sendo instrumentado
     */
    LogEventBuilder method(String methodName);
    
    /**
     * Define os argumentos do método (após redação de PII)
     */
    LogEventBuilder args(Object args);
    
    /**
     * Define o valor de retorno do método (após redação de PII)
     */
    LogEventBuilder ret(Object returnValue);
    
    /**
     * Define a duração da execução em milissegundos
     */
    LogEventBuilder durationMs(long duration);
    
    /**
     * Define o tamanho da entrada em bytes
     */
    LogEventBuilder sizeIn(long sizeIn);
    
    /**
     * Define o tamanho da saída em bytes
     */
    LogEventBuilder sizeOut(long sizeOut);
    
    // Campos específicos para eventos de negócio
    
    /**
     * Define o tipo do evento de negócio (ex: "Rental", "Payment")
     */
    LogEventBuilder eventType(String eventType);
    
    /**
     * Define o nome do evento de negócio (ex: "ReservationCreated", "PaymentApproved")
     */
    LogEventBuilder eventName(String eventName);
    
    /**
     * Define a versão do schema do evento
     */
    LogEventBuilder eventVersion(int version);
    
    /**
     * Define o payload do evento de negócio
     */
    LogEventBuilder eventPayload(Object payload);
    
    // Campos específicos para HTTP
    
    /**
     * Define o método HTTP (GET, POST, etc.)
     */
    LogEventBuilder httpMethod(String method);
    
    /**
     * Define o path HTTP
     */
    LogEventBuilder httpPath(String path);
    
    /**
     * Define o status HTTP
     */
    LogEventBuilder httpStatus(int status);
    
    /**
     * Define o IP remoto
     */
    LogEventBuilder remoteIp(String remoteIp);
    
    // Campos específicos para Kafka
    
    /**
     * Define o tópico Kafka
     */
    LogEventBuilder topic(String topic);
    
    /**
     * Define a partição Kafka
     */
    LogEventBuilder partition(int partition);
    
    /**
     * Define o offset Kafka
     */
    LogEventBuilder offset(long offset);
    
    /**
     * Define a chave da mensagem Kafka
     */
    LogEventBuilder key(String key);
    
    // Campos específicos para banco de dados
    
    /**
     * Define o sistema de banco (mongodb, postgres, etc.)
     */
    LogEventBuilder dbSystem(String system);
    
    /**
     * Define a operação no banco (find, insert, update, etc.)
     */
    LogEventBuilder dbOperation(String operation);
    
    /**
     * Define a coleção/tabela
     */
    LogEventBuilder collection(String collection);
    
    // Campos de erro
    
    /**
     * Adiciona informações de erro/exceção
     */
    LogEventBuilder error(Throwable throwable);
    
    /**
     * Define o tipo de erro
     */
    LogEventBuilder errorKind(String kind);
    
    /**
     * Define a mensagem de erro
     */
    LogEventBuilder errorMessage(String message);
    
    /**
     * Define o stack trace do erro
     */
    LogEventBuilder errorStack(String stackTrace);
    
    // Campos de política
    
    /**
     * Define se o log foi amostrado
     */
    LogEventBuilder sampled(boolean sampled);
    
    /**
     * Define se o payload foi truncado
     */
    LogEventBuilder truncated(boolean truncated);
    
    /**
     * Define os campos que foram mascarados
     */
    LogEventBuilder redactedFields(String... fields);
}
