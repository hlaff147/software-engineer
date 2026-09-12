---
name: python-modern-standards
description: >-
  Enforces Python 3.11+ modern idioms, Pydantic v2, and quality tooling. Activate when writing or reviewing Python code.
---
# 🎯 Python Modern Standards

Enforces Python 3.11+ modern idioms, Pydantic v2, and quality tooling.

## Rules
- ALWAYS use Python 3.11+ syntax: `X | Y` union types (not `Union[X, Y]`), `Self`, `Annotated`.
- ALWAYS use Pydantic v2 conventions: `.model_dump()` (not `.dict()`), `.model_validate()` (not `.parse_obj()`), `model_config = ConfigDict(...)` (not inner `class Config`).
- ALWAYS use `pathlib.Path` exclusively (ban `os.path.join()`, `os.path.exists()`).
- ALWAYS use `ruff` for linting/formatting (not flake8+black+isort separately).
- ALWAYS use `uv` for package management when possible.
- ALWAYS use type hints on ALL function signatures — NEVER use bare `dict` or `list` without type parameters.
- ALWAYS use `@dataclass(frozen=True, slots=True)` for simple value objects.
- ALWAYS put `from __future__ import annotations` at the top of every module.
- ALWAYS use the `logging` module with `structlog` patterns (not `print()` for debugging).
- NEVER use mutable default arguments (`def f(x=[])` → `def f(x: list | None = None)`).
- ALWAYS prefer f-strings over `.format()` or `%` formatting.
- ALWAYS use context managers for resource handling (`with open(...)`, `async with session`).
- ALWAYS use explicit `__all__` in public module APIs.

## Verification
- Run `ruff check .` to check for lint errors.
- Run `ruff format --check .` to verify formatting.
- Run `pytest` to ensure tests pass.
