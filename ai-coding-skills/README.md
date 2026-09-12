# 🧠 AI Coding Skills — 10 Production-Ready Skills for AI-Powered IDEs

> **A curated collection of 10 high-impact AI coding skills, each implemented in multiple IDE formats (Cursor, GitHub Copilot, Windsurf, Cline, Claude Code, Gemini/Antigravity).**

## 📖 What Are AI Coding Skills?

AI Coding Skills (also called "rules", "instructions", or "custom instructions") are structured instruction files that **teach AI coding agents how to behave** within your project. They transform a generic AI assistant into a **specialized pair programmer** that enforces your team's coding standards, catches anti-patterns, and follows your architectural decisions.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Code Editor (IDE)                       │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Your Code   │◄──►│   AI Agent   │◄──►│   Skills/    │      │
│  │  (.java,     │    │  (Copilot,   │    │   Rules      │      │
│  │   .py, .ts)  │    │   Cursor,    │    │  (SKILL.md,  │      │
│  │              │    │   Claude)    │    │  .cursorrules)│      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│                              │                                  │
│                              ▼                                  │
│                    ┌──────────────────┐                         │
│                    │  Better Code:    │                         │
│                    │  • Idiomatic     │                         │
│                    │  • Secure        │                         │
│                    │  • Tested        │                         │
│                    │  • Consistent    │                         │
│                    └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 The 10 Skills

| # | Skill | Category | Problem It Solves | IDE Formats |
|---|-------|----------|-------------------|-------------|
| 1 | [**Java Spring Boot 3 Standards**](./01-java-spring-boot-standards/) | 🟢 Language | Java 8 boilerplate, field injection, `javax.*` imports | 4 formats |
| 2 | [**Python Modern Standards**](./02-python-modern-standards/) | 🟢 Language | Legacy Python idioms, Pydantic v1, `os.path` | 4 formats |
| 3 | [**Next.js App Router**](./03-nextjs-app-router/) | 🔵 Framework | Pages Router confusion, `'use client'` everywhere | 4 formats |
| 4 | [**TDD & Unit Testing**](./04-tdd-unit-testing/) | 🟡 Workflow | Superficial happy-path tests, no edge cases | 4 formats |
| 5 | [**Security OWASP Guardrail**](./05-security-owasp-guardrail/) | 🔴 Security | SQL injection, hardcoded secrets, weak crypto | 4 formats |
| 6 | [**Conventional Commits**](./06-conventional-commits/) | 🟡 Workflow | Vague commit messages, PR descriptions without context | 4 formats |
| 7 | [**Memory Bank Continuity**](./07-memory-bank-continuity/) | 🟣 Meta-Agent | Agent amnesia between sessions | 4 formats |
| 8 | [**Anti-Hallucination Verifier**](./08-anti-hallucination-verifier/) | 🟣 Meta-Agent | Agents editing blind, hallucinating APIs, broken builds | 4 formats |
| 9 | [**REST API Contract-First**](./09-rest-api-contract-first/) | 🔵 Architecture | Inconsistent URLs, non-standard errors, ad-hoc pagination | 4 formats |
| 10 | [**Token Router Optimizer**](./10-token-router-optimizer/) | 🟣 Meta-Agent | 90% token waste reading large files | 4 formats |

---

## 📐 Anatomy of a Skill

Every skill in this collection follows the same structure, implemented in 4 IDE formats:

```
<skill-name>/
├── SKILL.md                  # Gemini / Antigravity format (.agents/skills/)
├── .cursorrules              # Cursor format (.cursor/rules/)
├── copilot-instructions.md   # GitHub Copilot (.github/copilot-instructions.md)
└── README.md                 # Didactic explanation with examples
```

### The SKILL.md Format (Gemini/Antigravity)

```yaml
---
name: skill-name              # Unique identifier (kebab-case)
description: >-               # CRITICAL: Agent reads this to decide activation
  When to use and what it does.
---
```

The body contains **dense, imperative instructions** — no conversational fluff:

```markdown
## Rules
- NEVER do X           ← Negative constraints (LLMs follow these well)
- ALWAYS do Y          ← Explicit requirements
- PREFER Z over W      ← Preference ordering

## Verification
- Run `mvn test`       ← Self-correction loop
- Check lint output
```

### Key Principles for Effective Skills

| Principle | Why It Works |
|-----------|-------------|
| **Negative Constraints** | LLMs follow "NEVER do X" better than "try to avoid X" |
| **Glob Scoping** | Load rules only when relevant files are open (saves context) |
| **Concrete Examples** | Bad → Good code pairs are more effective than abstract rules |
| **Verification Steps** | Self-correction loop catches >80% of hallucinations |
| **Information Density** | Skip preambles like "You are a helpful assistant..." |

---

## 🔧 Quick Start: How to Install Skills

### Cursor

```bash
# Option 1: Project-level scoped rules (recommended)
mkdir -p .cursor/rules
cp ai-coding-skills/01-java-spring-boot-standards/.cursorrules .cursor/rules/java-standards.mdc

# Option 2: Legacy single-file rules
cat ai-coding-skills/01-java-spring-boot-standards/.cursorrules >> .cursorrules
```

### GitHub Copilot

```bash
mkdir -p .github
cp ai-coding-skills/01-java-spring-boot-standards/copilot-instructions.md .github/copilot-instructions.md
```

### Windsurf (Codeium)

```bash
# Copy content to .windsurfrules at project root
cp ai-coding-skills/01-java-spring-boot-standards/.cursorrules .windsurfrules
```

### Cline / Roo Code

```bash
# Copy content to .clinerules at project root
cp ai-coding-skills/01-java-spring-boot-standards/.cursorrules .clinerules
```

### Claude Code

```bash
# Add to CLAUDE.md at project root
cat ai-coding-skills/01-java-spring-boot-standards/SKILL.md >> CLAUDE.md
```

### Gemini / Antigravity

```bash
# Copy the SKILL.md into .agents/skills/
mkdir -p .agents/skills/java-spring-boot-standards
cp ai-coding-skills/01-java-spring-boot-standards/SKILL.md .agents/skills/java-spring-boot-standards/
```

> 📖 For a complete portability guide across all IDEs, see [PORTABILITY.md](./PORTABILITY.md).

---

## 🗺️ IDE Format Comparison

| Feature | Cursor | Copilot | Windsurf | Cline | Claude Code | Gemini/AGY |
|---------|--------|---------|----------|-------|-------------|------------|
| **File** | `.cursor/rules/*.mdc` | `.github/copilot-instructions.md` | `.windsurfrules` | `.clinerules` | `CLAUDE.md` | `.agents/skills/*/SKILL.md` |
| **Frontmatter** | `description`, `globs`, `alwaysApply` | None | None | None | None | `name`, `description` |
| **Glob Scoping** | ✅ Native | ❌ | ❌ | ❌ | ❌ | ✅ Via description |
| **On-Demand Loading** | ✅ `alwaysApply: false` | ❌ Always loaded | ❌ Always loaded | ✅ Via modes | ❌ Always loaded | ✅ Progressive disclosure |
| **Multiple Files** | ✅ One per `.mdc` | ❌ Single file | ❌ Single file | ✅ With `.roomodes` | ❌ Single file | ✅ One per skill dir |
| **Subdirectories** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ scripts/, examples/ |

---

## 📊 Category Breakdown

### 🟢 Language Standards (Skills 1-2)
Skills that enforce modern idiomatic patterns for specific programming languages. Prevent agents from generating outdated syntax or legacy API usage.

### 🔵 Framework & Architecture (Skills 3, 9)
Skills that enforce framework-specific best practices and API design standards. Prevent common architectural mistakes and inconsistencies.

### 🟡 Workflow & Quality (Skills 4, 6)
Skills that improve the development workflow: testing practices, commit hygiene, and code review processes.

### 🔴 Security (Skill 5)
Skills that enforce security best practices based on OWASP Top 10. Catch vulnerabilities before they reach production.

### 🟣 Meta-Agent (Skills 7, 8, 10)
Skills that optimize the AI agent itself: memory across sessions, hallucination prevention, and token efficiency.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Coding Skills Ecosystem                   │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Language    │  │  Framework  │  │  Workflow   │            │
│  │  Standards   │  │  & Arch     │  │  & Quality  │            │
│  │             │  │             │  │             │            │
│  │ • Java 21+  │  │ • Next.js   │  │ • TDD       │            │
│  │ • Python    │  │ • REST API  │  │ • Commits   │            │
│  │   3.11+     │  │   Contract  │  │             │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
│         │                │                │                    │
│         └────────────────┼────────────────┘                    │
│                          │                                      │
│                          ▼                                      │
│              ┌───────────────────────┐                          │
│              │    Meta-Agent Layer   │                          │
│              │                       │                          │
│              │ • Memory Bank         │                          │
│              │ • Anti-Hallucination  │                          │
│              │ • Token Optimizer     │                          │
│              │ • Security Guardrail  │                          │
│              └───────────────────────┘                          │
│                          │                                      │
│                          ▼                                      │
│     ┌──────────────────────────────────────────────┐           │
│     │           Multi-IDE Portability               │           │
│     │  Cursor │ Copilot │ Windsurf │ Cline │ Claude │           │
│     └──────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 References & Credits

This collection was inspired by and built upon the work of the AI coding community:

| Source | Description |
|--------|-------------|
| [cursor.directory](https://cursor.directory) | Largest community directory with 1,000+ cursor rules |
| [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules) | Curated collection of production `.cursorrules` files |
| [Cline Memory Bank](https://github.com/cline/cline) | Original Memory Bank continuity pattern |
| [Roo Code Modes](https://github.com/RooVetGit/Roo-Code) | Role-based agent modes and test mode |
| [Conventional Commits](https://www.conventionalcommits.org/) | Commit message specification |
| [OWASP Top 10](https://owasp.org/www-project-top-ten/) | Web application security risks |
| [RFC 7807](https://datatracker.ietf.org/doc/html/rfc7807) | Problem Details for HTTP APIs |
| [agentic-token-optimization](../agentic-token-optimization/) | Token router & pre-tool hooks (this repo) |

---

## 🚀 Getting Started

1. **Browse the skills** — Each skill directory has a `README.md` explaining what it does and why
2. **Pick your format** — Choose the file format for your IDE (see [PORTABILITY.md](./PORTABILITY.md))
3. **Copy to your project** — Follow the Quick Start instructions above
4. **Customize** — Adapt the rules to your team's specific conventions
5. **Combine** — Mix multiple skills for comprehensive coverage

---

## 📝 Tech Stack

`Markdown` · `YAML Frontmatter` · `Bash` · `Python` · `Cursor Rules` · `GitHub Copilot Instructions` · `Windsurf Rules` · `Cline Rules` · `CLAUDE.md` · `SKILL.md (Gemini/Antigravity)`

---

## 📁 Directory Structure

```
ai-coding-skills/
├── README.md                              # This file
├── PORTABILITY.md                         # IDE portability guide
├── 01-java-spring-boot-standards/         # Java 21+ & Spring Boot 3
├── 02-python-modern-standards/            # Python 3.11+ & Pydantic v2
├── 03-nextjs-app-router/                  # Next.js App Router & RSC
├── 04-tdd-unit-testing/                   # TDD with AAA & mutation testing
├── 05-security-owasp-guardrail/           # OWASP Top 10 security rules
├── 06-conventional-commits/               # Git commits & PR descriptions
├── 07-memory-bank-continuity/             # Multi-session context memory
├── 08-anti-hallucination-verifier/        # Read-before-write guardrail
├── 09-rest-api-contract-first/            # REST API design standards
└── 10-token-router-optimizer/             # Token consumption optimization
```
