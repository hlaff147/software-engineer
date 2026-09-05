package com.portfolio.fleet.repository.custom;

import com.portfolio.fleet.domain.maintenance.MaintenanceSchedule;
import com.portfolio.fleet.dto.MaintenanceFilterRequest;
import jakarta.inject.Singleton;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Predicate;
import jakarta.persistence.criteria.Root;
import jakarta.transaction.Transactional;
import java.util.ArrayList;
import java.util.List;

/**
 * 💡 JPA TIP: Criteria API & EntityManager Integration
 * When query conditions are composed dynamically at runtime (e.g. advanced search filters),
 * JPA Criteria API guarantees syntax and type safety while avoiding SQL injection vulnerabilities.
 */
@Singleton
public class CustomMaintenanceRepositoryImpl implements CustomMaintenanceRepository {

    @PersistenceContext
    private final EntityManager entityManager;

    public CustomMaintenanceRepositoryImpl(EntityManager entityManager) {
        this.entityManager = entityManager;
    }

    @Override
    @Transactional
    public List<MaintenanceSchedule> findSchedulesByDynamicCriteria(
            MaintenanceFilterRequest filter, 
            int page, 
            int pageSize) {

        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<MaintenanceSchedule> query = cb.createQuery(MaintenanceSchedule.class);
        Root<MaintenanceSchedule> root = query.from(MaintenanceSchedule.class);

        List<Predicate> predicates = buildPredicates(cb, root, filter);
        query.where(predicates.toArray(new Predicate[0]));
        query.orderBy(cb.desc(root.get("scheduledDate")));

        TypedQuery<MaintenanceSchedule> typedQuery = entityManager.createQuery(query);
        typedQuery.setFirstResult(page * pageSize);
        typedQuery.setMaxResults(pageSize);

        return typedQuery.getResultList();
    }

    @Override
    @Transactional
    public long countSchedulesByDynamicCriteria(MaintenanceFilterRequest filter) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Long> countQuery = cb.createQuery(Long.class);
        Root<MaintenanceSchedule> root = countQuery.from(MaintenanceSchedule.class);

        List<Predicate> predicates = buildPredicates(cb, root, filter);
        countQuery.select(cb.count(root));
        countQuery.where(predicates.toArray(new Predicate[0]));

        return entityManager.createQuery(countQuery).getSingleResult();
    }

    private List<Predicate> buildPredicates(
            CriteriaBuilder cb, 
            Root<MaintenanceSchedule> root, 
            MaintenanceFilterRequest filter) {

        List<Predicate> predicates = new ArrayList<>();

        if (filter == null) {
            return predicates;
        }

        if (filter.assetId() != null) {
            predicates.add(cb.equal(root.get("asset").get("id"), filter.assetId()));
        }
        if (filter.status() != null) {
            predicates.add(cb.equal(root.get("status"), filter.status()));
        }
        if (filter.priority() != null) {
            predicates.add(cb.equal(root.get("priority"), filter.priority()));
        }
        if (filter.fromDate() != null) {
            predicates.add(cb.greaterThanOrEqualTo(root.get("scheduledDate"), filter.fromDate()));
        }
        if (filter.toDate() != null) {
            predicates.add(cb.lessThanOrEqualTo(root.get("scheduledDate"), filter.toDate()));
        }
        if (filter.maxCost() != null) {
            predicates.add(cb.lessThanOrEqualTo(root.get("estimatedCost"), filter.maxCost()));
        }

        return predicates;
    }
}
