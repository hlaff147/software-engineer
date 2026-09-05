package com.portfolio.fleet.domain.telemetry;

import com.portfolio.fleet.domain.common.GpsCoordinate;
import jakarta.persistence.Column;
import jakarta.persistence.Embedded;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.time.Instant;

/**
 * 💡 JPA TIP: High-Throughput Append-Only Entity
 * Optimized for high write volumes. Notice no bidirectional back-references,
 * simple primary key, and embedded coordinates. Ideal for JDBC batching demos!
 */
@Entity
@Table(name = "telemetry_readings")
public class TelemetryReading {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "sensor_mac", nullable = false, length = 30)
    private String sensorMac;

    @Column(name = "timestamp", nullable = false)
    private Instant timestamp;

    @Column(name = "temperature_celsius")
    private Double temperatureCelsius;

    @Column(name = "battery_volts")
    private Double batteryVolts;

    @Column(name = "speed_kmh")
    private Double speedKmh;

    @Embedded
    private GpsCoordinate location;

    public TelemetryReading() {
    }

    public TelemetryReading(String sensorMac, Instant timestamp, Double temperatureCelsius, Double batteryVolts, Double speedKmh, GpsCoordinate location) {
        this.sensorMac = sensorMac;
        this.timestamp = timestamp;
        this.temperatureCelsius = temperatureCelsius;
        this.batteryVolts = batteryVolts;
        this.speedKmh = speedKmh;
        this.location = location;
    }

    public Long getId() {
        return id;
    }

    public String getSensorMac() {
        return sensorMac;
    }

    public void setSensorMac(String sensorMac) {
        this.sensorMac = sensorMac;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

    public Double getTemperatureCelsius() {
        return temperatureCelsius;
    }

    public void setTemperatureCelsius(Double temperatureCelsius) {
        this.temperatureCelsius = temperatureCelsius;
    }

    public Double getBatteryVolts() {
        return batteryVolts;
    }

    public void setBatteryVolts(Double batteryVolts) {
        this.batteryVolts = batteryVolts;
    }

    public Double getSpeedKmh() {
        return speedKmh;
    }

    public void setSpeedKmh(Double speedKmh) {
        this.speedKmh = speedKmh;
    }

    public GpsCoordinate getLocation() {
        return location;
    }

    public void setLocation(GpsCoordinate location) {
        this.location = location;
    }
}
