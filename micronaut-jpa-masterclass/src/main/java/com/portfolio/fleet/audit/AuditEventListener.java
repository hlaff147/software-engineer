package com.portfolio.fleet.audit;

import com.portfolio.fleet.repository.AuditLogRepository;
import io.micronaut.context.event.ApplicationEventListener;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.Async;
import io.micronaut.scheduling.annotation.ExecuteOn;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * 💡 Enterprise Pattern: Async Audit Decoupling
 * Domain events are asynchronously saved to an audit ledger on a Virtual Thread (Java 21/25),
 * ensuring zero latency overhead on the originating business transaction.
 */
@Singleton
public class AuditEventListener implements ApplicationEventListener<AuditEvent> {

    private static final Logger log = LoggerFactory.getLogger(AuditEventListener.class);
    private final AuditLogRepository auditLogRepository;

    public AuditEventListener(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @Override
    @Async
    @ExecuteOn(TaskExecutors.BLOCKING)
    @Transactional(Transactional.TxType.REQUIRES_NEW)
    public void onApplicationEvent(AuditEvent event) {
        log.info("Processing asynchronous audit event: {} for entity ID {}", event.action(), event.entityId());
        AuditLog logEntry = new AuditLog(
            event.entityName(),
            event.entityId(),
            event.action(),
            event.details(),
            event.operator()
        );
        auditLogRepository.save(logEntry);
    }
}
