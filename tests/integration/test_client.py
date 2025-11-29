"""Integration tests for WorldAnvilClient HTTP behaviors."""

from __future__ import annotations

from collections.abc import AsyncGenerator

import httpx
import pytest
import pytest_asyncio
import respx
from httpx import Response

from world_anvil_mcp.client import HTTP_STATUS_TOO_MANY_REQUESTS, WorldAnvilClient
from world_anvil_mcp.exceptions import (
    WorldAnvilAPIError,
    WorldAnvilAuthError,
    WorldAnvilNotFoundError,
    WorldAnvilRateLimitError,
)

BASE_URL = "https://www.worldanvil.com/api/external/boromir"


@pytest_asyncio.fixture
async def client(mock_client_config: dict[str, str]) -> AsyncGenerator[WorldAnvilClient, None]:
    """Provide an initialized client for tests."""
    async with WorldAnvilClient(
        app_key=mock_client_config["app_key"],
        user_token=mock_client_config["user_token"],
        base_url=mock_client_config["base_url"],
    ) as client:
        yield client


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_get_identity_uses_cache(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """Second identity call should use cache (one HTTP call only)."""
    respx_mock.get("/identity").mock(
        return_value=Response(200, json={"id": "user-1", "username": "tester"}),
    )

    first = await client.get_identity()
    second = await client.get_identity()

    assert first["id"] == "user-1"
    assert second["username"] == "tester"
    assert respx_mock.calls.call_count == 1


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_get_identity_auth_error(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """401 should raise WorldAnvilAuthError."""
    respx_mock.get("/identity").mock(return_value=Response(401))

    with pytest.raises(WorldAnvilAuthError):
        await client.get_identity()


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_success_false_raises_api_error(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """World Anvil success=false quirk should surface as API error."""
    respx_mock.get("/user").mock(
        return_value=Response(200, json={"success": False, "error": "not allowed"}),
    )

    with pytest.raises(WorldAnvilAPIError, match="success=false"):
        await client.get_current_user(granularity=1)


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_list_worlds_uses_string_granularity(
    respx_mock: respx.MockRouter, client: WorldAnvilClient
) -> None:
    """Granularity must be stringified in outgoing requests."""
    route = respx_mock.get("/user/worlds").mock(
        return_value=Response(200, json={"worlds": [{"id": "w1", "name": "Alpha"}]}),
    )

    worlds = await client.list_worlds(granularity=2)

    assert worlds[0]["id"] == "w1"
    assert route.calls[0].request.url.params["granularity"] == "2"


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_update_world_invalidates_cache(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """Write operations should invalidate cached world entries."""
    world_id = "world-123"
    respx_mock.get(f"/world/{world_id}").mock(
        side_effect=[
            Response(
                200,
                json={
                    "id": world_id,
                    "name": "Old",
                    "article_count": 1,
                    "category_count": 0,
                },
            ),
            Response(
                200,
                json={
                    "id": world_id,
                    "name": "New",
                    "article_count": 1,
                    "category_count": 0,
                },
            ),
        ],
    )
    respx_mock.patch(f"/world/{world_id}").mock(
        return_value=Response(
            200,
            json={
                "id": world_id,
                "name": "New",
                "article_count": 1,
                "category_count": 0,
            },
        ),
    )

    await client.get_world(world_id)
    await client.update_world(world_id, name="New")
    updated = await client.get_world(world_id)

    assert updated["name"] == "New"
    assert respx_mock.calls.call_count == 3  # get -> patch -> get (cache invalidated)


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_rate_limit_error_exposes_retry_after(
    respx_mock: respx.MockRouter, client: WorldAnvilClient
) -> None:
    """429 responses should raise with retry_after information."""
    respx_mock.get("/identity").mock(
        return_value=Response(HTTP_STATUS_TOO_MANY_REQUESTS, headers={"Retry-After": "30"}),
    )

    with pytest.raises(WorldAnvilRateLimitError) as exc:
        await client.get_identity()

    assert exc.value.retry_after == 30


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_get_world_not_found_raises(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """404 responses should surface as NotFound errors."""
    respx_mock.get("/world/missing").mock(return_value=Response(404))

    with pytest.raises(WorldAnvilNotFoundError):
        await client.get_world("missing")


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_server_error_raises_api_error(
    respx_mock: respx.MockRouter,
    client: WorldAnvilClient,
) -> None:
    """5xx responses should raise API errors with status detail."""
    respx_mock.get("/identity").mock(return_value=Response(500, text="boom"))

    with pytest.raises(WorldAnvilAPIError, match="Server error 500"):
        await client.get_identity()


@pytest.mark.integration
@pytest.mark.asyncio
@respx.mock(base_url=BASE_URL)
async def test_timeout_exhausts_retries(
    respx_mock: respx.MockRouter,
    mock_client_config: dict[str, str],
) -> None:
    """Timeouts should surface as RuntimeError after configured retries."""
    respx_mock.get("/identity").mock(side_effect=httpx.TimeoutException("timeout"))

    async with WorldAnvilClient(
        app_key=mock_client_config["app_key"],
        user_token=mock_client_config["user_token"],
        base_url=mock_client_config["base_url"],
        max_retries=1,
    ) as short_client:
        with pytest.raises(RuntimeError, match="Request failed after 1 attempts"):
            await short_client.get_identity()
