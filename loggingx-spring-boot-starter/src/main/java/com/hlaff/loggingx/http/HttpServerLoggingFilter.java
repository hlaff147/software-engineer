package com.hlaff.loggingx.http;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.annotation.Order;
import org.springframework.lang.NonNull;
import org.springframework.web.filter.OncePerRequestFilter;
import org.springframework.web.util.ContentCachingRequestWrapper;
import org.springframework.web.util.ContentCachingResponseWrapper;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Enumeration;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Filtro para logging de requisições HTTP recebidas pelo servidor.
 * Gera logs estruturados com informações de entrada e saída HTTP.
 */
@Slf4j
@RequiredArgsConstructor
@Order(100) // Executa após CorrelationFilter
public class HttpServerLoggingFilter extends OncePerRequestFilter {

    private final StructuredLogger structuredLogger;
    private final LoggingXProperties properties;

    @Override
    protected void doFilterInternal(@NonNull HttpServletRequest request,
                                  @NonNull HttpServletResponse response,
                                  @NonNull FilterChain filterChain) throws ServletException, IOException {

        if (!properties.getHttp().getServer().isEnabled()) {
            filterChain.doFilter(request, response);
            return;
        }

        // Wrappa request e response para capturar conteúdo
        ContentCachingRequestWrapper wrappedRequest = new ContentCachingRequestWrapper(request);
        ContentCachingResponseWrapper wrappedResponse = new ContentCachingResponseWrapper(response);

        long startTime = System.nanoTime();

        try {
            filterChain.doFilter(wrappedRequest, wrappedResponse);
            
            long duration = (System.nanoTime() - startTime) / 1_000_000;
            logHttpRequest(wrappedRequest, wrappedResponse, duration, null);

        } catch (Exception e) {
            long duration = (System.nanoTime() - startTime) / 1_000_000;
            logHttpRequest(wrappedRequest, wrappedResponse, duration, e);
            throw e;
        } finally {
            // Importante: copia o conteúdo de volta para a resposta
            wrappedResponse.copyBodyToResponse();
        }
    }

    private void logHttpRequest(ContentCachingRequestWrapper request,
                              ContentCachingResponseWrapper response,
                              long duration,
                              Exception error) {

        if (error != null) {
            structuredLogger.error(event -> buildHttpEvent(event, request, response, duration, error));
        } else {
            structuredLogger.info(event -> buildHttpEvent(event, request, response, duration, null));
        }
    }

    private void buildHttpEvent(com.hlaff.loggingx.core.logger.LogEventBuilder event,
                               ContentCachingRequestWrapper request,
                               ContentCachingResponseWrapper response,
                               long duration,
                               Exception error) {

        event.component("http-server")
             .httpMethod(request.getMethod())
             .httpPath(request.getRequestURI())
             .httpStatus(response.getStatus())
             .durationMs(duration)
             .sizeIn(request.getContentAsByteArray().length)
             .sizeOut(response.getContentAsByteArray().length);

        // Adiciona IP remoto
        String remoteIp = getClientIpAddress(request);
        if (remoteIp != null) {
            event.remoteIp(remoteIp);
        }

        // Adiciona query string se presente
        if (request.getQueryString() != null) {
            event.put("queryString", request.getQueryString());
        }

        // Adiciona corpo da requisição se habilitado
        if (properties.getHttp().getServer().isLogBody()) {
            String requestBody = getRequestBody(request);
            if (requestBody != null && !requestBody.isEmpty()) {
                event.put("requestBody", requestBody);
            }

            String responseBody = getResponseBody(response);
            if (responseBody != null && !responseBody.isEmpty()) {
                event.put("responseBody", responseBody);
            }
        }

        // Adiciona headers se habilitado
        if (properties.getHttp().getServer().isLogHeaders()) {
            event.put("requestHeaders", getRequestHeaders(request));
            event.put("responseHeaders", getResponseHeaders(response));
        }

        // Adiciona erro se presente
        if (error != null) {
            event.error(error);
        }

        event.sampled(true);
    }

    private String getClientIpAddress(HttpServletRequest request) {
        String[] headerNames = {
            "X-Forwarded-For",
            "X-Real-IP", 
            "Proxy-Client-IP",
            "WL-Proxy-Client-IP",
            "HTTP_X_FORWARDED_FOR",
            "HTTP_X_FORWARDED",
            "HTTP_X_CLUSTER_CLIENT_IP",
            "HTTP_CLIENT_IP",
            "HTTP_FORWARDED_FOR",
            "HTTP_FORWARDED",
            "HTTP_VIA",
            "REMOTE_ADDR"
        };

        for (String headerName : headerNames) {
            String ip = request.getHeader(headerName);
            if (ip != null && !ip.isEmpty() && !"unknown".equalsIgnoreCase(ip)) {
                // Pega o primeiro IP se houver múltiplos (separados por vírgula)
                return ip.split(",")[0].trim();
            }
        }

        return request.getRemoteAddr();
    }

    private String getRequestBody(ContentCachingRequestWrapper request) {
        byte[] content = request.getContentAsByteArray();
        if (content.length > 0) {
            return new String(content, StandardCharsets.UTF_8);
        }
        return null;
    }

    private String getResponseBody(ContentCachingResponseWrapper response) {
        byte[] content = response.getContentAsByteArray();
        if (content.length > 0) {
            return new String(content, StandardCharsets.UTF_8);
        }
        return null;
    }

    private Map<String, String> getRequestHeaders(HttpServletRequest request) {
        Map<String, String> headers = new LinkedHashMap<>();
        Enumeration<String> headerNames = request.getHeaderNames();
        
        while (headerNames.hasMoreElements()) {
            String headerName = headerNames.nextElement();
            headers.put(headerName, request.getHeader(headerName));
        }
        
        return headers;
    }

    private Map<String, String> getResponseHeaders(HttpServletResponse response) {
        Map<String, String> headers = new LinkedHashMap<>();
        
        for (String headerName : response.getHeaderNames()) {
            headers.put(headerName, response.getHeader(headerName));
        }
        
        return headers;
    }
}
