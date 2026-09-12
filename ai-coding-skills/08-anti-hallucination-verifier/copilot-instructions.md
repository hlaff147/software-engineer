<🎯 Anti-Hallucination Verifier>
Enforce strict verification loops to prevent hallucinations.

## Rules
- ALWAYS read-before-write: NEVER edit or overwrite a file without reading at least the surrounding 50 lines of any edit target.
- ALWAYS perform signature verification: NEVER guess function signatures, method names, import paths, or class hierarchies. Read the source file or run type-check commands.
- NEVER use phantom APIs: DO NOT reference library methods, framework APIs, or third-party functions without verifying they exist in the installed version. Check documentation or run `--help`.
- ALWAYS run the build verification loop after making changes:
  - Java: `mvn test-compile` or `gradle compileJava`
  - Python: `ruff check .` and `python -c "import module"`
  - TypeScript: `npx tsc --noEmit`
  - Go: `go build ./...`
- ALWAYS run relevant tests after code changes. Fix them before declaring the task complete.
- NEVER emit placeholder code like `// ... rest of implementation here`, `// TODO: implement`, `# your code here`, or `/* ... existing code ... */`. Write COMPLETE, FUNCTIONAL code.
- NEVER truncate file output with `// ... remaining code unchanged`. Show the complete replacement block.
- ALWAYS verify imports resolve correctly after adding them. NEVER add imports from packages not in the dependency manifest.
- ALWAYS review the `git diff` before committing to ensure no unintended deletions, no formatting-only changes mixed with logic, and no stale references.

## Verification
- Build passes
- Tests pass
- `git diff` shows only intended changes
