"""Shared pytest fixtures for World Anvil MCP Server tests.

This module provides common fixtures used across all test modules, including
mock client configurations, sample data generators, and test utilities.
"""

import os
from typing import AsyncGenerator, Generator

import pytest
from faker import Faker


@pytest.fixture
def faker_seed() -> int:
    """Provide deterministic seed for Faker.

    Returns:
        int: Seed value for reproducible test data.
    """
    return 12345


@pytest.fixture
def faker(faker_seed: int) -> Faker:
    """Provide Faker instance with deterministic seed.

    Args:
        faker_seed: Seed for reproducible data generation.

    Returns:
        Faker: Configured Faker instance.
    """
    fake = Faker()
    Faker.seed(faker_seed)
    return fake


@pytest.fixture
def mock_client_config() -> dict[str, str]:
    """Provide test configuration for WorldAnvilClient.

    Returns:
        dict: Configuration dict with test credentials and base URL.
    """
    return {
        "app_key": "test-app-key-12345",
        "user_token": "test-user-token-67890",
        "base_url": "https://www.worldanvil.com/api/external/boromir",
    }


@pytest.fixture
def sample_user_data(faker: Faker) -> dict:
    """Generate sample user JSON response.

    Args:
        faker: Faker instance for data generation.

    Returns:
        dict: Sample user data matching World Anvil API format.
    """
    return {
        "id": faker.uuid4(),
        "username": faker.user_name(),
        "email": faker.email(),
        "isPremium": True,
        "url": f"https://www.worldanvil.com/author/{faker.user_name()}",
    }


@pytest.fixture
def sample_world_data(faker: Faker) -> dict:
    """Generate sample world JSON response.

    Args:
        faker: Faker instance for data generation.

    Returns:
        dict: Sample world data matching World Anvil API format.
    """
    world_id = faker.uuid4()
    return {
        "id": world_id,
        "title": faker.sentence(nb_words=3).rstrip("."),
        "url": f"https://www.worldanvil.com/w/{world_id}",
        "excerpt": faker.paragraph(nb_sentences=2),
        "tags": [faker.word() for _ in range(3)],
    }


@pytest.fixture
def sample_article_data(faker: Faker) -> dict:
    """Generate sample article JSON response.

    Args:
        faker: Faker instance for data generation.

    Returns:
        dict: Sample article data matching World Anvil API format.
    """
    article_id = faker.uuid4()
    world_id = faker.uuid4()
    return {
        "id": article_id,
        "title": faker.sentence(nb_words=4).rstrip("."),
        "state": "public",
        "url": f"https://www.worldanvil.com/w/{world_id}/a/{article_id}",
        "world": {"id": world_id, "title": "Test World"},
        "tags": [faker.word() for _ in range(2)],
        "content": f"# {faker.sentence()}\n\n{faker.paragraph(nb_sentences=5)}",
    }


@pytest.fixture
def sample_category_data(faker: Faker) -> dict:
    """Generate sample category JSON response.

    Args:
        faker: Faker instance for data generation.

    Returns:
        dict: Sample category data matching World Anvil API format.
    """
    return {
        "id": faker.uuid4(),
        "title": faker.word().title(),
        "url": f"https://www.worldanvil.com/category/{faker.uuid4()}",
    }


@pytest.fixture
def has_live_credentials() -> bool:
    """Check if live API credentials are available.

    Returns:
        bool: True if both WORLD_ANVIL_API_KEY and WORLD_ANVIL_USER_TOKEN
            environment variables are set.
    """
    return bool(
        os.getenv("WORLD_ANVIL_API_KEY") and os.getenv("WORLD_ANVIL_USER_TOKEN")
    )


@pytest.fixture
def live_api_config() -> dict[str, str] | None:
    """Provide live API credentials if available.

    Returns:
        dict | None: Configuration dict with live credentials, or None if not available.
    """
    app_key = os.getenv("WORLD_ANVIL_API_KEY")
    user_token = os.getenv("WORLD_ANVIL_USER_TOKEN")

    if not app_key or not user_token:
        return None

    return {
        "app_key": app_key,
        "user_token": user_token,
        "base_url": "https://www.worldanvil.com/api/external/boromir",
    }
