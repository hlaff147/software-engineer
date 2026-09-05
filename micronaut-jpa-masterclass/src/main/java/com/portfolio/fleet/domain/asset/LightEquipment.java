package com.portfolio.fleet.domain.asset;

import jakarta.persistence.Column;
import jakarta.persistence.DiscriminatorValue;
import jakarta.persistence.Entity;

@Entity
@DiscriminatorValue("LIGHT")
public class LightEquipment extends Equipment {

    @Column(name = "is_portable")
    private Boolean portable = true;

    @Column(name = "voltage_requirement")
    private Integer voltageRequirement;

    public LightEquipment() {
    }

    public LightEquipment(String serialNumber, String brand, String model, Boolean portable, Integer voltageRequirement) {
        super(serialNumber, brand, model);
        this.portable = portable;
        this.voltageRequirement = voltageRequirement;
    }

    public Boolean getPortable() {
        return portable;
    }

    public void setPortable(Boolean portable) {
        this.portable = portable;
    }

    public Integer getVoltageRequirement() {
        return voltageRequirement;
    }

    public void setVoltageRequirement(Integer voltageRequirement) {
        this.voltageRequirement = voltageRequirement;
    }
}
