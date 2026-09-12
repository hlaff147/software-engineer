#!/usr/bin/env bash
# ==============================================================================
# check-deploy-tags.sh — Validates deployment tags in commit messages
# Usage: ./check-deploy-tags.sh <commit-msg-file>
# ==============================================================================

set -euo pipefail

COMMIT_FILE="${1:-}"

if [[ -z "$COMMIT_FILE" || ! -f "$COMMIT_FILE" ]]; then
    echo "Usage: $0 <path-to-commit-msg-file>"
    exit 1
fi

CONTENT=$(cat "$COMMIT_FILE")

if echo "$CONTENT" | grep -q "#deployuat" && echo "$CONTENT" | grep -q "#auto"; then
    echo "🚢 Deploy tags detected: #deployuat #auto"
    echo "✅ CI/CD will trigger automated UAT deployment."
    exit 0
else
    echo "ℹ️  No deploy tags found. Standard commit without deployment."
    exit 0
fi
