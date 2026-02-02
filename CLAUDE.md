# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Rules

- `__init__.py` 사용 금지
- `__main__.py` 사용 금지, CLI는 `[project.scripts]` 사용
- 글로벌 변수 사용 금지

## Python

린팅/포맷팅: `uvx ruff check --fix && uvx ruff format`

Python 코드 수정 후 반드시 통과해야 함.

## Markdown

포맷팅: `bunx -bun markdownlint-cli2 --fix "*.md" "docs/**/*.md"`

lint 실패 시 자동으로 수정할 것.

## Commit Convention

형식: `type: 한국어 설명`

커밋은 논리적 단위로 최대한 나눠서 할 것.

타입:

- `feat`: 새 기능 추가
- `fix`: 버그 수정
- `refactor`: 리팩토링
- `docs`: 문서 변경
- `chore`: 기타 변경

## Build and Run

This project uses `uv` as the package manager with Python 3.13.

```bash
# Run the application
uv run main.py

# Install dependencies
uv sync
```
