---
name: cursor-deploy-commit-guardrail
description: >-
  Intercepts git commits in Cursor to ask if a deploy is required, appending '#deployuat #auto' upon confirmation.
  Also creates and pushes empty trigger commits ("commit no content") with exact message 'ci: #deployuat #auto' on demand.
  Activate when preparing, formatting, or executing git commits or when asked to trigger a UAT deployment.
---

# 🚀 Cursor Deploy Commit Guardrail & Trigger

Intercepts git commit actions by the Cursor agent. Enforces an interactive confirmation step asking the user whether standard commits should trigger a UAT deployment, and provides a direct command for empty trigger commits ("commit no content") that immediately trigger CI/CD pipelines.

---

## 🚫 Critical Negative Constraints (Anti-Patterns)

- **NEVER execute a standard `git commit` without asking**: The agent must NEVER commit working tree changes without asking the deploy confirmation question first.
- **NEVER alter tag spelling or casing**: The deployment tags MUST be strictly `#deployuat #auto` (lowercase, space-separated). Any typo (`#deployUAT`, `#deploy_uat`) will fail CI/CD regex triggers.
- **NEVER alter the empty trigger commit message**: For no-content commits, the message MUST be exactly `"ci: #deployuat #auto"`.
- **NEVER push to the wrong branch**: Always inspect the current active branch using `git branch --show-current` before running `git push origin <branch>`.

---

## 📋 Mode 1: Interactive Standard Commit Protocol

Whenever you have finished code changes and are ready to stage and commit:

### Step 1: Draft the Commit Message & Stop
Draft a clean Conventional Commit message (`<type>(<scope>): <description>`). **DO NOT** execute `git commit` yet.

### Step 2: Ask the Deploy Question
Prompt the user explicitly in chat:

> 🚢 **Confirmação de Deploy:**
> Deseja acionar o deploy (UAT) com este commit? (**Sim / Não**)

### Step 3: Format & Execute Based on Response

#### If User responds "Sim" / "Yes" / "Deploy":
Append a blank line and the mandatory `#deployuat #auto` tags at the end of the commit message:

```bash
git commit -m "$(cat << 'EOF'
feat(auth): add OAuth2 token validation and refresh endpoint

Implement JWT validation middleware with expiration checks.

#deployuat #auto
EOF
)"
```

#### If User responds "Não" / "No":
Commit with standard formatting, omitting the deployment tags entirely:

```bash
git commit -m "$(cat << 'EOF'
feat(auth): add OAuth2 token validation and refresh endpoint

Implement JWT validation middleware with expiration checks.
EOF
)"
```

---

## ⚡ Mode 2: Empty Trigger Commit Protocol ("Commit No Content")

When the user requests to trigger a deployment without code changes (e.g., *"cria um commit no content com ci: #deployuat #auto"*, *"trigger deploy"*, *"dispara o deploy em uat"*, *"commit vazio de deploy"*):

### Automated Execution Sequence:

1. **Detect Current Branch**:
   ```bash
   BRANCH=$(git branch --show-current)
   ```

2. **Execute Empty Commit**:
   Create a commit without staged files using `--allow-empty` and the exact message:
   ```bash
   git commit --allow-empty -m "ci: #deployuat #auto"
   ```

3. **Push to Remote**:
   ```bash
   git push origin "$BRANCH"
   ```

4. **Confirm to User in Chat**:
   ```text
   🚢 Commit vazio de deploy criado com sucesso!
   - Branch: <branch>
   - Mensagem: ci: #deployuat #auto
   - Commit Hash: <short-hash>
   🚀 Push enviado para origin/<branch>. Pipeline UAT disparada!
   ```

---

## 📐 Exact Tag Specification

| Context | Exact Format | CI/CD Regex Match |
|---|---|---|
| **Standard Commit with Deploy** | `<Conventional Message>\n\n#deployuat #auto` | Matches `#deployuat` and `#auto` in body |
| **No-Content Empty Trigger Commit** | `ci: #deployuat #auto` | Exact match for pipeline manual trigger |

---

## 🧪 Helper Scripts

- **Validate message tags**: [`scripts/check-deploy-tags.sh <file>`](./scripts/check-deploy-tags.sh)
- **One-command empty trigger**: [`scripts/trigger-deploy.sh`](./scripts/trigger-deploy.sh)
