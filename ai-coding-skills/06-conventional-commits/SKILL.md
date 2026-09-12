---
name: conventional-commits
description: >-
  Enforces Conventional Commits format and meaningful PR descriptions. Activate when creating commits, writing commit messages, or generating pull request descriptions.
---

<🎯 Title>
Conventional Commits

## Rules
- Commit format: `<type>(<scope>): <short imperative description>`
- Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`
- Subject line: max 72 characters, imperative mood ("add" not "added" or "adds")
- Body (optional): explain WHY, not WHAT — the diff shows what changed
- Breaking changes: `feat!:` or `BREAKING CHANGE:` footer
- Scope examples: `feat(auth):`, `fix(payment):`, `refactor(api):`
- NEVER write vague messages: "updated code", "fixed bug", "WIP", "misc changes"
- PR description template:
  - **Motivation**: Why is this change needed?
  - **Solution**: What approach was taken and why?
  - **Key Changes**: Table of changed files with descriptions
  - **Testing**: How was this verified?
  - **Breaking Changes**: Any backward-incompatible changes?
- Atomic commits: each commit should represent ONE logical change
- NEVER commit commented-out code, debug prints, or TODO items without ticket references

## Verification
- Run `scripts/validate-commit-msg.sh` on pre-commit hook
