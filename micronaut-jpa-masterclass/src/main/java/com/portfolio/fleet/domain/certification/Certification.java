package com.portfolio.fleet.domain.certification;

import com.portfolio.fleet.audit.AuditableEntity;
import com.portfolio.fleet.domain.operator.Operator;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.Table;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

/**
 * 💡 JPA TIP: @ManyToMany Relationship (Non-Owning Side)
 * When modeling Many-to-Many relationships, one side MUST define mappedBy to designate
 * the other side as the owner of the @JoinTable.
 */
@Entity
@Table(name = "certifications")
public class Certification extends AuditableEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "code", nullable = false, unique = true, length = 50)
    private String code;

    @Column(name = "name", nullable = false, length = 150)
    private String name;

    @Column(name = "issuing_body", length = 100)
    private String issuingBody;

    @Column(name = "validity_months")
    private Integer validityMonths;

    @ManyToMany(mappedBy = "certifications")
    private Set<Operator> operators = new HashSet<>();

    public Certification() {
    }

    public Certification(String code, String name, String issuingBody, Integer validityMonths) {
        this.code = code;
        this.name = name;
        this.issuingBody = issuingBody;
        this.validityMonths = validityMonths;
    }

    public Long getId() {
        return id;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getIssuingBody() {
        return issuingBody;
    }

    public void setIssuingBody(String issuingBody) {
        this.issuingBody = issuingBody;
    }

    public Integer getValidityMonths() {
        return validityMonths;
    }

    public void setValidityMonths(Integer validityMonths) {
        this.validityMonths = validityMonths;
    }

    public Set<Operator> getOperators() {
        return operators;
    }

    public void setOperators(Set<Operator> operators) {
        this.operators = operators;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Certification that)) return false;
        return Objects.equals(code, that.code);
    }

    @Override
    public int hashCode() {
        return Objects.hash(code);
    }
}
