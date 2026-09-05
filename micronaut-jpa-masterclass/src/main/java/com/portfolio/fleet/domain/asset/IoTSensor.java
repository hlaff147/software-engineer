package com.portfolio.fleet.domain.asset;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Table;

/**
 * 💡 JPA TIP: Another Joined Table Subclass
 * Shares identity with 'assets.id' while storing IoT telemetries configuration.
 */
@Entity
@Table(name = "iot_sensors")
public class IoTSensor extends Asset {

    @Column(name = "mac_address", nullable = false, unique = true, length = 30)
    private String macAddress;

    @Column(name = "firmware_version", length = 30)
    private String firmwareVersion;

    @Column(name = "battery_level_percentage")
    private Integer batteryLevelPercentage = 100;

    @Enumerated(EnumType.STRING)
    @Column(name = "sensor_type", length = 30)
    private SensorType sensorType = SensorType.GPS_TRACKER;

    @Column(name = "polling_interval_seconds")
    private Integer pollingIntervalSeconds = 30;

    public IoTSensor() {
    }

    public IoTSensor(String assetCode, String name, AssetStatus status, String macAddress, SensorType sensorType) {
        super(assetCode, name, status);
        this.macAddress = macAddress;
        this.sensorType = sensorType;
    }

    public String getMacAddress() {
        return macAddress;
    }

    public void setMacAddress(String macAddress) {
        this.macAddress = macAddress;
    }

    public String getFirmwareVersion() {
        return firmwareVersion;
    }

    public void setFirmwareVersion(String firmwareVersion) {
        this.firmwareVersion = firmwareVersion;
    }

    public Integer getBatteryLevelPercentage() {
        return batteryLevelPercentage;
    }

    public void setBatteryLevelPercentage(Integer batteryLevelPercentage) {
        this.batteryLevelPercentage = batteryLevelPercentage;
    }

    public SensorType getSensorType() {
        return sensorType;
    }

    public void setSensorType(SensorType sensorType) {
        this.sensorType = sensorType;
    }

    public Integer getPollingIntervalSeconds() {
        return pollingIntervalSeconds;
    }

    public void setPollingIntervalSeconds(Integer pollingIntervalSeconds) {
        this.pollingIntervalSeconds = pollingIntervalSeconds;
    }
}
