package com.hlaff.loggingx.jdbc;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import net.ttddyy.dsproxy.ExecutionInfo;
import net.ttddyy.dsproxy.QueryInfo;
import net.ttddyy.dsproxy.listener.QueryExecutionListener;

import java.util.List;

/**
 * Listener de execução de queries JDBC que gera logs estruturados
 * para statements SQL.
 */
@Slf4j
@RequiredArgsConstructor
public class LoggingQueryExecutionListener implements QueryExecutionListener {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    @Override
    public void beforeQuery(ExecutionInfo execInfo, List<QueryInfo> queryInfoList) {
        if (!properties.getJdbc().isLogStatements()) {
            return;
        }

        try {
            for (QueryInfo queryInfo : queryInfoList) {
                String sql = queryInfo.getQuery();
                structuredLogger.debug(event -> {
                    event.component("jdbc")
                         .dbSystem("sql")
                         .dbOperation(extractOperation(sql))
                         .put("db.statement", sql);

                    if (properties.getJdbc().isLogParameters()) {
                        event.put("db.parameters", queryInfo.getParametersList().toString());
                    }

                    event.sampled(true);
                });
            }
        } catch (Exception e) {
            log.debug("Erro ao logar início de query JDBC: {}", e.getMessage());
        }
    }

    @Override
    public void afterQuery(ExecutionInfo execInfo, List<QueryInfo> queryInfoList) {
        long duration = execInfo.getElapsedTime();

        if (properties.getJdbc().isSlowQueriesOnly() &&
            duration < properties.getJdbc().getSlowThresholdMs()) {
            return;
        }

        try {
            for (QueryInfo queryInfo : queryInfoList) {
                String sql = queryInfo.getQuery();
                if (execInfo.getThrowable() == null) {
                    structuredLogger.info(event -> {
                        event.component("jdbc")
                             .dbSystem("sql")
                             .dbOperation(extractOperation(sql))
                             .durationMs(duration)
                             .put("db.statement", sql);

                        if (properties.getJdbc().isLogParameters()) {
                            event.put("db.parameters", queryInfo.getParametersList().toString());
                        }

                        event.sampled(true);
                    });
                } else {
                    structuredLogger.error(event -> {
                        event.component("jdbc")
                             .dbSystem("sql")
                             .dbOperation(extractOperation(sql))
                             .durationMs(duration)
                             .put("db.statement", sql)
                             .errorKind(execInfo.getThrowable().getClass().getSimpleName())
                             .errorMessage(execInfo.getThrowable().getMessage());

                        if (properties.isIncludeStacktrace()) {
                            event.error(execInfo.getThrowable());
                        }

                        if (properties.getJdbc().isLogParameters()) {
                            event.put("db.parameters", queryInfo.getParametersList().toString());
                        }

                        event.sampled(true);
                    });
                }
            }
        } catch (Exception e) {
            log.debug("Erro ao logar execução de query JDBC: {}", e.getMessage());
        }
    }

    private String extractOperation(String sql) {
        if (sql == null) {
            return null;
        }
        String trimmed = sql.trim();
        int idx = trimmed.indexOf(' ');
        return idx > 0 ? trimmed.substring(0, idx).toLowerCase() : trimmed.toLowerCase();
    }
}

