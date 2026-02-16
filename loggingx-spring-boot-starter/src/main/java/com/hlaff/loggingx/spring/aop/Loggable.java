package com.hlaff.loggingx.spring.aop;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Anotação para habilitar logging automático de entrada/saída de métodos.
 * Pode ser aplicada em classes (para todos os métodos) ou métodos específicos.
 * 
 * Exemplo de uso:
 * <pre>
 * {@code
 * @Loggable
 * @Service
 * public class PaymentService {
 *     
 *     @Loggable(logArgs = false) // não loga argumentos por segurança
 *     public PaymentResult processPayment(String cardToken, BigDecimal amount) {
 *         // ...
 *     }
 * }
 * }
 * </pre>
 */
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Loggable {
    
    /**
     * Nível de log para emissão dos eventos (padrão: INFO).
     */
    LogLevel level() default LogLevel.INFO;
    
    /**
     * Se deve logar argumentos do método (padrão: true).
     * Útil desabilitar para métodos com dados sensíveis.
     */
    boolean logArgs() default true;
    
    /**
     * Se deve logar valor de retorno do método (padrão: true).
     * Útil desabilitar para métodos que retornam dados sensíveis.
     */
    boolean logReturn() default true;
    
    /**
     * Tamanho máximo do payload antes do truncamento (padrão: 4096).
     * Ajuda a controlar o volume de logs em produção.
     */
    int maxPayloadLength() default 4096;
    
    /**
     * Se deve incluir duração da execução no log (padrão: true).
     */
    boolean includeDuration() default true;
    
    /**
     * Se deve aplicar sampling a este método/classe (padrão: true).
     * Quando false, sempre loga independente da configuração de sampling.
     */
    boolean respectSampling() default true;
}
