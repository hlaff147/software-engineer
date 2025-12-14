package com.demo.servicebuspoc.controller;

import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusMessage;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.atomic.AtomicLong;

/**
 * ☠️ ANTI-PATTERN EXTREMO - RESOURCE LEAK ☠️
 * 
 * Este controller demonstra o PIOR cenário possível em produção!
 * 
 * PROBLEMAS CRÍTICOS DESTA IMPLEMENTAÇÃO:
 * 1. Cria nova conexão TCP/AMQP a cada request
 * 2. ⚠️ NUNCA FECHA AS CONEXÕES - VAZAMENTO DE RECURSOS!
 * 3. Acumula conexões abertas na memória indefinidamente
 * 4. Causa esgotamento de:
 *    - File descriptors (sockets TCP)
 *    - Memória heap (buffers do Netty)
 *    - Threads do sistema
 *    - Portas efêmeras TCP
 * 
 * Este código VAI derrubar sua aplicação sob carga!
 * Use APENAS para demonstração do problema!
 */
@RestController
@RequestMapping("/api/v1")
public class BadProducerController {

    private static final Logger logger = LoggerFactory.getLogger(BadProducerController.class);
    
    // Contador para rastrear quantas conexões foram criadas
    private static final AtomicLong connectionCounter = new AtomicLong(0);
    
    // ☠️ VAZAMENTO INTENCIONAL: Lista que acumula TODAS as conexões abertas
    // Isso simula o que acontece quando você esquece de fechar recursos
    private static final List<ServiceBusSenderClient> leakedConnections = 
            Collections.synchronizedList(new ArrayList<>());

    @Value("${azure.servicebus.connection-string}")
    private String connectionString;

    @Value("${azure.servicebus.queue-name}")
    private String queueName;

    /**
     * ☠️ ANTI-PATTERN EXTREMO: Cria conexão e NUNCA fecha!
     * 
     * Para cada requisição HTTP:
     * 1. Instancia um novo ServiceBusClientBuilder
     * 2. Cria uma nova conexão TCP com o Service Bus
     * 3. Realiza handshake TLS/AMQP (muito custoso!)
     * 4. Envia a mensagem
     * 5. ⚠️ NÃO FECHA A CONEXÃO - ela fica pendurada para sempre!
     * 
     * Sob carga (100-500 requests), isso RAPIDAMENTE causa:
     * - OutOfMemoryError (heap exhaustion)
     * - Too many open files (file descriptor exhaustion)
     * - Thread explosion
     * - Timeout em novas conexões
     */
    @PostMapping("/bad-producer")
    public ResponseEntity<String> sendBadMessage(@RequestBody String message) {
        long connectionId = connectionCounter.incrementAndGet();
        long startTime = System.currentTimeMillis();
        
        logger.error("☠️ RESOURCE LEAK: Criando conexão #{} que NUNCA será fechada!", connectionId);

        try {
            // ❌ CRIANDO CONEXÃO QUE NUNCA SERÁ FECHADA
            ServiceBusSenderClient sender = new ServiceBusClientBuilder()
                    .connectionString(connectionString)
                    .sender()
                    .queueName(queueName)
                    .buildClient();

            long connectionTime = System.currentTimeMillis() - startTime;
            logger.warn("Conexão #{} estabelecida em {}ms - VAZANDO RECURSOS!", connectionId, connectionTime);

            // ☠️ ADICIONANDO À LISTA DE VAZAMENTOS
            // Isso impede que o garbage collector libere a conexão
            leakedConnections.add(sender);

            // Envia a mensagem
            sender.sendMessage(new ServiceBusMessage(message));

            long totalTime = System.currentTimeMillis() - startTime;
            
            // Estima memória vazada (aproximadamente 1-2MB por conexão)
            long estimatedLeakMB = leakedConnections.size() * 2;
            
            logger.error("☠️ Mensagem enviada. Conexões VAZADAS: {}. Memória estimada vazada: ~{}MB", 
                    leakedConnections.size(), estimatedLeakMB);

            return ResponseEntity.ok(String.format(
                    "☠️ RESOURCE LEAK! Conexão #%d criada e NÃO FECHADA. " +
                    "Tempo: %dms. Conexões vazadas: %d. ~%dMB vazados.",
                    connectionId, totalTime, leakedConnections.size(), estimatedLeakMB
            ));

        } catch (Exception e) {
            logger.error("💀 ERRO (provavelmente resources exhausted) na conexão #{}: {}", 
                    connectionId, e.getMessage());
            return ResponseEntity.internalServerError()
                    .body(String.format("💀 ERRO: %s. Conexões vazadas até agora: %d", 
                            e.getMessage(), leakedConnections.size()));
        }
        // ⚠️ NOTA: NÃO HÁ FINALLY BLOCK - NENHUM CLEANUP!
    }

    /**
     * Endpoint para ver estatísticas de vazamentos.
     */
    @GetMapping("/bad-producer/stats")
    public ResponseEntity<String> getLeakStats() {
        long leakCount = leakedConnections.size();
        long estimatedMemoryMB = leakCount * 2; // ~2MB por conexão
        
        Runtime runtime = Runtime.getRuntime();
        long usedMemoryMB = (runtime.totalMemory() - runtime.freeMemory()) / (1024 * 1024);
        long maxMemoryMB = runtime.maxMemory() / (1024 * 1024);
        
        String stats = String.format(
                "☠️ ESTATÍSTICAS DE VAZAMENTO:\n" +
                "- Conexões vazadas: %d\n" +
                "- Memória estimada vazada: ~%dMB\n" +
                "- Memória JVM em uso: %dMB / %dMB\n" +
                "- Threads ativas: %d",
                leakCount, estimatedMemoryMB, usedMemoryMB, maxMemoryMB,
                Thread.activeCount()
        );
        
        logger.warn(stats);
        return ResponseEntity.ok(stats);
    }

    /**
     * Endpoint para resetar e FECHAR todas as conexões vazadas.
     * Use para limpar o estado entre testes.
     */
    @PostMapping("/bad-producer/cleanup")
    public ResponseEntity<String> cleanupLeaks() {
        int leakCount = leakedConnections.size();
        logger.info("🧹 Limpando {} conexões vazadas...", leakCount);
        
        int closed = 0;
        int errors = 0;
        
        for (ServiceBusSenderClient sender : leakedConnections) {
            try {
                sender.close();
                closed++;
            } catch (Exception e) {
                errors++;
                logger.warn("Erro ao fechar conexão: {}", e.getMessage());
            }
        }
        
        leakedConnections.clear();
        connectionCounter.set(0);
        
        // Sugere GC para liberar memória
        System.gc();
        
        return ResponseEntity.ok(String.format(
                "🧹 Limpeza concluída. Fechadas: %d. Erros: %d. " +
                "Execute novamente para ver a memória liberada.",
                closed, errors
        ));
    }
}
