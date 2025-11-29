# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**World Anvil MCP Server** - An MCP (Model Context Protocol) server that bridges Claude Code with the World Anvil API for AI-assisted D&D campaign management and worldbuilding.

**Status**: Phase 0.4 (Early Implementation) — Architecture complete; core scaffolding in progress
**License**: BSD 3-Clause
**Python**: 3.11+ required

---

## Architecture

### Core Design Principles

1. **MCP-Native**: Built-in FastMCP Context integration (not bolted on)
2. **Async-First**: All I/O uses async/await with httpx.AsyncClient
3. **Type-Safe**: Pydantic v2 models for all API responses
4. **Resilient**: Built-in retry logic, rate limiting, and caching
5. **Workflow-Driven**: Designed for 10 specific D&D campaign workflows (see `docs/workflows/`)

### Component Architecture

```
MCP Server (FastMCP)
  └─> WorldAnvilClient (main entry point)
       ├─> Endpoint Classes (ArticleEndpoint, WorldEndpoint, etc.)
       │    └─> BaseEndpoint (generic request handling)
       │         ├─> ResponseCache (TTL-based caching)
       │         ├─> RateLimiter (token bucket, 60 req/min)
       │         └─> Retry Logic (tenacity with exponential backoff)
       └─> httpx.AsyncClient (connection pooling, timeout management)
```

**Key Pattern**: The client delegates to specialized endpoint classes (15+ endpoints planned), each inheriting from `BaseEndpoint[T]` generic that handles:
- Request execution with MCP Context logging
- Automatic retries for transient failures (RateLimitError, ServerError)
- Response caching with granularity-aware keys
- Error parsing and exception mapping

### Critical Implementation Details

**Authentication**: World Anvil uses custom headers (NOT Bearer tokens):
```python
headers = {
    "x-auth-token": user_token,      # Lowercase, not X-Auth-Token
    "x-application-key": app_key,    # Lowercase, not X-Application-Key
}
```

**Granularity**: Must be passed as STRING, not integer:
```python
# ✅ Correct
params = {"granularity": "2"}

# ❌ Wrong
params = {"granularity": 2}  # API will reject
```

**Pagination**: World-scoped list endpoints use POST (not GET) with JSON body:
```python
# List articles in world
response = await client.post(
    f"/world/{world_id}/articles",
    json={"limit": 50, "offset": 0}
)
```

**Write Operations**: Base endpoints support CRUD via PUT/PATCH/DELETE:
- PUT: Create new resource
- PATCH: Update existing resource
- DELETE: Remove resource

---

## Development Commands

### Environment Management (uv + venv)

Use a project-local virtual environment at `.venv` managed by uv. Do not use system Python.

```bash
# Create and activate venv
uv venv --python 3.11 .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Install with dev extras
uv pip install -e .[dev]

# Optional: run without activation
uv run ruff check . && uv run mypy src && uv run pytest -q
```

### Setup

```bash
# Install dependencies with uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code (auto-fix)
ruff format .

# Lint (auto-fix where possible)
ruff check --fix .

# Type check (strict mode)
mypy src/

# Run all quality checks
ruff format . && ruff check . && mypy src/
```

### Testing

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Run only unit tests (fast, no I/O)
pytest -m unit

# Run only integration tests (mocked API)
pytest -m integration

# Run specific test file
pytest tests/test_client.py

# Run specific test function
pytest tests/test_client.py::test_client_initialization

# Run with verbose output
pytest -v

# Skip end-to-end tests (require live API credentials)
pytest -m "not e2e"
```

**Coverage Requirement**: ≥85% overall, ≥90% for core client

### Running the Server

```bash
# Start MCP server
world-anvil-mcp

# Or run directly
python -m world_anvil_mcp.server
```

---

## Quality Standards

### Code Style

- **Line length**: 100 characters
- **Docstrings**: Google style, required for all public APIs
- **Type hints**: Required for all public functions/methods (mypy strict mode)
- **Imports**: Organized by ruff's isort (stdlib → third-party → local)

### Testing Strategy

Three test levels (use pytest markers):

1. **Unit** (`@pytest.mark.unit`): Fast (<100ms), no I/O, test components in isolation
2. **Integration** (`@pytest.mark.integration`): Mocked HTTP (respx), test component interactions
3. **E2E** (`@pytest.mark.e2e`): Live API, requires credentials, skip in CI

**Mock Patterns**:
- HTTP mocking: Use `respx` for httpx calls
- MCP Context: Use `AsyncMock` from unittest.mock
- Test data: Use `Faker` with deterministic seeds

### Documentation

Every public API needs:
- Comprehensive Google-style docstring
- Args/Returns/Raises sections
- Example usage in docstring
- Type hints on all parameters and returns

Example:
```python
async def get_article(self, article_id: str, granularity: str = "1") -> Article:
    """Retrieve a single article by ID.

    Args:
        article_id: Unique identifier for the article.
        granularity: Detail level as string ("-1", "0", "1", "2", "3").
            Higher values return more detail. Defaults to "1".

    Returns:
        Article object with details based on granularity level.

    Raises:
        NotFoundError: Article does not exist.
        AuthenticationError: Invalid credentials.
        RateLimitError: Rate limit exceeded (60 req/min).

    Example:
        >>> article = await client.articles.get("abc123", granularity="2")
        >>> print(f"{article.title}: {article.content}")
    """
```

---

## Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `mcp` | ≥1.0.0 | Official MCP SDK (https://github.com/modelcontextprotocol/python-sdk) |
| `httpx` | ≥0.27.0 | Async HTTP client |
| `pydantic` | ≥2.0.0 | Data validation and serialization |
| `tenacity` | ≥8.0.0 | Retry logic with exponential backoff |
| `cachetools` | ≥5.0.0 | TTL cache implementation |
| `pytest` | ≥8.0.0 | Testing framework |
| `respx` | ≥0.20.0 | HTTP mocking for tests |
| `ruff` | Latest | Formatting and linting |
| `mypy` | ≥1.8.0 | Type checking (strict mode) |

**Always use latest stable versions** when adding new dependencies.

---

## Project Structure

Target structure (some modules are not yet committed during Phase 0.4):

```
src/world_anvil_mcp/
├── server.py              # MCP server entry point (FastMCP)
├── client.py              # WorldAnvilClient main class
├── endpoints/             # Endpoint implementations
│   ├── base.py           # BaseEndpoint generic
│   ├── articles.py       # ArticleEndpoint
│   ├── worlds.py         # WorldEndpoint
│   └── ...               # 15+ endpoint classes
├── models/               # Pydantic response models
│   ├── article.py
│   ├── world.py
│   └── ...
├── exceptions.py         # Custom exception hierarchy
├── cache.py             # ResponseCache implementation
└── rate_limit.py        # RateLimiter implementation

tests/
├── conftest.py          # Shared fixtures
├── test_client.py       # WorldAnvilClient tests
├── endpoints/
│   ├── conftest.py     # Endpoint-specific fixtures
│   ├── test_articles.py
│   └── ...
└── models/
    ├── test_article.py
    └── ...

docs/
├── specs/               # Architecture and tool specifications
├── workflows/           # 10 D&D campaign workflow examples
├── quality/             # Code quality and testing standards
└── research/            # API analysis and design decisions
```

---

## Important Documentation

### Must-Read Before Implementation

1. **`docs/specs/client-architecture.md`** - Complete client architecture design
2. **`docs/specs/tool-specifications.md`** - All 34 MCP tools with Pydantic models
3. **`docs/quality/api-client-patterns.md`** - Async patterns, MCP Context integration, CRUD operations
4. **`docs/research/pywaclient-analysis.md`** - World Anvil API quirks and patterns

### Workflow References

See `docs/workflows/` for 10 detailed D&D campaign workflows:
- Session Note-Taking (WF-002) - Real-time during play, <500ms response requirement
- NPC Generation (WF-003)
- Quick NPC Lookup (WF-005) - Session-critical, cache-heavy

**Design Priority**: Session-time operations must be fast. Pre-cache frequently accessed content.

---

## World Anvil API Quirks

**From pywaclient analysis** (`docs/research/pywaclient-analysis.md`):

1. **Success Flag Pattern**: Some 200 OK responses include `{"success": false, "error": "..."}` - must check both status code AND success flag

2. **Nested ID Objects**: Filters use nested objects, not direct IDs:
   ```python
   # ✅ Correct
   {"categoryId": {"id": "123"}}

   # ❌ Wrong
   {"categoryId": "123"}
   ```

3. **Granularity Values**: String "-1", "0", "1", "2", "3" (not integers 0-2)

4. **Rate Limiting**: 60 requests per minute, implement token bucket algorithm

5. **Authentication Headers**: Lowercase `x-auth-token` and `x-application-key` (not capitalized)

---

## Environment Variables

Required for development:

```env
WORLD_ANVIL_APP_KEY=your_application_key
WORLD_ANVIL_USER_TOKEN=your_user_token
```

Get credentials from: https://www.worldanvil.com/api-keys

**Security**: Never commit `.env` file or hardcode credentials.

---

## Git Workflow

- **License**: BSD 3-Clause (see LICENSE)
- **Author**: Steven Peterson (not Scott Peterson - corrected in Phase 0)
- **Branches**: Feature branches only, never work on main
- **Commits**: Meaningful messages, incremental commits

---

## Quality Gate Integration (MANDATORY)

### Before Marking Tasks Complete

**CRITICAL**: ALWAYS run quality gates before marking TodoWrite items "completed":

```bash
# Quality gate validation (activate venv first)
source .venv/bin/activate

# 1. Type Coverage (mypy strict)
python -m mypy src/
# Expected: Success: no issues found in N source files

# 2. Code Quality (ruff)
ruff check src/
# Expected: All checks passed!

# 3. Formatting (ruff)
ruff format --check .
# Expected: All files formatted correctly

# 4. Tests (pytest)
pytest -q
# Expected: N passed, M skipped (100% pass rate)

# 5. Coverage (for implemented components)
pytest --cov=src --cov-report=term-missing
# Expected: ≥90% for Days 1-4 components

# ALL must pass before marking "completed"
```

**Rationale**: Prevents backtracking to fix quality issues later. Early validation = cheaper fixes.

**Evidence**: Phase 1.1 marked "complete" prematurely → 1.5 hours lost fixing 29 violations.

---

## Sub-Agent Output Validation

### After Sub-Agent Code Generation

Sub-agents accelerate development but require language-specific validation BEFORE accepting output:

**Python Validation Checklist**:
- [ ] Class methods have `self` parameter
- [ ] Type hints present (mypy strict compliance)
- [ ] Pydantic v2 validation (no auto-coercion assumptions)
- [ ] Docstrings follow Google style
- [ ] Tests use correct patterns (Arrange-Act-Assert)

**All Languages**:
- [ ] Run formatter before accepting
- [ ] Run linter before accepting
- [ ] Run type checker before accepting
- [ ] Verify tests pass

**Validation Pattern**:
```bash
# After sub-agent completes
source .venv/bin/activate
ruff format . && ruff check src/ && mypy src/ && pytest -q

# ONLY accept output if all pass
```

**Rationale**: Sub-agents optimize for speed. Validation ensures quality.

**Evidence**: Phase 1.1 sub-agent generated 184 tests without `self` parameter → automated fix required.

---

## Environment Setup Protocol (MANDATORY)

### Package Installation Verification

ALWAYS verify uv/venv before installing packages:

```bash
# 1. Verify uv installed
which uv && uv --version

# 2. Verify venv exists
test -d .venv && echo "✅ venv exists" || echo "❌ Create venv first"

# 3. Activate venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\Activate.ps1  # Windows

# 4. Install packages with uv
uv pip install <package>

# 5. Verify installation
python -c "import <package>; print('✅ Installed')"
```

**Never** install to system Python. Always use project-local venv at `.venv`.

**Rationale**: Prevents environment pollution and "wrong Python" errors.

---

## Current Phase Status

**Phase 1.1 (Days 1-4)**: ✅ Complete - Foundation & Initial API
- ✅ CI/CD Pipeline (GitHub Actions with 7 quality gates)
- ✅ WorldAnvilClient (async context manager with retry logic)
- ✅ InMemoryCache (TTL + LRU eviction)
- ✅ Exception Hierarchy (6 exception classes with attributes)
- ✅ EcosystemDetector (MCP companion integration)
- ✅ Pydantic Models (Identity, User, World, WorldSummary)
- ✅ MCP Tools (5 tools: user identity, user profile, world list/get/update)
- ✅ Unit Tests (225 tests passing, ~100% coverage for Days 1-4 components)
- ✅ Quality Gates (100% type coverage, 0 violations, 100% pass rate)

**Phase 1.1 (Days 5-6)**: ⏳ Next - Write API Validation + Integration Tests
- ⏳ Write operations (PATCH, DELETE endpoints)
- ⏳ Integration tests for client/server/tools
- ⏳ Live API validation

Coverage achieved: 43.68% overall (Days 1-4 components at ~100%)
See `docs/pdca/phase-1.1-foundation/` for detailed PDCA documentation.

---

## References

- **World Anvil API**: https://www.worldanvil.com/api/external/boromir/documentation
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **OpenAPI Spec**: `openapi.yml` (World Anvil Boromir API v2)
