# Code Quality Rules

**Phase**: 0.3 - Quality Standards
**Status**: Complete
**Date**: 2025-11-28

---

## Overview

This document defines code quality standards for the World Anvil MCP Server project, ensuring consistency, maintainability, and professional quality across all Python code.

---

## Python Version

**Minimum**: Python 3.11
**Target**: Python 3.11+
**Rationale**: Type hints improvements, better error messages, performance gains

---

## Code Formatting: ruff

We use [ruff](https://docs.astral.sh/ruff/) as our primary linting and formatting tool (latest stable version).

### Configuration

**File**: `pyproject.toml`

```toml
[tool.ruff]
target-version = "py311"
line-length = 100
indent-width = 4

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "ANN",    # flake8-annotations
    "ASYNC",  # flake8-async
    "S",      # flake8-bandit (security)
    "B",      # flake8-bugbear
    "A",      # flake8-builtins
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "EM",     # flake8-errmsg
    "FA",     # flake8-future-annotations
    "ISC",    # flake8-implicit-str-concat
    "ICN",    # flake8-import-conventions
    "G",      # flake8-logging-format
    "PIE",    # flake8-pie
    "T20",    # flake8-print
    "PYI",    # flake8-pyi
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SLF",    # flake8-self
    "SLOT",   # flake8-slots
    "SIM",    # flake8-simplify
    "TID",    # flake8-tidy-imports
    "TCH",    # flake8-type-checking
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "PL",     # pylint
    "TRY",    # tryceratops
    "FLY",    # flynt
    "PERF",   # perflint
    "RUF",    # ruff-specific rules
]

ignore = [
    "ANN101",  # Missing type annotation for self
    "ANN102",  # Missing type annotation for cls
    "D203",    # 1 blank line required before class docstring (conflicts with D211)
    "D213",    # Multi-line docstring summary should start at the second line (conflicts with D212)
    "S104",    # Possible binding to all interfaces
    "S603",    # subprocess call: check for execution of untrusted input
    "PLR0913", # Too many arguments to function call
    "TRY003",  # Avoid specifying long messages outside the exception class
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",    # Use of assert detected (expected in tests)
    "ANN201",  # Missing return type annotation for public function
    "ARG001",  # Unused function argument (common in fixtures)
    "PLR2004", # Magic value used in comparison
]
"__init__.py" = [
    "F401",    # Imported but unused (re-exports)
]

[tool.ruff.lint.isort]
known-first-party = ["world_anvil_mcp"]
combine-as-imports = true
force-wrap-aliases = true

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
```

### Usage

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Fix auto-fixable issues
ruff check --fix .
```

---

## Type Checking: mypy

We use [mypy](https://mypy.readthedocs.io/) in strict mode for comprehensive type checking (latest stable version).

### Configuration

**File**: `pyproject.toml`

```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
check_untyped_defs = true
strict_equality = true
strict_optional = true
warn_unreachable = true
pretty = true
show_error_codes = true
show_error_context = true
show_column_numbers = true

# Per-module configuration
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
disallow_untyped_calls = false

[[tool.mypy.overrides]]
module = "cachetools.*"
ignore_missing_imports = true
```

### Type Annotation Requirements

1. **All public functions and methods** must have complete type annotations
2. **All class attributes** must be annotated
3. **Return types** must be explicit (no implicit `None`)
4. **Use modern syntax**: `list[str]` not `List[str]` (Python 3.11+)
5. **Use `typing` imports** only when needed (Self, Protocol, TypeVar, etc.)

**Examples**:

```python
# ✅ Good
from typing import Self

class User:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name

    def to_dict(self) -> dict[str, str]:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(id=data["id"], name=data["name"])

# ❌ Bad - Missing annotations
class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}
```

### Usage

```bash
# Type check entire project
mypy src/

# Type check specific file
mypy src/world_anvil_mcp/client.py
```

---

## Docstring Standards

We follow **Google-style docstrings** as enforced by ruff's pydocstyle rules.

### Requirements

1. **All public modules, classes, functions, and methods** must have docstrings
2. **Private functions** (`_function`) should have docstrings if non-trivial
3. **Magic methods** need docstrings only if behavior is non-standard
4. Use **triple double-quotes** (`"""`)
5. **First line** is a concise summary (imperative mood)
6. **Blank line** between summary and details
7. **Args, Returns, Raises** sections as needed

### Module Docstrings

```python
"""World Anvil API client implementation.

This module provides an async HTTP client for the World Anvil Boromir API v2,
with built-in caching, rate limiting, and retry logic optimized for MCP usage.

Example:
    >>> async with WorldAnvilClient(app_key="...", user_token="...") as client:
    ...     article = await client.articles.get("article-id")
    ...     print(article.title)
"""
```

### Class Docstrings

```python
class WorldAnvilClient:
    """Async HTTP client for World Anvil Boromir API v2.

    Provides MCP-optimized access to World Anvil resources with built-in
    caching, rate limiting, and retry logic. Designed for use as an async
    context manager.

    Attributes:
        users: User endpoint operations.
        worlds: World endpoint operations.
        articles: Article endpoint operations.
        ctx: Optional MCP Context for logging and progress.

    Example:
        >>> async with WorldAnvilClient(app_key="key", user_token="token") as client:
        ...     user = await client.users.get_identity()
        ...     worlds = await client.worlds.list(user_id=user.id)
    """
```

### Function/Method Docstrings

```python
async def get_article(
    self,
    article_id: str,
    granularity: str = "1"
) -> Article:
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
        ServerError: World Anvil API server error.

    Example:
        >>> article = await client.articles.get("abc123", granularity="2")
        >>> print(f"{article.title}: {article.content}")
    """
```

### Property Docstrings

```python
@property
def is_published(self) -> bool:
    """True if article state is 'public', False otherwise."""
    return self.state == "public"
```

---

## Code Organization

### File Structure

```
src/world_anvil_mcp/
├── __init__.py           # Package exports
├── server.py             # MCP server implementation (FastMCP)
├── client.py             # Main WorldAnvilClient class
├── endpoints/            # Endpoint implementations
│   ├── __init__.py
│   ├── base.py          # BaseEndpoint generic
│   ├── users.py         # UserEndpoint
│   ├── worlds.py        # WorldEndpoint
│   ├── articles.py      # ArticleEndpoint
│   └── ...
├── models/              # Pydantic models
│   ├── __init__.py
│   ├── user.py
│   ├── world.py
│   ├── article.py
│   └── ...
├── exceptions.py        # Custom exception hierarchy
├── cache.py            # ResponseCache implementation
└── rate_limit.py       # RateLimiter implementation

tests/
├── __init__.py
├── conftest.py         # Shared fixtures
├── test_client.py
├── test_endpoints/
│   ├── test_users.py
│   ├── test_worlds.py
│   └── ...
└── test_models/
    ├── test_user.py
    └── ...
```

### Import Organization

Enforced by ruff's isort integration:

1. **Standard library** imports
2. **Third-party** imports
3. **Local application** imports
4. **Blank line** between groups

```python
# Standard library
import asyncio
from typing import Self

# Third-party
import httpx
from mcp import Context
from pydantic import BaseModel, Field

# Local
from world_anvil_mcp.exceptions import NotFoundError
from world_anvil_mcp.models import Article
```

### Naming Conventions

Following PEP 8 and enforced by ruff:

- **Modules**: `lowercase_with_underscores.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `lowercase_with_underscores()`
- **Constants**: `UPPERCASE_WITH_UNDERSCORES`
- **Private**: `_leading_underscore`
- **Type variables**: `T`, `ModelT`, `ResponseT` (PascalCase)

```python
# ✅ Good
DEFAULT_RATE_LIMIT = 60
class WorldAnvilClient: ...
async def get_article(...) -> Article: ...
def _parse_response(...) -> dict: ...

# ❌ Bad
default_rate_limit = 60  # Should be UPPERCASE
class worldAnvilClient: ...  # Should be PascalCase
async def GetArticle(...): ...  # Should be lowercase_with_underscores
```

---

## Code Complexity

### Maximum Line Length

**100 characters** (configured in ruff)

**Rationale**: Balance between readability and modern screen sizes

### Function Complexity

- **Maximum cyclomatic complexity**: 10 (enforced by ruff's PLR rules)
- **Maximum function length**: 50 lines (soft limit)
- **Maximum arguments**: 5 (soft limit, use dataclasses/models for more)

**Refactor if**:
- Function exceeds 50 lines
- Cyclomatic complexity > 10
- More than 5 parameters

### Class Complexity

- **Maximum methods per class**: 20 (soft limit)
- **Single Responsibility Principle**: Each class should have one reason to change
- **Favor composition** over inheritance

---

## Error Handling

### Exception Hierarchy

All custom exceptions inherit from base exception class:

```python
class WorldAnvilError(Exception):
    """Base exception for World Anvil API errors."""

class AuthenticationError(WorldAnvilError):
    """Invalid or missing authentication credentials."""

class NotFoundError(WorldAnvilError):
    """Requested resource does not exist."""
```

### Error Messages

- **Use f-strings** for formatting
- **Include context**: IDs, endpoints, status codes
- **Be specific**: "Article abc123 not found" not "Not found"
- **No secrets** in error messages

```python
# ✅ Good
raise NotFoundError(f"Article {article_id} not found at endpoint {endpoint}")

# ❌ Bad
raise NotFoundError("Not found")  # Not specific
raise AuthenticationError(f"Auth failed with token {token}")  # Leaks secret
```

---

## Async/Await Patterns

### Requirements

1. **All I/O operations** must be async
2. **Use async context managers** for resource management
3. **Prefer `asyncio.gather()`** for parallel operations
4. **Avoid blocking calls** in async functions

```python
# ✅ Good
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# Parallel operations
articles = await asyncio.gather(
    client.articles.get("id1"),
    client.articles.get("id2"),
    client.articles.get("id3")
)

# ❌ Bad
client = httpx.Client()  # Synchronous client
response = client.get(url)  # Blocking call
```

---

## Security

Enforced by ruff's bandit rules (S prefix):

1. **No hardcoded secrets** (S105, S106)
2. **Use secrets module** for random values (S311)
3. **Validate input** before use (S602, S603)
4. **No eval/exec** (S102, S307)
5. **Secure defaults** for network bindings (S104)

```python
# ✅ Good
import secrets
api_key = os.environ["WORLD_ANVIL_API_KEY"]
random_value = secrets.token_urlsafe(32)

# ❌ Bad
api_key = "sk_1234567890abcdef"  # Hardcoded secret (S105)
random_value = random.random()  # Not cryptographically secure (S311)
```

---

## Testing Integration

Code quality checks are integrated with testing:

```bash
# Run all quality checks
make quality

# Individual checks
make format    # ruff format
make lint      # ruff check
make typecheck # mypy
```

### Pre-commit Hook

Quality checks run automatically before commits (see Phase 0.4).

---

## Continuous Integration

Quality checks run in CI pipeline:

```yaml
# .github/workflows/ci.yml (example)
- name: Check formatting
  run: ruff format --check .

- name: Lint
  run: ruff check .

- name: Type check
  run: mypy src/
```

---

## IDE Integration

### VS Code

**File**: `.vscode/settings.json`

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": true,
      "source.organizeImports": true
    }
  },
  "python.linting.enabled": true,
  "python.linting.mypyEnabled": true,
  "ruff.organizeImports": true
}
```

### PyCharm

1. Install ruff plugin from marketplace
2. Enable "Reformat code on save"
3. Configure external tool for mypy

---

## Quality Metrics

### Target Standards

- **ruff**: 0 errors, 0 warnings
- **mypy**: 0 type errors (strict mode)
- **Test coverage**: ≥85% (see testing-requirements.md)
- **Docstring coverage**: 100% for public API

### Measurement

```bash
# Check ruff compliance
ruff check . --statistics

# Check mypy compliance
mypy src/ --strict

# Generate coverage report
pytest --cov=src --cov-report=term-missing
```

---

## Exceptions and Overrides

### When to Use `# type: ignore`

Minimize usage. Only when:
1. Third-party library has incorrect type stubs
2. Complex generic that mypy cannot infer
3. Add comment explaining why: `# type: ignore[error-code]  # Reason`

```python
# ✅ Acceptable
result = complex_function()  # type: ignore[return-value]  # Upstream bug in library-stubs

# ❌ Not acceptable
result = complex_function()  # type: ignore  # No explanation
```

### When to Use `# noqa`

Minimize usage. Only when:
1. False positive from linter
2. Intentional violation with strong rationale
3. Add specific error code: `# noqa: E501` not `# noqa`

```python
# ✅ Acceptable
url = "https://www.worldanvil.com/api/external/boromir/v2/articles/very-long-article-id-example"  # noqa: E501

# ❌ Not acceptable
bad_code()  # noqa  # Too broad, no explanation
```

---

## References

- [ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [PEP 257 Docstring Conventions](https://peps.python.org/pep-0257/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

---

**Status**: Complete ✅
**Next**: testing-requirements.md
