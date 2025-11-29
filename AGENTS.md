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

### Environment Verification Protocol (MANDATORY)
**Before installing any packages**, verify environment:
```bash
which uv && uv --version  # Confirm uv is available
test -d .venv             # Confirm venv exists
source .venv/bin/activate # Activate venv
uv pip install <package>  # Now safe to install
```
**Never** install to system Python. **Always** verify environment first.
**Rationale**: Prevents "wrong Python" environment issues and system pollution.
**Evidence**: Phase 1.1 environment protocol prevented installation errors.

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

## Sub-Agent Development & Validation
When using sub-agents or parallel task execution, **always validate outputs** with language-specific checks before accepting as complete.

### Python Validation Checklist (MANDATORY)
Before accepting sub-agent Python code:
- [ ] **Class methods** have `self` as first parameter
- [ ] **Type hints** present on all function/method signatures (mypy strict compliance)
- [ ] **Pydantic v2** validation patterns used (no auto-coercion assumptions: `{"id": "123"}` not `{"id": 123}`)
- [ ] **Docstrings** follow Google style (Args/Returns/Raises sections with examples)
- [ ] **Test patterns** follow Arrange-Act-Assert structure
- [ ] **Imports** organized correctly (stdlib → third-party → local)
- [ ] **Async patterns** use `async`/`await` correctly (no blocking calls in async functions)

**Why This Matters**: Sub-agents optimize for speed but may miss language-specific patterns.
**Evidence**: Phase 1.1 sub-agent generated 184 test methods without `self` parameter → all tests failed initially.

### Validation Process
1. **Generate**: Sub-agent creates code in parallel
2. **Review**: Apply language-specific checklist
3. **Fix**: Address any validation failures
4. **Quality Gate**: Run mypy/ruff/pytest before accepting
5. **Complete**: Mark task complete only after all gates pass

## Commit & Pull Requests
- Use clear, scoped commits; Conventional Commits style is preferred (e.g., `feat: add status tool`).
- PRs must include: summary, rationale, test coverage notes, and any config changes.
- Link related issues; add screenshots or sample CLI output when behavior changes.
- Branching: use feature branches only; do not push directly to `main`.
- CI-friendly: ensure `ruff`, `mypy`, and `pytest` all pass locally before opening.

### Quality Gate Integration (MANDATORY)
**Before committing or marking tasks complete**, run ALL quality gates:
```bash
source .venv/bin/activate
python -m mypy src/            # Type coverage: 100% required
ruff check src/                # Code quality: 0 violations required
ruff format --check .          # Formatting: 100% compliance
pytest -q                      # Tests: 100% pass rate
pytest --cov=src --cov-report=term-missing  # Coverage: ≥90% for new code
```
**ALL gates must pass** before marking work "completed" or opening PR.
**Rationale**: Prevents backtracking to fix quality issues after claiming completion.
**Evidence**: Phase 1.1 marked "complete" without quality gates → 1.5 hours lost fixing 29 violations.

## Security & Configuration
- Do not commit secrets. Use `.env` with: `WORLD_ANVIL_APP_KEY`, `WORLD_ANVIL_USER_TOKEN` (optional `WORLD_ANVIL_API_BASE`).
- Validate presence of required env vars; handle missing config gracefully.
