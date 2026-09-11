#!/usr/bin/env bash
# ==============================================================================
# test-token-router.sh
# 
# Suíte de testes automatizados para verificar os três comportamentos do hook:
# 1. Bloqueio de arquivo grande (> limiar)
# 2. Permissão de leitura direcionada (targeted read com intervalo)
# 3. Permissão de arquivo pequeno (< limiar)
# 4. Execução do utilitário bulk-read e code-write
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="$SCRIPT_DIR/hook-check-file-size.sh"
BULK_READ="$SCRIPT_DIR/bulk-read.py"
CODE_WRITE="$SCRIPT_DIR/code-write.py"

chmod +x "$HOOK" "$BULK_READ" "$CODE_WRITE"

TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

echo "🧪 Iniciando testes do Token Router & Pre-Tool Hook..."

# Criação de arquivo pequeno (50 linhas)
SMALL_FILE="$TMP_DIR/small.txt"
seq 1 50 > "$SMALL_FILE"

# Criação de arquivo grande (500 linhas)
LARGE_FILE="$TMP_DIR/large.txt"
seq 1 500 > "$LARGE_FILE"

# Teste 1: Arquivo pequeno deve passar livremente
echo -n "• Teste 1: Leitura de arquivo pequeno (< 350 linhas)... "
if "$HOOK" "$SMALL_FILE"; then
    echo "✅ PASSOU (Permitido)"
else
    echo "❌ FALHOU"
    exit 1
fi

# Teste 2: Arquivo grande sem intervalo deve ser bloqueado
echo -n "• Teste 2: Leitura de arquivo grande (> 350 linhas)... "
if "$HOOK" "$LARGE_FILE" 2>/dev/null; then
    echo "❌ FALHOU (Deveria ter sido bloqueado)"
    exit 1
else
    echo "✅ PASSOU (Bloqueado com sucesso)"
fi

# Teste 3: Leitura direcionada em arquivo grande (intervalo de 20 linhas) deve passar
echo -n "• Teste 3: Leitura direcionada com offset/limit (linhas 100 a 120)... "
if "$HOOK" "$LARGE_FILE" 100 120; then
    echo "✅ PASSOU (Permitido)"
else
    echo "❌ FALHOU"
    exit 1
fi

# Teste 4: Execução do bulk-read
echo -n "• Teste 4: Execução do utilitário bulk-read.py... "
OUTPUT=$(python3 "$BULK_READ" --question "Estrutura geral" --paths "$LARGE_FILE" "$SMALL_FILE")
if [[ "$OUTPUT" == *"Analisados 2 arquivos"* ]]; then
    echo "✅ PASSOU"
else
    echo "❌ FALHOU"
    exit 1
fi

# Teste 5: Execução do code-write direto em disco
echo -n "• Teste 5: Execução do utilitário code-write.py direto em disco... "
TARGET_FILE="$TMP_DIR/GeneratedClass.java"
python3 "$CODE_WRITE" --spec "Gerar classe mock" --reference "$SMALL_FILE" --target "$TARGET_FILE" >/dev/null
if [ -f "$TARGET_FILE" ]; then
    echo "✅ PASSOU (Arquivo gravado fisicamente)"
else
    echo "❌ FALHOU"
    exit 1
fi

echo ""
echo "🎉 Todos os 5 testes passaram com sucesso!"
