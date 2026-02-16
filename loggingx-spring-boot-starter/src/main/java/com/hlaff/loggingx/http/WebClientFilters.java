package com.hlaff.loggingx.http;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import com.hlaff.loggingx.spring.mdc.CorrelationFilter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.ExchangeFilterFunction;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.time.Instant;

/**
 * Filtros para WebClient (WebFlux) que adicionam correlationId nas requisições
 * e geram logs estruturados de saída HTTP reativa.
 */
@Slf4j
@RequiredArgsConstructor
public class WebClientFilters {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    /**
     * Filtro para adicionar correlationId e logging em WebClient
     */
    public ExchangeFilterFunction correlationAndLogging() {
        return ExchangeFilterFunction.ofRequestProcessor(this::addCorrelationId)
                .andThen(ExchangeFilterFunction.ofResponseProcessor(this::logResponse));
    }

    /**
     * Filtro apenas para correlationId (sem logging)
     */
    public ExchangeFilterFunction correlationOnly() {
        return ExchangeFilterFunction.ofRequestProcessor(this::addCorrelationId);
    }

    /**
     * Filtro apenas para logging (sem modificar headers)
     */
    public ExchangeFilterFunction loggingOnly() {
        return ExchangeFilterFunction.ofResponseProcessor(this::logResponse);
    }

    private Mono<ClientRequest> addCorrelationId(ClientRequest request) {
        String correlationId = MDC.get(CorrelationFilter.MDC_CORRELATION_KEY);
        
        ClientRequest.Builder builder = ClientRequest.from(request);
        
        if (correlationId != null) {
            builder.headers(headers -> headers.add(CorrelationFilter.CORRELATION_ID_HEADER, correlationId));
        }
        
        return Mono.just(builder.build())
                .doOnNext(req -> req.attribute("startTime").orElse(Instant.now()));
    }

    private Mono<ClientResponse> logResponse(ClientResponse response) {
        if (!properties.getHttp().getClient().isEnabled()) {
            return Mono.just(response);
        }

        return response.toEntity(String.class)
                .map(entity -> {
                    logHttpResponse(response, entity.getBody());
                    return response;
                })
                .onErrorResume(throwable -> {
                    logHttpError(response, throwable);
                    return Mono.just(response);
                });
    }

    private void logHttpResponse(ClientResponse response, String responseBody) {
        try {
            // Para simplificar, vamos calcular a duração usando timestamp atual
            // Em implementação mais avançada, poderia usar Context do Reactor
            long duration = 0; // Placeholder - em produção seria calculado corretamente

            structuredLogger.info(event -> {
                event.component("http-client-reactive")
                     .httpMethod(response.request().getMethod().name())
                     .httpPath(response.request().getURI().getPath())
                     .httpStatus(response.statusCode().value())
                     .durationMs(duration);

                if (properties.getHttp().getClient().isLogBody() && responseBody != null) {
                    event.put("responseBody", responseBody);
                }

                if (properties.getHttp().getClient().isLogHeaders()) {
                    event.put("responseHeaders", response.headers().asHttpHeaders().toSingleValueMap());
                }

                event.put("url", response.request().getURI().toString());
                event.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar resposta HTTP reativa: {}", e.getMessage());
        }
    }

    private void logHttpError(ClientResponse response, Throwable error) {
        try {
            // Para simplificar, vamos calcular a duração usando timestamp atual
            // Em implementação mais avançada, poderia usar Context do Reactor
            long duration = 0; // Placeholder - em produção seria calculado corretamente

            structuredLogger.error(event -> {
                event.component("http-client-reactive")
                     .httpMethod(response.request().getMethod().name())
                     .httpPath(response.request().getURI().getPath())
                     .httpStatus(response.statusCode().value())
                     .durationMs(duration)
                     .error((Throwable) error);

                if (properties.getHttp().getClient().isLogHeaders()) {
                    event.put("responseHeaders", response.headers().asHttpHeaders().toSingleValueMap());
                }

                event.put("url", response.request().getURI().toString());
                event.sampled(true);
            });

        } catch (Exception e) {
            log.debug("Erro ao logar erro HTTP reativo: {}", e.getMessage());
        }
    }
}
