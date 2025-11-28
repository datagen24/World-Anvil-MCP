Architecture
============

This section documents the architectural design of the World Anvil MCP Server.

.. toctree::
   :maxdepth: 2
   :caption: Architecture Topics:

   overview
   client_design
   mcp_integration
   caching_strategy
   error_handling

System Overview
---------------

The World Anvil MCP Server follows a **layered architecture** with clear separation of concerns:

.. code-block:: text

    ┌─────────────────────────────────────────────────┐
    │           Claude Code / User Layer              │
    │  (Natural language interactions via MCP)        │
    └─────────────────────┬───────────────────────────┘
                          │
    ┌─────────────────────▼───────────────────────────┐
    │              MCP Protocol Layer                  │
    │  - FastMCP Server                                │
    │  - Tool handlers                                 │
    │  - Resource providers                            │
    └─────────────────────┬───────────────────────────┘
                          │
    ┌─────────────────────▼───────────────────────────┐
    │           WorldAnvilClient Layer                 │
    │  - Main entry point                              │
    │  - Endpoint coordination                         │
    │  - Session management                            │
    └─────────────────────┬───────────────────────────┘
                          │
    ┌─────────────────────▼───────────────────────────┐
    │            Endpoint Layer                        │
    │  - ArticleEndpoint                               │
    │  - WorldEndpoint                                 │
    │  - CategoryEndpoint                              │
    │  - MapEndpoint                                   │
    │  - CampaignEndpoint                              │
    └─────────────────────┬───────────────────────────┘
                          │
    ┌─────────────────────▼───────────────────────────┐
    │           BaseEndpoint Layer                     │
    │  - HTTP request handling                         │
    │  - Response parsing                              │
    │  - Error transformation                          │
    └─────────┬───────────┬────────────┬───────────────┘
              │           │            │
    ┌─────────▼─────┐ ┌──▼──────┐ ┌───▼──────────┐
    │ ResponseCache │ │RateLimiter│ │ RetryLogic   │
    │ (TTL-based)   │ │(60 req/min)│ │ (exponential)│
    └───────────────┘ └───────────┘ └──────────────┘
                          │
    ┌─────────────────────▼───────────────────────────┐
    │         World Anvil Boromir API v2               │
    │  (REST API with custom authentication)           │
    └──────────────────────────────────────────────────┘

Layered Design
--------------

Layer 1: MCP Protocol Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Expose World Anvil operations to Claude Code via Model Context Protocol.

**Components**:

- **FastMCP Server**: Handles MCP protocol communication
- **Tool Handlers**: Map MCP tool calls to client methods
- **Resource Providers**: Expose schemas and templates

**Responsibilities**:

- Protocol compliance (MCP specification)
- Tool registration and discovery
- Request validation
- Response serialization

**Example Tool Handler**:

.. code-block:: python

    from mcp.server import Server
    from world_anvil_mcp import WorldAnvilClient

    server = Server("world-anvil")
    client = WorldAnvilClient()

    @server.call_tool()
    async def get_article(arguments: dict) -> dict:
        """MCP tool handler for get_article."""
        article = await client.articles.get(arguments["article_id"])
        return article.model_dump()

Layer 2: WorldAnvilClient Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Main entry point providing unified access to all World Anvil operations.

**Responsibilities**:

- Session management (httpx.AsyncClient)
- Endpoint initialization and coordination
- Configuration management
- Resource cleanup

**Design Pattern**: **Facade Pattern** - Provides simplified interface to complex subsystem.

**Example**:

.. code-block:: python

    class WorldAnvilClient:
        """Unified client for World Anvil API operations."""

        def __init__(
            self,
            app_key: str,
            user_token: str,
            base_url: str = "https://www.worldanvil.com/api/external/boromir",
        ):
            self._session = httpx.AsyncClient(base_url=base_url)
            self._cache = ResponseCache()
            self._rate_limiter = RateLimiter(rate=60, per=60.0)

            # Initialize endpoints
            self.articles = ArticleEndpoint(self._session, self._cache, ...)
            self.worlds = WorldEndpoint(self._session, self._cache, ...)
            self.categories = CategoryEndpoint(self._session, self._cache, ...)

Layer 3: Endpoint Layer
~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Specialized classes for different resource types (articles, worlds, etc.).

**Responsibilities**:

- Resource-specific operations (CRUD)
- Parameter validation
- Response transformation to Pydantic models

**Design Pattern**: **Repository Pattern** - Encapsulates data access logic.

**Example**:

.. code-block:: python

    class ArticleEndpoint(BaseEndpoint):
        """Handle article-related operations."""

        async def get(self, article_id: str, granularity: str = "2") -> Article:
            """Get a specific article."""
            response = await self._request(
                "GET",
                f"/articles/{article_id}",
                params={"granularity": granularity}
            )
            return Article(**response)

        async def list(
            self,
            world_id: str,
            category_id: str | None = None,
        ) -> list[Article]:
            """List articles with optional filters."""
            params = {"worldId": world_id}
            if category_id:
                params["categoryId"] = category_id

            response = await self._request("GET", "/articles", params=params)
            return [Article(**item) for item in response]

Layer 4: BaseEndpoint Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Purpose**: Common HTTP request handling for all endpoints.

**Responsibilities**:

- HTTP method abstraction (GET, POST, PUT, DELETE)
- Authentication header injection
- Cache integration
- Rate limit enforcement
- Retry logic coordination
- Error handling and transformation

**Design Pattern**: **Template Method Pattern** - Defines skeleton of request handling.

**Example**:

.. code-block:: python

    class BaseEndpoint:
        """Base class for all endpoint implementations."""

        async def _request(
            self,
            method: str,
            path: str,
            params: dict | None = None,
            json: dict | None = None,
        ) -> dict | list:
            """Make authenticated HTTP request with caching and retry."""
            # Check cache
            cache_key = self._cache_key(method, path, params)
            if cached := self._cache.get(cache_key):
                return cached

            # Rate limiting
            await self._rate_limiter.acquire()

            # Make request with retry
            response = await self._retry_request(method, path, params, json)

            # Cache successful response
            self._cache.set(cache_key, response.json())

            return response.json()

Infrastructure Components
-------------------------

ResponseCache
~~~~~~~~~~~~~

**Purpose**: TTL-based caching to reduce API calls and improve response time.

**Implementation**: Dictionary with expiration timestamps.

**Cache Strategy**:

.. list-table::
   :header-rows: 1
   :widths: 30 20 50

   * - Resource Type
     - TTL
     - Rationale
   * - World metadata
     - 1 hour
     - Rarely changes
   * - Article content
     - 5 minutes
     - May be edited during sessions
   * - Category hierarchy
     - 15 minutes
     - Moderate change frequency
   * - Search results
     - 2 minutes
     - Frequently changing, needs freshness
   * - Map data
     - 30 minutes
     - Stable structure

**Example**:

.. code-block:: python

    class ResponseCache:
        """TTL-based response cache."""

        def __init__(self, default_ttl: int = 300):
            self._cache: dict[str, tuple[Any, float]] = {}
            self._default_ttl = default_ttl

        def get(self, key: str) -> Any | None:
            """Get cached value if not expired."""
            if key in self._cache:
                value, expires_at = self._cache[key]
                if time.time() < expires_at:
                    return value
                del self._cache[key]
            return None

        def set(self, key: str, value: Any, ttl: int | None = None) -> None:
            """Cache value with expiration."""
            ttl = ttl or self._default_ttl
            expires_at = time.time() + ttl
            self._cache[key] = (value, expires_at)

RateLimiter
~~~~~~~~~~~

**Purpose**: Enforce World Anvil API rate limits (60 requests/minute).

**Implementation**: Token bucket algorithm.

**Behavior**:

- Tokens refill at 1 per second (60/min)
- Maximum 60 tokens in bucket
- Each request consumes 1 token
- Requests wait if no tokens available

**Example**:

.. code-block:: python

    class RateLimiter:
        """Token bucket rate limiter."""

        def __init__(self, rate: int = 60, per: float = 60.0):
            self._rate = rate
            self._per = per
            self._tokens = rate
            self._last_update = time.time()

        async def acquire(self) -> None:
            """Acquire token, waiting if necessary."""
            while True:
                now = time.time()
                elapsed = now - self._last_update
                self._tokens = min(
                    self._rate,
                    self._tokens + (elapsed * self._rate / self._per)
                )
                self._last_update = now

                if self._tokens >= 1:
                    self._tokens -= 1
                    return

                # Wait for token
                await asyncio.sleep(self._per / self._rate)

Retry Logic
~~~~~~~~~~~

**Purpose**: Handle transient failures with exponential backoff.

**Implementation**: tenacity library with custom retry conditions.

**Retry Strategy**:

- **Retryable errors**: Network errors, 5xx responses, rate limits
- **Non-retryable errors**: 4xx client errors (except 429)
- **Max attempts**: 3 retries
- **Backoff**: Exponential (1s, 2s, 4s)

**Example**:

.. code-block:: python

    from tenacity import (
        retry,
        stop_after_attempt,
        wait_exponential,
        retry_if_exception_type,
    )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception_type((NetworkError, RateLimitError)),
    )
    async def _retry_request(self, method: str, path: str, ...) -> httpx.Response:
        """Make HTTP request with automatic retry."""
        response = await self._session.request(method, path, ...)
        response.raise_for_status()
        return response

Data Flow
---------

Request Flow Example
~~~~~~~~~~~~~~~~~~~~

**User request**: "Get article abc-123"

1. **Claude Code** receives natural language request
2. **MCP Server** translates to ``get_article`` tool call
3. **Tool Handler** validates arguments, calls ``client.articles.get("abc-123")``
4. **ArticleEndpoint** prepares request parameters
5. **BaseEndpoint** checks cache (miss)
6. **RateLimiter** acquires token (may wait)
7. **HTTP Client** makes authenticated GET request
8. **Retry Logic** handles transient failures
9. **BaseEndpoint** parses JSON response
10. **ResponseCache** stores result (TTL: 5 minutes)
11. **ArticleEndpoint** transforms to Pydantic ``Article`` model
12. **Tool Handler** serializes to JSON for MCP
13. **Claude Code** presents formatted response to user

Response Flow with Cache Hit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**User request**: "Get article abc-123" (second time within 5 minutes)

1. **Claude Code** → MCP Server → Tool Handler → ``client.articles.get("abc-123")``
2. **BaseEndpoint** checks cache (**hit**)
3. **ResponseCache** returns cached response
4. **ArticleEndpoint** transforms to ``Article`` model
5. **Tool Handler** → MCP Server → Claude Code
6. **User** receives instant response

**Performance Gain**: ~500ms → ~10ms

Error Handling Architecture
----------------------------

Exception Hierarchy
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    WorldAnvilError (base exception)
    ├── WorldAnvilAPIError (API-related errors)
    │   ├── AuthenticationError (401, 403)
    │   ├── NotFoundError (404)
    │   ├── RateLimitError (429)
    │   ├── ValidationError (400)
    │   └── ServerError (5xx)
    └── WorldAnvilClientError (client-side errors)
        ├── ConfigurationError (invalid config)
        └── CacheError (cache failures)

Error Transformation
~~~~~~~~~~~~~~~~~~~~

HTTP errors are transformed to domain-specific exceptions:

.. code-block:: python

    async def _handle_error(self, response: httpx.Response) -> None:
        """Transform HTTP errors to domain exceptions."""
        if response.status_code == 401:
            raise AuthenticationError("Invalid credentials")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {response.url}")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif 400 <= response.status_code < 500:
            raise ValidationError(f"Invalid request: {response.text}")
        elif response.status_code >= 500:
            raise ServerError(f"Server error: {response.status_code}")

Error Recovery Patterns
~~~~~~~~~~~~~~~~~~~~~~~

**Retry with Backoff** (transient failures):

.. code-block:: python

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    async def _retry_request(...):
        """Automatic retry for network errors and 5xx."""

**Graceful Degradation** (cache on error):

.. code-block:: python

    try:
        response = await self._request(...)
    except WorldAnvilAPIError:
        # Return stale cache if available
        if stale := self._cache.get_stale(cache_key):
            return stale
        raise

**Fallback Strategies** (alternative approaches):

.. code-block:: python

    try:
        article = await client.articles.get(article_id)
    except NotFoundError:
        # Fallback to search
        results = await client.articles.search(term=article_name)
        article = results[0] if results else None

Security Architecture
---------------------

Authentication
~~~~~~~~~~~~~~

World Anvil uses **custom header-based authentication**:

.. code-block:: python

    headers = {
        "x-application-key": app_key,  # Lowercase!
        "x-auth-token": user_token,    # Lowercase!
    }

**Security Considerations**:

- Credentials never logged or exposed
- Environment variables for configuration
- No credential storage in cache
- Separate test/production credentials

Input Validation
~~~~~~~~~~~~~~~~

All inputs validated at multiple layers:

1. **MCP Layer**: Tool argument schemas
2. **Endpoint Layer**: Parameter type checking
3. **Pydantic Models**: Strict validation
4. **API Layer**: Server-side validation

**Example**:

.. code-block:: python

    class Article(BaseModel):
        """Article model with strict validation."""

        id: str = Field(..., pattern=r"^[a-f0-9-]{36}$")
        title: str = Field(..., min_length=1, max_length=255)
        state: Literal["public", "private", "draft"]

Output Sanitization
~~~~~~~~~~~~~~~~~~~

Responses sanitized before returning to users:

- HTML content escaped for display
- Sensitive fields filtered (API keys, tokens)
- PII handling according to privacy requirements

Performance Architecture
------------------------

Performance Targets
~~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Operation Type
     - Target (P95)
     - Strategy
   * - Cached reads
     - <50ms
     - Memory cache
   * - Simple API calls
     - <500ms
     - Keep-alive, caching
   * - Complex searches
     - <2s
     - Pagination, indexing
   * - Batch operations
     - <5s
     - Parallel requests

Optimization Strategies
~~~~~~~~~~~~~~~~~~~~~~~

**Connection Pooling**:

.. code-block:: python

    # httpx.AsyncClient maintains connection pool
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
    client = httpx.AsyncClient(limits=limits)

**Parallel Requests**:

.. code-block:: python

    async def batch_get_articles(article_ids: list[str]) -> list[Article]:
        """Fetch multiple articles in parallel."""
        tasks = [client.articles.get(id) for id in article_ids]
        return await asyncio.gather(*tasks)

**Lazy Loading**:

.. code-block:: python

    class Article(BaseModel):
        """Article with lazy content loading."""

        id: str
        title: str
        content: str | None = None  # Only load if requested

**Streaming Responses** (future):

.. code-block:: python

    async def stream_articles(world_id: str) -> AsyncIterator[Article]:
        """Stream articles without loading all into memory."""
        async for page in paginate("/articles", world_id):
            for item in page:
                yield Article(**item)

Deployment Architecture
-----------------------

MCP Server Deployment
~~~~~~~~~~~~~~~~~~~~~

**Local Development**:

.. code-block:: bash

    # Start server manually
    world-anvil-mcp

**Claude Code Integration**:

.. code-block:: json

    {
      "mcpServers": {
        "world-anvil": {
          "command": "world-anvil-mcp",
          "env": {
            "WORLD_ANVIL_API_KEY": "...",
            "WORLD_ANVIL_USER_TOKEN": "..."
          }
        }
      }
    }

**Docker Deployment** (future):

.. code-block:: dockerfile

    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN pip install .
    CMD ["world-anvil-mcp"]

Scalability Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Current Scale**: Single-user, local execution

**Future Considerations**:

- Multi-tenant support (separate credentials per user)
- Distributed caching (Redis)
- Load balancing (multiple server instances)
- Database backing (persistent storage)

Monitoring and Observability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Logging**:

.. code-block:: python

    import logging

    logger = logging.getLogger("world_anvil_mcp")
    logger.info("Fetching article %s", article_id)

**Metrics** (future):

- Request latency (P50, P95, P99)
- Cache hit rate
- Rate limit utilization
- Error rates by type

**Tracing** (future):

- Distributed tracing with OpenTelemetry
- Request correlation IDs
- Performance profiling

Design Patterns Summary
-----------------------

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Pattern
     - Where Used
     - Purpose
   * - Facade
     - WorldAnvilClient
     - Unified interface
   * - Repository
     - Endpoint classes
     - Data access abstraction
   * - Template Method
     - BaseEndpoint._request
     - Common request flow
   * - Singleton
     - ResponseCache, RateLimiter
     - Shared state
   * - Strategy
     - Retry logic
     - Configurable behavior
   * - Factory
     - Model creation
     - Object construction
   * - Async Context Manager
     - Client lifecycle
     - Resource cleanup

Future Architecture Evolution
------------------------------

Phase 1: Core Foundation (Current)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Read-only operations
- Basic caching and rate limiting
- MCP tool integration

Phase 2: Write Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Article creation and updates
- Category management
- Map marker operations

Phase 3: Advanced Features
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Real-time notifications (webhooks)
- Batch operations
- Advanced caching strategies
- Optimistic concurrency control

Phase 4: Multi-User Scale
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Multi-tenant architecture
- User session management
- Distributed caching
- Load balancing

See Also
--------

- :doc:`overview` - Architecture overview
- :doc:`client_design` - Client design details
- :doc:`mcp_integration` - MCP integration patterns
- :doc:`../development/index` - Development guide
