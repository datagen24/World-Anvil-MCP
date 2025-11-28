"""Example tests demonstrating testing patterns for World Anvil MCP Server.

This module provides reference examples for writing unit, integration, and e2e tests.
These tests will be replaced during Phase 1 implementation.
"""

import pytest


@pytest.mark.unit
def test_example_unit():
    """Example unit test (fast, no I/O).

    Unit tests should test individual components in isolation without
    any external dependencies or I/O operations.
    """
    # Example: Test a pure function or model
    result = 1 + 1
    assert result == 2


@pytest.mark.unit
def test_example_with_faker(faker):
    """Example unit test using Faker fixture.

    Args:
        faker: Faker instance with deterministic seed from conftest.py.
    """
    # Generate test data
    username = faker.user_name()
    email = faker.email()

    # Verify data format
    assert isinstance(username, str)
    assert "@" in email


@pytest.mark.unit
def test_example_with_sample_data(sample_article_data):
    """Example unit test using sample data fixture.

    Args:
        sample_article_data: Sample article data from conftest.py.
    """
    # Verify sample data structure
    assert "id" in sample_article_data
    assert "title" in sample_article_data
    assert sample_article_data["state"] == "public"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_example_integration():
    """Example integration test (async, mocked API).

    Integration tests should test component interactions with mocked
    external services using respx for HTTP mocking.

    Note: This is a placeholder. Real integration tests will use respx
    to mock httpx requests during Phase 1 implementation.
    """
    # Example: Test async operation
    async def async_operation():
        return "success"

    result = await async_operation()
    assert result == "success"


@pytest.mark.e2e
@pytest.mark.skipif(
    condition=True,  # Will be replaced with has_live_credentials fixture
    reason="Requires live World Anvil API credentials",
)
@pytest.mark.asyncio
async def test_example_e2e():
    """Example end-to-end test (requires live API).

    E2E tests should be skipped unless WORLD_ANVIL_API_KEY and
    WORLD_ANVIL_USER_TOKEN environment variables are set.

    Note: This is a placeholder. Real e2e tests will use live_api_config
    fixture during Phase 1 implementation.
    """
    # Example: Test against live API
    result = "skipped"
    assert result == "skipped"
