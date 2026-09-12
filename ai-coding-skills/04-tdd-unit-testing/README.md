# TDD & Unit Testing Skill

This skill enforces rigorous test-driven development, encouraging explicit AAA patterns, edge case coverage, and strict mocking rules.

## 🎯 Problem
Superficial tests pass and give developers a false sense of security without actually catching bugs or protecting against refactoring regressions. Tautological tests pass simply because they are executed.

## ✅ Solution
Implement test suites using mutation testing mindsets, strict structural boundaries, robust data factory patterns, and precise assertions.

See `examples/bad-test.java` and `examples/good-test.java` for concrete comparisons.

## 📐 Anatomy of the skill
- Mandates Arrange-Act-Assert (AAA) layout formatting.
- Explicit requirement for Negative paths (nulls, empties, bounds).
- Prevents mocking the System Under Test.
- Mandates high-quality assertion frameworks (AssertJ, etc).
- Prohibits disabling tests without an explicit JIRA/Ticket number.

## 🔧 How to install

### 1. Cursor
Copy `.cursorrules` to the root of your repository.

### 2. GitHub Copilot
Copy `copilot-instructions.md` to `.github/copilot-instructions.md`.

### 3. Gemini / Antigravity
Add `SKILL.md` to your skills directory.

## 📊 Expected impact
- Higher confidence in test suite integrity.
- Increased detection of regressions during refactors.
- Greater clarity in test failures because of explicitly named behaviors.

## 🔗 References
- Roo Code test mode
- mutation-testing project in this repo
