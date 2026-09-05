# 🔍 Pillar 3: Advanced Querying & Projections

> JPQL, Native Queries, DTO Projections, and Type-Safe Criteria API

---

## 1. Constructor-Expression DTO Projections

Loading full entities introduces memory overhead and First-Level Cache management costs. For read-only operations (e.g. dashboards, exports), **DTO Projections** project columns directly into Java records:

```java
@Query("""
    SELECT new com.portfolio.fleet.dto.AssetSummaryDTO(
        a.id, a.assetCode, a.name, a.status, o.name
    )
    FROM Asset a
    LEFT JOIN a.operator o
    WHERE a.status = :status
    ORDER BY a.name ASC
""")
List<AssetSummaryDTO> findSummariesByStatus(AssetStatus status);
```

### Why Projections Win for Read-Heavy Workloads:
1. **Zero Persistence Context Overhead:** Results are not managed; dirty checking snapshots are bypassed.
2. **Reduced Network Payload:** Only required columns (`id`, `assetCode`, `name`, `status`, `operator_name`) are retrieved.
3. **Immutable Carriers:** Using Java records guarantees immutability.

---

## 2. Dynamic Criteria API Queries

When search criteria are dynamic (optional date ranges, multi-field filters), the Criteria API builds queries with compile-time type safety:

```java
CriteriaBuilder cb = entityManager.getCriteriaBuilder();
CriteriaQuery<MaintenanceSchedule> query = cb.createQuery(MaintenanceSchedule.class);
Root<MaintenanceSchedule> root = query.from(MaintenanceSchedule.class);

List<Predicate> predicates = new ArrayList<>();
if (filter.status() != null) {
    predicates.add(cb.equal(root.get("status"), filter.status()));
}
if (filter.priority() != null) {
    predicates.add(cb.equal(root.get("priority"), filter.priority()));
}
if (filter.maxCost() != null) {
    predicates.add(cb.lessThanOrEqualTo(root.get("estimatedCost"), filter.maxCost()));
}

query.where(predicates.toArray(new Predicate[0]));
TypedQuery<MaintenanceSchedule> typedQuery = entityManager.createQuery(query);
typedQuery.setFirstResult(page * pageSize);
typedQuery.setMaxResults(pageSize);
return typedQuery.getResultList();
```

