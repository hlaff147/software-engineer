package com.demo.servicebuspoc;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Aplicação principal da PoC de Azure Service Bus.
 * 
 * Esta aplicação demonstra a diferença entre:
 * - Anti-pattern: Criar nova conexão a cada request (BadProducerController)
 * - Best Practice: Reutilizar conexão singleton (GoodProducerController)
 */
@SpringBootApplication
public class ServiceBusPocApplication {

    public static void main(String[] args) {
        SpringApplication.run(ServiceBusPocApplication.class, args);
    }

}
