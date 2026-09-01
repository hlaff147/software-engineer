# 🤖 Project Rules & Agent Instructions — Software & AI Engineer Portfolio

Welcome to the **Software & AI Engineer Portfolio** repository (`software-engineer`).
This file provides mandatory operating rules and guidance for any AI coding agent operating in this repository.

---

## 🎯 Repository Purpose & Architecture

This repository is a curated collection of production-ready software engineering, AI/ML, distributed systems, system design, and study guides maintained by Humberto Filho ([@hlaff147](https://github.com/hlaff147)).

### 📂 Root Directory Invariant
> [!IMPORTANT]
> **Strict Root Policy**: The root of the repository must contain **ONLY** configuration files and top-level entrypoints:
> - `README.md` (Main portfolio showcase)
> - `.gitignore` (Git ignore rules)
> - `GEMINI.md` (This agent instructions file)
> - Subdirectories for individual projects, study modules, and `.agents/`
>
> **NEVER** create loose `.md`, `.txt`, `.java`, `.py` or other files directly in the repository root. Always place them inside a corresponding project directory or create an appropriate folder (e.g. `ai-engineer/`, `java-developer/`).

---

## 🔄 Documentation Synchronization Rules

Whenever you make any of the following changes:
1. **Adding a new project or study guide folder**
2. **Deleting or renaming an existing folder**
3. **Modifying an existing project's core architecture, tech stack, or public API**

You **MUST**:
1. Update `.agents/MEMORY.md` with the latest metadata (name, category, stack, status, description).
2. Ensure the sub-project has its own local `README.md` with standard sections (Overview, Architecture, Tech Stack, How to Run).
3. Update the root [README.md](./README.md):
   - **Repository Highlights table** (ensure accurate project counts per category).
   - **Study Guides & Documentation table** (if applicable).
   - **Showcase section** (add/update project details, architecture diagrams, and features).
   - **Architecture & Design Patterns table** (if new patterns are demonstrated).
   - **Complete Tech Stack diagram/table** (if new libraries or tools are used).
   - **Repository Structure ASCII tree** (reflect the exact file structure).

---

## 📐 Coding & Project Standards

1. **Naming Conventions**:
   - Subdirectories should use `kebab-case` (e.g., `ai-engineer`, `api-versioning`, `open-finance`). Existing legacy names (`userApi`, `study_interview_system_design`, `hedge_fund_bot`) are preserved.
2. **Language Conventions**:
   - Repository-wide documentation, project READMEs, and technical summaries should default to **English** (en-US).
   - Interview preparation and study guides may be written in Brazilian Portuguese (**pt-BR**) as designated in their respective headers.
3. **Documentation Integrity**:
   - Preserve existing comments, tests, and documentation unless explicitly refactoring.
   - Always verify that relative links inside Markdown files point to valid, existing paths.

---

## 🧠 Memory Bank & Skills

- Detailed project catalog & state: [.agents/MEMORY.md](./.agents/MEMORY.md)
- Documentation sync workflow: [.agents/skills/doc-sync/SKILL.md](./.agents/skills/doc-sync/SKILL.md)
- Memory bank management workflow: [.agents/skills/memory-bank/SKILL.md](./.agents/skills/memory-bank/SKILL.md)
- Documentation formatting standards: [.agents/rules/documentation-standards.md](./.agents/rules/documentation-standards.md)
