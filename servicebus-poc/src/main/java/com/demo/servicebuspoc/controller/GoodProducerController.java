package com.demo.servicebuspoc.controller;

import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.concurrent.atomic.AtomicLong;

/**
 * ✅ BEST PRACTICE CONTROLLER ✅
 * 
 * Este controller demonstra a forma CORRETA de usar o Azure Service Bus SDK.
 * 
 * BENEFÍCIOS DESTA IMPLEMENTAÇÃO:
 * 1. Reutiliza a mesma conexão TCP/AMQP para todas as requests
 * 2. Handshake TLS realizado apenas uma vez (no startup)
 * 3. Buffers de memória reutilizados
 * 4. Threads gerenciadas eficientemente
 * 5. Baixo consumo de CPU e memória sob carga
 * 
 * O ServiceBusSenderClient é injetado como Singleton via Spring DI.
 */
@RestController
@RequestMapping("/api/v1")
public class GoodProducerController {

    private static final Logger logger = LoggerFactory.getLogger(GoodProducerController.class);

    // Contador para rastrear quantas mensagens foram enviadas
    private static final AtomicLong messageCounter = new AtomicLong(0);

    // ✅ CORRETO: Cliente injetado como Singleton
    private final ServiceBusSenderClient senderClient;

    /**
     * Injeção de dependência via construtor.
     * O Spring injeta o bean Singleton criado em ServiceBusConfig.
     */
    public GoodProducerController(ServiceBusSenderClient senderClient) {
        this.senderClient = senderClient;
        logger.info("✅ BEST PRACTICE: GoodProducerController inicializado com ServiceBusSenderClient Singleton");
    }

    /**
     * ✅ BEST PRACTICE: Reutiliza conexão existente!
     * 
     * Para cada requisição HTTP:
     * 1. Usa o ServiceBusSenderClient Singleton já existente
     * 2. A conexão TCP/AMQP já está estabelecida
     * 3. Apenas envia a mensagem (operação leve)
     * 
     * Sob carga (1000+ requests), isso resulta em:
     * - Baixo uso de CPU (sem handshakes repetidos)
     * - Baixa alocação de memória (buffers reutilizados)
     * - Número constante de threads
     * - Performance consistente e estável
     */
    @PostMapping("/good-producer")
    public ResponseEntity<String> sendGoodMessage(@RequestBody String message) {
        long messageId = messageCounter.incrementAndGet();
        long startTime = System.currentTimeMillis();
        
        logger.debug("✅ BEST PRACTICE: Enviando mensagem #{} via conexão Singleton", messageId);

        try {
            // ✅ CORRETO: Reutiliza o cliente existente
            senderClient.sendMessage(new ServiceBusMessage(message));

            long totalTime = System.currentTimeMillis() - startTime;
            logger.info("Mensagem #{} enviada com sucesso. Tempo: {}ms", messageId, totalTime);

            return ResponseEntity.ok(String.format(
                    "✓ Mensagem enviada (BEST PRACTICE). Mensagem #%d. Tempo: %dms. " +
                    "Total de mensagens enviadas: %d (mesma conexão)",
                    messageId, totalTime, messageCounter.get()
            ));

        } catch (Exception e) {
            logger.error("Erro ao enviar mensagem #{}: {}", messageId, e.getMessage());
            return ResponseEntity.internalServerError()
                    .body("Erro: " + e.getMessage());
        }
    }

    /**
     * Endpoint para resetar o contador de mensagens.
     */
    @PostMapping("/good-producer/reset-counter")
    public ResponseEntity<String> resetCounter() {
        long previousValue = messageCounter.getAndSet(0);
        logger.info("Contador de mensagens resetado. Valor anterior: {}", previousValue);
        return ResponseEntity.ok("Contador resetado. Valor anterior: " + previousValue);
    }

    /**
     * Endpoint para verificar status do cliente.
     */
    @PostMapping("/good-producer/status")
    public ResponseEntity<String> getStatus() {
        return ResponseEntity.ok(String.format(
                "Status: Cliente Singleton ativo. Mensagens enviadas: %d",
                messageCounter.get()
        ));
    }
}
