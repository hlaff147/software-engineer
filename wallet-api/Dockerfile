# Dockerfile para Wallet API
FROM openjdk:17-jdk-slim as builder

# Informações do build
LABEL maintainer="hlaff@example.com"
LABEL version="1.0.0"
LABEL description="Wallet API - Sistema de carteiras digitais"

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração do Maven
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./

# Download das dependências (cache layer)
RUN ./mvnw dependency:go-offline -B

# Copiar código fonte
COPY src/ src/

# Build da aplicação
RUN ./mvnw clean package -DskipTests -B && \
    java -Djarmode=layertools -jar target/*.jar extract

# Runtime stage
FROM openjdk:17-jre-slim

# Instalar curl para health checks
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Criar usuário não-root
RUN groupadd -r wallet && useradd -r -g wallet wallet

# Definir diretório de trabalho
WORKDIR /app

# Copiar layers da aplicação para otimizar cache
COPY --from=builder --chown=wallet:wallet app/dependencies/ ./
COPY --from=builder --chown=wallet:wallet app/spring-boot-loader/ ./
COPY --from=builder --chown=wallet:wallet app/snapshot-dependencies/ ./
COPY --from=builder --chown=wallet:wallet app/application/ ./

# Mudar para usuário não-root
USER wallet

# Expor porta da aplicação
EXPOSE 8080

# Variáveis de ambiente padrão
ENV JAVA_OPTS="-Xmx512m -Xms256m" \
    SPRING_PROFILES_ACTIVE="docker"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Comando de inicialização
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS org.springframework.boot.loader.launch.JarLauncher"]
