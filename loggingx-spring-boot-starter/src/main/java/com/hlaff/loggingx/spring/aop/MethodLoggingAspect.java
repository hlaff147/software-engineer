package com.hlaff.loggingx.spring.aop;

import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.core.redact.Redactor;
import com.hlaff.loggingx.spring.config.LoggingXProperties;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.core.annotation.AnnotationUtils;

import java.lang.reflect.Method;
import java.util.Map;

/**
 * Aspecto responsável por interceptar métodos anotados com @Loggable
 * e gerar logs estruturados de entrada/saída com duração e tratamento de erros.
 */
@Aspect
@Slf4j
@RequiredArgsConstructor
public class MethodLoggingAspect {

    private final StructuredLogger structuredLogger;
    private final Redactor redactor;
    private final LoggingXProperties properties;

    /**
     * Pointcut para métodos anotados com @Loggable
     */
    @Pointcut("@annotation(com.hlaff.loggingx.spring.aop.Loggable)")
    public void loggableMethod() {}

    /**
     * Pointcut para classes anotadas com @Loggable
     */
    @Pointcut("within(@com.hlaff.loggingx.spring.aop.Loggable *)")
    public void loggableClass() {}

    /**
     * Advice principal que intercepta execução de métodos
     */
    @Around("loggableMethod() || loggableClass()")
    public Object aroundLoggable(ProceedingJoinPoint joinPoint) throws Throwable {
        if (!properties.isEnabled()) {
            return joinPoint.proceed();
        }

        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
        Method method = signature.getMethod();
        Class<?> declaringClass = method.getDeclaringClass();

        // Busca anotação @Loggable no método ou na classe
        Loggable loggableAnnotation = findLoggableAnnotation(method, declaringClass);
        
        if (loggableAnnotation == null) {
            return joinPoint.proceed();
        }

        long startTime = System.nanoTime();
        String className = declaringClass.getSimpleName();
        String methodName = method.getName();

        // Processa argumentos se habilitado
        Map<String, Object> processedArgs = Map.of();
        if (loggableAnnotation.logArgs()) {
            processedArgs = redactor.redactArgs(
                signature.getParameterNames(),
                joinPoint.getArgs(),
                loggableAnnotation.maxPayloadLength()
            );
        }

        try {
            // Executa o método original
            Object result = joinPoint.proceed();
            
            // Calcula duração se habilitado
            Long duration = null;
            if (loggableAnnotation.includeDuration()) {
                duration = (System.nanoTime() - startTime) / 1_000_000;
            }

            // Processa valor de retorno se habilitado
            Object processedReturn = null;
            if (loggableAnnotation.logReturn() && result != null) {
                processedReturn = redactor.redactValue(result, loggableAnnotation.maxPayloadLength());
            }

            // Emite log de sucesso
            emitSuccessLog(loggableAnnotation.level(), className, methodName, 
                          processedArgs, processedReturn, duration);

            return result;

        } catch (Throwable throwable) {
            // Calcula duração em caso de erro
            Long duration = null;
            if (loggableAnnotation.includeDuration()) {
                duration = (System.nanoTime() - startTime) / 1_000_000;
            }

            // Emite log de erro
            emitErrorLog(className, methodName, processedArgs, duration, throwable);
            
            throw throwable;
        }
    }

    private Loggable findLoggableAnnotation(Method method, Class<?> declaringClass) {
        // Primeiro verifica se o método tem a anotação
        Loggable methodAnnotation = AnnotationUtils.findAnnotation(method, Loggable.class);
        if (methodAnnotation != null) {
            return methodAnnotation;
        }

        // Se não encontrou no método, verifica na classe
        return AnnotationUtils.findAnnotation(declaringClass, Loggable.class);
    }

    private void emitSuccessLog(LogLevel level, String className, String methodName, 
                               Map<String, Object> args, Object returnValue, Long duration) {
        
        switch (level) {
            case TRACE -> structuredLogger.trace(event -> buildLogEvent(event, className, methodName, args, returnValue, duration));
            case DEBUG -> structuredLogger.debug(event -> buildLogEvent(event, className, methodName, args, returnValue, duration));
            case WARN -> structuredLogger.warn(event -> buildLogEvent(event, className, methodName, args, returnValue, duration));
            case ERROR -> structuredLogger.error(event -> buildLogEvent(event, className, methodName, args, returnValue, duration));
            default -> structuredLogger.info(event -> buildLogEvent(event, className, methodName, args, returnValue, duration));
        }
    }

    private void emitErrorLog(String className, String methodName, 
                             Map<String, Object> args, Long duration, Throwable throwable) {
        
        structuredLogger.error(event -> {
            event.component("aop")
                 .clazz(className)
                 .method(methodName)
                 .args(args)
                 .error(throwable);
            
            if (duration != null) {
                event.durationMs(duration);
            }
        });
    }

    private void buildLogEvent(com.hlaff.loggingx.core.logger.LogEventBuilder event, 
                              String className, String methodName, 
                              Map<String, Object> args, Object returnValue, Long duration) {
        
        event.component("aop")
             .clazz(className)
             .method(methodName);

        if (!args.isEmpty()) {
            event.args(args);
        }

        if (returnValue != null) {
            event.ret(returnValue);
        }

        if (duration != null) {
            event.durationMs(duration);
        }

        event.sampled(true);
    }
}
