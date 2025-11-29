# Repository Guidelines

## Project Structure & Modules
- Source code lives in `src/world_anvil_mcp/` (entry: `server.py`).
- Package name: `world_anvil_mcp`; console script: `world-anvil-mcp`.
- Tests in `tests/` (place unit tests as `tests/test_*.py`).
- Docs and planning in `docs/` and `claudedocs/`; OpenAPI at `openapi.yml`.
- Configuration via `.env` (see `.env.example`).

## Environment Setup (uv + venv)
- Install uv (one-time): `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv`).
- Create project-local venv: `uv venv --python 3.11 .venv`.
- Activate: macOS/Linux `source .venv/bin/activate`; Windows PowerShell `.venv/Scripts/Activate.ps1`.
- Install dev deps: `uv pip install -e .[dev]`.
- Tip: Use `uv run <cmd>` to run tools without activating (e.g., `uv run ruff check .`).

## Build, Test, and Development
- Create env and install (dev):
  - `uv pip install -e .[dev]` or `pip install -e .[dev]`
- Run server locally:
  - `world-anvil-mcp` or `python -m world_anvil_mcp.server`
- Lint & type-check:
  - `ruff format .` then `ruff check .` (line length 100) and `mypy src` (strict)
- Tests & coverage:
  - `pytest -q` and `pytest --cov=src --cov-report=term-missing`
- Build artifact (optional):
  - `python -m build` (requires `build` package) or `hatch build`

## Coding Style & Naming
- Python 3.11; prefer type hints everywhere; pass `mypy --strict`.
- Ruff rules enabled: `E,F,I,N,W,UP`; imports sorted by ruff/isort; 100-char lines.
- Naming: `snake_case` functions/modules, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.
- Public APIs live under `world_anvil_mcp.api` or `server` tools/resources; keep I/O at edges.
- Public APIs should include Google-style docstrings with Args/Returns/Raises and examples.

## Testing Guidelines
- Use `pytest` (async supported via `pytest-asyncio`).
- Name tests `test_<unit>.py`; mirror module paths when practical.
- Prefer small, isolated unit tests; add async tests for coroutine tools.
- Use markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.e2e` (skip e2e in CI).
- Coverage targets: ≥85% overall, ≥90% for core client modules; include env/config edge cases.

## Commit & Pull Requests
- Use clear, scoped commits; Conventional Commits style is preferred (e.g., `feat: add status tool`).
- PRs must include: summary, rationale, test coverage notes, and any config changes.
- Link related issues; add screenshots or sample CLI output when behavior changes.
- Branching: use feature branches only; do not push directly to `main`.
- CI-friendly: ensure `ruff`, `mypy`, and `pytest` all pass locally before opening.

## Security & Configuration
- Do not commit secrets. Use `.env` with: `WORLD_ANVIL_APP_KEY`, `WORLD_ANVIL_USER_TOKEN` (optional `WORLD_ANVIL_API_BASE`).
- Validate presence of required env vars; handle missing config gracefully.
