package com.hlaff.loggingx.spring.config;

import com.hlaff.loggingx.core.logger.Slf4jStructuredLogger;
import com.hlaff.loggingx.core.logger.StructuredLogger;
import com.hlaff.loggingx.core.redact.DefaultRedactor;
import com.hlaff.loggingx.core.redact.Redactor;
import com.hlaff.loggingx.http.CorrelatingClientInterceptor;
import com.hlaff.loggingx.http.HttpServerLoggingFilter;
import com.hlaff.loggingx.http.WebClientFilters;
import com.hlaff.loggingx.kafka.KafkaLoggingHelper;
import com.hlaff.loggingx.mongo.LoggingMongoCommandListener;
import com.hlaff.loggingx.spring.aop.BusinessEventAspect;
import com.hlaff.loggingx.spring.aop.MethodLoggingAspect;
import com.hlaff.loggingx.spring.mdc.CorrelationFilter;
import com.mongodb.event.CommandListener;
import lombok.extern.slf4j.Slf4j;
import org.apache.kafka.clients.consumer.ConsumerInterceptor;
import org.apache.kafka.clients.producer.ProducerInterceptor;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.boot.autoconfigure.condition.ConditionalOnClass;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.autoconfigure.condition.ConditionalOnWebApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.boot.web.client.RestTemplateCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.WebClient;

/**
 * AutoConfiguration principal do LoggingX.
 * Configura automaticamente todos os componentes da biblioteca baseado
 * nas dependências presentes no classpath e nas propriedades de configuração.
 */
@Slf4j
@AutoConfiguration
@EnableConfigurationProperties(LoggingXProperties.class)
@ConditionalOnProperty(prefix = "loggingx", name = "enabled", havingValue = "true", matchIfMissing = true)
public class LoggingXAutoConfiguration {

    // ========================================
    // COMPONENTES PRINCIPAIS (CORE)
    // ========================================

    @Bean
    @ConditionalOnMissingBean
    public StructuredLogger structuredLogger(LoggingXProperties properties) {
        log.info("Configurando LoggingX StructuredLogger para serviço: {}", properties.getService());
        return new Slf4jStructuredLogger(properties);
    }

    @Bean
    @ConditionalOnMissingBean
    public Redactor redactor(LoggingXProperties properties) {
        log.debug("Configurando LoggingX Redactor com {} chaves para mascaramento", 
                 properties.getRedactKeys().size());
        return new DefaultRedactor(properties);
    }

    // ========================================
    // ASPECTOS AOP
    // ========================================

    @Bean
    @ConditionalOnMissingBean
    public MethodLoggingAspect methodLoggingAspect(StructuredLogger structuredLogger, 
                                                  Redactor redactor,
                                                  LoggingXProperties properties) {
        log.info("Configurando LoggingX MethodLoggingAspect");
        return new MethodLoggingAspect(structuredLogger, redactor, properties);
    }

    @Bean
    @ConditionalOnMissingBean
    public BusinessEventAspect businessEventAspect(StructuredLogger structuredLogger,
                                                   Redactor redactor,
                                                   LoggingXProperties properties) {
        log.info("Configurando LoggingX BusinessEventAspect");
        return new BusinessEventAspect(structuredLogger, redactor, properties);
    }

    // ========================================
    // FILTROS WEB
    // ========================================

    @Bean
    @ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
    @ConditionalOnClass(CorrelationFilter.class)
    @ConditionalOnMissingBean
    public CorrelationFilter correlationFilter() {
        log.info("Configurando LoggingX CorrelationFilter");
        return new CorrelationFilter();
    }

    @Bean
    @ConditionalOnWebApplication(type = ConditionalOnWebApplication.Type.SERVLET)
    @ConditionalOnProperty(prefix = "loggingx.http.server", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public HttpServerLoggingFilter httpServerLoggingFilter(StructuredLogger structuredLogger,
                                                           LoggingXProperties properties) {
        log.info("Configurando LoggingX HttpServerLoggingFilter");
        return new HttpServerLoggingFilter(structuredLogger, properties);
    }

    // ========================================
    // CONECTORES HTTP
    // ========================================

    @Bean
    @ConditionalOnClass(RestTemplate.class)
    @ConditionalOnProperty(prefix = "loggingx.http.client", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public RestTemplateCustomizer loggingXRestTemplateCustomizer(StructuredLogger structuredLogger,
                                                                LoggingXProperties properties) {
        log.info("Configurando LoggingX RestTemplateCustomizer");
        return restTemplate -> {
            CorrelatingClientInterceptor interceptor = new CorrelatingClientInterceptor(structuredLogger, properties);
            restTemplate.getInterceptors().add(interceptor);
        };
    }

    @Bean
    @ConditionalOnClass(WebClient.class)
    @ConditionalOnProperty(prefix = "loggingx.http.client", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public WebClientFilters webClientFilters(StructuredLogger structuredLogger,
                                            LoggingXProperties properties) {
        log.info("Configurando LoggingX WebClientFilters");
        return new WebClientFilters(structuredLogger, properties);
    }

    // ========================================
    // CONECTORES KAFKA
    // ========================================

    @Bean
    @ConditionalOnClass(ProducerInterceptor.class)
    @ConditionalOnProperty(prefix = "loggingx.kafka", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public KafkaLoggingHelper kafkaLoggingHelper(StructuredLogger structuredLogger,
                                                LoggingXProperties properties) {
        log.info("Configurando LoggingX KafkaLoggingHelper");
        return new KafkaLoggingHelper(structuredLogger, properties);
    }

    /**
     * Registra a classe do ProducerInterceptor para uso nas configurações do Kafka.
     * O app consumer deve configurar: 
     * spring.kafka.producer.properties.interceptor.classes=com.hlaff.loggingx.kafka.CorrelatingProducerInterceptor
     */
    @Bean("loggingXKafkaProducerInterceptorClass")
    @ConditionalOnClass(ProducerInterceptor.class)
    @ConditionalOnProperty(prefix = "loggingx.kafka", name = "enabled", havingValue = "true", matchIfMissing = true)
    public Class<?> kafkaProducerInterceptorClass() {
        try {
            Class<?> clazz = Class.forName("com.hlaff.loggingx.kafka.CorrelatingProducerInterceptor");
            log.info("Registrada classe do Kafka ProducerInterceptor: {}", clazz.getName());
            return clazz;
        } catch (ClassNotFoundException e) {
            log.debug("Classe CorrelatingProducerInterceptor não encontrada no classpath");
            return Object.class;
        }
    }

    /**
     * Registra a classe do ConsumerInterceptor para uso nas configurações do Kafka.
     * O app consumer deve configurar:
     * spring.kafka.consumer.properties.interceptor.classes=com.hlaff.loggingx.kafka.CorrelatingConsumerInterceptor
     */
    @Bean("loggingXKafkaConsumerInterceptorClass")
    @ConditionalOnClass(ConsumerInterceptor.class)
    @ConditionalOnProperty(prefix = "loggingx.kafka", name = "enabled", havingValue = "true", matchIfMissing = true)
    public Class<?> kafkaConsumerInterceptorClass() {
        try {
            Class<?> clazz = Class.forName("com.hlaff.loggingx.kafka.CorrelatingConsumerInterceptor");
            log.info("Registrada classe do Kafka ConsumerInterceptor: {}", clazz.getName());
            return clazz;
        } catch (ClassNotFoundException e) {
            log.debug("Classe CorrelatingConsumerInterceptor não encontrada no classpath");
            return Object.class;
        }
    }

    // ========================================
    // CONECTORES AZURE SERVICE BUS
    // ========================================

    @Bean
    @ConditionalOnClass(com.azure.messaging.servicebus.ServiceBusClientBuilder.class)
    @ConditionalOnProperty(prefix = "loggingx.servicebus", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public com.hlaff.loggingx.servicebus.ServiceBusLoggingHelper serviceBusLoggingHelper(StructuredLogger structuredLogger,
                                                                                         LoggingXProperties properties) {
        log.info("Configurando LoggingX ServiceBusLoggingHelper");
        return new com.hlaff.loggingx.servicebus.ServiceBusLoggingHelper(structuredLogger, properties);
    }

    // ========================================
    // CONECTORES MONGODB
    // ========================================

    @Bean
    @ConditionalOnClass(CommandListener.class)
    @ConditionalOnProperty(prefix = "loggingx.mongo", name = "enabled", havingValue = "true", matchIfMissing = true)
    @ConditionalOnMissingBean
    public LoggingMongoCommandListener loggingMongoCommandListener(StructuredLogger structuredLogger,
                                                                  LoggingXProperties properties) {
        log.info("Configurando LoggingX LoggingMongoCommandListener");
        return new LoggingMongoCommandListener(structuredLogger, properties);
    }

    // ========================================
    // CONECTORES JDBC
    // ========================================

    @Bean
    @ConditionalOnClass(net.ttddyy.dsproxy.support.ProxyDataSourceBuilder.class)
    @ConditionalOnProperty(prefix = "loggingx.jdbc", name = "enabled", havingValue = "true")
    @ConditionalOnMissingBean
    public com.hlaff.loggingx.jdbc.LoggingQueryExecutionListener loggingQueryExecutionListener(StructuredLogger structuredLogger,
                                                                                              LoggingXProperties properties) {
        log.info("Configurando LoggingX LoggingQueryExecutionListener");
        return new com.hlaff.loggingx.jdbc.LoggingQueryExecutionListener(structuredLogger, properties);
    }

    @Bean
    @ConditionalOnClass(net.ttddyy.dsproxy.support.ProxyDataSourceBuilder.class)
    @ConditionalOnProperty(prefix = "loggingx.jdbc", name = "enabled", havingValue = "true")
    public com.hlaff.loggingx.jdbc.LoggingDataSourceProxyBeanPostProcessor loggingDataSourceProxyBeanPostProcessor(com.hlaff.loggingx.jdbc.LoggingQueryExecutionListener listener) {
        log.info("Configurando LoggingX LoggingDataSourceProxyBeanPostProcessor");
        return new com.hlaff.loggingx.jdbc.LoggingDataSourceProxyBeanPostProcessor(listener);
    }

    // ========================================
    // INFORMAÇÕES DE INICIALIZAÇÃO
    // ========================================

    public LoggingXAutoConfiguration(LoggingXProperties properties) {
        log.info("========================================");
        log.info("🚀 LoggingX inicializado com sucesso!");
        log.info("   Serviço: {}", properties.getService());
        log.info("   Ambiente: {}", properties.getEnv());
        log.info("   Versão: {}", properties.getVersion());
        log.info("   HTTP habilitado: {}", properties.getHttp().isEnabled());
        log.info("   Kafka habilitado: {}", properties.getKafka().isEnabled());
        log.info("   ServiceBus habilitado: {}", properties.getServicebus().isEnabled());
        log.info("   MongoDB habilitado: {}", properties.getMongo().isEnabled());
        log.info("   JDBC habilitado: {}", properties.getJdbc().isEnabled());
        log.info("   Chaves para mascaramento: {}", properties.getRedactKeys().size());
        log.info("========================================");
    }
}
