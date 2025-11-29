"""MCP tools for World Anvil user and identity endpoints.

This module provides registered MCP tools for retrieving user information
and verifying authentication status with the World Anvil API.

Available Tools:
    - get_identity: Get current user's basic identity information
    - get_current_user: Get full user profile with membership details
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from ..client import WorldAnvilClient
from ..models.user import Identity, User


def register_user_tools(server: FastMCP, client: WorldAnvilClient) -> None:
    """Register user-related MCP tools.

    Registers the following tools with the MCP server:
    - get_identity: Retrieve basic user identity
    - get_current_user: Retrieve full user profile

    Args:
        server: MCP server instance to register tools with
        client: Initialized WorldAnvilClient for API requests

    Example:
        >>> from mcp.server import Server
        >>> from world_anvil_mcp.client import WorldAnvilClient
        >>> server = Server("world-anvil")
        >>> async with WorldAnvilClient(app_key, token) as client:
        ...     register_user_tools(server, client)
    """

    @server.tool()
    async def get_identity() -> list[TextContent]:
        """Get the current authenticated user's identity.

        Retrieves basic identity information (id and username) to verify
        API connectivity and authentication status. This is the minimal
        endpoint useful for session validation.

        Returns:
            User identity with id and username formatted as plain text

        Raises:
            WorldAnvilAuthError: Authentication credentials are invalid
            WorldAnvilAPIError: API request failed

        Example:
            >>> result = await get_identity()
            >>> print(result[0].text)
            Authenticated as: player1 (ID: user123)
        """
        data = await client.get_identity()
        identity = Identity.model_validate(data)

        return [
            TextContent(
                type="text",
                text=(f"Authenticated as: {identity.username} (ID: {identity.id})"),
            )
        ]

    @server.tool()
    async def get_current_user(granularity: int = 1) -> list[TextContent]:
        """Get full profile details for the current authenticated user.

        Retrieves detailed user information including profile metadata,
        email, membership status, and account creation date. Granularity
        controls the detail level of returned information.

        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full).
                Defaults to 1 (standard details).
                - 0: Basic user info (id, username)
                - 1: Standard profile with email and membership
                - 2: Full profile with all available fields

        Returns:
            Formatted user profile information as plain text

        Raises:
            WorldAnvilAuthError: Authentication credentials are invalid
            WorldAnvilAPIError: API request failed

        Example:
            >>> result = await get_current_user(granularity=2)
            >>> print(result[0].text)
            # User: player1
            - ID: user123
            - Membership: Grandmaster
            - Email: player@example.com
        """
        data = await client.get_current_user(granularity=granularity)
        user = User.model_validate(data)

        # Build formatted text output
        lines = [f"# User: {user.username}", f"- ID: {user.id}"]

        # Add membership, defaulting to "Free" if not present
        membership = user.membership or "Free"
        lines.append(f"- Membership: {membership}")

        # Add email if present
        if user.email:
            lines.append(f"- Email: {user.email}")

        text_output = "\n".join(lines)

        return [TextContent(type="text", text=text_output)]
