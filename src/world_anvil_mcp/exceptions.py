"""World Anvil API exception hierarchy.

This module defines custom exceptions for the World Anvil MCP Server, providing
granular error handling for different API failure scenarios.

Exception Hierarchy:
    WorldAnvilError (base)
    ├── WorldAnvilAuthError (401, 403 - authentication/authorization)
    ├── WorldAnvilAPIError (generic 4xx/5xx with status code)
    ├── WorldAnvilRateLimitError (429 - rate limited)
    ├── WorldAnvilNotFoundError (404 - resource not found)
    └── WorldAnvilValidationError (invalid request/payload)

Usage:
    >>> from world_anvil_mcp.exceptions import WorldAnvilAuthError
    >>> try:
    ...     response = await client.get_identity()
    ... except WorldAnvilAuthError as e:
    ...     print(f"Authentication failed: {e}")
    ... except WorldAnvilRateLimitError as e:
    ...     print(f"Rate limited. Retry after {e.retry_after} seconds")
    ... except WorldAnvilNotFoundError as e:
    ...     print(f"Resource not found: {e}")
"""

from __future__ import annotations


class WorldAnvilError(Exception):
    """Base exception for all World Anvil API errors.

    This is the parent class for all custom exceptions raised by the
    World Anvil MCP Server. Use this to catch any World Anvil-specific error.

    Example:
        >>> try:
        ...     await client.get_article(article_id)
        ... except WorldAnvilError as e:
        ...     handle_world_anvil_error(e)
    """


class WorldAnvilAuthError(WorldAnvilError):
    """Authentication or authorization failure (401, 403).

    Raised when authentication credentials are invalid, missing, or when
    the authenticated user lacks sufficient permissions to perform the
    requested operation.

    Common causes:
        - Invalid or expired user token
        - Invalid application key
        - User lacks permission for the resource/operation
        - Missing or malformed authentication headers

    Example:
        >>> try:
        ...     await client.get_identity()
        ... except WorldAnvilAuthError:
        ...     print("Invalid credentials provided")
    """


class WorldAnvilAPIError(WorldAnvilError):
    """General API error with optional HTTP status code.

    Raised for generic API errors (4xx, 5xx responses) that don't fit
    more specific exception types. Includes the HTTP status code for
    debugging and error handling logic.

    Args:
        message: Human-readable error message describing what went wrong.
        status_code: HTTP response status code (e.g., 400, 500).
            Defaults to None if status code is unavailable.

    Attributes:
        status_code: HTTP response status code, if available.

    Example:
        >>> try:
        ...     await client.post_article(data)
        ... except WorldAnvilAPIError as e:
        ...     print(f"API error (HTTP {e.status_code}): {e}")
    """

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize WorldAnvilAPIError with message and optional status code.

        Args:
            message: Error message describing the failure.
            status_code: HTTP status code (optional). Defaults to None.
        """
        super().__init__(message)
        self.status_code = status_code


class WorldAnvilRateLimitError(WorldAnvilError):
    """Rate limit exceeded (429).

    Raised when the client exceeds the API rate limit (60 requests per minute).
    Includes a retry_after value indicating how long to wait before retrying.

    The World Anvil API enforces a token bucket rate limiter at 60 requests
    per minute. This exception is raised when that limit is exceeded.

    Args:
        message: Human-readable error message (typically includes rate limit info).
        retry_after: Number of seconds to wait before retrying.
            Defaults to 60 (conservative default).

    Attributes:
        retry_after: Number of seconds to wait before retrying the request.

    Example:
        >>> try:
        ...     await client.get_article(article_id)
        ... except WorldAnvilRateLimitError as e:
        ...     await asyncio.sleep(e.retry_after)
        ...     await client.get_article(article_id)  # Retry
    """

    def __init__(self, message: str, retry_after: int = 60) -> None:
        """Initialize WorldAnvilRateLimitError with retry-after value.

        Args:
            message: Error message describing the rate limit.
            retry_after: Seconds to wait before retrying (default: 60).
        """
        super().__init__(message)
        self.retry_after = retry_after


class WorldAnvilNotFoundError(WorldAnvilError):
    """Resource not found (404).

    Raised when a requested resource (article, world, NPC, etc.) does not exist
    or has been deleted. This typically indicates the resource ID is invalid
    or the resource has been removed since last access.

    Common causes:
        - Invalid or non-existent article/world ID
        - Resource was deleted
        - User does not have access to the resource

    Example:
        >>> try:
        ...     await client.get_article("invalid-id")
        ... except WorldAnvilNotFoundError:
        ...     print("Article does not exist")
    """


class WorldAnvilValidationError(WorldAnvilError):
    """Request validation failed.

    Raised when the client request fails validation before being sent to the API,
    or when the API rejects the request due to invalid parameters or payload.

    Common causes:
        - Invalid parameter type or value
        - Required parameter missing
        - Payload structure does not match API schema
        - String parameter expected but integer provided (e.g., granularity)

    Note:
        The World Anvil API has specific quirks with parameter validation.
        For example, the granularity parameter must always be a STRING
        ("0", "1", "2", "3"), never an integer.

    Example:
        >>> try:
        ...     await client.get_article(article_id, granularity=2)
        ... except WorldAnvilValidationError:
        ...     print("Invalid granularity (must be string '0'-'3')")
    """
