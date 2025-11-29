"""Tests for user authentication models.

Tests Identity and User Pydantic models with validation,
serialization, and flexibility for API evolution.
"""

from datetime import datetime

import pytest

from world_anvil_mcp.models.user import Identity, User


class TestIdentity:
    """Tests for Identity model."""

    def test_identity_minimal_valid(self) -> None:
        """Test creating Identity with required fields only."""
        identity = Identity(
            id="user123",
            username="testuser",
        )
        assert identity.id == "user123"
        assert identity.username == "testuser"

    def test_identity_with_extra_fields(self) -> None:
        """Test Identity accepts extra fields for API flexibility."""
        identity = Identity(
            id="user123",
            username="testuser",
            extra_field="extra_value",
            another_field=42,
        )
        assert identity.id == "user123"
        assert identity.username == "testuser"
        # Extra fields should be stored but accessible via dict
        assert identity.model_dump().get("extra_field") == "extra_value"
        assert identity.model_dump().get("another_field") == 42

    def test_identity_serialization(self) -> None:
        """Test Identity serialization to dict and JSON."""
        identity = Identity(
            id="user456",
            username="anotheruser",
        )
        data = identity.model_dump()
        assert data["id"] == "user456"
        assert data["username"] == "anotheruser"

    def test_identity_missing_required_field(self) -> None:
        """Test Identity validation fails without required field."""
        with pytest.raises(ValueError, match="Field required"):
            Identity(  # type: ignore[call-arg]
                id="user789"
                # Missing username
            )

    def test_identity_missing_id(self) -> None:
        """Test Identity validation fails without id."""
        with pytest.raises(ValueError, match="Field required"):
            Identity(  # type: ignore[call-arg]
                username="testuser"
                # Missing id
            )


class TestUser:
    """Tests for User model."""

    def test_user_required_fields_only(self) -> None:
        """Test creating User with only required fields."""
        user = User(
            id="user123",
            username="testuser",
        )
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email is None
        assert user.avatar is None
        assert user.membership is None
        assert user.created_at is None

    def test_user_with_all_fields(self) -> None:
        """Test User with all optional fields provided."""
        created = datetime.fromisoformat("2023-01-15T10:30:00")
        user = User(
            id="user123",
            username="testuser",
            email="test@example.com",
            avatar="https://example.com/avatar.jpg",
            membership="premium",
            created_at=created,
        )
        assert user.id == "user123"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.avatar == "https://example.com/avatar.jpg"
        assert user.membership == "premium"
        assert user.created_at == created

    def test_user_datetime_parsing(self) -> None:
        """Test User parses ISO 8601 datetime strings."""
        user = User(
            id="user123",
            username="testuser",
            created_at="2023-06-20T15:45:30",
        )
        assert isinstance(user.created_at, datetime)
        assert user.created_at.year == 2023
        assert user.created_at.month == 6
        assert user.created_at.day == 20

    def test_user_with_extra_fields(self) -> None:
        """Test User accepts extra fields for API flexibility."""
        user = User(
            id="user123",
            username="testuser",
            custom_field="custom_value",
            metadata={"key": "value"},
        )
        assert user.id == "user123"
        data = user.model_dump()
        assert data.get("custom_field") == "custom_value"
        assert data.get("metadata") == {"key": "value"}

    def test_user_serialization(self) -> None:
        """Test User serialization to dict."""
        created = datetime.fromisoformat("2023-03-10T12:00:00")
        user = User(
            id="user456",
            username="anotheruser",
            email="another@example.com",
            created_at=created,
        )
        data = user.model_dump()
        assert data["id"] == "user456"
        assert data["username"] == "anotheruser"
        assert data["email"] == "another@example.com"
        assert data["created_at"] == created

    def test_user_serialization_with_none_values(self) -> None:
        """Test User serialization includes None values."""
        user = User(
            id="user789",
            username="minimaluser",
        )
        data = user.model_dump()
        assert data["id"] == "user789"
        assert data["username"] == "minimaluser"
        assert data["email"] is None
        assert data["avatar"] is None
        assert data["membership"] is None
        assert data["created_at"] is None

    def test_user_missing_required_field(self) -> None:
        """Test User validation fails without required field."""
        with pytest.raises(ValueError, match="Field required"):
            User(  # type: ignore[call-arg]
                id="user999"
                # Missing username
            )
