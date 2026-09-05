package com.portfolio.fleet.domain.common;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import java.util.Objects;

/**
 * 💡 JPA TIP: @Embeddable Value Object
 * An embeddable represents a fine-grained domain concept that has NO lifecycle or identity
 * of its own. Its state is stored directly in the columns of the owning entity table.
 */
@Embeddable
public class GpsCoordinate {

    @Column(name = "latitude")
    private Double latitude;

    @Column(name = "longitude")
    private Double longitude;

    @Column(name = "altitude_meters")
    private Double altitudeMeters;

    public GpsCoordinate() {
    }

    public GpsCoordinate(Double latitude, Double longitude, Double altitudeMeters) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.altitudeMeters = altitudeMeters;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getAltitudeMeters() {
        return altitudeMeters;
    }

    public void setAltitudeMeters(Double altitudeMeters) {
        this.altitudeMeters = altitudeMeters;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof GpsCoordinate that)) return false;
        return Objects.equals(latitude, that.latitude) &&
               Objects.equals(longitude, that.longitude) &&
               Objects.equals(altitudeMeters, that.altitudeMeters);
    }

    @Override
    public int hashCode() {
        return Objects.hash(latitude, longitude, altitudeMeters);
    }
}
