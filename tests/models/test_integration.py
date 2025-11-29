"""Integration tests for Pydantic models with realistic API responses.

Demonstrates model usage with typical World Anvil API response patterns.
"""

from datetime import datetime

from world_anvil_mcp.models.user import Identity, User
from world_anvil_mcp.models.world import World, WorldSummary


def test_identity_from_api_response() -> None:
    """Test Identity model with typical /identity endpoint response."""
    api_response = {
        "id": "12345",
        "username": "dungeon_master",
    }
    identity = Identity(**api_response)
    assert identity.id == "12345"
    assert identity.username == "dungeon_master"


def test_user_from_api_response() -> None:
    """Test User model with typical /user endpoint response."""
    api_response = {
        "id": "12345",
        "username": "dungeon_master",
        "email": "dm@campaign.local",
        "avatar": "https://api.worldanvil.com/avatars/dm.jpg",
        "membership": "master",
        "created_at": "2020-06-15T10:30:00Z",
    }
    user = User(**api_response)
    assert user.id == "12345"
    assert user.username == "dungeon_master"
    assert user.email == "dm@campaign.local"
    assert user.membership == "master"
    assert isinstance(user.created_at, datetime)


def test_world_summary_from_list_response() -> None:
    """Test WorldSummary with response from /user/worlds (granularity 0)."""
    api_responses = [
        {"id": "world_1", "name": "The Forgotten Realms"},
        {"id": "world_2", "name": "Mystara"},
        {"id": "world_3", "name": "Eberron"},
    ]
    worlds = [WorldSummary(**response) for response in api_responses]
    assert len(worlds) == 3
    assert worlds[0].name == "The Forgotten Realms"
    assert worlds[1].name == "Mystara"
    assert worlds[2].name == "Eberron"


def test_world_from_get_response_granularity_1() -> None:
    """Test World model with /world/{id} response (granularity 1)."""
    api_response = {
        "id": "campaign_2024",
        "name": "Rise of the Dark Lord",
        "description": "An epic campaign of good vs evil",
        "genre": "High Fantasy",
        "locale": "en_US",
        "article_count": 45,
        "category_count": 7,
        "created_at": "2023-01-20T14:00:00Z",
        "updated_at": "2024-11-15T09:30:00Z",
    }
    world = World(**api_response)
    assert world.id == "campaign_2024"
    assert world.name == "Rise of the Dark Lord"
    assert world.article_count == 45
    assert world.category_count == 7
    assert isinstance(world.created_at, datetime)
    assert isinstance(world.updated_at, datetime)


def test_world_from_get_response_granularity_2() -> None:
    """Test World model with /world/{id} response (granularity 2) including owner."""
    api_response = {
        "id": "campaign_2024",
        "name": "Rise of the Dark Lord",
        "description": "An epic campaign of good vs evil",
        "genre": "High Fantasy",
        "locale": "en_US",
        "article_count": 45,
        "category_count": 7,
        "rpg_system": "D&D 5e",
        "created_at": "2023-01-20T14:00:00Z",
        "updated_at": "2024-11-15T09:30:00Z",
        "owner": {
            "id": "user_999",
            "username": "campaign_master",
            "email": "master@campaign.local",
        },
    }
    world = World(**api_response)
    assert world.owner is not None
    assert world.owner["username"] == "campaign_master"
    assert world.rpg_system == "D&D 5e"


def test_world_with_extra_api_fields() -> None:
    """Test World handles extra API fields gracefully."""
    api_response = {
        "id": "custom_world",
        "name": "Hidden Realm",
        "description": "A secret world",
        # Extra fields that might be added in future API versions
        "thumbnail_url": "https://example.com/thumb.jpg",
        "featured": True,
        "visibility": "private",
        "tags": ["homebrew", "experimental"],
    }
    world = World(**api_response)
    assert world.name == "Hidden Realm"
    # Extra fields are captured in model dump
    data = world.model_dump()
    assert data.get("thumbnail_url") == "https://example.com/thumb.jpg"
    assert data.get("featured") is True
    assert data.get("tags") == ["homebrew", "experimental"]


def test_world_summary_serialization_roundtrip() -> None:
    """Test WorldSummary serialization and deserialization."""
    original = WorldSummary(id="test_world", name="Test World")
    serialized = original.model_dump()
    deserialized = WorldSummary(**serialized)
    assert deserialized.id == original.id
    assert deserialized.name == original.name


def test_user_datetime_parsing_various_formats() -> None:
    """Test User parses various ISO 8601 datetime formats."""
    test_cases = [
        "2023-01-15T10:30:00",
        "2023-01-15T10:30:00Z",
        "2023-01-15T10:30:00+00:00",
    ]
    for created_at_str in test_cases:
        user = User(id="test", username="user", created_at=created_at_str)
        assert isinstance(user.created_at, datetime)
        assert user.created_at.year == 2023


def test_world_null_optional_fields() -> None:
    """Test World handles null values for optional fields."""
    api_response = {
        "id": "minimal_world",
        "name": "Minimal World",
        "description": None,
        "genre": None,
        "locale": None,
        "article_count": None,
        "category_count": None,
        "rpg_system": None,
        "created_at": None,
        "updated_at": None,
        "owner": None,
    }
    world = World(**api_response)
    assert world.name == "Minimal World"
    assert world.description is None
    assert world.article_count is None
    assert world.owner is None
