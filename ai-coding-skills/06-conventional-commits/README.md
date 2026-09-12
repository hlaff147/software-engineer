# Conventional Commits

## 🎯 Problem
Inconsistent, vague commit messages make it difficult to understand project history, generate changelogs, or identify where a bug was introduced.

**Bad Examples:**
```text
updated code
```
```text
fixed bug in login
```
```text
WIP
```

## ✅ Solution
Use Conventional Commits format to provide clear, machine-readable, and structured history.

**Good Examples:**
```text
feat(auth): add JWT authentication
```
```text
fix(payment): resolve missing Stripe token issue
```
```text
docs(readme): update installation steps
```

## 📐 Anatomy of the skill
The skill defines strict rules for commit messages:
- A specific structure `<type>(<scope>): <subject>`
- Enforced types (`feat`, `fix`, `chore`, etc.)
- Length constraints (max 72 characters for subject)
- Best practices like atomic commits and PR templates.

## 🔧 How to install
- **Git Hooks**: Copy `scripts/validate-commit-msg.sh` to `.git/hooks/commit-msg` and make it executable (`chmod +x`).
- **Gemini/Antigravity**: Place `SKILL.md` in your AI coding skills directory.
- **Cursor**: Copy `.cursorrules` into the root of your project.
- **GitHub Copilot**: Save `copilot-instructions.md` as `.github/copilot-instructions.md`.

## 📊 Expected impact
- Automated changelog generation.
- Clearer commit history for debugging (`git bisect`).
- Standardized pull requests with detailed descriptions.

## 🔗 References
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
