"""MCP tools for World Anvil world endpoints with ecosystem integration."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from ..client import WorldAnvilClient
from ..ecosystem.detector import EcosystemDetector
from ..models.world import World, WorldSummary


def register_world_tools(
    server: FastMCP,
    client: WorldAnvilClient,
    ecosystem: EcosystemDetector,
) -> None:
    """Register world-related MCP tools.

    Args:
        server: The MCP server instance.
        client: The WorldAnvilClient for API calls.
        ecosystem: The EcosystemDetector for integration hints.

    Example:
        >>> register_world_tools(server, client, ecosystem)
    """

    @server.tool()
    async def list_worlds(granularity: int = 1) -> list[TextContent]:
        """List all worlds accessible to the user.

        Args:
            granularity: Detail level (1-3). Defaults to 1.

        Returns:
            Formatted markdown list of worlds with ecosystem hints.

        Raises:
            AuthenticationError: Invalid credentials.
            RateLimitError: Rate limit exceeded.
        """
        worlds_data = await client.list_worlds(granularity=granularity)

        if not worlds_data:
            return [
                TextContent(
                    type="text", text=("No worlds found. Create a world at worldanvil.com first.")
                )
            ]

        lines = ["# Your Worlds", ""]

        for world_data in worlds_data:
            world = WorldSummary.model_validate(world_data)
            lines.append(f"- **{world.name}** (ID: `{world.id}`)")

        lines.append("")
        lines.append(f"*Total: {len(worlds_data)} worlds*")

        # Add ecosystem integration hints
        integration_hint = ecosystem.get_ecosystem_status()
        if integration_hint:
            lines.extend(["", "---", "", integration_hint])

        return [TextContent(type="text", text="\n".join(lines))]

    @server.tool()
    async def get_world(
        world_id: str,
        granularity: int = 1,
    ) -> list[TextContent]:
        """Retrieve a specific world by ID.

        Args:
            world_id: The unique identifier of the world.
            granularity: Detail level (1-3). Defaults to 1.

        Returns:
            Formatted markdown with world details.

        Raises:
            NotFoundError: World does not exist.
            AuthenticationError: Invalid credentials.
            RateLimitError: Rate limit exceeded.
        """
        world_data = await client.get_world(world_id, granularity=granularity)
        world = World.model_validate(world_data)

        lines = [f"# {world.name}", ""]
        lines.append(f"**ID**: `{world.id}`")

        if world.genre:
            lines.append(f"**Genre**: {world.genre}")
        else:
            lines.append("**Genre**: Not set")

        if world.description:
            lines.extend(["", "## Description", "", world.description])

        # Content section
        lines.extend(["", "## Content", ""])
        lines.append(f"- **Articles**: {world.article_count or 0}")
        lines.append(f"- **Categories**: {world.category_count or 0}")

        if hasattr(world, "rpg_system") and world.rpg_system:
            lines.append(f"- **RPG System**: {world.rpg_system}")

        return [TextContent(type="text", text="\n".join(lines))]

    @server.tool()
    async def update_world(
        world_id: str,
        name: str | None = None,
        description: str | None = None,
        genre: str | None = None,
    ) -> list[TextContent]:
        """Update a world's properties.

        Args:
            world_id: The unique identifier of the world.
            name: New name for the world. Optional.
            description: New description for the world. Optional.
            genre: New genre for the world. Optional.

        Returns:
            Confirmation message with updated world details.

        Raises:
            NotFoundError: World does not exist.
            AuthenticationError: Invalid credentials.
            ValidationError: Invalid parameters.
            RateLimitError: Rate limit exceeded.
        """
        updates = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if genre is not None:
            updates["genre"] = genre

        if not updates:
            return [
                TextContent(
                    type="text",
                    text=("No updates specified. Provide name, description, or genre to update."),
                )
            ]

        world_data = await client.update_world(world_id, **updates)
        world = World.model_validate(world_data)

        return [
            TextContent(
                type="text",
                text=f"✅ Updated world: **{world.name}** (`{world.id}`)",
            )
        ]
