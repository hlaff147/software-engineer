---
name: token-router-optimizer
description: >-
  Optimizes AI agent token consumption by intercepting large file reads and delegating to lightweight workers. Activate when working in large codebases where files exceed 350 lines.
---
<🎯 Token Router Optimizer>
Optimize context windows by delegating large files to lightweight bulk reader workers.

## Rules
- ALWAYS intercept large file reads: When answering conceptual questions, architecture mapping, or dependency analysis on files with > 350 lines, NEVER read the entire file with native tools.
- ALWAYS delegate to a bulk reader: Invoke a lightweight worker model to read and synthesize large files into dense bullet points:
  `python3 scripts/pre-tool-hook.py read --paths <file> --question "<your question>"`
- ALWAYS delegate boilerplate generation: When generating test files, DTOs, stubs, or repetitive boilerplate, delegate to a code-writer worker:
  `python3 scripts/pre-tool-hook.py write --spec "<requirements>" --reference <style_file> --target <output_path>`
- PREFER targeted reads: Native file reading tools are reserved for surgical edits where you specify `StartLine`/`EndLine` covering < 350 lines.
- ALWAYS respect context budgets: Before reading multiple files, estimate total lines. If > 1000 lines combined, use bulk reader delegation.
- ALWAYS adhere to the dense output contract: Worker output must be raw bullet points with class/method/line references, zero preamble, and strictly scoped to the question asked.
- NEVER dump boilerplate: If generated code is > 100 lines, write directly to disk instead of displaying in the chat window.

## Verification
- Monitor context window usage
- Verify worker scripts are available at `scripts/pre-tool-hook.py`
