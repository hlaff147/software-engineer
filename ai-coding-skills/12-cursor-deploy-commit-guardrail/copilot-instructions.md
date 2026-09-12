# Deploy Commit Guardrail & Trigger for GitHub Copilot

## 1. Standard Commits
Before proposing or executing `git commit` for staged code changes:
- Always ask the user: "Deseja acionar o deploy (UAT) com este commit? (Sim / Não)"
- If the user confirms ("Sim"), append `#deployuat #auto` on a new line preceded by an empty line.
- If the user denies ("Não"), commit without the tags.

## 2. Empty Trigger Commits ("Commit No Content")
When the user asks to trigger a deployment without code changes ("commit no content", "commit vazio", "trigger deploy"):
- Execute an empty commit using `--allow-empty`:
  `git commit --allow-empty -m "ci: #deployuat #auto"`
- Immediately push to the current branch:
  `git push origin $(git branch --show-current)`

## 3. Strict Formatting Rules
- Tags must be strictly `#deployuat #auto` in lowercase.
- Empty commit message must be strictly `"ci: #deployuat #auto"`.
