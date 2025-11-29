"""User authentication models for World Anvil API.

This module provides Pydantic v2 models for user-related API responses:
- Identity: Minimal user identity from /identity endpoint
- User: Full user details from /user endpoint with profile information

Both models support flexible validation with extra fields allowed to handle
API evolution gracefully.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Identity(BaseModel):
    """User identity from /identity endpoint.

    Minimal user identification returned by the /identity endpoint,
    used for authentication verification and session validation.

    Attributes:
        id: User unique identifier assigned by World Anvil.
        username: Display username for the user account.

    Example:
        >>> identity = await client.get_identity()
        >>> print(f"Authenticated as: {identity.username} (ID: {identity.id})")
    """

    id: str = Field(..., description="User unique identifier")
    username: str = Field(..., description="Display username")

    model_config = ConfigDict(extra="allow")


class User(BaseModel):
    """User profile details from /user endpoint.

    Complete user information including profile data, email, avatar,
    and guild membership status. Retrieved from the /user endpoint
    after successful authentication.

    Attributes:
        id: User unique identifier assigned by World Anvil.
        username: Display username for the user account.
        email: User email address (optional).
        avatar: URL to user's avatar image (optional).
        membership: Guild membership level or tier (optional).
        created_at: Account creation timestamp in ISO 8601 format (optional).

    Example:
        >>> user = await client.get_user()
        >>> print(f"User: {user.username}")
        >>> print(f"Member since: {user.created_at}")
        >>> if user.membership:
        ...     print(f"Guild Member: {user.membership}")
    """

    id: str = Field(..., description="User unique identifier")
    username: str = Field(..., description="Display username")
    email: str | None = Field(None, description="User email address")
    avatar: str | None = Field(None, description="Avatar image URL")
    membership: str | None = Field(None, description="Guild membership level")
    created_at: datetime | None = Field(None, description="Account creation date")

    model_config = ConfigDict(extra="allow")
