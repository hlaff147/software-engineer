#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛑 Parando Wallet API...${NC}"

# Verificar se docker-compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ docker-compose não encontrado.${NC}"
    exit 1
fi

# Verificar se existe docker-compose.yml
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ docker-compose.yml não encontrado no diretório atual.${NC}"
    exit 1
fi

# Mostrar containers antes de parar
echo -e "${BLUE}📊 Containers atualmente rodando:${NC}"
docker-compose ps

# Parar os serviços
echo -e "${YELLOW}🔽 Parando serviços...${NC}"
docker-compose stop

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Serviços parados com sucesso!${NC}"
else
    echo -e "${RED}❌ Erro ao parar os serviços.${NC}"
fi

# Opção para remover containers
echo ""
read -p "🗑️  Deseja remover os containers também? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🗑️ Removendo containers...${NC}"
    docker-compose down
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Containers removidos com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao remover containers.${NC}"
    fi
fi

# Opção para remover volumes (dados)
echo ""
read -p "⚠️  Deseja remover os volumes (DADOS SERÃO PERDIDOS)? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}🔥 ATENÇÃO: Removendo volumes (dados serão perdidos)...${NC}"
    docker-compose down -v
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Volumes removidos com sucesso!${NC}"
    else
        echo -e "${RED}❌ Erro ao remover volumes.${NC}"
    fi
fi

echo ""
echo -e "${BLUE}📊 Status final dos containers:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}🎉 Processo de parada concluído!${NC}"
echo ""
echo -e "${BLUE}🔧 Para iniciar novamente:${NC}"
echo -e "  🚀 ${YELLOW}./start.sh${NC} ou ${YELLOW}docker-compose up -d${NC}"
echo ""
echo -e "${BLUE}💡 Dicas:${NC}"
echo -e "  📜 Ver logs salvos:    ${YELLOW}docker-compose logs${NC}"
echo -e "  🧹 Limpeza completa:   ${YELLOW}docker system prune -a${NC}"
