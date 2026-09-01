---
name: memory-bank
description: >-
  Use this skill to inspect, query, or update the repository memory bank (.agents/MEMORY.md).
  Active when adding new projects, retiring components, or retrieving high-level architectural
  metadata across the codebase.
---

# 🧠 Memory Bank Management Skill

This skill guides the agent in maintaining the repository's long-term memory bank located at `.agents/MEMORY.md`.

---

## 📌 Memory Bank Responsibilities

The Memory Bank serves as the centralized source of truth for:
1. Complete inventory of all projects, subservices, and study modules.
2. Accurate categorization of each project (AI/ML, Backend APIs, Open Finance, Event Streaming, Database, Testing, Observability, Study Guides).
3. Primary tech stack and runtime requirements per module.
4. Status and existence of local `README.md` files.

---

## 🛠️ Operations

### 1. Querying Project Metadata
- Read [.agents/MEMORY.md](../../MEMORY.md) to quickly understand the role of any module without having to traverse its source files.

### 2. Registering a New Project
When a new project is created in the repository:
1. Add a new row to the inventory table in `.agents/MEMORY.md`:
   ```markdown
   | [`<folder-name>/`](../<folder-name>) | <Category> | <Tech Stack> | ✅ Active | ✅ Yes | <Brief Description> |
   ```
2. Increment the corresponding count in the "Category Summary & Project Counts" section.
3. Trigger the `doc-sync` skill to update the main `README.md`.

### 3. Updating an Existing Project
When a project's stack or capabilities change:
1. Modify the corresponding row in `.agents/MEMORY.md`.
2. Ensure the local `README.md` reflects the changes.
3. Trigger the `doc-sync` skill to sync the main `README.md`.
