# 🔄 IDE Portability Guide — AI Coding Skills Across Editors

> How to use the same AI coding skill in **7 different IDEs and tools**.

---

## 📋 Format Mapping

Each skill in this collection is provided in 3 native formats. This guide shows how to adapt them to **any** AI-powered IDE.

| IDE / Tool | File Location | Format | Scoped? | Multiple Files? |
|------------|--------------|--------|---------|-----------------|
| **Cursor** | `.cursor/rules/<name>.mdc` | YAML frontmatter + Markdown | ✅ Glob patterns | ✅ One per `.mdc` |
| **Cursor (legacy)** | `.cursorrules` | Plain Markdown | ❌ | ❌ Single file |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Plain Markdown | ❌ | ❌ Single file |
| **Windsurf** | `.windsurfrules` | Plain Markdown | ❌ | ❌ Single file |
| **Cline** | `.clinerules` | Plain Markdown | ❌ | ✅ Via `.roomodes` |
| **Claude Code** | `CLAUDE.md` | Plain Markdown | ❌ | ❌ Single file |
| **Gemini / Antigravity** | `.agents/skills/<name>/SKILL.md` | YAML frontmatter + Markdown | ✅ Via description | ✅ One per directory |

---

## 🔧 Conversion Templates

### From `SKILL.md` → Cursor `.mdc`

The `SKILL.md` format (Gemini/Antigravity) converts to Cursor's scoped rules by adding `globs` and `alwaysApply`:

```yaml
# SKILL.md (source)
---
name: java-spring-boot-standards
description: >-
  Enforces modern Java 21+ and Spring Boot 3 standards.
---

# Java Spring Boot 3 Standards
- NEVER use @Autowired on fields...
```

```yaml
# .cursor/rules/java-standards.mdc (target)
---
description: Enforces modern Java 21+ and Spring Boot 3 standards.
globs: ["**/*.java", "**/pom.xml", "**/application*.yml"]
alwaysApply: false
---

# Java Spring Boot 3 Standards
- NEVER use @Autowired on fields...
```

**Key differences**:
- Replace `name` with `description` (Cursor uses description only)
- Add `globs` array with relevant file patterns
- Add `alwaysApply: false` (or `true` for meta-skills like security)
- Body content stays the same

---

### From `SKILL.md` → GitHub Copilot

Strip the frontmatter entirely. Copilot reads plain markdown:

```markdown
# Java Spring Boot 3 Standards

- NEVER use @Autowired on fields...
```

**Key differences**:
- Remove YAML frontmatter block (`---` delimiters)
- No scoping — all instructions apply globally
- If combining multiple skills, separate with `---` horizontal rules
- Place at `.github/copilot-instructions.md`

---

### From `SKILL.md` → Windsurf

Same as Copilot — strip frontmatter, save as `.windsurfrules`:

```markdown
# Java Spring Boot 3 Standards

- NEVER use @Autowired on fields...

---

# Python Modern Standards

- ALWAYS use Python 3.11+ union syntax...
```

**Key differences**:
- Single file at project root (`.windsurfrules`)
- Concatenate multiple skills with `---` separators
- No scoping mechanism — all rules always active

---

### From `SKILL.md` → Cline / Roo Code

For basic usage, strip frontmatter and save as `.clinerules`:

```markdown
# Java Spring Boot 3 Standards

- NEVER use @Autowired on fields...
```

For **role-based modes**, create `.roomodes`:

```json
{
  "customModes": [
    {
      "slug": "java-dev",
      "name": "Java Developer",
      "roleDefinition": "You enforce Java 21+ and Spring Boot 3 standards...",
      "groups": ["read", "edit", "command"],
      "customInstructions": "See .clinerules for detailed rules."
    },
    {
      "slug": "reviewer",
      "name": "Code Reviewer",
      "roleDefinition": "You review code for quality and security...",
      "groups": ["read"],
      "customInstructions": "Focus on OWASP and testing rules."
    }
  ]
}
```

---

### From `SKILL.md` → Claude Code

Strip frontmatter, append to `CLAUDE.md`:

```markdown
# Java Spring Boot 3 Standards

- NEVER use @Autowired on fields...
```

**Key differences**:
- Single `CLAUDE.md` at project root
- Supports `~/.claude/CLAUDE.md` for global rules
- Concatenate multiple skills into one file

---

## 📊 Feature Comparison Deep Dive

### Scoping Mechanisms

```
┌────────────────────────────────────────────────────────────────┐
│                     Scoping Strategies                         │
│                                                                │
│  Cursor (.mdc)         Gemini (SKILL.md)      Others           │
│  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐ │
│  │ globs:       │      │ description: │      │              │ │
│  │ ["**/*.java"] │      │ "Activate    │      │  No scoping  │ │
│  │              │      │  when writing │      │  All rules   │ │
│  │ alwaysApply: │      │  Java code"  │      │  always      │ │
│  │ false        │      │              │      │  active      │ │
│  └──────────────┘      └──────────────┘      └──────────────┘ │
│  Files trigger          Agent decides          Everything      │
│  rule loading           based on context       in context      │
└────────────────────────────────────────────────────────────────┘
```

### Loading Priority

| Priority | Cursor | Gemini/AGY |
|----------|--------|------------|
| 1 (Highest) | Project `.cursor/rules/` | Workspace `.agents/skills/` |
| 2 | User settings rules | `skills.json` declared |
| 3 | Legacy `.cursorrules` | Global `~/.gemini/config/` |
| 4 | — | Built-in skills |

### Context Window Impact

| Format | Token Cost | Strategy |
|--------|-----------|----------|
| `alwaysApply: true` | High — always in context | Use sparingly (security, anti-hallucination) |
| `alwaysApply: false` + globs | Low — loaded on demand | Best for language/framework skills |
| Gemini progressive disclosure | Low — only name+description loaded | Full content loaded on activation |
| Copilot/Windsurf/Claude single file | Medium — everything loaded | Keep total instructions concise |

---

## 🎯 Best Practices for Multi-IDE Projects

### 1. Choose a Canonical Format

Pick one format as your **source of truth** and generate others from it:

```
SKILL.md (canonical) ──► .cursorrules (generated)
                     ──► copilot-instructions.md (generated)
                     ──► .windsurfrules (generated)
```

### 2. Combine Skills Strategically

For single-file IDEs (Copilot, Windsurf, Claude), combine only the most relevant skills:

```markdown
<!-- .github/copilot-instructions.md -->

# Java Spring Boot 3 Standards
...rules...

---

# Security OWASP Guardrail
...rules...

---

# REST API Contract-First
...rules...
```

> ⚠️ **Token Budget**: Keep combined instructions under 2,000 words for single-file formats. Prioritize the most impactful rules.

### 3. Use Meta-Skills Globally

Skills 7 (Memory Bank), 8 (Anti-Hallucination), and 10 (Token Router) are **meta-skills** that apply regardless of language or framework. Set these to `alwaysApply: true` in Cursor, or include them in every combined file.

### 4. Scope Language Skills

Skills 1 (Java), 2 (Python), and 3 (Next.js) should only activate when relevant files are open. In Cursor, use appropriate `globs`. For other IDEs, only include the language skill relevant to your project.

---

## 📚 Additional Resources

- [Cursor Rules Documentation](https://docs.cursor.com/context/rules-for-ai)
- [GitHub Copilot Custom Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)
- [Windsurf Rules Guide](https://docs.codeium.com/windsurf/customization)
- [Cline Custom Instructions](https://github.com/cline/cline)
- [Claude Code CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code)
- [Gemini Antigravity Skills Guide](https://cloud.google.com/gemini/docs)
