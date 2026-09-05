package com.portfolio.fleet.audit;

import io.micronaut.core.annotation.Introspected;
import java.time.Instant;

/**
 * 💡 Java 25 Feature: Record as Domain Event
 * Compact, immutable data carrier representing an audit state change.
 */
@Introspected
public record AuditEvent(
    String entityName,
    String entityId,
    String action,
    String details,
    String operator,
    Instant timestamp
) {}
