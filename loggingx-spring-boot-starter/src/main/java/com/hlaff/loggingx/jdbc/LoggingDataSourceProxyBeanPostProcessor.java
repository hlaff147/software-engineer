package com.hlaff.loggingx.jdbc;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import net.ttddyy.dsproxy.support.ProxyDataSourceBuilder;
import org.springframework.beans.BeansException;
import org.springframework.beans.factory.config.BeanPostProcessor;

import javax.sql.DataSource;

/**
 * BeanPostProcessor que envolve DataSources com ProxyDataSource para
 * interceptar execuções de SQL e delegar ao listener de logging.
 */
@Slf4j
@RequiredArgsConstructor
public class LoggingDataSourceProxyBeanPostProcessor implements BeanPostProcessor {

    private final LoggingQueryExecutionListener listener;

    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        if (bean instanceof DataSource dataSource) {
            try {
                return ProxyDataSourceBuilder.create(dataSource)
                        .name(beanName)
                        .listener(listener)
                        .build();
            } catch (Exception e) {
                log.debug("Falha ao criar ProxyDataSource para {}: {}", beanName, e.getMessage());
            }
        }
        return bean;
    }
}

