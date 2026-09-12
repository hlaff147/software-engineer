# Memory Bank Continuity

## 🎯 Problem
AI coding agents often suffer from "amnesia" between sessions. When you start a new conversation, the AI forgets the project's architecture, past decisions, and current progress, leading to repeated questions or broken code.

## ✅ Solution
Use a Memory Bank—a dedicated directory containing concise files that the AI agent reads at the start of every session and updates at the end of the session.

**Before:**
AI: "What tech stack are we using? How is the database structured?" (Wastes time and context tokens).

**After:**
AI reads `memory-bank/techContext.md` and `memory-bank/systemPatterns.md` on initialization.
AI: "I see we are using Node.js and PostgreSQL. Picking up from your last session on the payment gateway, I'll start implementing the Stripe webhooks."

## 📐 Anatomy of the skill
The skill defines 5 core files:
1. `projectbrief.md`: Core mission and scope.
2. `systemPatterns.md`: Architecture and design patterns.
3. `techContext.md`: Tech stack and dependencies.
4. `activeContext.md`: Current focus and session logs.
5. `progress.md`: Completed features and pending items.

The rules dictate reading these at the start and updating them incrementally at the end of a session.

## 🔧 How to install
- **Initialization**: Copy `resources/memory-bank-template.md` contents into a `memory-bank/` directory.
- **Gemini/Antigravity**: Place `SKILL.md` in your AI coding skills directory.
- **Cursor**: Copy `.cursorrules` into the root of your project.
- **GitHub Copilot**: Save `copilot-instructions.md` as `.github/copilot-instructions.md`.

## 📊 Expected impact
- Zero context loss between chat sessions.
- Faster onboarding for AI agents and human developers alike.
- Automated progress tracking.

## 🔗 References
- Cline/Roo Code community pattern (Memory Bank)
