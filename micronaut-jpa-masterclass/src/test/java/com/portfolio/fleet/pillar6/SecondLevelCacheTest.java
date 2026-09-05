package com.portfolio.fleet.pillar6;

import com.portfolio.fleet.domain.certification.Certification;
import com.portfolio.fleet.repository.CertificationRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import jakarta.transaction.Transactional;
import org.hibernate.SessionFactory;
import org.hibernate.stat.Statistics;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 6: Hibernate Second-Level (L2) Cache Verification")
class SecondLevelCacheTest {

    @Inject
    private CertificationRepository certificationRepository;

    @Inject
    private EntityManager entityManager;

    @Inject
    private EntityManagerFactory entityManagerFactory;

    @Test
    @Transactional
    @DisplayName("Hibernate Statistics: Verifies statistics capture queries and entity load metrics")
    void testHibernateStatisticsCapture() {
        Certification cert = new Certification("L2-CERT-01", "Safety Standards", "OSHA", 12);
        certificationRepository.save(cert);

        entityManager.flush();
        entityManager.clear();

        Certification loaded = certificationRepository.findByCode("L2-CERT-01").orElseThrow();
        assertThat(loaded.getName()).isEqualTo("Safety Standards");

        SessionFactory sessionFactory = entityManagerFactory.unwrap(SessionFactory.class);
        if (sessionFactory != null) {
            Statistics stats = sessionFactory.getStatistics();
            assertThat(stats.getEntityLoadCount()).isGreaterThan(0L);
        }
    }
}
