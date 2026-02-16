package com.hlaff.loggingx.spring.aop;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Anotação para marcar métodos que devem emitir eventos de negócio.
 * Eventos de negócio são logs estruturados que representam fatos relevantes ao domínio.
 * 
 * Exemplo de uso:
 * <pre>
 * {@code
 * @Service
 * public class ReservationService {
 *     
 *     @BusinessEvent(type = "Rental", name = "ReservationCreated", version = 1)
 *     public ReservationResult createReservation(ReservationRequest request) {
 *         // ... lógica de negócio
 *         return result; // será usado como payload do evento
 *     }
 *     
 *     @BusinessEvent(type = "Payment", name = "PaymentApproved", version = 2)
 *     public PaymentApprovalEvent approvePayment(PaymentRequest request) {
 *         // ... 
 *         return approvalEvent;
 *     }
 * }
 * }
 * </pre>
 */
@Target({ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface BusinessEvent {
    
    /**
     * Tipo/categoria do evento de negócio (ex: "Rental", "Payment", "User").
     * Usado para agrupar eventos relacionados.
     */
    String type();
    
    /**
     * Nome específico do evento (ex: "ReservationCreated", "PaymentApproved").
     * Deve ser específico e descritivo da ação realizada.
     */
    String name();
    
    /**
     * Versão do schema do evento (padrão: 1).
     * Incrementar quando houver mudanças na estrutura do payload.
     */
    int version() default 1;
    
    /**
     * Se deve usar o valor de retorno do método como payload (padrão: true).
     * Quando false, o payload pode ser definido programaticamente.
     */
    boolean useReturnAsPayload() default true;
    
    /**
     * Nível de log para o evento de negócio (padrão: INFO).
     */
    LogLevel level() default LogLevel.INFO;
    
    /**
     * Se deve aplicar redação de PII no payload (padrão: true).
     */
    boolean redactPayload() default true;
}
