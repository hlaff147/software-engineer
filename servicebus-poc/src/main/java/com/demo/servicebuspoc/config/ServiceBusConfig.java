package com.demo.servicebuspoc.config;

import com.azure.messaging.servicebus.ServiceBusClientBuilder;
import com.azure.messaging.servicebus.ServiceBusSenderClient;
import jakarta.annotation.PreDestroy;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Configuração do Azure Service Bus seguindo as BEST PRACTICES.
 * 
 * O ServiceBusSenderClient é criado uma única vez (Singleton) e reutilizado
 * por toda a aplicação. Isso evita:
 * - Overhead de handshake TLS/AMQP repetido
 * - Criação excessiva de threads
 * - Consumo desnecessário de CPU e memória
 */
@Configuration
public class ServiceBusConfig {

    private static final Logger logger = LoggerFactory.getLogger(ServiceBusConfig.class);

    @Value("${azure.servicebus.connection-string}")
    private String connectionString;

    @Value("${azure.servicebus.queue-name}")
    private String queueName;

    private ServiceBusSenderClient senderClient;

    /**
     * Cria um Bean Singleton do ServiceBusSenderClient.
     * 
     * Esta é a forma CORRETA de gerenciar o ciclo de vida do cliente:
     * - Instanciado uma única vez no startup da aplicação
     * - Reutilizado por todas as requisições
     * - Fechado graciosamente no shutdown
     */
    @Bean
    public ServiceBusSenderClient serviceBusSenderClient() {
        logger.info("=== BEST PRACTICE: Criando ServiceBusSenderClient Singleton ===");
        logger.info("Connection String: {}...", connectionString.substring(0, Math.min(50, connectionString.length())));
        logger.info("Queue Name: {}", queueName);

        this.senderClient = new ServiceBusClientBuilder()
                .connectionString(connectionString)
                .sender()
                .queueName(queueName)
                .buildClient();

        logger.info("ServiceBusSenderClient criado com sucesso! Este cliente será reutilizado.");
        return senderClient;
    }

    /**
     * Fecha o cliente graciosamente no shutdown da aplicação.
     */
    @PreDestroy
    public void cleanup() {
        if (senderClient != null) {
            logger.info("Fechando ServiceBusSenderClient no shutdown...");
            senderClient.close();
            logger.info("ServiceBusSenderClient fechado com sucesso.");
        }
    }
}
