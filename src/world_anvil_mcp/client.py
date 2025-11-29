# src/world_anvil_mcp/client.py
"""World Anvil API Client with async HTTP and MCP integration.

This module provides the core async HTTP client for the World Anvil Boromir API,
designed specifically for MCP integration with:
- Automatic retry with exponential backoff
- In-memory caching with TTL
- World Anvil API quirk handling (lowercase headers, string granularity)
- Comprehensive error handling

Critical API Quirks:
1. Lowercase Headers: x-auth-token and x-application-key (NOT capitalized)
2. Granularity Parameter: MUST be STRING ("0", "1", "2", "3") not integer
3. Success Flag Pattern: Some 200 OK responses include {"success": false, "error": "..."}
4. Rate Limiting: 60 requests per minute (token bucket algorithm needed)

Example:
    >>> async with WorldAnvilClient(app_key, user_token) as client:
    ...     identity = await client.get_identity()
    ...     print(f"Authenticated as: {identity['username']}")
"""

from __future__ import annotations

import asyncio
import random
from typing import Any

import httpx

from .cache import InMemoryCache
from .exceptions import (
    WorldAnvilAPIError,
    WorldAnvilAuthError,
    WorldAnvilNotFoundError,
    WorldAnvilRateLimitError,
)

# HTTP Status Code Constants
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_NOT_FOUND = 404
HTTP_STATUS_TOO_MANY_REQUESTS = 429
HTTP_STATUS_CLIENT_ERROR = 400
HTTP_STATUS_SERVER_ERROR = 500


class WorldAnvilClient:
    """Async client for World Anvil Boromir API.

    Designed for MCP integration with automatic retry, caching, and
    comprehensive error handling for all World Anvil API quirks.

    Args:
        app_key: World Anvil application key from API settings
        user_token: User authentication token from API settings
        base_url: API base URL (default: production endpoint)
        timeout: Request timeout in seconds (default: 30.0)
        max_retries: Maximum retry attempts for transient failures (default: 3)
        cache_ttl: Default cache TTL in seconds (default: 300)

    Raises:
        RuntimeError: If client used outside async context manager

    Example:
        >>> async with WorldAnvilClient(app_key, user_token) as client:
        ...     # Cached for 1 hour
        ...     identity = await client.get_identity()
        ...     # Cached for 5 minutes
        ...     worlds = await client.list_worlds(granularity=1)
        ...     # Updates invalidate cache
        ...     await client.update_world(world_id, name="New Name")
    """

    BASE_URL = "https://www.worldanvil.com/api/external/boromir"

    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        cache_ttl: int = 300,
    ) -> None:
        """Initialize the World Anvil API client.

        Args:
            app_key: Application key from World Anvil API settings
            user_token: User token from World Anvil API settings
            base_url: Override base URL (default: production)
            timeout: HTTP request timeout in seconds
            max_retries: Maximum retry attempts
            cache_ttl: Default cache TTL in seconds
        """
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_cache_ttl = cache_ttl

        # In-memory cache with TTL and LRU eviction
        self._cache = InMemoryCache(
            default_ttl=cache_ttl,
            max_entries=1000,  # Configurable cache size
        )

        # HTTP client (initialized in context manager)
        self._client: httpx.AsyncClient | None = None

    @property
    def headers(self) -> dict[str, str]:
        """Authentication headers for all requests.

        CRITICAL: World Anvil uses lowercase header names:
        - x-application-key (NOT X-Application-Key)
        - x-auth-token (NOT X-Auth-Token)

        These headers are case-sensitive and must be lowercase.

        Returns:
            Dictionary with authentication and content-type headers
        """
        return {
            "x-application-key": self.app_key,
            "x-auth-token": self.user_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def __aenter__(self) -> WorldAnvilClient:
        """Async context manager entry.

        Creates and initializes the httpx.AsyncClient with proper
        configuration for World Anvil API.

        Returns:
            Self for context manager usage
        """
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:  # noqa: ANN401
        """Async context manager exit.

        Properly closes the httpx client and cleans up resources.

        Args:
            *args: Exception info (unused)
        """
        if self._client:
            await self._client.aclose()
            self._client = None

    async def _request(  # noqa: PLR0912, PLR0915
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        cache_key: str | None = None,
        cache_ttl: int | None = None,
    ) -> dict[str, Any]:
        """Execute HTTP request with retry and caching.

        Implements the core request logic with:
        - Cache checking for GET requests
        - Exponential backoff retry with jitter
        - World Anvil error response handling
        - Cache invalidation on writes

        Args:
            method: HTTP method (GET, POST, PATCH, PUT, DELETE)
            path: API endpoint path (e.g., "/identity")
            params: Query parameters
            json: JSON body for POST/PATCH/PUT
            cache_key: Cache key for GET requests (None to skip caching)
            cache_ttl: Cache TTL override (uses default if None)

        Returns:
            Response JSON as dictionary

        Raises:
            WorldAnvilAuthError: Authentication or authorization failure (401, 403)
            WorldAnvilNotFoundError: Resource not found (404)
            WorldAnvilRateLimitError: Rate limit exceeded (429)
            WorldAnvilAPIError: General API errors (4xx, 5xx)
            RuntimeError: Client not initialized or network failures
        """
        # Check cache for GET requests
        if method == "GET" and cache_key:
            cached = self._cache.get(cache_key)
            if cached is not None:
                # Type assertion: cached value is dict[str, Any]
                return cached  # type: ignore[no-any-return]

        if not self._client:
            msg = (
                "Client not initialized. Use async context manager: "
                "async with WorldAnvilClient(...) as client:"
            )
            raise RuntimeError(msg)

        last_error: Exception | None = None

        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                )

                # Handle error status codes
                if response.status_code == HTTP_STATUS_UNAUTHORIZED:
                    msg = (
                        "Authentication failed: Invalid API credentials. "
                        "Check WORLD_ANVIL_APP_KEY and WORLD_ANVIL_USER_TOKEN."
                    )
                    raise WorldAnvilAuthError(msg)
                if response.status_code == HTTP_STATUS_FORBIDDEN:
                    msg = (
                        "Authorization failed: Insufficient permissions. "
                        "Ensure you have Grandmaster guild membership."
                    )
                    raise WorldAnvilAuthError(msg)
                if response.status_code == HTTP_STATUS_NOT_FOUND:
                    msg = f"Resource not found: {path}"
                    raise WorldAnvilNotFoundError(msg)
                if response.status_code == HTTP_STATUS_TOO_MANY_REQUESTS:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    msg = (
                        f"Rate limit exceeded. Retry after {retry_after} seconds. "
                        "World Anvil API allows 60 requests per minute."
                    )
                    raise WorldAnvilRateLimitError(
                        msg,
                        retry_after=retry_after,
                    )
                if response.status_code >= HTTP_STATUS_SERVER_ERROR:
                    msg = (
                        f"Server error {response.status_code}: {response.text}. "
                        "World Anvil API may be experiencing issues."
                    )
                    raise WorldAnvilAPIError(
                        msg,
                        status_code=response.status_code,
                    )
                if response.status_code >= HTTP_STATUS_CLIENT_ERROR:
                    msg = f"API error {response.status_code}: {response.text}"
                    raise WorldAnvilAPIError(
                        msg,
                        status_code=response.status_code,
                    )

                # Parse JSON response
                data = response.json()

                # Check for success flag pattern (World Anvil quirk)
                # Some 200 OK responses include {"success": false, "error": "..."}
                if isinstance(data, dict) and not data.get("success", True):
                    error_msg = data.get("error", "Unknown error")
                    msg = f"API returned success=false: {error_msg}"
                    raise WorldAnvilAPIError(
                        msg,
                        status_code=response.status_code,
                    )

                # Cache successful GET responses
                if method == "GET" and cache_key:
                    effective_ttl = cache_ttl if cache_ttl is not None else self.default_cache_ttl
                    self._cache.set(cache_key, data, ttl=effective_ttl)

                # Invalidate cache on writes
                if method in ("POST", "PATCH", "PUT", "DELETE"):
                    # Pattern-based invalidation using regex
                    # Extract resource type from path (e.g., "world" from "/world/123")
                    resource_type = path.split("/")[1] if "/" in path else ""
                    if resource_type:
                        # Invalidate all keys containing the resource type
                        self._cache.invalidate_pattern(f".*{resource_type}.*")

                # Type assertion: data is dict[str, Any]
                return data  # type: ignore[no-any-return]

            except httpx.TimeoutException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff with jitter
                    backoff = (2**attempt) + (random.random() * 0.1)  # noqa: S311
                    await asyncio.sleep(backoff)

            except httpx.RequestError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff with jitter
                    backoff = (2**attempt) + (random.random() * 0.1)  # noqa: S311
                    await asyncio.sleep(backoff)

        # All retries exhausted
        msg = f"Request failed after {self.max_retries} attempts: {last_error}"
        raise RuntimeError(msg)

    # -------------------------------------------------------------------------
    # User & Identity Endpoints
    # -------------------------------------------------------------------------

    async def get_identity(self) -> dict[str, Any]:
        """Get current user identity.

        Retrieves basic identity information for the authenticated user.
        This is the simplest endpoint and useful for validating API connectivity.

        Returns:
            User identity dictionary with:
                - id (str): User unique identifier
                - username (str): Display username

        Raises:
            RuntimeError: Authentication failure or API error

        Example:
            >>> identity = await client.get_identity()
            >>> print(f"User ID: {identity['id']}")
            >>> print(f"Username: {identity['username']}")

        Note:
            This endpoint is cached for 1 hour (3600 seconds) as user
            identity rarely changes during an MCP session.
        """
        return await self._request(
            "GET",
            "/identity",
            cache_key="identity",
            cache_ttl=3600,  # 1 hour - rarely changes
        )

    async def get_current_user(self, granularity: int = 1) -> dict[str, Any]:
        """Get current user details with configurable granularity.

        Retrieves detailed information about the authenticated user including
        membership level, stats, and profile information.

        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
                - 0: Basic info only
                - 1: Standard details (default)
                - 2: Full profile with all fields

        Returns:
            User details dictionary including:
                - id (str): User unique identifier
                - username (str): Display username
                - email (str | None): User email
                - membership (str | None): Guild membership level
                - created_at (str | None): Account creation timestamp

        Raises:
            RuntimeError: Authentication failure or API error

        Example:
            >>> user = await client.get_current_user(granularity=2)
            >>> print(f"Membership: {user.get('membership', 'Free')}")

        Note:
            CRITICAL: Granularity MUST be passed as STRING to the API.
            The client handles integer-to-string conversion automatically.
        """
        return await self._request(
            "GET",
            "/user",
            params={"granularity": str(granularity)},  # MUST be string!
            cache_key=f"user:self:{granularity}",
            cache_ttl=3600,  # 1 hour
        )

    # -------------------------------------------------------------------------
    # World Endpoints
    # -------------------------------------------------------------------------

    async def list_worlds(self, granularity: int = 1) -> list[dict[str, Any]]:
        """List all worlds owned by authenticated user.

        Retrieves a list of all worlds created by or owned by the current user.
        Use this to discover available worlds before accessing specific content.

        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
                - 0: ID and name only
                - 1: Standard details with counts
                - 2: Full world metadata

        Returns:
            List of world dictionaries, each containing:
                - id (str): World unique identifier
                - name (str): World name
                - description (str | None): World description (granularity 1+)
                - article_count (int | None): Number of articles (granularity 1+)

        Raises:
            RuntimeError: Authentication failure or API error

        Example:
            >>> worlds = await client.list_worlds(granularity=0)
            >>> for world in worlds:
            ...     print(f"{world['name']}: {world['id']}")

        Note:
            The response may be wrapped in a "worlds" key or returned directly
            as a list. This method normalizes both formats.
        """
        response = await self._request(
            "GET",
            "/user/worlds",
            params={"granularity": str(granularity)},  # MUST be string!
            cache_key=f"worlds:list:{granularity}",
            cache_ttl=300,  # 5 minutes
        )
        # Normalize response format (may be wrapped in "worlds" key)
        return response.get("worlds", response) if isinstance(response, dict) else response  # type: ignore[no-any-return]

    async def get_world(self, world_id: str, granularity: int = 1) -> dict[str, Any]:
        """Get world details by ID.

        Retrieves detailed information about a specific world including
        metadata, content counts, and configuration.

        Args:
            world_id: World unique identifier (from list_worlds)
            granularity: Detail level (0=minimal, 1=standard, 2=full)
                - 0: Basic world info
                - 1: Standard details with counts
                - 2: Full metadata and configuration

        Returns:
            World details dictionary including:
                - id (str): World unique identifier
                - name (str): World name
                - description (str | None): World description
                - genre (str | None): World genre
                - article_count (int | None): Number of articles
                - category_count (int | None): Number of categories

        Raises:
            RuntimeError: World not found, permission denied, or API error

        Example:
            >>> world = await client.get_world("abc123", granularity=2)
            >>> print(f"{world['name']}: {world['description']}")
            >>> print(f"Articles: {world.get('article_count', 0)}")

        Note:
            Higher granularity levels return more fields but may be slower.
            Use granularity=0 for quick lookups.
        """
        return await self._request(
            "GET",
            f"/world/{world_id}",
            params={"granularity": str(granularity)},  # MUST be string!
            cache_key=f"world:{world_id}:{granularity}",
            cache_ttl=300,  # 5 minutes
        )

    async def update_world(
        self,
        world_id: str,
        **updates: Any,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Update world metadata.

        Updates editable fields of a world. Only provided fields are updated;
        omitted fields remain unchanged.

        Args:
            world_id: World unique identifier
            **updates: Fields to update, may include:
                - name (str): New world name
                - description (str): New description
                - genre (str): New genre
                - locale (str): Language/locale setting

        Returns:
            Updated world details dictionary

        Raises:
            RuntimeError: World not found, permission denied, or API error

        Example:
            >>> result = await client.update_world(
            ...     "world123",
            ...     name="New Campaign Name",
            ...     description="Updated world description"
            ... )
            >>> print(f"Updated: {result['name']}")

        Note:
            This is a write operation and will invalidate all world-related
            cache entries. Write API availability was validated in Phase 1.1.
        """
        return await self._request(
            "PATCH",
            f"/world/{world_id}",
            json=updates,
        )
