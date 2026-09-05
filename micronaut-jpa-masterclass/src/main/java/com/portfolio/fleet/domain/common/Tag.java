package com.portfolio.fleet.domain.common;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import java.util.Objects;

/**
 * 💡 JPA TIP: Embeddable inside @ElementCollection
 * Value objects stored inside collections do not have their own primary key;
 * Hibernate manages their rows via the parent entity foreign key.
 */
@Embeddable
public class Tag {

    @Column(name = "tag_key", nullable = false, length = 50)
    private String key;

    @Column(name = "tag_value", nullable = false, length = 100)
    private String value;

    public Tag() {
    }

    public Tag(String key, String value) {
        this.key = key;
        this.value = value;
    }

    public String getKey() {
        return key;
    }

    public void setKey(String key) {
        this.key = key;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Tag tag)) return false;
        return Objects.equals(key, tag.key) && Objects.equals(value, tag.value);
    }

    @Override
    public int hashCode() {
        return Objects.hash(key, value);
    }
}
