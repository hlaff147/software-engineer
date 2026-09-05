# ==============================================================================
# Multi-Stage Dockerfile: Micronaut Data JPA Masterclass
# ==============================================================================
# Stage 1: Builder (Compiles AOT artifacts and builds executable shadow JAR)
# Stage 2: Runtime (Minimal Eclipse Temurin JRE container with non-root security)
# ==============================================================================

# ── Stage 1: Build Environment ──
FROM eclipse-temurin:21-jdk AS builder

WORKDIR /build

# Copy Gradle wrapper and build definitions first for optimal layer caching
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts gradle.properties ./
RUN chmod +x gradlew

# Download dependencies in an isolated layer
RUN ./gradlew dependencies --no-daemon


# Copy application source code
COPY src/ src/

# Build application layers (Ahead-of-Time compilation + layered distribution)
RUN ./gradlew buildLayers -x test --no-daemon

# ── Stage 2: Optimized JRE Runtime ──
FROM eclipse-temurin:21-jre

LABEL maintainer="Humberto Filho <@hlaff147>"
LABEL description="Micronaut 4 Data JPA Masterclass Enterprise Runtime"

# Security: Create dedicated unprivileged system user
RUN groupadd -r fleet && useradd -r -g fleet -u 1001 fleet

WORKDIR /home/app

# Copy the layered distribution from builder stage
COPY --from=builder --chown=fleet:fleet /build/build/docker/main/layers/libs/ /home/app/libs/
COPY --from=builder --chown=fleet:fleet /build/build/docker/main/layers/resources/ /home/app/resources/
COPY --from=builder --chown=fleet:fleet /build/build/docker/main/layers/app/ /home/app/

USER 1001:fleet

EXPOSE 8080

# Configure JVM flags honoring cgroup limits in Docker
ENV MICRONAUT_ENVIRONMENTS=docker \
    JAVA_TOOL_OPTIONS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:InitialRAMPercentage=50.0 -XX:+ExitOnOutOfMemoryError -Djava.security.egd=file:/dev/./urandom"

ENTRYPOINT ["java", "-jar", "/home/app/application.jar"]
