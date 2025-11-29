"""Integration tests for server utilities and resources."""

from __future__ import annotations

import json

import pytest

from world_anvil_mcp import server


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_api_status_ready(monkeypatch: pytest.MonkeyPatch) -> None:
    """Status tool reports ready when credentials are present."""
    monkeypatch.setenv("WORLD_ANVIL_APP_KEY", "app-key")
    monkeypatch.setenv("WORLD_ANVIL_USER_TOKEN", "user-token")
    monkeypatch.setenv("WORLD_ANVIL_API_BASE", "https://api.test")

    status = await server.get_api_status()

    assert status["status"] == "ready"
    assert status["api_base"] == "https://api.test"
    assert status["has_app_key"] is True
    assert status["has_user_token"] is True


@pytest.mark.integration
@pytest.mark.asyncio
async def test_get_api_status_not_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    """Status tool reports not_configured when credentials are missing."""
    monkeypatch.delenv("WORLD_ANVIL_APP_KEY", raising=False)
    monkeypatch.delenv("WORLD_ANVIL_USER_TOKEN", raising=False)

    status = await server.get_api_status()

    assert status["status"] == "not_configured"
    assert status["has_app_key"] is False
    assert status["has_user_token"] is False


@pytest.mark.integration
def test_config_resource_json(monkeypatch: pytest.MonkeyPatch) -> None:
    """Configuration resource should emit JSON with expected fields."""
    monkeypatch.setenv("WORLD_ANVIL_APP_KEY", "app-key")
    monkeypatch.setenv("WORLD_ANVIL_USER_TOKEN", "user-token")
    result = server.get_config_status()

    data = json.loads(result)

    assert data["server"] == "World Anvil MCP"
    assert data["configured"] is True
    assert data["api_base"] == "https://www.worldanvil.com/api/external/boromir"


@pytest.mark.integration
def test_main_warns_and_runs(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main should warn when env missing and invoke server run."""
    monkeypatch.delenv("WORLD_ANVIL_APP_KEY", raising=False)
    monkeypatch.delenv("WORLD_ANVIL_USER_TOKEN", raising=False)

    run_called = False

    def fake_run() -> None:
        nonlocal run_called
        run_called = True

    monkeypatch.setattr(server.mcp, "run", fake_run)

    server.main()

    captured = capsys.readouterr().out
    assert "WORLD_ANVIL_APP_KEY not set" in captured
    assert "WORLD_ANVIL_USER_TOKEN not set" in captured
    assert run_called is True
