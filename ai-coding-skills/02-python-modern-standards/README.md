# Python Modern Standards

Enforces Python 3.11+ modern idioms, Pydantic v2, and quality tooling. Activate when writing or reviewing Python code.

## 🎯 Problem
Older Python code frequently uses outdated typing conventions, slow package management, and fragmented tools for linting and formatting.

## ✅ Solution
Use modern Python features (3.11+), unified tooling (Ruff, uv), and the latest schema validation frameworks (Pydantic v2).

### Examples

**BAD: `Union[str, int]`**
```python
from typing import Union
def process(data: Union[str, int]): ...
```

**GOOD: `str | int`**
```python
def process(data: str | int): ...
```

**BAD: `.dict()`**
```python
user_data = user.dict()
```

**GOOD: `.model_dump()`**
```python
user_data = user.model_dump()
```

**BAD: `os.path.join()`**
```python
import os
path = os.path.join('dir', 'subdir')
```

**GOOD: `Path() / 'subdir'`**
```python
from pathlib import Path
path = Path('dir') / 'subdir'
```

**BAD: mutable default**
```python
def process_items(items=[]): ...
```

**GOOD: immutable default**
```python
def process_items(items: list[str] | None = None): ...
```

## 📐 Anatomy of the skill
This skill ensures all Python development uses current best practices: clean typing without imports, fast rust-based tooling, immutable data structures, robust resource handling, and strict typing. 

## 🔧 How to install

### Cursor
Copy `.cursorrules` to the root of your repository.

### GitHub Copilot
Copy `copilot-instructions.md` to `.github/copilot-instructions.md`.

### Windsurf / Gemini
Use `SKILL.md` in your AI coding skills or custom instructions directory.

## 📊 Expected impact
- Cleaner, more readable syntax
- Much faster linting, formatting, and package resolution
- Less risk of state leaking through mutable defaults
- Safer refactoring due to precise type hints

## 🔗 References
- [Pydantic V2 Documentation](https://docs.pydantic.dev/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [cursor.directory/python](https://cursor.directory/)
