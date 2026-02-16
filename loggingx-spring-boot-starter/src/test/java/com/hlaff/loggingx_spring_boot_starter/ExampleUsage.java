package com.hlaff.loggingx_spring_boot_starter;

import com.hlaff.loggingx.spring.aop.BusinessEvent;
import com.hlaff.loggingx.spring.aop.Loggable;
import com.hlaff.loggingx.spring.aop.Sensitive;
import lombok.Builder;
import lombok.Data;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.Instant;

/**
 * Exemplo de uso do LoggingX mostrando as principais funcionalidades
 */
public class ExampleUsage {

    @Loggable
    @Service
    public static class PaymentService {
        
        /**
         * Método com logging automático de entrada/saída
         */
        public PaymentResult processPayment(String customerId, BigDecimal amount) {
            // Simula processamento
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            
            return PaymentResult.builder()
                .id("PAY-" + System.currentTimeMillis())
                .customerId(customerId)
                .amount(amount)
                .status("APPROVED")
                .build();
        }
        
        /**
         * Método que não loga argumentos sensíveis
         */
        @Loggable(logArgs = false)
        public boolean validateCard(@Sensitive String cardNumber, @Sensitive String cvv) {
            // cardNumber e cvv serão mascarados nos logs
            return cardNumber != null && cvv != null && cvv.length() == 3;
        }
        
        /**
         * Método que emite evento de negócio
         */
        @BusinessEvent(type = "Payment", name = "PaymentApproved", version = 1)
        public PaymentApprovedEvent approvePayment(String paymentId, BigDecimal amount) {
            return PaymentApprovedEvent.builder()
                .paymentId(paymentId)
                .amount(amount)
                .approvedAt(Instant.now())
                .approver("SYSTEM")
                .build();
        }
    }

    @Data
    @Builder
    public static class PaymentResult {
        private String id;
        private String customerId;
        private BigDecimal amount;
        private String status;
    }

    @Data
    @Builder
    public static class PaymentApprovedEvent {
        private String paymentId;
        private BigDecimal amount;
        private Instant approvedAt;
        private String approver;
    }
}
