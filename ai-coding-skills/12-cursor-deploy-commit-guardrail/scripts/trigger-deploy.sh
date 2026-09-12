#!/usr/bin/env bash
# ==============================================================================
# trigger-deploy.sh — Creates an empty commit with 'ci: #deployuat #auto' and pushes
# Usage: ./trigger-deploy.sh [--dry-run]
# ==============================================================================

set -euo pipefail

DRY_RUN="${1:-}"
BRANCH=$(git branch --show-current)

if [[ -z "$BRANCH" ]]; then
    echo "❌ Error: Could not determine current git branch (detached HEAD?)."
    exit 1
fi

COMMIT_MSG="ci: #deployuat #auto"

if [[ "$DRY_RUN" == "--dry-run" ]]; then
    echo "[DRY RUN] Would execute:"
    echo "  git commit --allow-empty -m \"$COMMIT_MSG\""
    echo "  git push origin \"$BRANCH\""
    exit 0
fi

echo "🚢 Creating empty deploy trigger commit on branch '$BRANCH'..."
git commit --allow-empty -m "$COMMIT_MSG"

COMMIT_HASH=$(git rev-parse --short HEAD)
echo "✅ Created commit $COMMIT_HASH: \"$COMMIT_MSG\""

echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo "🎉 Push completed successfully! UAT deployment pipeline triggered."
