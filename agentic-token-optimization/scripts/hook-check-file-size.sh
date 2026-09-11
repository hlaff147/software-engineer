#!/usr/bin/env bash
# ==============================================================================
# hook-check-file-size.sh
# 
# Pre-Tool Interception Hook para Agentes de Código.
# Bloqueia chamadas de leitura direta em arquivos que excedem o limiar de linhas,
# forçando a delegação para o leitor em massa (bulk-reader) para economizar tokens.
#
# Uso:
#   ./hook-check-file-size.sh <caminho_do_arquivo> [start_line] [end_line]
# ==============================================================================

set -euo pipefail

TARGET_FILE="${1:-}"
START_LINE="${2:-}"
END_LINE="${3:-}"
THRESHOLD="${AGENT_DELEGATION_THRESHOLD:-350}"

if [ -z "$TARGET_FILE" ]; then
    echo "Uso: $0 <caminho_do_arquivo> [start_line] [end_line]" >&2
    exit 0
fi

# 1. Se o arquivo não existir fisicamente, permite que a ferramenta nativa lide com o erro
if [ ! -f "$TARGET_FILE" ]; then
    exit 0
fi

# 2. Targeted Reads: se a leitura solicitou um intervalo explícito de linhas
if [ -n "$START_LINE" ] && [ -n "$END_LINE" ]; then
    DELTA=$((END_LINE - START_LINE))
    if [ "$DELTA" -lt "$THRESHOLD" ]; then
        # Leitura pontual autorizada (baixo consumo de tokens)
        exit 0
    fi
fi

# 3. Calcula o total de linhas do arquivo
LINE_COUNT=$(wc -l < "$TARGET_FILE" | tr -d ' ')

# 4. Verificação de limiar
if [ "$LINE_COUNT" -ge "$THRESHOLD" ]; then
    cat <<EOF >&2
[BLOQUEIO DE POLÍTICA DE TOKENS]
Arquivo: $TARGET_FILE
Total de Linhas: $LINE_COUNT linhas (Limiar de leitura direta: $THRESHOLD linhas)

A leitura direta deste arquivo foi bloqueada para evitar o desperdício de tokens de contexto no modelo de fronteira.

Ações Recomendadas:
1. Para entender a estrutura ou responder a dúvidas, utilize o leitor em massa:
   python3 scripts/bulk-read.py --paths "$TARGET_FILE" --question "<sua pergunta>"

2. Para editar uma seção específica, efetue uma leitura direcionada com parâmetros de linha:
   view_file com StartLine e EndLine cobrindo menos de $THRESHOLD linhas.
EOF
    exit 1
fi

# Arquivo dentro do limite tolerado
exit 0
