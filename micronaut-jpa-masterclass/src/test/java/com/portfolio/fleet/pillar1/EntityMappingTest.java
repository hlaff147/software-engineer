package com.portfolio.fleet.pillar1;

import com.portfolio.fleet.domain.asset.AssetStatus;
import com.portfolio.fleet.domain.asset.FuelType;
import com.portfolio.fleet.domain.asset.HeavyEquipment;
import com.portfolio.fleet.domain.asset.LightEquipment;
import com.portfolio.fleet.domain.asset.SensorType;
import com.portfolio.fleet.domain.asset.Vehicle;
import com.portfolio.fleet.domain.asset.IoTSensor;
import com.portfolio.fleet.domain.certification.Certification;
import com.portfolio.fleet.domain.common.Address;
import com.portfolio.fleet.domain.common.GpsCoordinate;
import com.portfolio.fleet.domain.common.Money;
import com.portfolio.fleet.domain.common.Tag;
import com.portfolio.fleet.domain.operator.Operator;
import com.portfolio.fleet.domain.operator.OperatorLicense;
import com.portfolio.fleet.repository.AssetRepository;
import com.portfolio.fleet.repository.CertificationRepository;
import com.portfolio.fleet.repository.OperatorRepository;
import com.portfolio.fleet.repository.VehicleRepository;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import jakarta.inject.Inject;
import jakarta.persistence.EntityManager;
import jakarta.transaction.Transactional;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Optional;
import static org.assertj.core.api.Assertions.assertThat;

@MicronautTest(transactional = false)
@DisplayName("Pillar 1: Advanced Entity Mappings & Inheritance")
class EntityMappingTest {

    @Inject
    private VehicleRepository vehicleRepository;

    @Inject
    private AssetRepository assetRepository;

    @Inject
    private OperatorRepository operatorRepository;

    @Inject
    private CertificationRepository certificationRepository;

    @Inject
    private EntityManager entityManager;

    @Test
    @Transactional
    @DisplayName("Joined Table Inheritance: Vehicle inherits base Asset fields into separate joined table")
    void testJoinedTableInheritance() {
        Vehicle vehicle = new Vehicle("AST-TRUCK-01", "Volvo FH16", AssetStatus.ACTIVE, "ABC-1234", "VIN9876543210", 45000L, FuelType.DIESEL);
        vehicle.setLastKnownLocation(new GpsCoordinate(-23.5505, -46.6333, 760.0));
        vehicle.setRegistrationAddress(new Address("Avenida Paulista 1000", "São Paulo", "SP", "01310-100", "Brazil"));
        vehicle.getTags().add(new Tag("department", "logistics"));
        vehicle.getTags().add(new Tag("fleet_tier", "heavy_haul"));

        Vehicle saved = vehicleRepository.save(vehicle);
        assertThat(saved.getId()).isNotNull();

        entityManager.flush();
        entityManager.clear();

        Optional<Vehicle> fetched = vehicleRepository.findById(saved.getId());
        assertThat(fetched).isPresent();
        assertThat(fetched.get().getLicensePlate()).isEqualTo("ABC-1234");
        assertThat(fetched.get().getName()).isEqualTo("Volvo FH16");
        assertThat(fetched.get().getLastKnownLocation().getLatitude()).isEqualTo(-23.5505);
        assertThat(fetched.get().getTags()).hasSize(2);
    }

    @Test
    @Transactional
    @DisplayName("Single Table Inheritance: Heavy and Light equipment stored in single table with discriminator")
    void testSingleTableInheritance() {
        HeavyEquipment crane = new HeavyEquipment("SN-CRANE-999", "Liebherr", "LTM 11200", 1200.0, true);
        LightEquipment drill = new LightEquipment("SN-DRILL-111", "Bosch", "GBH 18V", true, 110);

        entityManager.persist(crane);
        entityManager.persist(drill);
        entityManager.flush();
        entityManager.clear();

        HeavyEquipment loadedCrane = entityManager.find(HeavyEquipment.class, crane.getId());
        LightEquipment loadedDrill = entityManager.find(LightEquipment.class, drill.getId());

        assertThat(loadedCrane).isNotNull();
        assertThat(loadedCrane.getMaxTonnage()).isEqualTo(1200.0);
        assertThat(loadedDrill).isNotNull();
        assertThat(loadedDrill.getPortable()).isTrue();
    }

    @Test
    @Transactional
    @DisplayName("Cascade ALL & Orphan Removal on @OneToOne Operator -> License")
    void testOneToOneCascadeAndOrphanRemoval() {
        Operator operator = new Operator("TransLog Express", "12.345.678/0001-90", "ops@translog.com", new Money(new BigDecimal("500000.00"), "BRL"));
        OperatorLicense license = new OperatorLicense("LIC-2026-XYZ", "ANTT", LocalDate.now(), LocalDate.now().plusYears(5));
        operator.setLicense(license);

        Operator saved = operatorRepository.save(operator);
        assertThat(saved.getId()).isNotNull();
        assertThat(saved.getLicense().getId()).isNotNull();

        entityManager.flush();
        entityManager.clear();

        // Verify orphanRemoval when unlinking license
        Operator fetched = operatorRepository.findById(saved.getId()).orElseThrow();
        Long oldLicenseId = fetched.getLicense().getId();
        fetched.setLicense(null); // Unlink license

        operatorRepository.update(fetched);
        entityManager.flush();
        entityManager.clear();

        OperatorLicense deletedLicense = entityManager.find(OperatorLicense.class, oldLicenseId);
        assertThat(deletedLicense).isNull(); // Orphan row automatically deleted by Hibernate!
    }

    @Test
    @Transactional
    @DisplayName("@ManyToMany: Operator and Certification mapping table persistence")
    void testManyToManyRelationship() {
        Operator operator = new Operator("AeroCargo Brazil", "98.765.432/0001-11", "contact@aerocargo.com", new Money(new BigDecimal("1000000.00"), "USD"));
        Certification cert1 = new Certification("ISO-9001", "Quality Management", "ISO", 36);
        Certification cert2 = new Certification("HAZMAT-BR", "Dangerous Goods Transport", "IBAMA", 24);

        certificationRepository.save(cert1);
        certificationRepository.save(cert2);

        operator.addCertification(cert1);
        operator.addCertification(cert2);
        operatorRepository.save(operator);

        entityManager.flush();
        entityManager.clear();

        Operator fetched = operatorRepository.findDetailedById(operator.getId()).orElseThrow();
        assertThat(fetched.getCertifications()).hasSize(2);
    }
}
