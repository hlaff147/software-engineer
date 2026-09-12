---
name: cursor-deploy-commit-guardrail
description: >-
  Intercepts git commit operations in Cursor to ask the user if the commit should trigger a deploy.
  Appends mandatory '#deployuat #auto' hashtags to the commit message when the user confirms.
  Activate when preparing, formatting, or executing git commits.
---

# 🚀 Cursor Deploy Commit Guardrail

Intercepts git commit actions by the Cursor agent. Forces an interactive confirmation step asking the user whether this commit should trigger an automated UAT deployment pipeline.

---

## 🚫 Critical Negative Constraints (Anti-Patterns)

- **NEVER execute `git commit` without asking**: The agent must NEVER run `git commit` automatically without asking the deploy confirmation question first.
- **NEVER append `#deployuat #auto` without explicit confirmation**: If the user answers "não", "no", or gives no response, do NOT include the deployment tags.
- **NEVER alter tag spelling or casing**: The deployment tags MUST be exactly `#deployuat #auto` (lowercase, space-separated). Any typo (`#deployUAT`, `#deploy-uat`) will fail CI/CD regex triggers.
- **NEVER inline tags on the subject line**: The tags MUST be placed on a separate footer line separated by a blank line from the commit body.

---

## 📋 1. The Interactive Commit Protocol

Whenever you (the AI agent) have finished coding and are ready to stage and commit changes, you **MUST execute this exact sequence**:

### Step 1: Draft the Commit Message & Stop
Draft a clean Conventional Commit message (`<type>(<scope>): <description>`). **DO NOT** execute the `git commit` command yet.

### Step 2: Ask the Deploy Question
Prompt the user explicitly in chat:

> 🚢 **Confirmação de Deploy:**
> Deseja acionar o deploy (UAT) com este commit? (**Sim / Não**)

### Step 3: Format Based on User Response

#### Option A — User responds "Sim" / "Yes":
Append a blank line and the mandatory `#deployuat #auto` tags at the end of the commit message.

```bash
git commit -m "$(cat << 'EOF'
feat(auth): add OAuth2 token validation and refresh endpoint

Implement JWT validation middleware with expiration checks.

#deployuat #auto
EOF
)"
```

#### Option B — User responds "Não" / "No":
Commit with standard formatting, omitting the deployment tags entirely:

```bash
git commit -m "$(cat << 'EOF'
feat(auth): add OAuth2 token validation and refresh endpoint

Implement JWT validation middleware with expiration checks.
EOF
)"
```

---

## 📐 2. Exact Tag Specification

| Requirement | Value | Notes |
|---|---|---|
| **Mandatory Tags** | `#deployuat #auto` | Both tags are required by the CI/CD pipeline |
| **Casing** | Lowercase only | Strict regex match |
| **Placement** | Commit message footer | Preceded by an empty line |
| **Format** | Multi-line string / heredoc | Preserves formatting in git history |

---

## 🧪 3. Verification Script

To verify that a commit message contains the required deployment tags when intended:
```bash
./scripts/check-deploy-tags.sh /path/to/COMMIT_EDITMSG
```
