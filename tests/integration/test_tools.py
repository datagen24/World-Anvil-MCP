"""Integration tests for MCP tool registration and outputs."""

from __future__ import annotations

from typing import cast
from unittest.mock import AsyncMock

import pytest
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from world_anvil_mcp.ecosystem.detector import EcosystemDetector
from world_anvil_mcp.tools.user import register_user_tools
from world_anvil_mcp.tools.world import register_world_tools


@pytest.fixture
def server() -> FastMCP:
    """Provide a fresh MCP server for tool registration."""
    return FastMCP("test-server")


@pytest.fixture
def mock_client() -> AsyncMock:
    """Provide an async mock client with default responses."""
    client = AsyncMock()
    client.get_identity.return_value = {"id": "u1", "username": "tester"}
    client.get_current_user.return_value = {
        "id": "u1",
        "username": "tester",
        "membership": "Grandmaster",
        "email": "tester@example.com",
    }
    client.list_worlds.return_value = []
    client.get_world.return_value = {
        "id": "w1",
        "name": "World One",
        "article_count": 1,
        "category_count": 0,
    }
    client.update_world.return_value = {
        "id": "w1",
        "name": "World Two",
        "article_count": 1,
        "category_count": 0,
    }
    return client


@pytest.mark.integration
@pytest.mark.asyncio
async def test_registers_user_tools_and_outputs_text(
    server: FastMCP,
    mock_client: AsyncMock,
) -> None:
    """User tools should register and call through to the client."""
    register_user_tools(server, mock_client)

    tools = await server.list_tools()
    tool_names = {tool.name for tool in tools}
    assert {"get_identity", "get_current_user"}.issubset(tool_names)

    contents, _ = await server.call_tool("get_identity", {})
    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    assert "Authenticated as" in first.text
    mock_client.get_identity.assert_awaited()

    contents, _ = await server.call_tool("get_current_user", {"granularity": 2})
    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    assert "Membership" in first.text
    mock_client.get_current_user.assert_awaited_with(granularity=2)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_worlds_handles_empty_state(server: FastMCP, mock_client: AsyncMock) -> None:
    """World list tool should respond gracefully with no worlds."""
    ecosystem = EcosystemDetector([])
    register_world_tools(server, mock_client, ecosystem)

    contents, _ = await server.call_tool("list_worlds", {"granularity": 1})

    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    assert "No worlds found" in first.text
    mock_client.list_worlds.assert_awaited_with(granularity=1)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_update_world_tool_validates_inputs(server: FastMCP, mock_client: AsyncMock) -> None:
    """Update world tool should enforce required updates and call client when provided."""
    ecosystem = EcosystemDetector([])
    register_world_tools(server, mock_client, ecosystem)

    # No updates provided
    contents, _ = await server.call_tool("update_world", {"world_id": "w1"})
    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    assert "No updates specified" in first.text
    mock_client.update_world.assert_not_awaited()

    # Provide a name update
    mock_client.update_world.reset_mock()
    mock_client.update_world.return_value = {
        "id": "w1",
        "name": "Renamed",
        "article_count": 1,
        "category_count": 0,
    }
    contents, _ = await server.call_tool("update_world", {"world_id": "w1", "name": "Renamed"})
    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    assert "Renamed" in first.text
    mock_client.update_world.assert_awaited_with("w1", name="Renamed")


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_world_formats_details(server: FastMCP, mock_client: AsyncMock) -> None:
    """get_world tool should format world metadata and counts."""
    ecosystem = EcosystemDetector([])
    mock_client.get_world.return_value = {
        "id": "w1",
        "name": "World One",
        "description": "A test world",
        "genre": "Sci-Fi",
        "article_count": 5,
        "category_count": 2,
        "rpg_system": "5e",
    }
    register_world_tools(server, mock_client, ecosystem)

    contents, _ = await server.call_tool("get_world", {"world_id": "w1", "granularity": 2})

    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    text = first.text
    assert "World One" in text
    assert "Articles" in text
    assert "Sci-Fi" in text
    mock_client.get_world.assert_awaited_with("w1", granularity=2)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_list_worlds_formats_and_adds_ecosystem_hint(
    server: FastMCP, mock_client: AsyncMock
) -> None:
    """list_worlds should include all worlds and ecosystem status section."""
    ecosystem = EcosystemDetector(["foundry_get_actors"])
    mock_client.list_worlds.return_value = [
        {"id": "w1", "name": "Alpha"},
        {"id": "w2", "name": "Beta"},
    ]
    register_world_tools(server, mock_client, ecosystem)

    contents, _ = await server.call_tool("list_worlds", {"granularity": 1})

    assert contents
    contents_list = cast(list[TextContent], list(contents))
    first = contents_list[0]
    assert isinstance(first, TextContent)
    text = first.text
    assert "Alpha" in text
    assert "Beta" in text
    assert "*Total: 2 worlds*" in text
    assert "Foundry VTT" in text
