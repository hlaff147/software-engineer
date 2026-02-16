package com.hlaff.loggingx.http;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import com.hlaff.loggingx.spring.mdc.CorrelationFilter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.http.HttpRequest;
import org.springframework.http.client.ClientHttpRequestExecution;
import org.springframework.http.client.ClientHttpRequestInterceptor;
import org.springframework.http.client.ClientHttpResponse;
import org.springframework.lang.NonNull;

import java.io.IOException;
import java.net.URI;

/**
 * Interceptor para RestTemplate que adiciona correlationId nas requisições
 * e gera logs estruturados de saída HTTP.
 */
@Slf4j
@RequiredArgsConstructor
public class CorrelatingClientInterceptor implements ClientHttpRequestInterceptor {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    @Override
    @NonNull
    public ClientHttpResponse intercept(@NonNull HttpRequest request, 
                                      @NonNull byte[] body, 
                                      @NonNull ClientHttpRequestExecution execution) throws IOException {

        // Adiciona correlationId no header se disponível
        String correlationId = MDC.get(CorrelationFilter.MDC_CORRELATION_KEY);
        if (correlationId != null) {
            request.getHeaders().add(CorrelationFilter.CORRELATION_ID_HEADER, correlationId);
        }

        long startTime = System.nanoTime();
        URI uri = request.getURI();
        String method = request.getMethod().name();

        try {
            ClientHttpResponse response = execution.execute(request, body);
            long duration = (System.nanoTime() - startTime) / 1_000_000;

            // Log de sucesso
            if (properties.getHttp().getClient().isEnabled()) {
                logHttpClientSuccess(method, uri, body, response, duration);
            }

            return response;

        } catch (IOException e) {
            long duration = (System.nanoTime() - startTime) / 1_000_000;
            
            // Log de erro
            if (properties.getHttp().getClient().isEnabled()) {
                logHttpClientError(method, uri, body, duration, e);
            }

            throw e;
        }
    }

    private void logHttpClientSuccess(String method, URI uri, byte[] body, 
                                    ClientHttpResponse response, long duration) {
        try {
            int statusCode = response.getStatusCode().value();
            
            structuredLogger.info(event -> {
                event.component("http-client")
                     .httpMethod(method)
                     .httpPath(uri.getPath())
                     .httpStatus(statusCode)
                     .durationMs(duration)
                     .sizeOut(body != null ? body.length : 0);

                if (properties.getHttp().getClient().isLogBody() && body != null && body.length > 0) {
                    event.put("requestBody", new String(body));
                }

                if (properties.getHttp().getClient().isLogHeaders()) {
                    event.put("requestHeaders", response.getHeaders().toSingleValueMap());
                }

                event.put("url", uri.toString());
                event.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao obter status da resposta HTTP: {}", e.getMessage());
        }
    }

    private void logHttpClientError(String method, URI uri, byte[] body, 
                                  long duration, IOException error) {
        
        structuredLogger.error(event -> {
            event.component("http-client")
                 .httpMethod(method)
                 .httpPath(uri.getPath())
                 .durationMs(duration)
                 .sizeOut(body != null ? body.length : 0)
                 .error(error);

            if (properties.getHttp().getClient().isLogBody() && body != null && body.length > 0) {
                event.put("requestBody", new String(body));
            }

            event.put("url", uri.toString());
            event.sampled(true);
        });
    }
}
