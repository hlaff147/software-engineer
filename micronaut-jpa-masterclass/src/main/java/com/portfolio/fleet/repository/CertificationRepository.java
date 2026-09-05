package com.portfolio.fleet.repository;

import com.portfolio.fleet.domain.certification.Certification;
import io.micronaut.data.annotation.Join;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.util.Optional;

@Repository
public interface CertificationRepository extends JpaRepository<Certification, Long> {

    Optional<Certification> findByCode(String code);

    @Query("SELECT c FROM Certification c LEFT JOIN FETCH c.operators WHERE c.code = :code")
    Optional<Certification> findWithOperatorsByCode(String code);
}
