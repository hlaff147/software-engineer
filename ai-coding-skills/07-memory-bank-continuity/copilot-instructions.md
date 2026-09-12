<🎯 Title>
Memory Bank Continuity

## Rules
- On SESSION START, read these 5 files in order (if they exist):
  1. `memory-bank/projectbrief.md` — Core mission, scope, success criteria
  2. `memory-bank/systemPatterns.md` — Architecture decisions, design patterns, component relationships
  3. `memory-bank/techContext.md` — Tech stack, versions, dependencies, build commands
  4. `memory-bank/activeContext.md` — Current focus, recent changes, active decisions
  5. `memory-bank/progress.md` — What works, what's left, known blockers
- On SESSION END (or after significant milestones), UPDATE:
  - `activeContext.md` with what was accomplished and what's next
  - `progress.md` with completed items and remaining work
- On ARCHITECTURE CHANGES, UPDATE:
  - `systemPatterns.md` with new patterns or modified decisions
  - `techContext.md` if stack/dependencies changed
- NEVER assume context from previous sessions without reading memory bank files
- NEVER overwrite memory bank files entirely — append or update specific sections
- Keep each file concise (< 200 lines) — link to detailed docs if needed
- Use consistent date stamps in `activeContext.md` entries: `## [YYYY-MM-DD] Session Title`

## Verification
- Check that `memory-bank/` directory exists, all 5 files present, `activeContext.md` has today's date
