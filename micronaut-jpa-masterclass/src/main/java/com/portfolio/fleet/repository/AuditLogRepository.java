package com.portfolio.fleet.repository;

import com.portfolio.fleet.audit.AuditLog;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import io.micronaut.data.model.Pageable;
import java.util.List;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {

    List<AuditLog> findByEntityNameAndEntityIdOrderByTimestampDesc(String entityName, String entityId);

    List<AuditLog> findOrderByTimestampDesc(Pageable pageable);

    default List<AuditLog> findTop20ByOrderByTimestampDesc() {
        return findOrderByTimestampDesc(Pageable.from(0, 20));
    }
}
