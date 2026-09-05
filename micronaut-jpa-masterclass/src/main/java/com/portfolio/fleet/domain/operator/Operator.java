package com.portfolio.fleet.domain.operator;

import com.portfolio.fleet.audit.AuditableEntity;
import com.portfolio.fleet.domain.asset.Asset;
import com.portfolio.fleet.domain.certification.Certification;
import com.portfolio.fleet.domain.common.Money;
import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;

/**
 * 💡 JPA TIP: Aggregate Root with Precise Cascading
 * - @OneToOne(cascade = CascadeType.ALL, orphanRemoval = true): Lifecycle of the license
 *   is strictly bounded to the Operator. If the operator is deleted or license unlinked,
 *   orphanRemoval ensures Hibernate triggers a SQL DELETE for the orphan row.
 * - @ManyToMany: Owning side defines @JoinTable with explicit joinColumns and inverseJoinColumns.
 */
@Entity
@Table(name = "operators")
public class Operator extends AuditableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "tax_id", nullable = false, unique = true, length = 30)
    private String taxId;

    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @Embedded
    private Money operationalBudget;

    @OneToOne(mappedBy = "operator", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.LAZY)
    private OperatorLicense license;

    @OneToMany(mappedBy = "operator", cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    private List<Asset> assets = new ArrayList<>();

    @ManyToMany(cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "operator_certifications",
        joinColumns = @JoinColumn(name = "operator_id"),
        inverseJoinColumns = @JoinColumn(name = "certification_id")
    )
    private Set<Certification> certifications = new HashSet<>();

    public Operator() {
    }

    public Operator(String name, String taxId, String email, Money operationalBudget) {
        this.name = name;
        this.taxId = taxId;
        this.email = email;
        this.operationalBudget = operationalBudget;
    }

    // 💡 JPA TIP: Helper method to maintain bidirectional relationship consistency in memory
    public void setLicense(OperatorLicense license) {
        this.license = license;
        if (license != null) {
            license.setOperator(this);
        }
    }

    public void addCertification(Certification certification) {
        this.certifications.add(certification);
        certification.getOperators().add(this);
    }

    public void removeCertification(Certification certification) {
        this.certifications.remove(certification);
        certification.getOperators().remove(this);
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTaxId() {
        return taxId;
    }

    public void setTaxId(String taxId) {
        this.taxId = taxId;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public Money getOperationalBudget() {
        return operationalBudget;
    }

    public void setOperationalBudget(Money operationalBudget) {
        this.operationalBudget = operationalBudget;
    }

    public OperatorLicense getLicense() {
        return license;
    }

    public List<Asset> getAssets() {
        return assets;
    }

    public void setAssets(List<Asset> assets) {
        this.assets = assets;
    }

    public Set<Certification> getCertifications() {
        return certifications;
    }

    public void setCertifications(Set<Certification> certifications) {
        this.certifications = certifications;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Operator operator)) return false;
        return Objects.equals(taxId, operator.taxId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(taxId);
    }
}
