#!/usr/bin/env bash
# ==============================================================================
# run_demo.sh
# 
# Demonstração interativa ponta a ponta do Token Router & Pre-Tool Interception.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN="$PROJECT_ROOT/bin/token-router"

export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"

GREEN="\033[0;32m"
RED="\033[0;31m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
NC="\033[0m"

echo -e "${BLUE}==============================================================================${NC}"
echo -e "${BLUE}       🚀 DEMONSTRAÇÃO PRÁTICA: TOKEN ROUTER & MODEL ROUTING                 ${NC}"
echo -e "${BLUE}==============================================================================${NC}"
echo ""

LARGE_FILE="$PROJECT_ROOT/examples/sample_large_service.py"
LINES=$(wc -l < "$LARGE_FILE" | tr -d ' ')

echo -e "${YELLOW}[Cenário 1]${NC} Agente tenta ler arquivo de serviço corporativo com ${LINES} linhas diretamente..."
echo -e "Comando: ${BLUE}bin/token-router check examples/sample_large_service.py${NC}"

if "$BIN" check "$LARGE_FILE" 2> /tmp/router_err.log; then
    echo -e "${RED}ERRO: O arquivo deveria ter sido bloqueado!${NC}"
    exit 1
else
    echo -e "${GREEN}✔ Interceptado pelo Pre-Tool Hook com sucesso!${NC}"
    echo -e "Mensagem orientativa exibida ao agente:"
    echo -e "${RED}$(cat /tmp/router_err.log)${NC}"
fi

echo ""
echo -e "${YELLOW}[Cenário 2]${NC} Agente necessita apenas inspecionar um método específico (Targeted Read L60-L80)..."
echo -e "Comando: ${BLUE}bin/token-router check examples/sample_large_service.py --start-line 60 --end-line 80 -v${NC}"
"$BIN" check "$LARGE_FILE" --start-line 60 --end-line 80 -v
echo -e "${GREEN}✔ Leitura pontual autorizada sem overhead de tokens desnecessários!${NC}"

echo ""
echo -e "${YELLOW}[Cenário 3]${NC} Agente delega a compreensão do arquivo para o Bulk Reader Worker..."
echo -e "Comando: ${BLUE}bin/token-router read --paths examples/sample_large_service.py --question \"Quais métodos realizam operações financeiras no ledger?\"${NC}"
echo ""
"$BIN" read --paths "$LARGE_FILE" --question "Quais métodos realizam operações financeiras no ledger?"
echo ""
echo -e "${GREEN}✔ Síntese concisa devolvida sem encher a janela de contexto principal (~90% economia de tokens)!${NC}"

echo ""
echo -e "${YELLOW}[Cenário 4]${NC} Agente gera novo arquivo de testes via Code Writer com gravação direta em disco..."
OUT_TEST="/tmp/GeneratedTransferTest.java"
echo -e "Comando: ${BLUE}bin/token-router write --spec \"Testes de estorno e conciliação\" --reference examples/sample_reference_test.py --target $OUT_TEST${NC}"
"$BIN" write --spec "Testes de estorno e conciliação" --reference "$PROJECT_ROOT/examples/sample_reference_test.py" --target "$OUT_TEST"

if [ -f "$OUT_TEST" ]; then
    echo -e "${GREEN}✔ Arquivo gravado fisicamente em disco sem tocar a janela de contexto do agente!${NC}"
    head -n 12 "$OUT_TEST"
fi

echo ""
echo -e "${BLUE}==============================================================================${NC}"
echo -e "${GREEN}  🎉 DEMONSTRAÇÃO CONCLUÍDA: Todos os 4 fluxos foram executados com sucesso! ${NC}"
echo -e "${BLUE}==============================================================================${NC}"
