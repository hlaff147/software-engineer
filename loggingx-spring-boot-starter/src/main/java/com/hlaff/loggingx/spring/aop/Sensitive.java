package com.hlaff.loggingx.spring.aop;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Anotação para marcar parâmetros ou campos como sensíveis.
 * Dados marcados com esta anotação serão mascarados nos logs.
 * 
 * Exemplo de uso:
 * <pre>
 * {@code
 * @Loggable
 * public class AuthService {
 *     
 *     public UserToken authenticate(String username, @Sensitive String password) {
 *         // password será mascarado como "***" nos logs
 *         // ...
 *     }
 *     
 *     public void processCreditCard(@Sensitive(maskWith = "####-####-####-XXXX") String cardNumber) {
 *         // cardNumber será mascarado com padrão customizado
 *         // ...
 *     }
 * }
 * }
 * </pre>
 */
@Target({ElementType.PARAMETER, ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface Sensitive {
    
    /**
     * Padrão usado para mascarar o valor sensível (padrão: "***").
     * Pode ser customizado para diferentes tipos de dados.
     */
    String maskWith() default "***";
    
    /**
     * Se deve mascarar completamente (true) ou parcialmente (false).
     * Mascaramento parcial pode manter prefixo/sufixo visível.
     */
    boolean fullMask() default true;
    
    /**
     * Número de caracteres visíveis no início (para mascaramento parcial).
     */
    int visiblePrefix() default 0;
    
    /**
     * Número de caracteres visíveis no final (para mascaramento parcial).
     */
    int visibleSuffix() default 0;
}
