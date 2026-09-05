plugins {
    id("groovy") 
    id("io.micronaut.application") version "4.4.3"
    id("io.micronaut.aot") version "4.4.3"
}

version = "1.0.0-SNAPSHOT"
group = "com.portfolio.fleet"

repositories {
    mavenCentral()
}

dependencies {
    // ── Micronaut Platform BOM (Guarantees version alignment across all modules) ──
    annotationProcessor(platform("io.micronaut.platform:micronaut-platform:4.4.3"))
    implementation(platform("io.micronaut.platform:micronaut-platform:4.4.3"))
    testAnnotationProcessor(platform("io.micronaut.platform:micronaut-platform:4.4.3"))

    // ── Micronaut Annotation Processors (Ahead-of-Time compilation) ──
    annotationProcessor("io.micronaut:micronaut-inject-java")
    annotationProcessor("io.micronaut.validation:micronaut-validation-processor")
    annotationProcessor("io.micronaut.data:micronaut-data-processor")

    // ── Core & HTTP ──
    implementation("io.micronaut:micronaut-http-server-netty")
    implementation("io.micronaut:micronaut-jackson-databind")
    implementation("io.micronaut.validation:micronaut-validation")
    implementation("jakarta.annotation:jakarta.annotation-api")

    // ── Micronaut Data JPA & Hibernate ──
    // JPA TIP: Micronaut Data precomputes query ASTs at compile time
    implementation("io.micronaut.data:micronaut-data-hibernate-jpa")
    implementation("io.micronaut.sql:micronaut-jdbc-hikari")

    // ── Database Drivers ──
    runtimeOnly("com.h2database:h2")
    runtimeOnly("org.postgresql:postgresql")

    // ── Hibernate L2 Cache (JCache + Ehcache) ──
    implementation("org.hibernate.orm:hibernate-jcache")
    implementation("org.ehcache:ehcache:3.10.8")

    // ── Logging & Metrics ──
    runtimeOnly("ch.qos.logback:logback-classic")
    runtimeOnly("org.yaml:snakeyaml")

    // ── Testing ──
    testAnnotationProcessor("io.micronaut:micronaut-inject-java")
    testImplementation("io.micronaut.test:micronaut-test-junit5")
    testImplementation("org.junit.jupiter:junit-jupiter-api")
    testImplementation("org.junit.jupiter:junit-jupiter-params")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")
    testImplementation("org.assertj:assertj-core:3.27.3")
}

application {
    mainClass.set("com.portfolio.fleet.Application")
}

java {
    sourceCompatibility = JavaVersion.VERSION_21
    targetCompatibility = JavaVersion.VERSION_21
    // JVM toolchain support for Java 21 / 25
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(21))
    }
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
    options.compilerArgs.addAll(listOf(
        "-parameters",
        "-Xlint:unchecked"
    ))
}

tasks.named<Test>("test") {
    useJUnitPlatform()
    testLogging {
        events("passed", "skipped", "failed")
    }
}

micronaut {
    runtime("netty")
    testRuntime("junit5")
    processing {
        incremental(true)
        annotations("com.portfolio.fleet.*")
    }
    aot {
        optimizeServiceLoading.set(false)
        convertYamlToJava.set(false)
        precomputeOperations.set(true)
        cacheEnvironment.set(true)
        optimizeClassLoading.set(true)
        deduceEnvironment.set(true)
        optimizeNetty.set(true)
    }
}
