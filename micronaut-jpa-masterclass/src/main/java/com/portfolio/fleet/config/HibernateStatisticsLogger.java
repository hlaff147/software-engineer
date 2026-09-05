package com.portfolio.fleet.config;

import io.micronaut.context.annotation.Requires;
import io.micronaut.context.event.ApplicationEventListener;
import io.micronaut.context.event.ShutdownEvent;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManagerFactory;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 💡 JPA TIP: Hibernate Statistics & Observability (Pillar 6)
 * Collects and prints vital metrics upon shutdown:
 * - Query cache hit/miss ratio
 * - Second-level cache hit/miss ratio
 * - Entity load count
 * - Number of executed queries
 */
@Singleton
@Requires(property = "jpa.default.properties.hibernate.generate_statistics", value = "true")
public class HibernateStatisticsLogger implements ApplicationEventListener<ShutdownEvent> {

    private static final Logger log = LoggerFactory.getLogger(HibernateStatisticsLogger.class);
    private final EntityManagerFactory entityManagerFactory;

    public HibernateStatisticsLogger(EntityManagerFactory entityManagerFactory) {
        this.entityManagerFactory = entityManagerFactory;
    }

    @Override
    public void onApplicationEvent(ShutdownEvent event) {
        SessionFactory sessionFactory = entityManagerFactory.unwrap(SessionFactory.class);
        if (sessionFactory != null) {
            Statistics stats = sessionFactory.getStatistics();
            log.info("══════════════════════════════════════════════════");
            log.info("📊 HIBERNATE PERFORMANCE & METRICS REPORT");
            log.info("══════════════════════════════════════════════════");
            log.info("Entities Loaded:           {}", stats.getEntityLoadCount());
            log.info("Queries Executed:          {}", stats.getQueryExecutionCount());
            log.info("L2 Cache Hit Count:        {}", stats.getSecondLevelCacheHitCount());
            log.info("L2 Cache Miss Count:       {}", stats.getSecondLevelCacheMissCount());
            log.info("L2 Cache Put Count:        {}", stats.getSecondLevelCachePutCount());
            log.info("Query Cache Hit Count:     {}", stats.getQueryCacheHitCount());
            log.info("Query Cache Miss Count:    {}", stats.getQueryCacheMissCount());
            log.info("Optimistic Failure Count:  {}", stats.getOptimisticFailureCount());
            log.info("══════════════════════════════════════════════════");
        }
    }
}
