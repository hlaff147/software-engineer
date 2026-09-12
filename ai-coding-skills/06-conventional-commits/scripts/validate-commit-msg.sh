#!/usr/bin/env bash
# Validates commit message follows Conventional Commits format
# Usage: ./validate-commit-msg.sh <commit-msg-file>
# Install as git hook: cp scripts/validate-commit-msg.sh .git/hooks/commit-msg

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

# Regex for Conventional Commits
PATTERN="^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\([a-z0-9_-]+\))?!?: .+"

if [[ ! $COMMIT_MSG =~ $PATTERN ]]; then
  echo "Error: Commit message does not follow Conventional Commits format."
  echo "Format: <type>(<scope>): <short imperative description>"
  echo "Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore"
  echo "Example: feat(auth): add login functionality"
  exit 1
fi

SUBJECT_LINE=$(head -n 1 "$COMMIT_MSG_FILE")
if [ ${#SUBJECT_LINE} -gt 72 ]; then
  echo "Error: Subject line must be 72 characters or less."
  exit 1
fi

echo "Commit message validation passed."
exit 0
