---
name: empty-deploy-commit-trigger
description: >-
  Creates an empty git commit ("commit no content") with the exact message 'ci: #deployuat #auto'
  and immediately pushes to the current branch to trigger automated UAT deployment pipelines.
  Activate when the user asks to trigger a deploy, create an empty deploy commit, or run 'ci: #deployuat #auto'.
---

# 🚀 Empty Deploy Commit Trigger ("Commit No Content")

Automates the creation and push of an empty git commit (`--allow-empty`) with the exact commit message `ci: #deployuat #auto` to re-run or trigger CI/CD deployment pipelines on demand without modifying any project code.

---

## 🚫 Critical Negative Constraints (Anti-Patterns)

- **NEVER modify files when asked for an empty deploy commit**: Do not edit code or stage changes. Use `--allow-empty`.
- **NEVER alter the commit message**: The commit message MUST be exactly `"ci: #deployuat #auto"` (lowercase tags, strict formatting for CI regexes).
- **NEVER push to a hardcoded branch**: Always resolve the active branch dynamically via `git branch --show-current`.
- **NEVER skip the push**: The empty commit is created specifically to trigger remote CI/CD pipelines; always push after creating it.

---

## 📋 Execution Protocol

When the user gives commands like:
- *"cria um commit no content de deploy e dá push"*
- *"trigger deploy"*
- *"commit vazio de deploy"*
- *"dispara deploy uat"*
- *"ci: #deployuat #auto"*

### Step-by-Step Sequence:

1. **Resolve Current Branch**:
   ```bash
   BRANCH=$(git branch --show-current)
   ```

2. **Execute Empty Commit**:
   ```bash
   git commit --allow-empty -m "ci: #deployuat #auto"
   ```

3. **Push to Remote**:
   ```bash
   git push origin "$BRANCH"
   ```

4. **Confirm in Chat**:
   ```text
   🚢 Commit no-content criado com sucesso!
   - Branch: <branch>
   - Mensagem: ci: #deployuat #auto
   - Commit Hash: <short-hash>
   🚀 Push enviado para origin/<branch>. Pipeline de deploy UAT acionada!
   ```

---

## 🧪 Helper Script

A ready-to-use script is available at [`scripts/trigger-deploy.sh`](./scripts/trigger-deploy.sh):
```bash
./scripts/trigger-deploy.sh
```
Dry-run support:
```bash
./scripts/trigger-deploy.sh --dry-run
```
