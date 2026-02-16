package com.hlaff.loggingx.spring.mdc;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.lang.NonNull;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.Optional;
import java.util.UUID;

/**
 * Filtro responsável por gerenciar correlationId nas requisições HTTP.
 * Extrai o correlationId do header X-Correlation-Id ou gera um novo UUID.
 * Propaga o correlationId através do MDC e adiciona na resposta.
 */
@Slf4j
@Order(Ordered.HIGHEST_PRECEDENCE)
public class CorrelationFilter extends OncePerRequestFilter {

    public static final String CORRELATION_ID_HEADER = "X-Correlation-Id";
    public static final String MDC_CORRELATION_KEY = "correlationId";

    @Override
    protected void doFilterInternal(@NonNull HttpServletRequest request, 
                                  @NonNull HttpServletResponse response, 
                                  @NonNull FilterChain filterChain) throws ServletException, IOException {

        String correlationId = extractOrGenerateCorrelationId(request);
        
        // Adiciona correlationId no MDC para propagação automática nos logs
        MDC.put(MDC_CORRELATION_KEY, correlationId);
        
        try {
            // Adiciona correlationId na resposta para cliente poder rastrear
            response.setHeader(CORRELATION_ID_HEADER, correlationId);
            
            filterChain.doFilter(request, response);
            
        } finally {
            // Remove do MDC para evitar vazamentos entre requisições
            MDC.remove(MDC_CORRELATION_KEY);
        }
    }

    /**
     * Extrai correlationId do header da requisição ou gera um novo.
     */
    private String extractOrGenerateCorrelationId(HttpServletRequest request) {
        return Optional.ofNullable(request.getHeader(CORRELATION_ID_HEADER))
                .filter(id -> !id.trim().isEmpty())
                .orElseGet(() -> {
                    String newId = generateCorrelationId();
                    log.debug("Gerado novo correlationId: {}", newId);
                    return newId;
                });
    }

    /**
     * Gera um novo correlation ID único.
     */
    protected String generateCorrelationId() {
        return UUID.randomUUID().toString();
    }
}
