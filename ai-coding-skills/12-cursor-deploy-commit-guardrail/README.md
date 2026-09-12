# 🚢 Cursor Deploy Commit Guardrail & Trigger

> **Intercepts standard git commits to prompt for UAT deploy (`#deployuat #auto`), and provides an automated empty trigger commit ("commit no content") workflow (`ci: #deployuat #auto` + push).**

---

## 🎯 The Problems This Solves

1. **Unintended or Missing Deploys on Standard Commits**:
   - Committing without `#deployuat #auto` causes CI/CD pipelines to skip UAT deployment.
   - Committing with deploy tags on every intermediate edit causes redundant builds and cloud resource waste.
   - The Cursor agent often commits automatically without asking developer intent.

2. **Manual Overhead for No-Content Deploy Triggers**:
   - Often, developers need to re-run or trigger a deployment pipeline on an existing branch without changing any source code.
   - Typing `git commit --allow-empty -m "ci: #deployuat #auto" && git push origin <branch>` manually is tedious and error-prone (e.g. typos in `#deployuat`).

---

## ✅ The Solution

This skill provides two distinct operational modes:

### Mode 1: Interactive Standard Commit Guardrail
Whenever code is modified and ready to commit:
1. The agent **stops** and prompts:
   > 🚢 **Confirmação de Deploy:**
   > Deseja acionar o deploy (UAT) com este commit? (**Sim / Não**)
2. **If "Sim"**: Formats commit message with `#deployuat #auto` footer.
3. **If "Não"**: Formats standard commit message without deploy tags.

### Mode 2: Empty Deploy Trigger ("Commit No Content")
Whenever you ask to trigger a deploy without changes (e.g. *"commit no content"*, *"dispara deploy"*, *"deploy uat"*, *"commit vazio"*):
1. The agent automatically executes:
   ```bash
   BRANCH=$(git branch --show-current)
   git commit --allow-empty -m "ci: #deployuat #auto"
   git push origin "$BRANCH"
   ```
2. The agent reports the created commit hash and branch, confirming the trigger!

---

## 💬 Interactive Cursor Chat Simulations

### Scenario 1: Standard Commit with Deploy Confirmation
```text
User: "Terminei as alterações no controller. Pode commitar."

Cursor Agent:
"🚢 Confirmação de Deploy:
Deseja acionar o deploy (UAT) com este commit? (Sim / Não)"

User: "Sim"

Cursor Agent:
"Commitando com tags de deploy:

$ git commit -m "$(cat << 'EOF'
feat(controller): add health status check endpoint

#deployuat #auto
EOF
)"
[main a1b2c3d] feat(controller): add health status check endpoint
✅ Commit realizado com tags de deploy UAT!"
```

---

### Scenario 2: Instant "Commit No Content" Trigger
```text
User: "Cria um commit no content de deploy e dá push"

Cursor Agent:
"Criando commit vazio e disparando pipeline UAT:

$ git commit --allow-empty -m "ci: #deployuat #auto"
[main 8f9e0d1] ci: #deployuat #auto

$ git push origin main
To github.com:org/repo.git
   a1b2c3d..8f9e0d1  main -> main

🚢 Commit no-content criado com sucesso!
- Mensagem: ci: #deployuat #auto
- Hash: 8f9e0d1
🚀 Push realizado na branch 'main'. Pipeline de deploy UAT acionada!"
```

---

## 📐 Exact Tag Specification

| Use Case | Format |
|---|---|
| **Standard Commit with Deploy** | `<Conventional Message>\n\n#deployuat #auto` |
| **No-Content Trigger Commit** | `ci: #deployuat #auto` (via `git commit --allow-empty`) |

---

## 🔧 How to Install in Cursor

```bash
mkdir -p .cursor/rules
cp ai-coding-skills/12-cursor-deploy-commit-guardrail/.cursorrules .cursor/rules/deploy-commit-guardrail.mdc
```

---

## 🧪 Included Helper Scripts

1. **[`scripts/trigger-deploy.sh`](./scripts/trigger-deploy.sh)**:
   Executes the empty commit and push automatically:
   ```bash
   ./ai-coding-skills/12-cursor-deploy-commit-guardrail/scripts/trigger-deploy.sh
   ```
   Supports dry-run testing:
   ```bash
   ./ai-coding-skills/12-cursor-deploy-commit-guardrail/scripts/trigger-deploy.sh --dry-run
   ```

2. **[`scripts/check-deploy-tags.sh`](./scripts/check-deploy-tags.sh)**:
   Validates if a commit message file contains deployment tags.
