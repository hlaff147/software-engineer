#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Iniciando Wallet API...${NC}"

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker não está rodando. Por favor, inicie o Docker primeiro.${NC}"
    exit 1
fi

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose não encontrado. Por favor, instale o Docker Compose.${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Subindo serviços com Docker Compose...${NC}"
docker-compose up -d

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Erro ao subir os serviços. Verificando logs...${NC}"
    docker-compose logs --tail=20
    exit 1
fi

echo -e "${YELLOW}⏳ Aguardando serviços ficarem prontos...${NC}"

# Aguardar MongoDB
echo -e "${BLUE}  🗄️ Aguardando MongoDB...${NC}"
for i in {1..30}; do
    if docker exec wallet-mongodb mongosh --quiet --eval "db.adminCommand('ping')" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✅ MongoDB pronto!${NC}"
        break
    fi
    echo -e "${YELLOW}  ⏳ MongoDB ainda inicializando... ($i/30)${NC}"
    sleep 2
done

# Aguardar aplicação Spring Boot
echo -e "${BLUE}  🌱 Aguardando Spring Boot...${NC}"
for i in {1..60}; do
    if curl -f http://localhost:8080/actuator/health > /dev/null 2>&1; then
        echo -e "${GREEN}  ✅ Spring Boot pronto!${NC}"
        break
    fi
    echo -e "${YELLOW}  ⏳ Spring Boot ainda inicializando... ($i/60)${NC}"
    sleep 3
done

# Verificar saúde final
echo -e "${BLUE}🔍 Verificando saúde da aplicação...${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:8080/actuator/health)
HEALTH_STATUS=$(echo "$HEALTH_RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

if [ "$HEALTH_STATUS" = "UP" ]; then
    echo -e "${GREEN}✅ Aplicação está saudável!${NC}"
else
    echo -e "${RED}❌ Aplicação com problemas. Status: $HEALTH_STATUS${NC}"
    echo "Response: $HEALTH_RESPONSE"
fi

# Verificar containers
echo -e "${BLUE}📊 Status dos containers:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}🎉 Wallet API está rodando!${NC}"
echo ""
echo -e "${BLUE}📍 URLs úteis:${NC}"
echo -e "  🌐 API Principal:      ${YELLOW}http://localhost:8080${NC}"
echo -e "  📚 Swagger UI:         ${YELLOW}http://localhost:8080/swagger-ui.html${NC}"
echo -e "  ❤️ Health Check:       ${YELLOW}http://localhost:8080/actuator/health${NC}"
echo -e "  🗄️ MongoDB:            ${YELLOW}mongodb://localhost:27017${NC}"
echo -e "  🎛️ Mongo Express:      ${YELLOW}http://localhost:8081${NC} (admin/admin123)"
echo ""
echo -e "${BLUE}📖 Documentação:${NC}"
echo -e "  📄 README.md:          Documentação completa"
echo -e "  🌐 CURL_EXAMPLES.md:   Exemplos de uso da API"
echo -e "  🐳 DOCKER.md:          Guia completo do Docker"
echo ""
echo -e "${BLUE}🔧 Comandos úteis:${NC}"
echo -e "  📜 Ver logs:           ${YELLOW}docker-compose logs -f${NC}"
echo -e "  🛑 Parar serviços:     ${YELLOW}./stop.sh${NC} ou ${YELLOW}docker-compose down${NC}"
echo -e "  🔄 Restart:            ${YELLOW}docker-compose restart${NC}"
echo ""
echo -e "${GREEN}💡 Dica: Execute um teste rápido com:${NC}"
echo -e "${YELLOW}curl -X POST http://localhost:8080/api/v1/wallets -H 'Content-Type: application/json' -d '{\"userId\": \"test\", \"currency\": \"BRL\"}' | jq .${NC}"
