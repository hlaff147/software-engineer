# 🚀 Empty Deploy Commit Trigger ("Commit No Content")

> **Automates creating and pushing an empty git commit (`--allow-empty`) with the exact commit message `ci: #deployuat #auto` to re-trigger CI/CD UAT deployments on demand.**

---

## 🎯 The Problem

Developers frequently need to **re-trigger an automated deployment pipeline** (e.g. UAT / Staging) without changing any code:
- A previous deployment step failed due to a transient infrastructure or network issue.
- External configurations or environment variables changed and a redeploy is needed.
- Typing `git commit --allow-empty -m "ci: #deployuat #auto" && git push origin <branch>` manually is cumbersome, slow, and prone to typos (which will cause the CI/CD pipeline regex to ignore the commit).

---

## ✅ The Solution

This skill allows you to instruct your AI assistant in natural language to trigger a deployment instantly:
- *"cria um commit no content de deploy e dá push"*
- *"trigger deploy"*
- *"commit vazio de deploy"*
- *"dispara deploy uat"*

The agent executes the exact command sequence:
```bash
BRANCH=$(git branch --show-current)
git commit --allow-empty -m "ci: #deployuat #auto"
git push origin "$BRANCH"
```

---

## 💬 Interactive Cursor Chat Simulation

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

## 📐 Anatomy of the Skill

```
13-empty-deploy-commit-trigger/
├── SKILL.md                  # Gemini / Antigravity format (.agents/skills/)
├── .cursorrules              # Cursor format
├── copilot-instructions.md   # GitHub Copilot format
├── scripts/
│   └── trigger-deploy.sh     # Executable bash helper script
└── README.md                 # This didactic guide
```

---

## 🔧 How to Install

### In Cursor
Place in `.cursor/rules/`:
```bash
mkdir -p .cursor/rules
cp ai-coding-skills/13-empty-deploy-commit-trigger/.cursorrules .cursor/rules/empty-deploy-trigger.mdc
```

### In GitHub Copilot
```bash
cat ai-coding-skills/13-empty-deploy-commit-trigger/copilot-instructions.md >> .github/copilot-instructions.md
```

---

## 🧪 Helper Script

You can also run the trigger script directly from the terminal:
```bash
./ai-coding-skills/13-empty-deploy-commit-trigger/scripts/trigger-deploy.sh
```
Or test in simulation mode:
```bash
./ai-coding-skills/13-empty-deploy-commit-trigger/scripts/trigger-deploy.sh --dry-run
# Output:
# [DRY RUN] Would execute:
#   git commit --allow-empty -m "ci: #deployuat #auto"
#   git push origin "main"
```
