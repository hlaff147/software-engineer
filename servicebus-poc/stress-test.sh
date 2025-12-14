#!/bin/bash

# ============================================
# Script de Stress Test para Azure Service Bus PoC
# ============================================
# Este script dispara múltiplas requisições para os endpoints
# bad-producer e good-producer para comparar performance e uso de recursos.
#
# USO:
#   ./stress-test.sh [NUMERO_DE_MENSAGENS] [PARALELISMO]
#
# EXEMPLOS:
#   ./stress-test.sh 100           # 100 mensagens, 10 paralelos (default)
#   ./stress-test.sh 500 20        # 500 mensagens, 20 paralelos
#   ./stress-test.sh 1000 50       # 1000 mensagens, 50 paralelos (stress pesado)
# ============================================

set -e

# Configurações
BASE_URL="http://localhost:8080/api/v1"
NUM_MESSAGES=${1:-100}
PARALLELISM=${2:-10}
MESSAGE_BODY='{"content": "Test message", "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}'

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Azure Service Bus PoC - Stress Test                    ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "📊 Configurações:"
echo -e "   • Mensagens: ${YELLOW}${NUM_MESSAGES}${NC}"
echo -e "   • Paralelismo: ${YELLOW}${PARALLELISM}${NC}"
echo -e "   • URL Base: ${YELLOW}${BASE_URL}${NC}"
echo ""

# Verifica se a aplicação está rodando
echo -e "${BLUE}🔍 Verificando se a aplicação está rodando...${NC}"
if ! curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/good-producer/status" -X POST 2>/dev/null | grep -q "200"; then
    echo -e "${RED}❌ Erro: Aplicação não está respondendo em ${BASE_URL}${NC}"
    echo -e "${YELLOW}💡 Inicie a aplicação com: ./mvnw spring-boot:run${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Aplicação está rodando!${NC}"
echo ""

# Função para enviar mensagens
send_messages() {
    local endpoint=$1
    local count=$2
    local parallel=$3
    
    seq 1 "$count" | xargs -P "$parallel" -I {} \
        curl -s -o /dev/null -w "%{http_code}:%{time_total}\n" \
        -X POST "${BASE_URL}/${endpoint}" \
        -H "Content-Type: application/json" \
        -d "${MESSAGE_BODY}"
}

# ============================================
# TESTE 1: Bad Producer (Anti-pattern)
# ============================================
echo -e "${RED}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║  ⚠️  TESTE 1: BAD PRODUCER (Anti-pattern)                   ║${NC}"
echo -e "${RED}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}⚠️  Este endpoint cria NOVA CONEXÃO a cada request!${NC}"
echo -e "${YELLOW}   Observe o uso de CPU/Memória/Threads no JConsole${NC}"
echo ""

# Reset counter
curl -s -X POST "${BASE_URL}/bad-producer/reset-counter" > /dev/null

echo -e "🚀 Iniciando envio de ${NUM_MESSAGES} mensagens para bad-producer..."
BAD_START=$(date +%s.%N)

# Envia mensagens e conta sucessos/falhas
BAD_RESULTS=$(send_messages "bad-producer" "$NUM_MESSAGES" "$PARALLELISM")
BAD_SUCCESS=$(echo "$BAD_RESULTS" | grep -c "^200:" || true)
BAD_FAILED=$((NUM_MESSAGES - BAD_SUCCESS))
BAD_TOTAL_TIME=$(echo "$BAD_RESULTS" | awk -F: '{sum += $2} END {print sum}')

BAD_END=$(date +%s.%N)
BAD_ELAPSED=$(echo "$BAD_END - $BAD_START" | bc)

echo ""
echo -e "${RED}📊 Resultados BAD PRODUCER:${NC}"
echo -e "   • Mensagens enviadas: ${BAD_SUCCESS}/${NUM_MESSAGES}"
echo -e "   • Falhas: ${BAD_FAILED}"
echo -e "   • Tempo total: ${BAD_ELAPSED}s"
echo -e "   • Tempo médio por request: $(echo "scale=3; $BAD_TOTAL_TIME / $NUM_MESSAGES" | bc)s"
echo ""

# Pausa para observação
echo -e "${YELLOW}⏸️  Aguardando 5 segundos para estabilização...${NC}"
sleep 5

# ============================================
# TESTE 2: Good Producer (Best Practice)
# ============================================
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  ✅ TESTE 2: GOOD PRODUCER (Best Practice)                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Este endpoint REUTILIZA a mesma conexão!${NC}"
echo -e "${GREEN}   Observe uso de recursos muito mais baixo no JConsole${NC}"
echo ""

# Reset counter
curl -s -X POST "${BASE_URL}/good-producer/reset-counter" > /dev/null

echo -e "🚀 Iniciando envio de ${NUM_MESSAGES} mensagens para good-producer..."
GOOD_START=$(date +%s.%N)

# Envia mensagens e conta sucessos/falhas
GOOD_RESULTS=$(send_messages "good-producer" "$NUM_MESSAGES" "$PARALLELISM")
GOOD_SUCCESS=$(echo "$GOOD_RESULTS" | grep -c "^200:" || true)
GOOD_FAILED=$((NUM_MESSAGES - GOOD_SUCCESS))
GOOD_TOTAL_TIME=$(echo "$GOOD_RESULTS" | awk -F: '{sum += $2} END {print sum}')

GOOD_END=$(date +%s.%N)
GOOD_ELAPSED=$(echo "$GOOD_END - $GOOD_START" | bc)

echo ""
echo -e "${GREEN}📊 Resultados GOOD PRODUCER:${NC}"
echo -e "   • Mensagens enviadas: ${GOOD_SUCCESS}/${NUM_MESSAGES}"
echo -e "   • Falhas: ${GOOD_FAILED}"
echo -e "   • Tempo total: ${GOOD_ELAPSED}s"
echo -e "   • Tempo médio por request: $(echo "scale=3; $GOOD_TOTAL_TIME / $NUM_MESSAGES" | bc)s"
echo ""

# ============================================
# COMPARAÇÃO FINAL
# ============================================
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║               📊 COMPARAÇÃO FINAL                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Calcula melhoria
if [ "$(echo "$BAD_ELAPSED > 0" | bc)" -eq 1 ]; then
    IMPROVEMENT=$(echo "scale=2; ($BAD_ELAPSED - $GOOD_ELAPSED) / $BAD_ELAPSED * 100" | bc)
    echo -e "   📈 Melhoria de performance: ${GREEN}${IMPROVEMENT}%${NC} mais rápido"
fi

echo ""
echo -e "   ┌─────────────────┬────────────────┬────────────────┐"
echo -e "   │     Métrica     │  Bad Producer  │ Good Producer  │"
echo -e "   ├─────────────────┼────────────────┼────────────────┤"
printf "   │ %-15s │ %14s │ %14s │\n" "Tempo Total" "${BAD_ELAPSED}s" "${GOOD_ELAPSED}s"
printf "   │ %-15s │ %14s │ %14s │\n" "Sucessos" "${BAD_SUCCESS}" "${GOOD_SUCCESS}"
printf "   │ %-15s │ %14s │ %14s │\n" "Falhas" "${BAD_FAILED}" "${GOOD_FAILED}"
echo -e "   └─────────────────┴────────────────┴────────────────┘"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Teste completo!${NC}"
echo -e ""
echo -e "${YELLOW}💡 DICA: Compare as métricas no JConsole/VisualVM:${NC}"
echo -e "   • Threads: Bad cria muitas threads temporárias"
echo -e "   • Heap Memory: Bad aloca mais memória por request"
echo -e "   • CPU: Bad tem picos de CPU pelos handshakes TLS/AMQP"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
