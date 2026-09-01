---
name: doc-sync
description: >-
  Use this skill whenever files or folders are added, deleted, or reorganized in the repository,
  or when the user requests to synchronize, update, or audit the root README.md, subproject READMEs,
  or the project memory bank.
---

# 🔄 Documentation Synchronization Skill

This skill defines the step-by-step workflow for keeping all repository documentation, README files, and the agent memory bank in sync.

---

## 📋 Synchronization Workflow

Follow these steps sequentially:

### Step 1: Scan Workspace and Audit against Memory Bank
1. Read [.agents/MEMORY.md](../../MEMORY.md) to inspect the known inventory of modules.
2. List top-level directories in the repository:
   - Identify any **new directories** not yet in `MEMORY.md`.
   - Identify any **removed directories** still present in `MEMORY.md`.
   - Identify any **renamed directories**.
3. Verify the root directory invariant: ensure **NO** loose `.md`, `.txt`, `.java`, or `.py` files exist in the root other than `README.md`, `.gitignore`, and `GEMINI.md`.

### Step 2: Ensure Local Project Documentation
For every directory listed in the inventory:
1. Verify that `README.md` exists locally inside that folder.
2. If `README.md` is missing, create one adhering to [.agents/rules/documentation-standards.md](../../rules/documentation-standards.md).
3. Check for broken relative links inside the local `README.md` (e.g., links to missing folders or missing files).

### Step 3: Update the Memory Bank
1. Update [.agents/MEMORY.md](../../MEMORY.md) with any newly added, removed, or updated projects.
2. Recalculate and update the category counts in the "Category Summary & Project Counts" section.

### Step 4: Synchronize the Root `README.md`
Update [README.md](../../../README.md) to reflect all changes:
1. **Repository Highlights table**: Ensure project counts per category match the memory bank exactly.
2. **Study Guides table**: Ensure all study modules are listed and properly linked.
3. **Showcase sections**: Ensure all projects have a dedicated showcase section with architecture diagram, patterns, tech stack, and key features.
4. **Architecture & Design Patterns summary table**: Add entries for any new design patterns introduced.
5. **Tech Stack summary table**: Ensure all programming languages, frameworks, brokers, databases, and test tools are represented.
6. **Repository Structure ASCII tree**: Keep the tree diagram matching the exact directory layout.

### Step 5: Verification & Validation
1. Verify that all relative links in `README.md` point to existing paths.
2. Verify that `git status` reflects only intended documentation changes.
