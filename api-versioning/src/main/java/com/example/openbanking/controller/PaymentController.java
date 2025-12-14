package com.example.openbanking.controller;

import com.example.openbanking.dto.v1.PaymentRequestV1;
import com.example.openbanking.dto.v2.PaymentRequestV2;
import com.example.openbanking.strategy.PaymentServiceFactory;
import com.example.openbanking.strategy.PaymentStrategy;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * Controller principal da API de Pagamentos.
 * 
 * Atua como ponto de entrada único para todas as versões.
 * A lógica de negócio é delegada para as implementações de PaymentStrategy.
 */
@RestController
@RequestMapping("/openbanking/payment")
public class PaymentController {

    private static final Logger log = LoggerFactory.getLogger(PaymentController.class);
    
    private final PaymentServiceFactory factory;
    private final ObjectMapper mapper;

    public PaymentController(PaymentServiceFactory factory, ObjectMapper mapper) {
        this.factory = factory;
        this.mapper = mapper;
    }

    /**
     * Cria um pagamento na versão especificada.
     * 
     * @param version Versão da API (ex: "1_0_0", "2_0_0")
     * @param rawPayload JSON do request (flexível para qualquer versão)
     */
    @PostMapping("/{version}")
    public ResponseEntity<?> createPayment(
            @PathVariable String version,
            @RequestBody JsonNode rawPayload) {

        log.info("Recebida requisição POST para versão: {}", version);
        
        // 1. Obter a estratégia correta
        PaymentStrategy strategy = factory.getStrategy(version);

        // 2. Converter JSON para DTO específico da versão
        Object dto = convertPayload(rawPayload, version);

        // 3. Executar lógica de negócio
        Object response = strategy.createPayment(dto);

        return ResponseEntity.ok(response);
    }

    /**
     * Recupera detalhes de um pagamento.
     */
    @GetMapping("/{version}/{id}")
    public ResponseEntity<?> getPayment(
            @PathVariable String version,
            @PathVariable String id) {
        
        log.info("Recebida requisição GET para versão: {}, id: {}", version, id);
        
        PaymentStrategy strategy = factory.getStrategy(version);
        Object response = strategy.getPayment(id);
        
        return ResponseEntity.ok(response);
    }
    
    /**
     * Endpoint de informação: lista versões suportadas.
     */
    @GetMapping("/versions")
    public ResponseEntity<?> listVersions() {
        return ResponseEntity.ok(factory.getAvailableVersions());
    }

    /**
     * Converte o JSON bruto para o DTO específico da versão.
     */
    private Object convertPayload(JsonNode json, String version) {
        return switch (version) {
            case "1_0_0" -> mapper.convertValue(json, PaymentRequestV1.class);
            case "2_0_0" -> mapper.convertValue(json, PaymentRequestV2.class);
            default -> throw new IllegalArgumentException(
                "DTO não definido para versão: " + version
            );
        };
    }
}
