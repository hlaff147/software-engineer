package com.portfolio.fleet.domain.asset;

import jakarta.persistence.Column;
import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

/**
 * 💡 JPA TIP: @DiscriminatorValue
 * Identifies this subclass in the 'equipment.equipment_type' column.
 */
@Entity
@DiscriminatorValue("HEAVY")
public class HeavyEquipment extends Equipment {

    @Column(name = "max_tonnage")
    private Double maxTonnage;

    @Column(name = "requires_certified_operator")
    private Boolean requiresCertifiedOperator = true;

    public HeavyEquipment() {
    }

    public HeavyEquipment(String serialNumber, String brand, String model, Double maxTonnage, Boolean requiresCertifiedOperator) {
        super(serialNumber, brand, model);
        this.maxTonnage = maxTonnage;
        this.requiresCertifiedOperator = requiresCertifiedOperator;
    }

    public Double getMaxTonnage() {
        return maxTonnage;
    }

    public void setMaxTonnage(Double maxTonnage) {
        this.maxTonnage = maxTonnage;
    }

    public Boolean getRequiresCertifiedOperator() {
        return requiresCertifiedOperator;
    }

    public void setRequiresCertifiedOperator(Boolean requiresCertifiedOperator) {
        this.requiresCertifiedOperator = requiresCertifiedOperator;
    }
}
