# Testing Requirements

**Phase**: 0.3 - Quality Standards
**Status**: Complete
**Date**: 2025-11-28

---

## Overview

This document defines comprehensive testing standards for the World Anvil MCP Server project, ensuring reliability, correctness, and maintainability through systematic test coverage.

---

## Testing Framework

### Primary Framework: pytest

**Version**: Latest stable pytest (≥8.0.0)

**Rationale**: Industry standard, excellent async support, rich plugin ecosystem

### Core Dependencies

```toml
[project.optional-dependencies]
test = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "pytest-timeout>=2.2.0",
    "httpx>=0.27.0",  # For test client
    "respx>=0.20.0",  # For mocking httpx
    "faker>=22.0.0",  # For test data generation
]
```

---

## Coverage Requirements

### Minimum Targets

- **Overall coverage**: ≥85%
- **Core client**: ≥90%
- **Endpoint implementations**: ≥85%
- **Models**: ≥95%
- **Error handling**: 100%

### Configuration

**File**: `pyproject.toml`

```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
timeout = 30
markers = [
    "unit: Unit tests (fast, no I/O)",
    "integration: Integration tests (may use network)",
    "e2e: End-to-end tests (require live API)",
    "slow: Tests that take >1 second",
]
addopts = [
    "--strict-markers",
    "--strict-config",
    "--showlocals",
    "--tb=short",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__init__.py",
    "*/conftest.py",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "@abstractmethod",
    "@overload",
]

[tool.coverage.html]
directory = "htmlcov"
```

### Usage

```bash
# Run tests with coverage
pytest --cov=src --cov-report=term-missing --cov-report=html

# Fail if coverage below threshold
pytest --cov=src --cov-fail-under=85
```

---

## Test Organization

### Directory Structure

```
tests/
├── conftest.py              # Shared fixtures
├── test_client.py           # WorldAnvilClient tests
├── test_server.py           # MCP server tests
├── test_cache.py            # ResponseCache tests
├── test_rate_limit.py       # RateLimiter tests
├── test_exceptions.py       # Exception hierarchy tests
├── endpoints/
│   ├── conftest.py         # Endpoint-specific fixtures
│   ├── test_base.py        # BaseEndpoint tests
│   ├── test_users.py       # UserEndpoint tests
│   ├── test_worlds.py      # WorldEndpoint tests
│   ├── test_articles.py    # ArticleEndpoint tests
│   ├── test_categories.py
│   └── ...
├── models/
│   ├── test_user.py        # User model tests
│   ├── test_world.py       # World model tests
│   ├── test_article.py     # Article model tests
│   └── ...
└── integration/
    ├── conftest.py         # Integration test fixtures
    ├── test_workflow_session_notes.py
    ├── test_workflow_npc_generation.py
    └── ...
```

---

## Test Types

### 1. Unit Tests

**Purpose**: Test individual components in isolation
**Marker**: `@pytest.mark.unit`
**Speed**: Fast (<100ms per test)
**Network**: No external calls (mocked)

**Example**:

```python
import pytest
from world_anvil_mcp.models import Article

@pytest.mark.unit
def test_article_is_published_true():
    """Article with state='public' should be published."""
    article = Article(
        id="test-id",
        title="Test Article",
        state="public",
        url="https://example.com/article"
    )
    assert article.is_published is True

@pytest.mark.unit
def test_article_is_published_false():
    """Article with state='draft' should not be published."""
    article = Article(
        id="test-id",
        title="Test Article",
        state="draft",
        url="https://example.com/article"
    )
    assert article.is_published is False
```

### 2. Integration Tests

**Purpose**: Test component interactions with mocked external services
**Marker**: `@pytest.mark.integration`
**Speed**: Medium (100ms-1s per test)
**Network**: Mocked HTTP calls (using respx)

**Example**:

```python
import pytest
import respx
from httpx import Response
from world_anvil_mcp.client import WorldAnvilClient

@pytest.mark.integration
@respx.mock
async def test_get_article_success(mock_client_config):
    """Successfully retrieve article with mocked API."""
    article_id = "test-article-id"

    # Mock API response
    respx.get(
        f"https://www.worldanvil.com/api/external/boromir/article/{article_id}",
        params={"granularity": "1"}
    ).mock(return_value=Response(200, json={
        "id": article_id,
        "title": "Test Article",
        "state": "public",
        "url": "https://example.com/article",
        "world": {"id": "world-1"},
    }))

    async with WorldAnvilClient(**mock_client_config) as client:
        article = await client.articles.get(article_id)

    assert article.id == article_id
    assert article.title == "Test Article"
    assert article.is_published is True
```

### 3. End-to-End Tests

**Purpose**: Test against live World Anvil API
**Marker**: `@pytest.mark.e2e`
**Speed**: Slow (>1s per test)
**Network**: Real API calls (requires credentials)

**Example**:

```python
import pytest
import os

@pytest.mark.e2e
@pytest.mark.skipif(
    not os.getenv("WORLD_ANVIL_API_KEY"),
    reason="Requires live API credentials"
)
async def test_get_user_identity_live():
    """Test user identity endpoint against live API."""
    from world_anvil_mcp.client import WorldAnvilClient

    async with WorldAnvilClient(
        app_key=os.environ["WORLD_ANVIL_API_KEY"],
        user_token=os.environ["WORLD_ANVIL_USER_TOKEN"]
    ) as client:
        user = await client.users.get_identity()

    assert user.id is not None
    assert user.username is not None
    assert "@" in user.email
```

---

## Fixture Patterns

### Shared Fixtures (conftest.py)

```python
import pytest
from typing import AsyncGenerator
from world_anvil_mcp.client import WorldAnvilClient

@pytest.fixture
def mock_client_config() -> dict[str, str]:
    """Provide test configuration for WorldAnvilClient."""
    return {
        "app_key": "test-app-key",
        "user_token": "test-user-token",
        "base_url": "https://www.worldanvil.com/api/external/boromir"
    }

@pytest.fixture
async def mock_client(mock_client_config) -> AsyncGenerator[WorldAnvilClient, None]:
    """Provide configured WorldAnvilClient for testing."""
    async with WorldAnvilClient(**mock_client_config) as client:
        yield client

@pytest.fixture
def sample_article_data() -> dict:
    """Provide sample article JSON response."""
    return {
        "id": "article-123",
        "title": "Sample Article",
        "state": "public",
        "url": "https://worldanvil.com/w/myworld/a/sample-article",
        "world": {"id": "world-1", "title": "My World"},
        "tags": ["test", "sample"],
        "content": "# Sample Content\n\nThis is a test.",
    }

@pytest.fixture
def faker_seed() -> int:
    """Provide deterministic seed for Faker."""
    return 12345
```

### Endpoint-Specific Fixtures

```python
# tests/endpoints/conftest.py
import pytest
from faker import Faker

@pytest.fixture
def faker(faker_seed: int) -> Faker:
    """Provide Faker instance with deterministic seed."""
    fake = Faker()
    Faker.seed(faker_seed)
    return fake

@pytest.fixture
def sample_user(faker: Faker) -> dict:
    """Generate sample user data."""
    return {
        "id": faker.uuid4(),
        "username": faker.user_name(),
        "email": faker.email(),
        "isPremium": faker.boolean(),
    }
```

---

## Mocking Strategies

### 1. HTTP Mocking with respx

For testing HTTP client behavior without real API calls:

```python
import respx
from httpx import Response

@respx.mock
async def test_rate_limit_error(mock_client):
    """Test rate limit error handling."""
    respx.get("https://www.worldanvil.com/api/external/boromir/user").mock(
        return_value=Response(429, json={"error": "Rate limit exceeded"})
    )

    from world_anvil_mcp.exceptions import RateLimitError

    with pytest.raises(RateLimitError, match="Rate limit exceeded"):
        await mock_client.users.get_identity()
```

### 2. MCP Context Mocking

For testing MCP integration without full MCP server:

```python
from unittest.mock import AsyncMock
import pytest

@pytest.fixture
def mock_mcp_context():
    """Provide mocked MCP Context."""
    ctx = AsyncMock()
    ctx.info = AsyncMock()
    ctx.error = AsyncMock()
    ctx.progress = AsyncMock()
    return ctx

async def test_client_logs_to_context(mock_mcp_context, mock_client_config):
    """Client should log API calls to MCP context."""
    async with WorldAnvilClient(**mock_client_config, ctx=mock_mcp_context) as client:
        with respx.mock:
            respx.get("...").mock(return_value=Response(200, json={...}))
            await client.articles.get("test-id")

    mock_mcp_context.info.assert_called()
```

### 3. Cache Mocking

For testing cache behavior:

```python
from unittest.mock import Mock

def test_cache_hit(sample_article_data):
    """Cache should return cached response."""
    from world_anvil_mcp.cache import ResponseCache

    cache = ResponseCache(maxsize=100)
    key = ("article", "test-id", "1")

    # Store in cache
    cache.set(key, sample_article_data)

    # Retrieve from cache
    result = cache.get(key)

    assert result == sample_article_data
```

---

## Async Testing Patterns

### Basic Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function with pytest-asyncio."""
    result = await async_operation()
    assert result == expected_value
```

### Testing Async Context Managers

```python
@pytest.mark.asyncio
async def test_client_context_manager(mock_client_config):
    """Client should properly manage HTTP client lifecycle."""
    client = WorldAnvilClient(**mock_client_config)

    # Before entering context
    assert not hasattr(client, "_http_client")

    async with client:
        # Inside context - HTTP client should be initialized
        assert client._http_client is not None

    # After exiting context - HTTP client should be closed
    assert client._http_client.is_closed
```

### Testing Parallel Operations

```python
import asyncio

@pytest.mark.asyncio
async def test_parallel_article_retrieval(mock_client):
    """Client should support parallel article retrieval."""
    with respx.mock:
        # Mock multiple endpoints
        for i in range(3):
            respx.get(f".../{i}").mock(return_value=Response(200, json={...}))

        # Retrieve in parallel
        articles = await asyncio.gather(
            mock_client.articles.get("0"),
            mock_client.articles.get("1"),
            mock_client.articles.get("2")
        )

    assert len(articles) == 3
```

---

## Error Handling Tests

### Testing Exception Hierarchy

```python
def test_exception_hierarchy():
    """All custom exceptions inherit from WorldAnvilError."""
    from world_anvil_mcp.exceptions import (
        WorldAnvilError,
        AuthenticationError,
        NotFoundError,
        RateLimitError
    )

    assert issubclass(AuthenticationError, WorldAnvilError)
    assert issubclass(NotFoundError, WorldAnvilError)
    assert issubclass(RateLimitError, WorldAnvilError)
```

### Testing Error Responses

```python
@respx.mock
async def test_authentication_error(mock_client):
    """Test 401 response raises AuthenticationError."""
    respx.get("...").mock(
        return_value=Response(401, json={"error": "Unauthorized"})
    )

    from world_anvil_mcp.exceptions import AuthenticationError

    with pytest.raises(AuthenticationError, match="Unauthorized"):
        await mock_client.users.get_identity()
```

### Testing Retry Logic

```python
@respx.mock
async def test_retry_on_server_error(mock_client):
    """Client should retry on 500 errors."""
    # First two calls fail, third succeeds
    route = respx.get("...").mock(
        side_effect=[
            Response(500, json={"error": "Internal server error"}),
            Response(500, json={"error": "Internal server error"}),
            Response(200, json={"id": "success"}),
        ]
    )

    result = await mock_client.users.get_identity()

    assert result.id == "success"
    assert route.call_count == 3  # Verify retries occurred
```

---

## Pydantic Model Tests

### Validation Tests

```python
import pytest
from pydantic import ValidationError

def test_article_model_validation():
    """Article model should validate required fields."""
    from world_anvil_mcp.models import Article

    # Valid data
    article = Article(
        id="123",
        title="Test",
        state="public",
        url="https://example.com"
    )
    assert article.id == "123"

    # Missing required field
    with pytest.raises(ValidationError) as exc_info:
        Article(title="Test", state="public")

    errors = exc_info.value.errors()
    assert any(e["loc"] == ("id",) for e in errors)
```

### Serialization Tests

```python
def test_article_serialization(sample_article_data):
    """Article model should serialize to JSON."""
    from world_anvil_mcp.models import Article

    article = Article(**sample_article_data)

    # Serialize to dict
    data = article.model_dump()
    assert data["id"] == sample_article_data["id"]
    assert data["title"] == sample_article_data["title"]

    # Serialize to JSON string
    json_str = article.model_dump_json()
    assert isinstance(json_str, str)
    assert sample_article_data["id"] in json_str
```

---

## Integration Test Examples

### Workflow-Based Integration Tests

```python
# tests/integration/test_workflow_session_notes.py

@pytest.mark.integration
@respx.mock
async def test_session_note_workflow(mock_client):
    """Test session note-taking workflow (WF-002)."""
    # Mock get_world
    respx.get(".../world/123").mock(return_value=Response(200, json={
        "id": "123",
        "title": "Storm King's Thunder"
    }))

    # Mock list recent sessions
    respx.post(".../world/123/articles").mock(return_value=Response(200, json={
        "articles": [
            {"id": "session-14", "title": "Session 14"},
            {"id": "session-13", "title": "Session 13"},
        ]
    }))

    # Mock search for NPC
    respx.post(".../search/articles").mock(return_value=Response(200, json={
        "results": [
            {"id": "npc-silvanus", "title": "Silvanus"}
        ]
    }))

    # Execute workflow steps
    world = await mock_client.worlds.get("123")
    sessions = await mock_client.articles.list(world_id="123", limit=10)
    npc_results = await mock_client.articles.search(query="Silvanus", world_id="123")

    # Verify workflow completion
    assert world.title == "Storm King's Thunder"
    assert len(sessions) == 2
    assert len(npc_results) == 1
    assert npc_results[0].title == "Silvanus"
```

---

## Performance Testing

### Timeout Configuration

```python
@pytest.mark.timeout(5)
async def test_fast_response(mock_client):
    """Article retrieval should complete within 5 seconds."""
    with respx.mock:
        respx.get("...").mock(return_value=Response(200, json={...}))
        article = await mock_client.articles.get("test-id")
    assert article is not None
```

### Cache Performance

```python
import time

def test_cache_performance():
    """Cache lookups should be fast (< 1ms)."""
    from world_anvil_mcp.cache import ResponseCache

    cache = ResponseCache(maxsize=1000)

    # Populate cache
    for i in range(100):
        cache.set(("article", str(i), "1"), {"id": str(i)})

    # Measure lookup time
    start = time.perf_counter()
    for i in range(100):
        cache.get(("article", str(i), "1"))
    duration = time.perf_counter() - start

    # Should complete 100 lookups in < 10ms
    assert duration < 0.01
```

---

## Test Data Generation

### Using Faker

```python
from faker import Faker

def test_with_faker(faker: Faker):
    """Generate realistic test data with Faker."""
    # Generate World Anvil-like data
    article_id = faker.uuid4()
    title = faker.sentence(nb_words=4)
    tags = [faker.word() for _ in range(3)]

    article = Article(
        id=article_id,
        title=title,
        state=faker.random_element(["public", "draft", "private"]),
        url=f"https://worldanvil.com/w/{faker.slug()}/a/{article_id}",
        tags=tags
    )

    assert article.id == article_id
    assert len(article.tags) == 3
```

---

## Running Tests

### Local Development

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test types
pytest -m unit                    # Unit tests only
pytest -m "unit or integration"   # Unit and integration
pytest -m "not e2e"               # Skip end-to-end tests

# Run specific test file
pytest tests/test_client.py

# Run specific test function
pytest tests/test_client.py::test_client_initialization

# Run with verbose output
pytest -v

# Run with debugging on failure
pytest --pdb

# Run failed tests only
pytest --lf  # last failed
pytest --ff  # failed first
```

### Continuous Integration

```bash
# CI test command (no color, strict)
pytest --cov=src --cov-report=term --cov-fail-under=85 -v --strict-markers
```

---

## Test Quality Standards

### Test Naming

- **Descriptive**: `test_get_article_returns_correct_data`
- **Not vague**: `test_article` ❌
- **Pattern**: `test_[function]_[scenario]_[expected_result]`

### Assertions

- **Use specific assertions**: `assert article.id == "123"` not `assert article`
- **Multiple assertions OK** when testing same concept
- **One concept per test**: Don't test article AND world in same test

### Test Independence

- **No test dependencies**: Each test should run independently
- **Idempotent**: Tests should produce same result every run
- **Clean state**: Use fixtures to ensure clean state

### Documentation

- **Every test needs docstring**: Brief summary of what's being tested
- **Complex tests**: Add inline comments for clarity

```python
@pytest.mark.unit
def test_article_is_published_for_public_state():
    """Article with state='public' should have is_published=True."""
    article = Article(id="1", title="Test", state="public", url="http://...")
    assert article.is_published is True
```

---

## Continuous Improvement

### Coverage Gaps

Regularly review coverage reports to identify untested code:

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open in browser
open htmlcov/index.html
```

### Test Metrics

Track test metrics over time:

- Total test count
- Test execution time
- Coverage percentage
- Flaky test rate

### Test Refactoring

Periodically refactor tests for:

- Reduced duplication
- Improved clarity
- Better fixture reuse
- Faster execution

---

## References

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [respx documentation](https://lundberg.github.io/respx/)
- [Faker documentation](https://faker.readthedocs.io/)
- [MCP Testing Patterns](https://github.com/modelcontextprotocol/python-sdk)

---

**Status**: Complete ✅
**Next**: documentation-standards.md
