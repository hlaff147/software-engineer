package com.portfolio.fleet.domain.asset;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;

/**
 * 💡 JPA TIP: Joined Table Subclass
 * 'vehicles' table has a primary key that is also a foreign key referencing 'assets.id'.
 * Attributes here are unique to vehicles, keeping the base 'assets' table clean and normalized.
 */
@Entity
@Table(name = "vehicles")
public class Vehicle extends Asset {

    @Column(name = "license_plate", nullable = false, unique = true, length = 20)
    private String licensePlate;

    @Column(name = "vin", nullable = false, unique = true, length = 30)
    private String vin;

    @Column(name = "mileage")
    private Long mileage = 0L;

    @Enumerated(EnumType.STRING)
    @Column(name = "fuel_type", length = 30)
    private FuelType fuelType = FuelType.DIESEL;

    @Column(name = "passenger_capacity")
    private Integer passengerCapacity;

    @Column(name = "cargo_capacity_kg")
    private Double cargoCapacityKg;

    public Vehicle() {
    }

    public Vehicle(String assetCode, String name, AssetStatus status, String licensePlate, String vin, Long mileage, FuelType fuelType) {
        super(assetCode, name, status);
        this.licensePlate = licensePlate;
        this.vin = vin;
        this.mileage = mileage;
        this.fuelType = fuelType;
    }

    public String getLicensePlate() {
        return licensePlate;
    }

    public void setLicensePlate(String licensePlate) {
        this.licensePlate = licensePlate;
    }

    public String getVin() {
        return vin;
    }

    public void setVin(String vin) {
        this.vin = vin;
    }

    public Long getMileage() {
        return mileage;
    }

    public void setMileage(Long mileage) {
        this.mileage = mileage;
    }

    public FuelType getFuelType() {
        return fuelType;
    }

    public void setFuelType(FuelType fuelType) {
        this.fuelType = fuelType;
    }

    public Integer getPassengerCapacity() {
        return passengerCapacity;
    }

    public void setPassengerCapacity(Integer passengerCapacity) {
        this.passengerCapacity = passengerCapacity;
    }

    public Double getCargoCapacityKg() {
        return cargoCapacityKg;
    }

    public void setCargoCapacityKg(Double cargoCapacityKg) {
        this.cargoCapacityKg = cargoCapacityKg;
    }
}
