# API Client Patterns

**Phase**: 0.3 - Quality Standards
**Status**: Complete
**Date**: 2025-11-28

---

## Overview

This document defines patterns and best practices for implementing the World Anvil API client, covering async operations, MCP Context integration, error handling, and CRUD operations.

---

## Core Dependencies

### Required Packages (Latest Stable)

```toml
[project]
dependencies = [
    "mcp>=1.0.0",              # Model Context Protocol SDK
    "httpx>=0.27.0",           # Async HTTP client
    "pydantic>=2.0.0",         # Data validation and serialization
    "python-dotenv>=1.0.0",    # Environment variable management
    "tenacity>=8.0.0",         # Retry logic with exponential backoff
    "cachetools>=5.0.0",       # TTL cache implementation
]
```

### Version Justification

- **mcp>=1.0.0**: Official MCP Python SDK from https://github.com/modelcontextprotocol/python-sdk
- **httpx>=0.27.0**: Modern async HTTP client, preferred over requests
- **pydantic>=2.0.0**: v2 for performance improvements and better typing
- **tenacity>=8.0.0**: Declarative retry logic with async support
- **cachetools>=5.0.0**: Lightweight caching without external dependencies

---

## Async Patterns

### Async Context Manager Pattern

**Always use async context managers** for resource lifecycle management.

```python
from typing import Self
import httpx

class WorldAnvilClient:
    """Async HTTP client for World Anvil API."""

    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str = "https://www.worldanvil.com/api/external/boromir",
        timeout: float = 30.0
    ) -> None:
        """Initialize client configuration.

        Args:
            app_key: World Anvil application key.
            user_token: User authentication token.
            base_url: API base URL (default production endpoint).
            timeout: Request timeout in seconds (default 30).
        """
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url
        self.timeout = timeout
        self._http_client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> Self:
        """Enter async context manager.

        Creates and configures the HTTP client with proper headers,
        timeout settings, and connection limits.

        Returns:
            Self: Configured client instance.
        """
        self._http_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._build_headers(),
            timeout=httpx.Timeout(timeout=self.timeout, connect=10.0),
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
            follow_redirects=True
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object | None
    ) -> None:
        """Exit async context manager.

        Ensures HTTP client is properly closed to avoid resource leaks.

        Args:
            exc_type: Exception type if error occurred.
            exc_val: Exception value if error occurred.
            exc_tb: Exception traceback if error occurred.
        """
        if self._http_client is not None:
            await self._http_client.aclose()
            self._http_client = None

    def _build_headers(self) -> dict[str, str]:
        """Build HTTP headers for API requests.

        Returns:
            dict: Headers with authentication and content type.
        """
        return {
            "x-auth-token": self.user_token,
            "x-application-key": self.app_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "world-anvil-mcp/0.1.0"
        }
```

**Usage**:

```python
# ✅ Good - Ensures cleanup
async with WorldAnvilClient(app_key="...", user_token="...") as client:
    article = await client.articles.get("article-id")

# ❌ Bad - No cleanup, resource leak
client = WorldAnvilClient(app_key="...", user_token="...")
# Missing await client.close() or context manager
```

### Async Method Pattern

```python
from typing import TypeVar, Generic

T = TypeVar("T")

class BaseEndpoint(Generic[T]):
    """Base class for API endpoint implementations."""

    def __init__(self, client: WorldAnvilClient) -> None:
        """Initialize endpoint with client reference.

        Args:
            client: Parent WorldAnvilClient instance.
        """
        self.client = client

    async def get(self, resource_id: str, **params: str | int) -> T:
        """Retrieve single resource by ID.

        Args:
            resource_id: Unique identifier for resource.
            **params: Additional query parameters.

        Returns:
            T: Typed resource object.

        Raises:
            NotFoundError: Resource does not exist.
            AuthenticationError: Invalid credentials.
        """
        endpoint = f"/{self._resource_name}/{resource_id}"
        response = await self._request("GET", endpoint, params=params)
        return self._model_class(**response)
```

### Parallel Operations Pattern

Use `asyncio.gather()` for parallel operations when safe:

```python
import asyncio
from typing import Sequence

async def get_multiple_articles(
    client: WorldAnvilClient,
    article_ids: Sequence[str],
    granularity: str = "1"
) -> list[Article]:
    """Retrieve multiple articles in parallel.

    Args:
        client: Configured WorldAnvilClient.
        article_ids: List of article IDs to retrieve.
        granularity: Detail level for all articles.

    Returns:
        list[Article]: Retrieved articles in same order as IDs.

    Example:
        >>> async with WorldAnvilClient(...) as client:
        ...     articles = await get_multiple_articles(
        ...         client,
        ...         ["id1", "id2", "id3"],
        ...         granularity="2"
        ...     )
    """
    tasks = [
        client.articles.get(article_id, granularity=granularity)
        for article_id in article_ids
    ]
    return await asyncio.gather(*tasks)
```

---

## MCP Context Integration

### Context Usage Pattern

```python
from mcp import Context

class WorldAnvilClient:
    """Async client with optional MCP Context integration."""

    def __init__(
        self,
        app_key: str,
        user_token: str,
        ctx: Context | None = None,
        **kwargs
    ) -> None:
        """Initialize client with optional MCP Context.

        Args:
            app_key: World Anvil application key.
            user_token: User authentication token.
            ctx: Optional MCP Context for logging and progress.
            **kwargs: Additional configuration options.
        """
        self.app_key = app_key
        self.user_token = user_token
        self.ctx = ctx
        # ... other initialization

    async def _log_info(self, message: str) -> None:
        """Log info message to MCP Context if available.

        Args:
            message: Message to log.
        """
        if self.ctx:
            await self.ctx.info(message)

    async def _log_error(self, message: str) -> None:
        """Log error message to MCP Context if available.

        Args:
            message: Error message to log.
        """
        if self.ctx:
            await self.ctx.error(message)

    async def _report_progress(self, current: int, total: int, operation: str) -> None:
        """Report operation progress to MCP Context if available.

        Args:
            current: Current progress count.
            total: Total items to process.
            operation: Description of operation in progress.
        """
        if self.ctx:
            await self.ctx.progress(current, total, operation)
```

### Request Logging Pattern

```python
async def _request(
    self,
    method: str,
    endpoint: str,
    params: dict | None = None,
    json: dict | None = None
) -> dict:
    """Execute HTTP request with MCP Context logging.

    Args:
        method: HTTP method (GET, POST, PUT, PATCH, DELETE).
        endpoint: API endpoint path.
        params: Query parameters.
        json: JSON request body.

    Returns:
        dict: Parsed JSON response.

    Raises:
        AuthenticationError: Invalid credentials (401).
        NotFoundError: Resource not found (404).
        RateLimitError: Rate limit exceeded (429).
        ServerError: Server error (500-599).
    """
    # Log request
    await self._log_info(f"{method} {endpoint}")

    try:
        response = await self._http_client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json
        )

        # Parse and return
        data = await self._parse_response(response)
        await self._log_info(f"{method} {endpoint} - Success")
        return data

    except Exception as e:
        await self._log_error(f"{method} {endpoint} - Error: {e}")
        raise
```

### Progress Reporting Pattern

```python
async def list_all_articles(
    self,
    world_id: str,
    category_id: str | None = None
) -> list[Article]:
    """Retrieve all articles with progress reporting.

    Args:
        world_id: World to list articles from.
        category_id: Optional category filter.

    Returns:
        list[Article]: All articles from world/category.
    """
    articles: list[Article] = []
    offset = 0
    limit = 50

    # Get first page to determine total
    first_page = await self.list(
        world_id=world_id,
        category_id=category_id,
        limit=limit,
        offset=0
    )

    articles.extend(first_page.articles)
    total = first_page.total

    # Report initial progress
    await self._report_progress(len(articles), total, "Fetching articles")

    # Fetch remaining pages
    while len(articles) < total:
        offset += limit
        page = await self.list(
            world_id=world_id,
            category_id=category_id,
            limit=limit,
            offset=offset
        )
        articles.extend(page.articles)
        await self._report_progress(len(articles), total, "Fetching articles")

    return articles
```

---

## Error Handling Patterns

### Exception Hierarchy

```python
class WorldAnvilError(Exception):
    """Base exception for World Anvil API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize error with message and optional status code.

        Args:
            message: Human-readable error message.
            status_code: HTTP status code if applicable.
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class AuthenticationError(WorldAnvilError):
    """Invalid or missing authentication credentials."""


class NotFoundError(WorldAnvilError):
    """Requested resource does not exist."""

    def __init__(
        self,
        message: str,
        resource_type: str,
        resource_id: str,
        status_code: int = 404
    ) -> None:
        """Initialize with resource details.

        Args:
            message: Error message.
            resource_type: Type of resource (e.g., "article").
            resource_id: ID of resource that was not found.
            status_code: HTTP status code (default 404).
        """
        super().__init__(message, status_code)
        self.resource_type = resource_type
        self.resource_id = resource_id


class RateLimitError(WorldAnvilError):
    """Rate limit exceeded."""


class ValidationError(WorldAnvilError):
    """Invalid request parameters or data."""


class ServerError(WorldAnvilError):
    """World Anvil API server error."""
```

### Response Parsing Pattern

```python
async def _parse_response(self, response: httpx.Response) -> dict:
    """Parse HTTP response and raise appropriate exceptions.

    Args:
        response: HTTP response from World Anvil API.

    Returns:
        dict: Parsed JSON response data.

    Raises:
        AuthenticationError: 401 status.
        NotFoundError: 404 status.
        RateLimitError: 429 status.
        ValidationError: 400 status.
        ServerError: 500-599 status.
    """
    # Check status code
    if response.status_code == 401:
        raise AuthenticationError(
            "Invalid authentication credentials",
            status_code=401
        )
    elif response.status_code == 404:
        raise NotFoundError(
            f"Resource not found: {response.url}",
            resource_type="unknown",
            resource_id="unknown",
            status_code=404
        )
    elif response.status_code == 429:
        raise RateLimitError(
            "Rate limit exceeded (60 requests per minute)",
            status_code=429
        )
    elif response.status_code == 400:
        data = response.json()
        raise ValidationError(
            data.get("error", "Invalid request"),
            status_code=400
        )
    elif 500 <= response.status_code < 600:
        raise ServerError(
            f"Server error: {response.status_code}",
            status_code=response.status_code
        )

    # Parse JSON
    try:
        data = response.json()
    except Exception as e:
        raise ServerError(f"Failed to parse response: {e}")

    # Check for success=false pattern (World Anvil quirk)
    if isinstance(data, dict) and data.get("success") is False:
        error_msg = data.get("error", "Unknown error")
        raise WorldAnvilError(f"API returned failure: {error_msg}")

    return data
```

---

## Retry Logic Patterns

### Retry Decorator Pattern

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

class BaseEndpoint:
    """Base endpoint with retry logic."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, ServerError))
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json: dict | None = None
    ) -> dict:
        """Execute HTTP request with automatic retries.

        Retries up to 3 times with exponential backoff (2-10 seconds)
        for rate limit and server errors only.

        Args:
            method: HTTP method.
            endpoint: API endpoint.
            params: Query parameters.
            json: Request body.

        Returns:
            dict: Parsed response.

        Raises:
            Various WorldAnvilError subclasses.
        """
        # Wait for rate limiter
        await self.client.rate_limiter.acquire()

        # Log to MCP Context
        await self.client._log_info(f"{method} {endpoint}")

        # Execute request
        response = await self.client._http_client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json
        )

        # Parse and return
        return await self.client._parse_response(response)
```

### Custom Retry Logic

```python
import asyncio

async def retry_with_backoff(
    func: Callable,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 10.0
) -> Any:
    """Execute function with exponential backoff retry logic.

    Args:
        func: Async function to execute.
        max_attempts: Maximum retry attempts.
        base_delay: Initial delay in seconds.
        max_delay: Maximum delay in seconds.

    Returns:
        Result from successful function execution.

    Raises:
        Exception from last attempt if all retries fail.
    """
    for attempt in range(max_attempts):
        try:
            return await func()
        except (RateLimitError, ServerError) as e:
            if attempt == max_attempts - 1:
                raise

            # Calculate exponential backoff
            delay = min(base_delay * (2 ** attempt), max_delay)
            await asyncio.sleep(delay)
```

---

## Rate Limiting Patterns

### Token Bucket Implementation

```python
import asyncio
import time

class RateLimiter:
    """Token bucket rate limiter for API requests."""

    def __init__(self, rate: int = 60, per: float = 60.0) -> None:
        """Initialize rate limiter.

        Args:
            rate: Number of requests allowed.
            per: Time period in seconds (default 60 for per-minute).
        """
        self.rate = rate
        self.per = per
        self.allowance = float(rate)
        self.last_check = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire token from bucket, waiting if necessary.

        Blocks until a token is available based on rate limit.
        """
        async with self._lock:
            current = time.monotonic()
            time_passed = current - self.last_check
            self.last_check = current

            # Refill tokens based on time passed
            self.allowance += time_passed * (self.rate / self.per)

            # Cap at max rate
            if self.allowance > self.rate:
                self.allowance = self.rate

            # Wait if no tokens available
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0
```

### Rate Limiter Integration

```python
class WorldAnvilClient:
    """Client with integrated rate limiting."""

    def __init__(
        self,
        app_key: str,
        user_token: str,
        rate_limit: int = 60,
        **kwargs
    ) -> None:
        """Initialize client with rate limiter.

        Args:
            app_key: API key.
            user_token: User token.
            rate_limit: Requests per minute (default 60).
            **kwargs: Additional options.
        """
        self.app_key = app_key
        self.user_token = user_token
        self.rate_limiter = RateLimiter(rate=rate_limit, per=60.0)
        # ... other initialization
```

---

## Caching Patterns

### TTL Cache Implementation

```python
from cachetools import TTLCache
from typing import Tuple, Any

class ResponseCache:
    """Time-to-live cache for API responses."""

    def __init__(self, maxsize: int = 1000, ttl: int = 300) -> None:
        """Initialize TTL cache.

        Args:
            maxsize: Maximum number of cached items.
            ttl: Time-to-live in seconds (default 5 minutes).
        """
        self._cache: TTLCache = TTLCache(maxsize=maxsize, ttl=ttl)

    def _make_key(
        self,
        resource_type: str,
        resource_id: str,
        granularity: str | None = None,
        **kwargs: Any
    ) -> Tuple:
        """Create cache key from request parameters.

        Args:
            resource_type: Type of resource (e.g., "article").
            resource_id: Resource identifier.
            granularity: Detail level if applicable.
            **kwargs: Additional parameters for key.

        Returns:
            Tuple: Immutable cache key.
        """
        key_parts = [resource_type, resource_id]
        if granularity is not None:
            key_parts.append(str(granularity))
        if kwargs:
            key_parts.extend(sorted(kwargs.items()))
        return tuple(key_parts)

    def get(self, key: Tuple) -> dict | None:
        """Retrieve cached response.

        Args:
            key: Cache key from _make_key.

        Returns:
            dict | None: Cached response or None if not found/expired.
        """
        return self._cache.get(key)

    def set(self, key: Tuple, value: dict) -> None:
        """Store response in cache.

        Args:
            key: Cache key from _make_key.
            value: Response data to cache.
        """
        self._cache[key] = value

    def clear(self) -> None:
        """Clear all cached items."""
        self._cache.clear()
```

### Cache-Aware Endpoint Pattern

```python
class ArticleEndpoint(BaseEndpoint[Article]):
    """Article endpoint with caching."""

    async def get(self, article_id: str, granularity: str = "1") -> Article:
        """Retrieve article with caching.

        Args:
            article_id: Article identifier.
            granularity: Detail level ("-1" to "3").

        Returns:
            Article: Article object.
        """
        # Check cache
        cache_key = self.client.cache._make_key(
            "article",
            article_id,
            granularity=granularity
        )

        cached = self.client.cache.get(cache_key)
        if cached is not None:
            await self.client._log_info(f"Cache hit: article/{article_id}")
            return Article(**cached)

        # Fetch from API
        await self.client._log_info(f"Cache miss: article/{article_id}")
        response = await self._request(
            "GET",
            f"/article/{article_id}",
            params={"granularity": granularity}
        )

        # Cache and return
        self.client.cache.set(cache_key, response)
        return Article(**response)
```

---

## CRUD Operation Patterns

### Read Operations

```python
class ArticleEndpoint(BaseEndpoint[Article]):
    """Article CRUD operations."""

    async def get(self, article_id: str, granularity: str = "1") -> Article:
        """Retrieve single article (READ)."""
        response = await self._request(
            "GET",
            f"/article/{article_id}",
            params={"granularity": granularity}
        )
        return Article(**response)

    async def list(
        self,
        world_id: str,
        category_id: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> ArticleList:
        """List articles in world/category (READ)."""
        body = {
            "limit": limit,
            "offset": offset
        }
        if category_id:
            body["categoryId"] = category_id

        response = await self._request(
            "POST",
            f"/world/{world_id}/articles",
            json=body
        )
        return ArticleList(**response)
```

### Create Operations

```python
async def create(
    self,
    world_id: str,
    title: str,
    category_id: str,
    state: str = "draft",
    content: str | None = None,
    **metadata: Any
) -> Article:
    """Create new article (CREATE).

    Args:
        world_id: World to create article in.
        title: Article title.
        category_id: Category for article.
        state: Publication state ("draft", "private", "public").
        content: Article content (optional).
        **metadata: Additional article metadata.

    Returns:
        Article: Newly created article.

    Raises:
        ValidationError: Invalid parameters.
        AuthenticationError: Invalid credentials.
    """
    # Build request body
    body = {
        "title": title,
        "categoryId": category_id,
        "state": state,
    }
    if content:
        body["content"] = content
    body.update(metadata)

    # Send PUT request to create
    response = await self._request(
        "PUT",
        f"/world/{world_id}/article",
        json=body
    )

    # Invalidate list cache
    self.client.cache.clear()

    return Article(**response)
```

### Update Operations

```python
async def update(
    self,
    article_id: str,
    **updates: Any
) -> Article:
    """Update existing article (UPDATE).

    Args:
        article_id: Article to update.
        **updates: Fields to update (title, content, state, etc.).

    Returns:
        Article: Updated article.

    Raises:
        NotFoundError: Article does not exist.
        ValidationError: Invalid update data.
    """
    # Send PATCH request
    response = await self._request(
        "PATCH",
        f"/article/{article_id}",
        json=updates
    )

    # Invalidate cache for this article
    cache_key = self.client.cache._make_key("article", article_id)
    if cache_key in self.client.cache._cache:
        del self.client.cache._cache[cache_key]

    return Article(**response)
```

### Delete Operations

```python
async def delete(self, article_id: str) -> None:
    """Delete article (DELETE).

    Args:
        article_id: Article to delete.

    Raises:
        NotFoundError: Article does not exist.
        AuthenticationError: Insufficient permissions.
    """
    # Send DELETE request
    await self._request(
        "DELETE",
        f"/article/{article_id}"
    )

    # Invalidate cache
    cache_key = self.client.cache._make_key("article", article_id)
    if cache_key in self.client.cache._cache:
        del self.client.cache._cache[cache_key]
```

---

## Pagination Patterns

### Scroll Collection Pattern

```python
from typing import AsyncIterator

async def iter_all_articles(
    self,
    world_id: str,
    category_id: str | None = None,
    page_size: int = 50
) -> AsyncIterator[Article]:
    """Iterate over all articles with automatic pagination.

    Args:
        world_id: World to iterate articles from.
        category_id: Optional category filter.
        page_size: Number of articles per page.

    Yields:
        Article: Individual articles.

    Example:
        >>> async for article in client.articles.iter_all_articles("world-1"):
        ...     print(article.title)
    """
    offset = 0

    while True:
        page = await self.list(
            world_id=world_id,
            category_id=category_id,
            limit=page_size,
            offset=offset
        )

        # Yield articles from this page
        for article in page.articles:
            yield article

        # Check if more pages exist
        if offset + page_size >= page.total:
            break

        offset += page_size
```

---

## Pydantic Model Patterns

### Model Definition

```python
from pydantic import BaseModel, Field, ConfigDict

class Article(BaseModel):
    """World Anvil article model.

    Attributes:
        id: Unique article identifier.
        title: Article title.
        state: Publication state (draft, private, public).
        url: Full URL to article on World Anvil.
        content: Article content (only at granularity 2+).
        tags: List of article tags.
        world: World metadata.
        category: Category metadata (if categorized).
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        validate_assignment=True
    )

    id: str
    title: str
    state: str
    url: str
    content: str | None = None
    tags: list[str] = Field(default_factory=list)
    world: dict[str, Any]
    category: dict[str, Any] | None = None

    @property
    def is_published(self) -> bool:
        """True if article is publicly published."""
        return self.state == "public"

    @property
    def world_id(self) -> str:
        """Extract world ID from nested world object."""
        return self.world.get("id", "")
```

---

## Testing Patterns

### Mock Client Pattern

```python
import pytest
import respx
from httpx import Response

@pytest.fixture
async def mock_client():
    """Provide mocked WorldAnvilClient for testing."""
    async with WorldAnvilClient(
        app_key="test-key",
        user_token="test-token"
    ) as client:
        yield client

@pytest.mark.integration
@respx.mock
async def test_get_article(mock_client):
    """Test article retrieval with mocked API."""
    # Mock API response
    respx.get(
        "https://www.worldanvil.com/api/external/boromir/article/test-id",
        params={"granularity": "1"}
    ).mock(return_value=Response(200, json={
        "id": "test-id",
        "title": "Test Article",
        "state": "public",
        "url": "https://example.com/article",
        "world": {"id": "world-1"}
    }))

    # Execute request
    article = await mock_client.articles.get("test-id")

    # Verify
    assert article.id == "test-id"
    assert article.title == "Test Article"
    assert article.is_published is True
```

---

## References

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [httpx Documentation](https://www.python-httpx.org/)
- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Tenacity Documentation](https://tenacity.readthedocs.io/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

---

**Status**: Complete ✅
**Phase 0.3**: All quality standards documents created
