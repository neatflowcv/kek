# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Rules

- `__init__.py` 사용 금지
- `__main__.py` 사용 금지, CLI는 `[project.scripts]` 사용

## Build and Run

This project uses `uv` as the package manager with Python 3.13.

```bash
# Run the application
uv run python main.py

# Install dependencies
uv sync
```
