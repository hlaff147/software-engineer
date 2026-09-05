# 🏛️ Pillar 1: Advanced Entity Mappings & Inheritance

> Jakarta Persistence (JPA 3.2) & Hibernate Entity Architecture Guide

---

## 1. Inheritance Strategies: Joined vs. Single Table

JPA provides three primary inheritance strategies for domain modeling. In this masterclass, we contrast **Joined Table** against **Single Table**.

### A. Joined Table Strategy (`InheritanceType.JOINED`)

Used for core asset types (`Asset`, `Vehicle`, `IoTSensor`):

```java
@Entity
@Table(name = "assets")
@Inheritance(strategy = InheritanceType.JOINED)
public abstract class Asset extends AuditableEntity { ... }

@Entity
@Table(name = "vehicles")
public class Vehicle extends Asset {
    @Column(name = "license_plate")
    private String licensePlate;
    ...
}
```

#### Database Physical Layout:
```text
┌────────────────────────────────────────────────────────┐
│ assets (id, asset_code, name, status, operator_id, ...)│
└────────────────────────────────────────────────────────┘
          ▲                                    ▲
          │ PK=FK                              │ PK=FK
┌──────────────────────────────────┐ ┌──────────────────────────────────────┐
│ vehicles (id, license_plate, ...)│ │ iot_sensors (id, mac_address, ...)   │
└──────────────────────────────────┘ └──────────────────────────────────────┘
```

* **Pros:** Fully normalized relational schema; no null columns for subclass-specific fields; foreign keys enforce referential integrity.
* **Cons:** Polymorphic queries require an `SQL JOIN` across all subclass tables.

---

### B. Single Table Strategy (`InheritanceType.SINGLE_TABLE`)

Used for equipment variants (`Equipment`, `HeavyEquipment`, `LightEquipment`):

```java
@Entity
@Table(name = "equipment")
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@DiscriminatorColumn(name = "equipment_type", discriminatorType = DiscriminatorType.STRING)
public abstract class Equipment extends AuditableEntity { ... }

@Entity
@DiscriminatorValue("HEAVY")
public class HeavyEquipment extends Equipment { ... }

@Entity
@DiscriminatorValue("LIGHT")
public class LightEquipment extends Equipment { ... }
```

* **Pros:** Maximum query performance — zero joins required to retrieve any subclass or polymorphic collection.
* **Cons:** Subclass-specific columns (`max_tonnage`, `voltage_requirement`) **must be nullable** at the database schema level.

---

## 2. Value Objects: `@Embeddable` & `@Embedded`

Value Objects represent descriptive domain aspects without persistent identity:

```java
@Embeddable
public class GpsCoordinate {
    private Double latitude;
    private Double longitude;
    private Double altitudeMeters;
}
```

### In Entity:
```java
@Embedded
private GpsCoordinate lastKnownLocation;

@Embedded
private Address registrationAddress;
```

### 💡 JPA TIP: `@AttributeOverrides`
When embedding the same value object multiple times in one entity:
```java
@Embedded
@AttributeOverrides({
    @AttributeOverride(name = "latitude", column = @Column(name = "origin_lat")),
    @AttributeOverride(name = "longitude", column = @Column(name = "origin_lon"))
})
private GpsCoordinate originLocation;
```

---

## 3. Collections of Value Objects: `@ElementCollection`

```java
@ElementCollection(fetch = FetchType.LAZY)
@CollectionTable(name = "asset_tags", joinColumns = @JoinColumn(name = "asset_id"))
private Set<Tag> tags = new HashSet<>();
```

* Maps value objects to an auxiliary table (`asset_tags`) without creating a separate entity.
* Rows are bound directly to `asset_id` and have no independent lifecycle.

---

## 4. Relationship Cascading & `orphanRemoval`

```java
@OneToOne(mappedBy = "operator", cascade = CascadeType.ALL, orphanRemoval = true)
private OperatorLicense license;
```

| Operation | `CascadeType.REMOVE` | `orphanRemoval = true` |
| :--- | :--- | :--- |
| `operatorRepository.delete(operator)` | Deletes license | Deletes license |
| `operator.setLicense(null)` | Leaves orphaned license row in DB | **Deletes orphan license row automatically** |

