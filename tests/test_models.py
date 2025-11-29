"""Tests for Pydantic models for user and world data.

Tests models including:
- Identity and User validation
- World and WorldSummary validation
- Optional field handling
- datetime parsing
- extra="allow" configuration for API flexibility
"""

from datetime import datetime

import pytest

from world_anvil_mcp.models.user import Identity, User
from world_anvil_mcp.models.world import World, WorldSummary


class TestIdentityModel:
    """Tests for Identity Pydantic model."""

    @pytest.mark.unit
    def test_identity_minimal_valid(self) -> None:
        """Test creating Identity with required fields only."""
        # Arrange
        data = {"id": "user123", "username": "testuser"}

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == "user123"
        assert identity.username == "testuser"

    @pytest.mark.unit
    def test_identity_with_extra_fields(self) -> None:
        """Test Identity accepts extra fields for API flexibility."""
        # Arrange
        data = {
            "id": "user123",
            "username": "testuser",
            "extra_field": "extra_value",
            "another_field": 42,
            "nested": {"key": "value"},
        }

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == "user123"
        assert identity.username == "testuser"
        # Extra fields should be stored
        identity_dict = identity.model_dump()
        assert identity_dict.get("extra_field") == "extra_value"
        assert identity_dict.get("another_field") == 42
        assert identity_dict.get("nested") == {"key": "value"}

    @pytest.mark.unit
    def test_identity_serialization(self) -> None:
        """Test Identity serialization to dict."""
        # Arrange
        identity = Identity(id="user456", username="anotheruser")

        # Act
        data = identity.model_dump()

        # Assert
        assert data["id"] == "user456"
        assert data["username"] == "anotheruser"

    @pytest.mark.unit
    def test_identity_serialization_json(self) -> None:
        """Test Identity serialization to JSON."""
        # Arrange
        identity = Identity(id="user789", username="jsonuser")

        # Act
        json_str = identity.model_dump_json()

        # Assert
        assert "user789" in json_str
        assert "jsonuser" in json_str

    @pytest.mark.unit
    def test_identity_missing_id(self) -> None:
        """Test Identity validation fails without id."""
        # Arrange
        data = {"username": "testuser"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            Identity(**data)

    @pytest.mark.unit
    def test_identity_missing_username(self) -> None:
        """Test Identity validation fails without username."""
        # Arrange
        data = {"id": "user123"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            Identity(**data)

    @pytest.mark.unit
    def test_identity_missing_both_required(self) -> None:
        """Test Identity validation fails without both required fields."""
        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            Identity()  # type: ignore[call-arg]

    @pytest.mark.unit
    def test_identity_type_validation(self) -> None:
        """Test Identity requires correct types (Pydantic v2 strict)."""
        # Arrange - Pydantic v2 requires exact types (no auto-coercion)
        data = {
            "id": "123",  # String as required
            "username": "testuser",
        }

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == "123"
        assert isinstance(identity.id, str)

    @pytest.mark.unit
    def test_identity_empty_strings(self) -> None:
        """Test Identity with empty string values."""
        # Arrange
        data = {"id": "", "username": ""}

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == ""
        assert identity.username == ""

    @pytest.mark.unit
    def test_identity_special_chars_in_strings(self) -> None:
        """Test Identity with special characters."""
        # Arrange
        data = {"id": "user-123@456", "username": "user.name_2023"}

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == "user-123@456"
        assert identity.username == "user.name_2023"


class TestUserModel:
    """Tests for User Pydantic model."""

    @pytest.mark.unit
    def test_user_required_fields_only(self) -> None:
        """Test creating User with only required fields."""
        # Arrange
        data = {"id": "user123", "username": "testuser"}

        # Act
        user = User(**data)

        # Assert
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email is None
        assert user.avatar is None
        assert user.membership is None
        assert user.created_at is None

    @pytest.mark.unit
    def test_user_with_all_fields(self) -> None:
        """Test User with all optional fields provided."""
        # Arrange
        created = datetime.fromisoformat("2023-01-15T10:30:00")
        data = {
            "id": "user123",
            "username": "testuser",
            "email": "test@example.com",
            "avatar": "https://example.com/avatar.jpg",
            "membership": "premium",
            "created_at": created,
        }

        # Act
        user = User(**data)

        # Assert
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.avatar == "https://example.com/avatar.jpg"
        assert user.membership == "premium"
        assert user.created_at == created

    @pytest.mark.unit
    def test_user_datetime_parsing_iso_string(self) -> None:
        """Test User parses ISO 8601 datetime strings."""
        # Arrange
        data = {
            "id": "user123",
            "username": "testuser",
            "created_at": "2023-06-20T15:45:30",
        }

        # Act
        user = User(**data)

        # Assert
        assert isinstance(user.created_at, datetime)
        assert user.created_at.year == 2023
        assert user.created_at.month == 6
        assert user.created_at.day == 20
        assert user.created_at.hour == 15
        assert user.created_at.minute == 45
        assert user.created_at.second == 30

    @pytest.mark.unit
    def test_user_datetime_with_microseconds(self) -> None:
        """Test User parses datetime with microseconds."""
        # Arrange
        data = {
            "id": "user123",
            "username": "testuser",
            "created_at": "2023-06-20T15:45:30.123456",
        }

        # Act
        user = User(**data)

        # Assert
        assert isinstance(user.created_at, datetime)
        assert user.created_at.microsecond == 123456

    @pytest.mark.unit
    def test_user_datetime_with_timezone(self) -> None:
        """Test User parses datetime with timezone info."""
        # Arrange
        data = {
            "id": "user123",
            "username": "testuser",
            "created_at": "2023-06-20T15:45:30+00:00",
        }

        # Act
        user = User(**data)

        # Assert
        assert isinstance(user.created_at, datetime)
        assert user.created_at.year == 2023

    @pytest.mark.unit
    def test_user_datetime_object(self) -> None:
        """Test User accepts datetime objects directly."""
        # Arrange
        created = datetime(2023, 6, 20, 15, 45, 30)
        data = {
            "id": "user123",
            "username": "testuser",
            "created_at": created,
        }

        # Act
        user = User(**data)

        # Assert
        assert user.created_at == created

    @pytest.mark.unit
    def test_user_with_extra_fields(self) -> None:
        """Test User accepts extra fields for API flexibility."""
        # Arrange
        data = {
            "id": "user123",
            "username": "testuser",
            "custom_field": "custom_value",
            "metadata": {"key": "value"},
            "is_premium": True,
        }

        # Act
        user = User(**data)

        # Assert
        assert user.id == "user123"
        user_dict = user.model_dump()
        assert user_dict.get("custom_field") == "custom_value"
        assert user_dict.get("metadata") == {"key": "value"}
        assert user_dict.get("is_premium") is True

    @pytest.mark.unit
    def test_user_serialization(self) -> None:
        """Test User serialization to dict."""
        # Arrange
        created = datetime.fromisoformat("2023-03-10T12:00:00")
        user = User(
            id="user456",
            username="anotheruser",
            email="another@example.com",
            created_at=created,
        )

        # Act
        data = user.model_dump()

        # Assert
        assert data["id"] == "user456"
        assert data["username"] == "anotheruser"
        assert data["email"] == "another@example.com"
        assert data["created_at"] == created

    @pytest.mark.unit
    def test_user_serialization_with_none_values(self) -> None:
        """Test User serialization includes None values."""
        # Arrange
        user = User(id="user789", username="minimaluser")

        # Act
        data = user.model_dump()

        # Assert
        assert data["id"] == "user789"
        assert data["username"] == "minimaluser"
        assert data["email"] is None
        assert data["avatar"] is None
        assert data["membership"] is None
        assert data["created_at"] is None

    @pytest.mark.unit
    def test_user_missing_required_id(self) -> None:
        """Test User validation fails without id."""
        # Arrange
        data = {"username": "testuser"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            User(**data)

    @pytest.mark.unit
    def test_user_missing_required_username(self) -> None:
        """Test User validation fails without username."""
        # Arrange
        data = {"id": "user123"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            User(**data)

    @pytest.mark.unit
    def test_user_optional_field_variations(self) -> None:
        """Test User with various optional field combinations."""
        # Arrange
        test_cases = [
            {"id": "u1", "username": "u1", "email": "test@example.com"},
            {"id": "u2", "username": "u2", "avatar": "https://example.com/pic.jpg"},
            {"id": "u3", "username": "u3", "membership": "premium"},
            {
                "id": "u4",
                "username": "u4",
                "email": "test@example.com",
                "avatar": "https://example.com/pic.jpg",
            },
        ]

        # Act & Assert
        for data in test_cases:
            user = User(**data)
            assert user.id == data["id"]
            assert user.username == data["username"]


class TestWorldSummaryModel:
    """Tests for WorldSummary Pydantic model."""

    @pytest.mark.unit
    def test_world_summary_minimal_valid(self) -> None:
        """Test creating WorldSummary with required fields."""
        # Arrange
        data = {"id": "world123", "name": "Eberron"}

        # Act
        world = WorldSummary(**data)

        # Assert
        assert world.id == "world123"
        assert world.name == "Eberron"

    @pytest.mark.unit
    def test_world_summary_with_extra_fields(self) -> None:
        """Test WorldSummary accepts extra fields."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Eberron",
            "url": "https://www.worldanvil.com/w/eberron",
            "tags": ["fantasy", "dnd5e"],
        }

        # Act
        world = WorldSummary(**data)

        # Assert
        assert world.id == "world123"
        assert world.name == "Eberron"
        world_dict = world.model_dump()
        assert world_dict.get("url") == "https://www.worldanvil.com/w/eberron"
        assert world_dict.get("tags") == ["fantasy", "dnd5e"]

    @pytest.mark.unit
    def test_world_summary_missing_id(self) -> None:
        """Test WorldSummary validation fails without id."""
        # Arrange
        data = {"name": "Eberron"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            WorldSummary(**data)

    @pytest.mark.unit
    def test_world_summary_missing_name(self) -> None:
        """Test WorldSummary validation fails without name."""
        # Arrange
        data = {"id": "world123"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            WorldSummary(**data)


class TestWorldModel:
    """Tests for World Pydantic model."""

    @pytest.mark.unit
    def test_world_required_fields_only(self) -> None:
        """Test creating World with only required fields."""
        # Arrange
        data = {"id": "world123", "name": "Eberron"}

        # Act
        world = World(**data)

        # Assert
        assert world.id == "world123"
        assert world.name == "Eberron"
        assert world.description is None
        assert world.genre is None
        assert world.locale is None
        assert world.article_count is None
        assert world.category_count is None
        assert world.rpg_system is None
        assert world.created_at is None
        assert world.updated_at is None
        assert world.owner is None

    @pytest.mark.unit
    def test_world_with_all_fields(self) -> None:
        """Test World with all optional fields provided."""
        # Arrange
        created = datetime.fromisoformat("2023-01-15T10:30:00")
        updated = datetime.fromisoformat("2023-06-20T15:45:30")
        owner = {"id": "user123", "name": "Dungeon Master"}

        data = {
            "id": "world123",
            "name": "Eberron",
            "description": "A world of magic and mystery",
            "genre": "Fantasy",
            "locale": "en_US",
            "article_count": 150,
            "category_count": 25,
            "rpg_system": "D&D 5e",
            "created_at": created,
            "updated_at": updated,
            "owner": owner,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.id == "world123"
        assert world.name == "Eberron"
        assert world.description == "A world of magic and mystery"
        assert world.genre == "Fantasy"
        assert world.locale == "en_US"
        assert world.article_count == 150
        assert world.category_count == 25
        assert world.rpg_system == "D&D 5e"
        assert world.created_at == created
        assert world.updated_at == updated
        assert world.owner == owner

    @pytest.mark.unit
    def test_world_datetime_parsing(self) -> None:
        """Test World parses ISO 8601 datetime strings."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Eberron",
            "created_at": "2023-01-15T10:30:00",
            "updated_at": "2023-06-20T15:45:30",
        }

        # Act
        world = World(**data)

        # Assert
        assert isinstance(world.created_at, datetime)
        assert isinstance(world.updated_at, datetime)
        assert world.created_at.year == 2023
        assert world.created_at.month == 1
        assert world.updated_at.year == 2023
        assert world.updated_at.month == 6

    @pytest.mark.unit
    def test_world_article_count_int(self) -> None:
        """Test World validates article_count as integer."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Eberron",
            "article_count": 150,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.article_count == 150
        assert isinstance(world.article_count, int)

    @pytest.mark.unit
    def test_world_article_count_coercion(self) -> None:
        """Test World coerces article_count to int."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Eberron",
            "article_count": "150",  # String
        }

        # Act
        world = World(**data)

        # Assert
        assert world.article_count == 150
        assert isinstance(world.article_count, int)

    @pytest.mark.unit
    def test_world_owner_dict(self) -> None:
        """Test World owner as arbitrary dict."""
        # Arrange
        owner = {
            "id": "user123",
            "name": "Dungeon Master",
            "email": "dm@example.com",
            "avatar": "https://example.com/avatar.jpg",
        }
        data = {
            "id": "world123",
            "name": "Eberron",
            "owner": owner,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.owner == owner
        assert world.owner["id"] == "user123"
        assert world.owner["name"] == "Dungeon Master"

    @pytest.mark.unit
    def test_world_with_extra_fields(self) -> None:
        """Test World accepts extra fields for API flexibility."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Eberron",
            "url": "https://www.worldanvil.com/w/eberron",
            "tags": ["fantasy", "dnd5e"],
            "is_public": True,
            "metadata": {"key": "value"},
        }

        # Act
        world = World(**data)

        # Assert
        assert world.id == "world123"
        world_dict = world.model_dump()
        assert world_dict.get("url") == "https://www.worldanvil.com/w/eberron"
        assert world_dict.get("tags") == ["fantasy", "dnd5e"]
        assert world_dict.get("is_public") is True

    @pytest.mark.unit
    def test_world_serialization(self) -> None:
        """Test World serialization to dict."""
        # Arrange
        created = datetime.fromisoformat("2023-01-15T10:30:00")
        world = World(
            id="world123",
            name="Eberron",
            description="A world of magic",
            genre="Fantasy",
            article_count=150,
            created_at=created,
        )

        # Act
        data = world.model_dump()

        # Assert
        assert data["id"] == "world123"
        assert data["name"] == "Eberron"
        assert data["description"] == "A world of magic"
        assert data["genre"] == "Fantasy"
        assert data["article_count"] == 150
        assert data["created_at"] == created

    @pytest.mark.unit
    def test_world_serialization_with_none_values(self) -> None:
        """Test World serialization includes None values."""
        # Arrange
        world = World(id="world123", name="Eberron")

        # Act
        data = world.model_dump()

        # Assert
        assert data["id"] == "world123"
        assert data["name"] == "Eberron"
        assert data["description"] is None
        assert data["genre"] is None
        assert data["article_count"] is None

    @pytest.mark.unit
    def test_world_missing_required_id(self) -> None:
        """Test World validation fails without id."""
        # Arrange
        data = {"name": "Eberron"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            World(**data)

    @pytest.mark.unit
    def test_world_missing_required_name(self) -> None:
        """Test World validation fails without name."""
        # Arrange
        data = {"id": "world123"}

        # Act & Assert
        with pytest.raises(ValueError, match="Field required"):
            World(**data)

    @pytest.mark.unit
    def test_world_zero_counts(self) -> None:
        """Test World handles zero article/category counts."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Empty World",
            "article_count": 0,
            "category_count": 0,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.article_count == 0
        assert world.category_count == 0

    @pytest.mark.unit
    def test_world_negative_counts(self) -> None:
        """Test World accepts negative counts (edge case)."""
        # Arrange
        data = {
            "id": "world123",
            "name": "World",
            "article_count": -1,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.article_count == -1


class TestModelExtraFieldsConfiguration:
    """Tests for extra="allow" configuration across all models."""

    @pytest.mark.unit
    def test_all_models_allow_extra_fields(self) -> None:
        """Test all models have extra="allow" in config."""
        # Arrange
        models = [Identity, User, WorldSummary, World]

        # Act & Assert
        for model in models:
            config = model.model_config
            assert config.get("extra") == "allow"

    @pytest.mark.unit
    def test_extra_fields_preserved_in_dict(self) -> None:
        """Test extra fields are preserved when serialized to dict."""
        # Arrange
        user_data = {
            "id": "user123",
            "username": "testuser",
            "custom_field": "custom_value",
            "another_custom": 42,
        }

        # Act
        user = User(**user_data)
        serialized = user.model_dump()

        # Assert
        assert serialized["custom_field"] == "custom_value"
        assert serialized["another_custom"] == 42

    @pytest.mark.unit
    def test_nested_extra_fields(self) -> None:
        """Test nested extra fields are preserved."""
        # Arrange
        world_data = {
            "id": "world123",
            "name": "Eberron",
            "metadata": {
                "nested": {
                    "deeply": {
                        "key": "value",
                    }
                }
            },
        }

        # Act
        world = World(**world_data)
        serialized = world.model_dump()

        # Assert
        assert serialized["metadata"]["nested"]["deeply"]["key"] == "value"


class TestModelValidationEdgeCases:
    """Tests for validation edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_identity_with_unicode_strings(self) -> None:
        """Test Identity with Unicode characters."""
        # Arrange
        data = {
            "id": "user_123_😀",
            "username": "用户名",
        }

        # Act
        identity = Identity(**data)

        # Assert
        assert identity.id == "user_123_😀"
        assert identity.username == "用户名"

    @pytest.mark.unit
    def test_user_with_very_long_email(self) -> None:
        """Test User with very long email address."""
        # Arrange
        long_email = "a" * 1000 + "@example.com"
        data = {
            "id": "user123",
            "username": "testuser",
            "email": long_email,
        }

        # Act
        user = User(**data)

        # Assert
        assert user.email == long_email

    @pytest.mark.unit
    def test_world_with_empty_strings(self) -> None:
        """Test World with empty string values."""
        # Arrange
        data = {
            "id": "",
            "name": "",
            "description": "",
            "genre": "",
        }

        # Act
        world = World(**data)

        # Assert
        assert world.id == ""
        assert world.name == ""
        assert world.description == ""
        assert world.genre == ""

    @pytest.mark.unit
    def test_world_summary_large_counts(self) -> None:
        """Test World with very large article counts."""
        # Arrange
        data = {
            "id": "world123",
            "name": "Massive World",
            "article_count": 1000000,
            "category_count": 10000,
        }

        # Act
        world = World(**data)

        # Assert
        assert world.article_count == 1000000
        assert world.category_count == 10000
