# World Anvil MCP Client Architecture

**Date**: 2025-11-28
**Status**: Phase 0.1 - Architecture Design
**Based On**:
- pywaclient analysis (docs/research/pywaclient-analysis.md)
- Tool specifications (docs/specs/tool-specifications.md)
- ADR-001: Custom client decision

---

## Executive Summary

The World Anvil MCP Client is an **async-first, MCP-optimized** API client built with:
- **httpx** for async HTTP
- **Pydantic v2** for type safety
- **cachetools** for granularity-aware caching
- **tenacity** for retry logic
- **FastMCP Context** for logging and progress

**Design Principles**:
1. **MCP-Native**: Built-in Context integration, not bolted on
2. **Type-Safe**: Pydantic models for all responses
3. **Performance-First**: Caching, connection pooling, parallel requests
4. **Resilient**: Retry logic, rate limiting, comprehensive error handling
5. **Developer-Friendly**: Clear patterns, good defaults, easy debugging

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Client Class Design](#client-class-design)
4. [Endpoint Organization](#endpoint-organization)
5. [Base Classes](#base-classes)
6. [MCP Context Integration](#mcp-context-integration)
7. [Caching Strategy](#caching-strategy)
8. [Retry Logic](#retry-logic)
9. [Rate Limiting](#rate-limiting)
10. [Error Handling](#error-handling)
11. [Implementation Examples](#implementation-examples)

---

## Architecture Overview

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   MCP Server (FastMCP)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              MCP Tools (@mcp.tool())                  │  │
│  │  - get_article()  - list_articles()  - search_*()    │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           WorldAnvilClient (Main Client)              │  │
│  │  - Context integration                                │  │
│  │  - Endpoint delegation                                │  │
│  │  - Lifecycle management                               │  │
│  └───────────────────────────────────────────────────────┘  │
│         │              │              │              │       │
│         ▼              ▼              ▼              ▼       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Articles │  │  Worlds  │  │Categories│  │   Maps   │   │
│  │ Endpoint │  │ Endpoint │  │ Endpoint │  │ Endpoint │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│         │              │              │              │       │
│         └──────────────┴──────────────┴──────────────┘       │
│                           │                                  │
│                           ▼                                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │          BaseEndpoint (Request Handling)              │  │
│  │  - _request() with retry                              │  │
│  │  - Response parsing                                   │  │
│  │  - Error mapping                                      │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│         ┌─────────────────┼─────────────────┐               │
│         ▼                 ▼                 ▼               │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐          │
│  │  Cache   │      │  Retry   │      │   Rate   │          │
│  │  Layer   │      │  Logic   │      │  Limiter │          │
│  └──────────┘      └──────────┘      └──────────┘          │
│         │                 │                 │               │
│         └─────────────────┴─────────────────┘               │
│                           │                                  │
│                           ▼                                  │
│              ┌─────────────────────────┐                     │
│              │  httpx.AsyncClient      │                     │
│              │  - Connection pooling   │                     │
│              │  - Timeout management   │                     │
│              └─────────────────────────┘                     │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            ▼
                 World Anvil API (Boromir)
```

---

## Core Components

### 1. WorldAnvilClient

**File**: `src/world_anvil_mcp/client.py`

**Purpose**: Main client facade with endpoint delegation and lifecycle management

**Responsibilities**:
- Instantiate and configure httpx.AsyncClient
- Create endpoint instances
- Manage authentication headers
- Provide async context manager
- Integrate MCP Context for logging

**Code Outline**:
```python
class WorldAnvilClient:
    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str = "https://www.worldanvil.com/api/external/boromir",
        ctx: Context | None = None,
        cache_maxsize: int = 1000,
        rate_limit: int = 60
    ):
        self.ctx = ctx
        self.cache = ResponseCache(maxsize=cache_maxsize)
        self.rate_limiter = RateLimiter(rate_limit)

        # Endpoint instances
        self.users = UserEndpoint(self)
        self.worlds = WorldEndpoint(self)
        self.articles = ArticleEndpoint(self)
        # ... 15 more endpoints

    async def __aenter__(self):
        """Initialize httpx client."""
        ...

    async def __aexit__(self, *args):
        """Close httpx client."""
        ...
```

---

### 2. Endpoint Classes

**Files**: `src/world_anvil_mcp/endpoints/*.py`

**Purpose**: Resource-specific API operations

**Hierarchy**:
```
BaseEndpoint
├── UserEndpoint
├── CrudEndpoint
│   ├── ArticleEndpoint
│   ├── CategoryEndpoint
│   ├── MapEndpoint
│   └── ... (12 more)
└── WorldEndpoint (extends CrudEndpoint)
```

---

### 3. Response Cache

**File**: `src/world_anvil_mcp/cache.py`

**Purpose**: Granularity-aware response caching with different TTLs

**Features**:
- Resource-type specific TTLs
- Granularity in cache keys
- Automatic invalidation
- LRU + TTL eviction

---

### 4. Retry Logic

**File**: `src/world_anvil_mcp/retry.py`

**Purpose**: Exponential backoff for transient errors

**Features**:
- Retry on 429, 503, timeouts
- Exponential backoff: 2s, 4s, 8s
- Max 3 attempts
- Respect Retry-After header

---

### 5. Rate Limiter

**File**: `src/world_anvil_mcp/rate_limit.py`

**Purpose**: Prevent API rate limit violations

**Features**:
- Token bucket algorithm
- Configurable rate (default: 60/minute)
- Async-safe with semaphore

---

### 6. Pydantic Models

**Files**: `src/world_anvil_mcp/models/*.py`

**Purpose**: Type-safe response validation

**Organization**:
```
models/
├── __init__.py
├── article.py      # Article, ArticleReference
├── world.py        # World, WorldReference
├── category.py     # Category, CategoryReference
├── map.py          # Map, MapMarker
├── user.py         # User
└── common.py       # BaseReference, BaseResource
```

---

### 7. Exceptions

**File**: `src/world_anvil_mcp/exceptions.py`

**Purpose**: Structured error handling

**Hierarchy**:
```
WorldAnvilError (base)
└── APIError
    ├── AuthenticationError (401)
    ├── AuthorizationError (403)
    ├── NotFoundError (404)
    ├── ValidationError (422)
    ├── RateLimitError (429)
    └── ServerError (500+)
```

---

## Client Class Design

### WorldAnvilClient

```python
# src/world_anvil_mcp/client.py

import httpx
from mcp.server.fastmcp import Context
from typing import Optional

from .cache import ResponseCache
from .rate_limit import RateLimiter
from .endpoints import (
    UserEndpoint,
    WorldEndpoint,
    ArticleEndpoint,
    CategoryEndpoint,
    MapEndpoint,
    # ... more endpoints
)

class WorldAnvilClient:
    """
    Async World Anvil API client optimized for MCP integration.

    Features:
    - Built-in MCP Context logging
    - Granularity-aware caching
    - Automatic retry with exponential backoff
    - Rate limiting
    - Type-safe Pydantic responses

    Example:
        async with WorldAnvilClient(app_key, token, ctx=ctx) as client:
            article = await client.articles.get("article-id", granularity=2)
            print(article.title)
    """

    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str = "https://www.worldanvil.com/api/external/boromir",
        ctx: Optional[Context] = None,
        cache_maxsize: int = 1000,
        rate_limit: int = 60,
        timeout: float = 30.0
    ):
        """
        Initialize World Anvil API client.

        Args:
            app_key: World Anvil application key
            user_token: User authentication token
            base_url: API base URL (default: Boromir API)
            ctx: Optional MCP Context for logging
            cache_maxsize: Maximum cache entries (default: 1000)
            rate_limit: Requests per minute (default: 60)
            timeout: Request timeout in seconds (default: 30)
        """
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url
        self.ctx = ctx
        self.timeout = timeout

        # Components
        self.cache = ResponseCache(maxsize=cache_maxsize)
        self.rate_limiter = RateLimiter(rate_limit)

        # HTTP client (created in __aenter__)
        self._http_client: Optional[httpx.AsyncClient] = None

        # Endpoint instances (initialized after client creation)
        self.users: Optional[UserEndpoint] = None
        self.worlds: Optional[WorldEndpoint] = None
        self.articles: Optional[ArticleEndpoint] = None
        self.categories: Optional[CategoryEndpoint] = None
        self.maps: Optional[MapEndpoint] = None
        # ... more endpoints

    async def __aenter__(self) -> "WorldAnvilClient":
        """
        Initialize HTTP client as async context manager.

        Returns:
            Self for context manager pattern
        """
        # Create httpx client with configuration
        self._http_client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._build_headers(),
            timeout=httpx.Timeout(
                timeout=self.timeout,
                connect=10.0
            ),
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5
            )
        )

        # Initialize endpoints
        self.users = UserEndpoint(self)
        self.worlds = WorldEndpoint(self)
        self.articles = ArticleEndpoint(self)
        self.categories = CategoryEndpoint(self)
        self.maps = MapEndpoint(self)
        # ... more endpoints

        if self.ctx:
            await self.ctx.info("World Anvil client initialized")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close HTTP client."""
        if self._http_client:
            await self._http_client.aclose()
            if self.ctx:
                await self.ctx.info("World Anvil client closed")

    def _build_headers(self) -> dict[str, str]:
        """
        Build authentication headers.

        Critical: Use lowercase header names!
        x-auth-token, x-application-key (not X-Auth-Token)

        Returns:
            Headers dict for requests
        """
        return {
            "x-auth-token": self.user_token,
            "x-application-key": self.app_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "world-anvil-mcp/0.1.0 (MCP Server)"
        }

    @property
    def http(self) -> httpx.AsyncClient:
        """
        Get HTTP client, ensuring it's initialized.

        Raises:
            RuntimeError: If client not initialized (use async with)
        """
        if self._http_client is None:
            raise RuntimeError(
                "Client not initialized. Use 'async with WorldAnvilClient(...) as client:'"
            )
        return self._http_client

    async def close(self):
        """Explicitly close client (if not using context manager)."""
        if self._http_client:
            await self._http_client.aclose()
```

---

## Endpoint Organization

### Base Endpoint

```python
# src/world_anvil_mcp/endpoints/base.py

from typing import TypeVar, Generic, Any
from pydantic import BaseModel
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from ..exceptions import RateLimitError, ServerError
from ..models.common import BaseResource

T = TypeVar('T', bound=BaseModel)

class BaseEndpoint(Generic[T]):
    """
    Base class for all endpoint implementations.

    Provides:
    - HTTP request methods with retry
    - Response parsing and validation
    - Error handling and mapping
    - Cache integration
    - MCP Context logging
    """

    def __init__(self, client: "WorldAnvilClient", base_path: str):
        """
        Initialize endpoint.

        Args:
            client: WorldAnvilClient instance
            base_path: API path for this endpoint (e.g., "article")
        """
        self.client = client
        self.path = base_path

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, ServerError))
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Make authenticated API request with retry.

        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            endpoint: API endpoint path
            params: Query parameters
            json: JSON body for POST/PATCH

        Returns:
            Parsed response dict

        Raises:
            AuthenticationError: Invalid credentials
            AuthorizationError: No access
            NotFoundError: Resource not found
            ValidationError: Invalid request data
            RateLimitError: Rate limit exceeded
            ServerError: Server-side error
        """
        # Rate limiting
        await self.client.rate_limiter.acquire()

        # Log request
        if self.client.ctx:
            await self.client.ctx.info(
                f"{method} {endpoint} "
                f"(params={params}, body={'present' if json else 'none'})"
            )

        # Make request
        response = await self.client.http.request(
            method,
            endpoint,
            params=params,
            json=json
        )

        # Parse and validate response
        return await self._parse_response(response, endpoint)

    async def _parse_response(
        self,
        response: httpx.Response,
        endpoint: str
    ) -> dict[str, Any]:
        """
        Parse response and handle errors.

        Critical: Check 'success' flag, not just status code!
        World Anvil API returns 200 OK with {"success": false} for errors.

        Args:
            response: httpx Response
            endpoint: Endpoint path for error messages

        Returns:
            Response data dict

        Raises:
            Various APIError subclasses
        """
        from ..exceptions import (
            AuthenticationError,
            AuthorizationError,
            NotFoundError,
            ValidationError,
            RateLimitError,
            ServerError,
            APIError
        )

        # Status code errors
        if response.status_code == 401:
            raise AuthenticationError(endpoint)
        elif response.status_code == 403:
            raise AuthorizationError(endpoint)
        elif response.status_code == 404:
            raise NotFoundError(endpoint)
        elif response.status_code == 422:
            data = response.json()
            raise ValidationError(endpoint, data.get('error', {}))
        elif response.status_code == 429:
            retry_after = response.headers.get('Retry-After')
            raise RateLimitError(
                endpoint,
                int(retry_after) if retry_after else None
            )
        elif response.status_code >= 500:
            raise ServerError(response.status_code, endpoint)

        # Parse 200 OK responses
        if response.status_code == 200:
            data = response.json()

            # Check success flag
            if 'success' not in data:
                raise APIError(
                    200,
                    "Response missing 'success' flag",
                    endpoint
                )

            if not data['success']:
                error_msg = data.get('error', 'Unknown error')
                raise APIError(
                    200,
                    f"API returned success=false: {error_msg}",
                    endpoint
                )

            return data

        # Unexpected status
        raise APIError(
            response.status_code,
            response.reason_phrase,
            endpoint
        )

    async def _get(
        self,
        resource_id: str,
        granularity: int = 1,
        model_class: type[T] = None
    ) -> T:
        """
        Get single resource by ID.

        Args:
            resource_id: Resource identifier
            granularity: Detail level (0-2)
            model_class: Pydantic model for validation

        Returns:
            Validated model instance
        """
        # Build cache key
        cache_key = self.client.cache.build_key(
            self.path,
            resource_id,
            granularity=granularity
        )

        # Check cache
        cached = self.client.cache.get(cache_key, self.path)
        if cached:
            if self.client.ctx:
                await self.client.ctx.info(f"Cache hit: {cache_key}")
            return model_class.model_validate(cached)

        # Fetch from API
        data = await self._request(
            'GET',
            f'/{self.path}',
            params={
                'id': resource_id,
                'granularity': str(granularity)  # IMPORTANT: String!
            }
        )

        # Cache response
        self.client.cache.set(cache_key, data, self.path)

        # Validate and return
        return model_class.model_validate(data)

    async def _list(
        self,
        endpoint: str,
        params: dict[str, Any],
        json_body: dict[str, Any],
        model_class: type[T],
        collection_key: str = 'entities'
    ) -> list[T]:
        """
        List resources with pagination.

        Args:
            endpoint: API endpoint
            params: Query parameters
            json_body: POST body with limit/offset
            model_class: Pydantic model for items
            collection_key: Key in response containing items

        Returns:
            List of validated model instances
        """
        # Build cache key
        cache_key = self.client.cache.build_key(
            'list',
            endpoint,
            **{**params, **json_body}
        )

        # Check cache
        cached = self.client.cache.get(cache_key, 'list')
        if cached:
            if self.client.ctx:
                await self.client.ctx.info(f"Cache hit: {cache_key}")
            return [model_class.model_validate(item) for item in cached]

        # Fetch from API
        data = await self._request(
            'POST',
            endpoint,
            params=params,
            json=json_body
        )

        # Extract collection
        items = data.get(collection_key, [])

        # Cache response
        self.client.cache.set(cache_key, items, 'list')

        # Validate and return
        return [model_class.model_validate(item) for item in items]
```

---

### CRUD Endpoint

```python
# src/world_anvil_mcp/endpoints/crud.py

from typing import TypeVar
from pydantic import BaseModel

from .base import BaseEndpoint

T = TypeVar('T', bound=BaseModel)

class CrudEndpoint(BaseEndpoint[T]):
    """
    Base class for endpoints supporting CRUD operations.

    Provides:
    - get(id, granularity) -> T
    - create(data) -> T (future)
    - update(id, data) -> T (future)
    - delete(id) -> None (future)
    """

    async def get(self, resource_id: str, granularity: int = 1) -> T:
        """
        Get resource by ID.

        Must be overridden in subclass to specify model_class.
        """
        raise NotImplementedError("Subclass must implement get()")
```

---

### Article Endpoint Example

```python
# src/world_anvil_mcp/endpoints/article.py

from ..models.article import Article, ArticleReference
from .crud import CrudEndpoint

class ArticleEndpoint(CrudEndpoint[Article]):
    """Article-specific operations."""

    def __init__(self, client):
        super().__init__(client, 'article')

    async def get(self, article_id: str, granularity: int = 1) -> Article:
        """
        Get article by ID.

        Args:
            article_id: Article UUID
            granularity: 0=preview, 1=standard, 2=extended with content

        Returns:
            Article model
        """
        return await self._get(article_id, granularity, Article)

    async def search(
        self,
        query: str,
        world_id: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[ArticleReference]:
        """
        Search articles by text.

        Args:
            query: Search query
            world_id: Optional world filter
            limit: Results per page (1-50)
            offset: Pagination offset

        Returns:
            List of article references
        """
        json_body = {
            'query': query,
            'limit': limit,
            'offset': offset
        }
        if world_id:
            json_body['world'] = {'id': world_id}

        return await self._list(
            f'/{self.path}/search',
            params={},
            json_body=json_body,
            model_class=ArticleReference
        )
```

---

### World Endpoint Example

```python
# src/world_anvil_mcp/endpoints/world.py

from ..models.world import World, WorldReference
from ..models.article import ArticleReference
from ..models.category import CategoryReference
from .crud import CrudEndpoint

class WorldEndpoint(CrudEndpoint[World]):
    """World-specific operations with list methods."""

    def __init__(self, client):
        super().__init__(client, 'world')
        # Additional paths for list endpoints
        self.path_articles = f'{self.path}/articles'
        self.path_categories = f'{self.path}/categories'
        self.path_maps = f'{self.path}/maps'
        # ... more list paths

    async def get(self, world_id: str, granularity: int = 1) -> World:
        """Get world by ID."""
        return await self._get(world_id, granularity, World)

    async def articles(
        self,
        world_id: str,
        category_id: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[ArticleReference]:
        """
        List articles in world.

        Args:
            world_id: World UUID
            category_id: Optional category filter ("-1" for uncategorized)
            limit: Results per page (1-50)
            offset: Pagination offset

        Returns:
            List of article references
        """
        json_body = {'limit': limit, 'offset': offset}
        if category_id:
            json_body['category'] = {'id': category_id}

        return await self._list(
            self.path_articles,
            params={'id': world_id},
            json_body=json_body,
            model_class=ArticleReference
        )

    async def categories(
        self,
        world_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> list[CategoryReference]:
        """List categories in world."""
        return await self._list(
            self.path_categories,
            params={'id': world_id},
            json_body={'limit': limit, 'offset': offset},
            model_class=CategoryReference
        )
```

---

## MCP Context Integration

### Logging Levels

```python
# Throughout client implementation

# Info: Normal operations
if self.ctx:
    await self.ctx.info("Fetching article 123")

# Warning: Recoverable issues
if self.ctx:
    await self.ctx.warning("Cache miss, fetching from API")

# Error: Failures
if self.ctx:
    await self.ctx.error(f"Failed to fetch article: {e}")
```

### Progress Reporting

```python
# For long-running operations (future)

async def get_all_articles(self, world_id: str) -> list[Article]:
    """Get all articles with progress reporting."""
    total = await self._get_article_count(world_id)

    if self.ctx:
        await self.ctx.info(f"Fetching {total} articles...")

    articles = []
    offset = 0
    limit = 50

    while offset < total:
        batch = await self.articles(world_id, limit=limit, offset=offset)
        articles.extend(batch)
        offset += limit

        if self.ctx:
            progress = min(100, int((offset / total) * 100))
            await self.ctx.info(f"Progress: {progress}% ({offset}/{total})")

    return articles
```

---

## Caching Strategy

Detailed in `tool-specifications.md` Caching Strategy section.

**Key Points**:
- Resource-type specific TTLs
- Granularity in cache keys
- LRU + TTL eviction
- Cache invalidation on writes (future)

---

## Retry Logic

```python
# src/world_anvil_mcp/retry.py

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from .exceptions import RateLimitError, ServerError

# Decorator applied to _request() method
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((RateLimitError, ServerError))
)
async def _request(...):
    ...
```

**Retry Strategy**:
- Max 3 attempts
- Exponential backoff: 2s, 4s, 8s
- Only retry on:
  - 429 Rate Limit (with Retry-After)
  - 500+ Server errors
  - Connection timeouts
- Don't retry on:
  - 401/403 Auth errors
  - 404 Not found
  - 422 Validation errors

---

## Rate Limiting

```python
# src/world_anvil_mcp/rate_limit.py

import asyncio
import time

class RateLimiter:
    """
    Token bucket rate limiter.

    Default: 60 requests per minute
    """

    def __init__(self, rate_limit: int = 60):
        """
        Initialize rate limiter.

        Args:
            rate_limit: Max requests per minute
        """
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self.last_refill = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self):
        """
        Acquire token for request.

        Blocks if no tokens available, refills at 1 per second.
        """
        async with self.lock:
            # Refill tokens based on time elapsed
            now = time.time()
            elapsed = now - self.last_refill
            refill = int(elapsed * (self.rate_limit / 60))

            if refill > 0:
                self.tokens = min(self.rate_limit, self.tokens + refill)
                self.last_refill = now

            # Wait if no tokens available
            while self.tokens <= 0:
                await asyncio.sleep(1)
                now = time.time()
                elapsed = now - self.last_refill
                refill = int(elapsed * (self.rate_limit / 60))

                if refill > 0:
                    self.tokens = min(self.rate_limit, self.tokens + refill)
                    self.last_refill = now

            # Consume token
            self.tokens -= 1
```

---

## Error Handling

Detailed in `tool-specifications.md` Error Handling section.

**Error Flow**:
```
Request → httpx → _parse_response()
                       │
                       ├─ 401 → AuthenticationError
                       ├─ 403 → AuthorizationError
                       ├─ 404 → NotFoundError
                       ├─ 422 → ValidationError
                       ├─ 429 → RateLimitError (retry)
                       ├─ 500+ → ServerError (retry)
                       └─ 200 → Check success flag
                                  ├─ true → return data
                                  └─ false → APIError
```

---

## Implementation Examples

### Basic Article Fetch

```python
# MCP Tool implementation

@mcp.tool()
async def get_article(article_id: str, granularity: int = 1, ctx: Context) -> dict:
    """Get article from World Anvil."""
    async with WorldAnvilClient(
        app_key=os.getenv("WORLD_ANVIL_APP_KEY"),
        user_token=os.getenv("WORLD_ANVIL_USER_TOKEN"),
        ctx=ctx
    ) as client:
        article = await client.articles.get(article_id, granularity)
        return article.model_dump()
```

### List with Pagination

```python
@mcp.tool()
async def list_world_articles(
    world_id: str,
    category_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """List articles in a world."""
    async with WorldAnvilClient(..., ctx=ctx) as client:
        articles = await client.worlds.articles(
            world_id,
            category_id=category_id,
            limit=limit,
            offset=offset
        )
        return {
            "entities": [a.model_dump() for a in articles],
            "meta": {
                "limit": limit,
                "offset": offset,
                "count": len(articles)
            }
        }
```

### Search with Error Handling

```python
@mcp.tool()
async def search_articles(query: str, world_id: str | None = None, ctx: Context) -> dict:
    """Search articles."""
    async with WorldAnvilClient(..., ctx=ctx) as client:
        try:
            results = await client.articles.search(query, world_id=world_id)
            return {"results": [r.model_dump() for r in results]}
        except NotFoundError:
            await ctx.warning(f"No articles found for: {query}")
            return {"results": []}
        except RateLimitError as e:
            await ctx.error(f"Rate limited, retry after {e.retry_after}s")
            raise
```

---

## File Structure

```
src/world_anvil_mcp/
├── __init__.py
├── client.py                    # WorldAnvilClient
├── cache.py                     # ResponseCache
├── rate_limit.py                # RateLimiter
├── retry.py                     # Retry decorators
├── exceptions.py                # Error classes
├── endpoints/
│   ├── __init__.py              # Export all endpoints
│   ├── base.py                  # BaseEndpoint
│   ├── crud.py                  # CrudEndpoint
│   ├── article.py               # ArticleEndpoint
│   ├── world.py                 # WorldEndpoint
│   ├── category.py              # CategoryEndpoint
│   ├── user.py                  # UserEndpoint
│   ├── map.py                   # MapEndpoint
│   └── ...                      # 15+ more endpoints
└── models/
    ├── __init__.py              # Export all models
    ├── common.py                # BaseReference, BaseResource
    ├── article.py               # Article, ArticleReference
    ├── world.py                 # World, WorldReference
    ├── category.py              # Category, CategoryReference
    ├── user.py                  # User
    ├── map.py                   # Map, MapMarker
    └── ...                      # 15+ more model files
```

---

## Testing Strategy

### Unit Tests
```python
# tests/test_client.py

@pytest.mark.asyncio
async def test_get_article():
    async with WorldAnvilClient(...) as client:
        article = await client.articles.get("test-id", granularity=1)
        assert article.id == "test-id"
        assert isinstance(article, Article)
```

### Integration Tests
```python
# tests/integration/test_article_endpoint.py

@pytest.mark.asyncio
async def test_article_caching():
    async with WorldAnvilClient(...) as client:
        # First call - cache miss
        article1 = await client.articles.get("test-id")

        # Second call - cache hit
        article2 = await client.articles.get("test-id")

        assert article1.id == article2.id
        # Verify cache was used (mock HTTP client)
```

### Mock Fixtures
```python
# tests/conftest.py

@pytest.fixture
def mock_world_anvil_api():
    with respx.mock:
        respx.get("/article").mock(return_value=httpx.Response(
            200,
            json={"success": True, "id": "test", "title": "Test Article"}
        ))
        yield
```

---

## Performance Targets

### Latency
- Cache hit: <10ms
- Simple GET: <500ms (p95)
- List operation: <1s (p95)
- Search: <2s (p95)

### Throughput
- 60 requests/minute (rate limit)
- 10 concurrent connections
- 1000 cached responses

### Resource Usage
- Memory: <100MB baseline
- Cache: ~50MB with 1000 entries
- Connections: Max 10 simultaneous

---

## Security Considerations

### Credential Management
- Never log API keys or tokens
- Use environment variables
- Clear sensitive data on client close

### HTTPS Only
- Force TLS for all requests
- Verify SSL certificates

### Rate Limiting
- Prevent API abuse
- Respect server limits

---

## Future Enhancements

### Phase 2+
1. **Write Operations** (when API supports)
   - create_article(), update_article(), delete_article()
   - Cache invalidation on writes

2. **Batch Operations**
   - Parallel fetching of multiple resources
   - Bulk operations with progress reporting

3. **Streaming Responses**
   - Server-Sent Events (if API supports)
   - Async iterators for large lists

4. **Advanced Caching**
   - Persistent cache (disk-based)
   - Cache warming strategies
   - Smart invalidation patterns

---

**Status**: ✅ Architecture Design Complete
**Date**: 2025-11-28
**Next**: Phase 0.3 - Quality Rules & Standards
