package com.hlaff.loggingx.mongo;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import com.mongodb.event.CommandFailedEvent;
import com.mongodb.event.CommandListener;
import com.mongodb.event.CommandStartedEvent;
import com.mongodb.event.CommandSucceededEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.bson.BsonDocument;
import org.bson.BsonValue;

import java.util.concurrent.TimeUnit;

/**
 * Listener para comandos MongoDB que gera logs estruturados
 * de operações de banco de dados.
 */
@Slf4j
@RequiredArgsConstructor
public class LoggingMongoCommandListener implements CommandListener {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    @Override
    public void commandStarted(CommandStartedEvent event) {
        if (!properties.getMongo().isLogCommands()) {
            return;
        }

        try {
            structuredLogger.debug(logEvent -> {
                logEvent.component("mongo")
                        .dbSystem("mongodb")
                        .dbOperation(event.getCommandName())
                        .put("db.name", event.getDatabaseName())
                        .put("requestId", event.getRequestId());

                // Extrai coleção se disponível
                String collection = extractCollection(event.getCommand(), event.getCommandName());
                if (collection != null) {
                    logEvent.collection(collection);
                }

                logEvent.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar início de comando MongoDB: {}", e.getMessage());
        }
    }

    @Override
    public void commandSucceeded(CommandSucceededEvent event) {
        if (!properties.getMongo().isLogCommands()) {
            return;
        }

        long durationMs = event.getElapsedTime(TimeUnit.MILLISECONDS);

        // Verifica se deve logar apenas queries lentas
        if (properties.getMongo().isSlowQueriesOnly() && 
            durationMs < properties.getMongo().getSlowThresholdMs()) {
            return;
        }

        try {
            structuredLogger.info(logEvent -> {
                logEvent.component("mongo")
                        .dbSystem("mongodb")
                        .dbOperation(event.getCommandName())
                        .durationMs(durationMs)
                        .put("requestId", event.getRequestId());

                // Adiciona informações do resultado se habilitado
                if (properties.getMongo().isLogResults() && event.getResponse() != null) {
                    addResultInfo(logEvent, event.getResponse(), event.getCommandName());
                }

                logEvent.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar sucesso de comando MongoDB: {}", e.getMessage());
        }
    }

    @Override
    public void commandFailed(CommandFailedEvent event) {
        if (!properties.getMongo().isLogCommands()) {
            return;
        }

        long durationMs = event.getElapsedTime(TimeUnit.MILLISECONDS);

        try {
            structuredLogger.error(logEvent -> {
                logEvent.component("mongo")
                        .dbSystem("mongodb")
                        .dbOperation(event.getCommandName())
                        .durationMs(durationMs)
                        .put("requestId", event.getRequestId())
                        .errorKind("MongoCommandException")
                        .errorMessage(event.getThrowable().getMessage());

                if (properties.isIncludeStacktrace()) {
                    logEvent.error(event.getThrowable());
                }

                logEvent.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar falha de comando MongoDB: {}", e.getMessage());
        }
    }

    /**
     * Extrai o nome da coleção do comando MongoDB
     */
    private String extractCollection(BsonDocument command, String commandName) {
        try {
            // Para a maioria dos comandos, o nome da coleção é o valor do comando
            BsonValue collectionValue = command.get(commandName);
            if (collectionValue != null && collectionValue.isString()) {
                return collectionValue.asString().getValue();
            }

            // Para alguns comandos específicos
            switch (commandName.toLowerCase()) {
                case "find":
                case "insert":
                case "update": 
                case "delete":
                case "count":
                case "distinct":
                case "aggregate":
                case "findandmodify":
                    BsonValue value = command.get(commandName);
                    if (value != null && value.isString()) {
                        return value.asString().getValue();
                    }
                    break;
                
                case "create":
                case "drop":
                    BsonValue createValue = command.get("create");
                    if (createValue != null && createValue.isString()) {
                        return createValue.asString().getValue();
                    }
                    break;
            }

        } catch (Exception e) {
            log.trace("Erro ao extrair coleção do comando MongoDB: {}", e.getMessage());
        }

        return null;
    }

    /**
     * Adiciona informações do resultado da operação ao log
     */
    private void addResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, 
                              BsonDocument response, String commandName) {
        try {
            // Informações comuns
            BsonValue ok = response.get("ok");
            if (ok != null) {
                logEvent.put("db.result.ok", ok.asNumber().intValue());
            }

            // Informações específicas por tipo de comando
            switch (commandName.toLowerCase()) {
                case "find":
                    addFindResultInfo(logEvent, response);
                    break;
                case "insert":
                    addInsertResultInfo(logEvent, response);
                    break;
                case "update":
                    addUpdateResultInfo(logEvent, response);
                    break;
                case "delete":
                    addDeleteResultInfo(logEvent, response);
                    break;
                case "count":
                    addCountResultInfo(logEvent, response);
                    break;
            }

        } catch (Exception e) {
            log.trace("Erro ao adicionar informações de resultado: {}", e.getMessage());
        }
    }

    private void addFindResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, BsonDocument response) {
        BsonValue cursor = response.get("cursor");
        if (cursor != null && cursor.isDocument()) {
            BsonDocument cursorDoc = cursor.asDocument();
            BsonValue firstBatch = cursorDoc.get("firstBatch");
            if (firstBatch != null && firstBatch.isArray()) {
                logEvent.put("db.result.docsReturned", firstBatch.asArray().size());
            }
        }
    }

    private void addInsertResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, BsonDocument response) {
        BsonValue n = response.get("n");
        if (n != null) {
            logEvent.put("db.result.docsInserted", n.asNumber().intValue());
        }
    }

    private void addUpdateResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, BsonDocument response) {
        BsonValue nMatched = response.get("nMatched");
        if (nMatched != null) {
            logEvent.put("db.result.docsMatched", nMatched.asNumber().intValue());
        }
        
        BsonValue nModified = response.get("nModified");
        if (nModified != null) {
            logEvent.put("db.result.docsModified", nModified.asNumber().intValue());
        }
    }

    private void addDeleteResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, BsonDocument response) {
        BsonValue n = response.get("n");
        if (n != null) {
            logEvent.put("db.result.docsDeleted", n.asNumber().intValue());
        }
    }

    private void addCountResultInfo(com.hlaff.loggingx.core.logger.LogEventBuilder logEvent, BsonDocument response) {
        BsonValue n = response.get("n");
        if (n != null) {
            logEvent.put("db.result.count", n.asNumber().longValue());
        }
    }
}
