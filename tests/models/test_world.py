"""Tests for world content models.

Tests WorldSummary and World Pydantic models with various granularity
levels, validation, and API flexibility.
"""

from datetime import datetime

import pytest

from world_anvil_mcp.models.world import World, WorldSummary


class TestWorldSummary:
    """Tests for WorldSummary model (granularity 0)."""

    def test_world_summary_minimal_valid(self) -> None:
        """Test creating WorldSummary with required fields."""
        world = WorldSummary(
            id="world123",
            name="My Awesome World",
        )
        assert world.id == "world123"
        assert world.name == "My Awesome World"

    def test_world_summary_with_extra_fields(self) -> None:
        """Test WorldSummary accepts extra fields for API flexibility."""
        world = WorldSummary(
            id="world456",
            name="Another World",
            thumbnail="https://example.com/thumb.jpg",
            visibility="public",
        )
        assert world.id == "world456"
        assert world.name == "Another World"
        data = world.model_dump()
        assert data.get("thumbnail") == "https://example.com/thumb.jpg"
        assert data.get("visibility") == "public"

    def test_world_summary_serialization(self) -> None:
        """Test WorldSummary serialization to dict."""
        world = WorldSummary(
            id="world789",
            name="Test World",
        )
        data = world.model_dump()
        assert data["id"] == "world789"
        assert data["name"] == "Test World"

    def test_world_summary_missing_required_field(self) -> None:
        """Test WorldSummary validation fails without required field."""
        with pytest.raises(ValueError, match="Field required"):
            WorldSummary(  # type: ignore[call-arg]
                id="world999"
                # Missing name
            )


class TestWorld:
    """Tests for World model (granularity 1-2)."""

    def test_world_required_fields_only(self) -> None:
        """Test creating World with only required fields."""
        world = World(
            id="world123",
            name="Epic Campaign",
        )
        assert world.id == "world123"
        assert world.name == "Epic Campaign"
        assert world.description is None
        assert world.genre is None
        assert world.article_count is None

    def test_world_with_all_fields(self) -> None:
        """Test World with all optional fields provided."""
        created = datetime.fromisoformat("2022-01-01T00:00:00")
        updated = datetime.fromisoformat("2023-12-15T10:30:00")
        owner = {"id": "owner123", "username": "dmaster"}

        world = World(
            id="world456",
            name="Grand Campaign",
            description="A world of magic and mystery",
            genre="Fantasy",
            locale="en_US",
            article_count=42,
            category_count=8,
            rpg_system="D&D 5e",
            created_at=created,
            updated_at=updated,
            owner=owner,
        )
        assert world.id == "world456"
        assert world.name == "Grand Campaign"
        assert world.description == "A world of magic and mystery"
        assert world.genre == "Fantasy"
        assert world.locale == "en_US"
        assert world.article_count == 42
        assert world.category_count == 8
        assert world.rpg_system == "D&D 5e"
        assert world.created_at == created
        assert world.updated_at == updated
        assert world.owner == owner

    def test_world_datetime_parsing(self) -> None:
        """Test World parses ISO 8601 datetime strings."""
        world = World(
            id="world789",
            name="Test World",
            created_at="2023-05-10T14:25:30",
            updated_at="2023-11-20T09:15:45",
        )
        assert isinstance(world.created_at, datetime)
        assert isinstance(world.updated_at, datetime)
        assert world.created_at.year == 2023
        assert world.created_at.month == 5
        assert world.updated_at.month == 11

    def test_world_integer_counts(self) -> None:
        """Test World validates integer counts correctly."""
        world = World(
            id="world999",
            name="Article Count Test",
            article_count=150,
            category_count=25,
        )
        assert world.article_count == 150
        assert world.category_count == 25

    def test_world_zero_counts(self) -> None:
        """Test World accepts zero counts."""
        world = World(
            id="world000",
            name="Empty World",
            article_count=0,
            category_count=0,
        )
        assert world.article_count == 0
        assert world.category_count == 0

    def test_world_with_extra_fields(self) -> None:
        """Test World accepts extra fields for API flexibility."""
        world = World(
            id="world111",
            name="Flexible World",
            description="A world that evolves with the API",
            custom_data={"setting": "cyberpunk", "tech_level": 7},
            tags=["magic", "conflict", "exploration"],
        )
        assert world.id == "world111"
        data = world.model_dump()
        assert data.get("custom_data") == {"setting": "cyberpunk", "tech_level": 7}
        assert data.get("tags") == ["magic", "conflict", "exploration"]

    def test_world_serialization_minimal(self) -> None:
        """Test World serialization with minimal fields."""
        world = World(
            id="world222",
            name="Minimal World",
        )
        data = world.model_dump()
        assert data["id"] == "world222"
        assert data["name"] == "Minimal World"
        assert data["description"] is None
        assert data["article_count"] is None

    def test_world_serialization_complete(self) -> None:
        """Test World serialization with all fields."""
        created = datetime.fromisoformat("2021-06-01T08:00:00")
        owner = {"id": "dm1", "username": "GameMaster"}

        world = World(
            id="world333",
            name="Complete World",
            description="Full world data",
            genre="Sci-Fi",
            locale="en_GB",
            article_count=99,
            category_count=15,
            rpg_system="Starfinder",
            created_at=created,
            updated_at=created,
            owner=owner,
        )
        data = world.model_dump()
        assert data["id"] == "world333"
        assert data["name"] == "Complete World"
        assert data["genre"] == "Sci-Fi"
        assert data["article_count"] == 99
        assert data["owner"] == owner

    def test_world_partial_fields(self) -> None:
        """Test World with some optional fields provided."""
        world = World(
            id="world444",
            name="Partial World",
            description="Only some fields",
            genre="Horror",
            # article_count omitted
            category_count=5,
            rpg_system="Call of Cthulhu",
        )
        assert world.description == "Only some fields"
        assert world.genre == "Horror"
        assert world.category_count == 5
        assert world.rpg_system == "Call of Cthulhu"
        assert world.article_count is None

    def test_world_missing_required_field(self) -> None:
        """Test World validation fails without required field."""
        with pytest.raises(ValueError, match="Field required"):
            World(  # type: ignore[call-arg]
                id="world555"
                # Missing name
            )

    def test_world_owner_nested_dict(self) -> None:
        """Test World owner as nested dictionary."""
        owner = {
            "id": "user_id_123",
            "username": "campaign_master",
            "email": "dm@example.com",
        }
        world = World(
            id="world666",
            name="Owned World",
            owner=owner,
        )
        assert world.owner == owner
        assert world.owner["username"] == "campaign_master"

    def test_world_null_owner(self) -> None:
        """Test World with null owner field."""
        world = World(
            id="world777",
            name="Ownerless World",
            owner=None,
        )
        assert world.owner is None
