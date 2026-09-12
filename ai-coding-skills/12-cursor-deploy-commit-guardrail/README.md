# 🚢 Cursor Deploy Commit Guardrail

> **Intercepts git commit actions by the Cursor agent, enforcing an interactive prompt that asks the user if the commit should trigger a deploy and appending `#deployuat #auto` when confirmed.**

---

## 🎯 The Problem

In modern CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins), automated deployment to testing environments (e.g. UAT / Staging) is often governed by **commit message tags**:
- Committing without `#deployuat #auto` results in **no deployment**, requiring manual triggers or redundant commits.
- Conversely, committing with tags on every micro-commit causes **unnecessary pipeline runs, cloud costs, and queue congestions**.
- AI coding agents like Cursor Composer frequently commit changes automatically without consulting the developer about deployment intent.

---

## ✅ The Solution

This skill establishes a strict **Pre-Commit Interception Barrier**:
1. Whenever the agent is ready to commit, it **MUST pause** and ask the user:
   > 🚢 **Confirmação de Deploy:**
   > Deseja acionar o deploy (UAT) com este commit? (**Sim / Não**)
2. If the user answers **"Sim"** (or "yes", "s", "deploy"), the agent appends the mandatory tags:
   ```
   #deployuat #auto
   ```
3. If the user answers **"Não"** (or "no", "n"), the agent commits normally without any deployment tags.

---

## 💬 Interactive Cursor Chat Simulation

### Scenario A: With Deployment (User says Yes)

```text
User: "Implementei o endpoint de login. Pode commitar."

Cursor Agent:
"Todas as alterações foram testadas e o build está verde.

🚢 Confirmação de Deploy:
Deseja acionar o deploy (UAT) com este commit? (Sim / Não)"

User: "Sim"

Cursor Agent:
"Commitando com tags de deploy:

$ git commit -m "$(cat << 'EOF'
feat(auth): add OAuth2 authentication endpoint

Implement JWT validation middleware with refresh token rotation.

#deployuat #auto
EOF
)"

[main 4f8a12b] feat(auth): add OAuth2 authentication endpoint
 2 files changed, 45 insertions(+)

✅ Commit realizado e pipeline UAT disparada com sucesso!"
```

---

### Scenario B: Without Deployment (User says No)

```text
User: "Refatorei o nome da variável no serviço. Pode commitar."

Cursor Agent:
"🚢 Confirmação de Deploy:
Deseja acionar o deploy (UAT) com este commit? (Sim / Não)"

User: "Não, só refatoração local."

Cursor Agent:
"Commitando sem tags de deploy:

$ git commit -m "refactor(service): rename internal cache variable"
[main 7c3d91a] refactor(service): rename internal cache variable
 1 file changed, 2 insertions(+), 2 deletions(-)

✅ Commit realizado localmente sem disparar pipeline de UAT."
```

---

## 📐 Anatomy of the Skill

```
12-cursor-deploy-commit-guardrail/
├── SKILL.md                  # Gemini / Antigravity format (.agents/skills/)
├── .cursorrules              # Cursor format (alwaysApply: true)
├── copilot-instructions.md   # GitHub Copilot format
├── scripts/
│   └── check-deploy-tags.sh  # Bash script to test commit message tags
└── README.md                 # This didactic guide
```

---

## 🔧 How to Install

### In Cursor
Place in `.cursor/rules/`:
```bash
mkdir -p .cursor/rules
cp ai-coding-skills/12-cursor-deploy-commit-guardrail/.cursorrules .cursor/rules/deploy-commit-guardrail.mdc
```

### In GitHub Copilot
```bash
cat ai-coding-skills/12-cursor-deploy-commit-guardrail/copilot-instructions.md >> .github/copilot-instructions.md
```

---

## 🧪 Testing the Deployment Validator Script

The included script [`scripts/check-deploy-tags.sh`](./scripts/check-deploy-tags.sh) allows you to verify message parsing:

```bash
# Test message with deploy tags:
echo -e "feat(api): update logic\n\n#deployuat #auto" > /tmp/msg.txt
./ai-coding-skills/12-cursor-deploy-commit-guardrail/scripts/check-deploy-tags.sh /tmp/msg.txt
# Output:
# 🚢 Deploy tags detected: #deployuat #auto
# ✅ CI/CD will trigger automated UAT deployment.
```
