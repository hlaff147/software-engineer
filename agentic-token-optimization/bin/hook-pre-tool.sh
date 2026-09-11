#!/usr/bin/env bash
# ==============================================================================
# bin/hook-pre-tool.sh
# 
# Hook de Interceptação Pré-Tool Universal para Agentes (Cursor, Claude Code, etc.)
# Invoca a lógica unificada do Token Router para bloquear leituras caras.
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROUTER_BIN="$SCRIPT_DIR/token-router"

TARGET_FILE="${1:-}"
START_LINE="${2:-}"
END_LINE="${3:-}"

if [ -z "$TARGET_FILE" ]; then
    exit 0
fi

ARGS=("$TARGET_FILE")
if [ -n "$START_LINE" ]; then
    ARGS+=("--start-line" "$START_LINE")
fi
if [ -n "$END_LINE" ]; then
    ARGS+=("--end-line" "$END_LINE")
fi

exec "$ROUTER_BIN" check "${ARGS[@]}"
