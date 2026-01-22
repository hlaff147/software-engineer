package com.openfinance.payments.adapter.input.filter;

import jakarta.servlet.*;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@Component
@Order(1)
public class JwtValidationFilter implements Filter {

    @Value("${app.jwt.secret}")
    private String jwtSecret;

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {

        HttpServletRequest httpRequest = (HttpServletRequest) request;
        HttpServletResponse httpResponse = (HttpServletResponse) response;

        String path = httpRequest.getRequestURI();

        // Skip filter for Swagger/OpenAPI endpoints
        if (path.contains("/swagger") || path.contains("/api-docs") || path.contains("/actuator")) {
            chain.doFilter(request, response);
            return;
        }

        String authorization = httpRequest.getHeader("Authorization");

        if (authorization == null || authorization.isBlank()) {
            log.warn("Missing Authorization header for path: {}", path);
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            httpResponse.setContentType("application/json");
            httpResponse.getWriter()
                    .write("""
                            {"errors":[{"code":"UNAUTHORIZED","title":"Não autorizado","detail":"Token de acesso não informado"}],"meta":{"requestDateTime":"%s"}}
                            """
                            .formatted(java.time.Instant.now().toString()));
            return;
        }

        // Simple JWT validation (mock - always accepts Bearer tokens)
        if (!authorization.startsWith("Bearer ")) {
            log.warn("Invalid Authorization format for path: {}", path);
            httpResponse.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            httpResponse.setContentType("application/json");
            httpResponse.getWriter()
                    .write("""
                            {"errors":[{"code":"INVALID_CLIENT","title":"Cliente inválido","detail":"Formato de token inválido"}],"meta":{"requestDateTime":"%s"}}
                            """
                            .formatted(java.time.Instant.now().toString()));
            return;
        }

        // Mock validation - in production, validate JWT signature, claims, etc.
        log.debug("[JWT MOCK] Token accepted for path: {}", path);

        chain.doFilter(request, response);
    }
}
