# Development Quick Start Guide

Fast setup and workflow for World Anvil MCP Server development.

## 5-Minute Setup

### Prerequisites
- Python 3.11+
- Git
- macOS, Linux, or Windows with PowerShell

### Installation

**macOS/Linux**:
```bash
# Clone repository
git clone <repo-url>
cd world-anvil

# Create virtual environment
uv venv --python 3.11 .venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev,test]"

# Verify setup
pytest --co -q  # List all tests (no execution)
```

**Windows PowerShell**:
```powershell
# Clone repository
git clone <repo-url>
cd world-anvil

# Create virtual environment
uv venv --python 3.11 .venv
.venv\Scripts\Activate.ps1

# Install dependencies
uv pip install -e ".[dev,test]"

# Verify setup
pytest --co -q
```

---

## Running Quality Checks

### All Checks (Recommended Before Commit)
```bash
# Format + Lint + Type + Tests
ruff format . && ruff check . && mypy src/world_anvil_mcp && pytest --cov=src/world_anvil_mcp --cov-fail-under=85

# Or with verbose output
ruff format . --diff
ruff check . --show-settings
mypy src/world_anvil_mcp --show-error-codes
pytest -v --cov-report=term-missing
```

### Individual Checks

**Format Check** (no auto-fix):
```bash
ruff format --check .
```

**Auto-Format**:
```bash
ruff format .
```

**Lint Check** (no auto-fix):
```bash
ruff check .
```

**Auto-Lint Fix**:
```bash
ruff check . --fix
```

**Type Check**:
```bash
mypy src/world_anvil_mcp
```

**Run Tests**:
```bash
# All tests
pytest

# Verbose output
pytest -v

# Show coverage
pytest --cov=src/world_anvil_mcp --cov-report=term-missing

# Specific test file
pytest tests/test_client.py

# Specific test function
pytest tests/test_client.py::test_client_initialization

# Only unit tests (fast)
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# With detailed output
pytest -vv --tb=short --showlocals
```

---

## Git Workflow

### Before Making Changes
```bash
# Ensure main is up to date
git checkout main
git pull

# Create feature branch
git checkout -b feature/my-feature
```

### Before Committing
```bash
# Run all quality checks
ruff format . && ruff check . && mypy src/world_anvil_mcp && pytest

# If all pass, commit
git add .
git commit -m "Add feature: my-feature"
```

### Before Pushing
```bash
# Ensure still on track
git log -1 --oneline  # Verify your commit

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub
# (Opens browser to create PR)
```

---

## Common Development Tasks

### Adding a New Module

1. Create file in `src/world_anvil_mcp/`:
```python
# src/world_anvil_mcp/my_module.py
"""Description of module."""

def my_function(param: str) -> str:
    """Function docstring.

    Args:
        param: Parameter description.

    Returns:
        Return description.

    Example:
        >>> my_function("test")
        'test'
    """
    return param
```

2. Add tests in `tests/`:
```python
# tests/test_my_module.py
"""Tests for my_module."""

import pytest
from world_anvil_mcp.my_module import my_function


class TestMyFunction:
    """Test my_function."""

    def test_my_function_success(self) -> None:
        """Test successful execution."""
        result = my_function("test")
        assert result == "test"

    def test_my_function_empty(self) -> None:
        """Test with empty input."""
        result = my_function("")
        assert result == ""
```

3. Run quality checks:
```bash
ruff format . && ruff check . && mypy src/world_anvil_mcp && pytest
```

### Fixing Type Errors

**Error Example**:
```
error: Argument 1 to "foo" has incompatible type "int"; expected "str"
```

**Solution**:
1. Add type hints to function signature
2. Use type annotations in variables
3. Use `cast()` only as last resort

```python
# Before
def process(data):
    return data.upper()

# After
def process(data: str) -> str:
    """Process string data."""
    return data.upper()
```

### Writing Async Tests

```python
"""Async test example."""

import pytest


class TestAsyncFunction:
    """Test async functions."""

    async def test_async_function(self) -> None:
        """Test async execution."""
        # Works automatically with pytest-asyncio
        result = await my_async_function()
        assert result is not None
```

### Mocking HTTP Requests

```python
"""Mock HTTP example."""

import pytest
import respx
from httpx import Response


@pytest.fixture
def mock_api() -> respx.Router:
    """Mock API responses."""
    router = respx.mock
    router.get("https://api.example.com/data").mock(
        return_value=Response(
            200,
            json={"status": "success", "data": [1, 2, 3]},
        )
    )
    return router


async def test_with_mocked_api(mock_api: respx.Router) -> None:
    """Test with mocked API."""
    with mock_api:
        # Your test code that makes HTTP calls
        pass
```

---

## Debugging

### Print Debugging
```python
# Use print statements (visible in pytest -s output)
print(f"Debug: {variable}")

# Run with output
pytest -s
```

### Pytest Debugging
```bash
# Show local variables on failure
pytest -l

# Drop into debugger on failure
pytest --pdb

# Drop into debugger on first failure
pytest -x --pdb

# Show more detailed output
pytest -vv --tb=long
```

### Type Checking Debugging
```bash
# Show error context
mypy src/world_anvil_mcp --show-error-context --show-column-numbers

# Show all errors
mypy src/world_anvil_mcp --show-error-codes
```

---

## Project Structure Reference

```
src/world_anvil_mcp/
├── __init__.py         # Package entry point
├── server.py           # MCP server (FastMCP)
├── client.py           # Main client class
├── endpoints/          # API endpoint implementations
├── models/             # Pydantic models
├── exceptions.py       # Custom exceptions
├── cache.py            # Caching implementation
└── rate_limit.py       # Rate limiting

tests/
├── conftest.py         # Shared test fixtures
├── test_client.py      # Client tests
├── endpoints/          # Endpoint tests
└── models/             # Model tests

docs/
├── CI_CD_PIPELINE.md   # This file
├── specs/              # Architecture specs
└── workflows/          # D&D workflow examples
```

---

## Environment Variables

**Development** (.env file, never commit):
```env
WORLD_ANVIL_APP_KEY=your_application_key
WORLD_ANVIL_USER_TOKEN=your_user_token
```

**Get credentials**:
1. Go to https://www.worldanvil.com/api-keys
2. Create API key
3. Create user token
4. Add to `.env` (add to `.gitignore`)

---

## Useful Commands

| Command | Purpose |
|---------|---------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose test output |
| `pytest -k "pattern"` | Run tests matching pattern |
| `pytest -m unit` | Run only unit tests |
| `pytest --cov --cov-report=html` | Generate coverage report |
| `ruff format .` | Auto-format code |
| `ruff check . --fix` | Auto-fix lint issues |
| `mypy src/world_anvil_mcp` | Type check |
| `git status` | Show changes |
| `git diff` | Show detailed changes |
| `git log --oneline` | Show commit history |

---

## Getting Help

### Error Messages
1. Read the full error message (scroll up for context)
2. Check the line number and file
3. Search the documentation
4. Check existing tests for examples

### Common Issues

**ImportError: No module named 'world_anvil_mcp'**
- Solution: Ensure `.venv/bin/activate` is sourced or use `uv run`

**Coverage below 85%**
- Run: `pytest --cov-report=term-missing` to find untested lines
- Add tests for missing coverage

**Type error: Incompatible types**
- Add type hints to function parameters and returns
- Use `from typing import ...` for complex types

**Test timeout**
- Check for infinite loops or blocking I/O
- Increase timeout: `pytest --timeout=60`

---

## Resources

- **Project CLAUDE.md**: `/Users/speterson/src/world-anvil/CLAUDE.md`
- **CI/CD Details**: `docs/CI_CD_PIPELINE.md`
- **Architecture**: `docs/specs/client-architecture.md`
- **Phase 1.1 Plan**: `docs/pdca/phase-1.1-foundation/plan.md`

---

**Last Updated**: 2025-11-29
**Status**: Ready for Phase 1.1 Implementation
