"""World content models for World Anvil API.

This module provides Pydantic v2 models for world-related API responses:
- WorldSummary: Minimal world reference (granularity level 0)
- World: Full world details with metadata (granularity levels 1-2)

Models validate responses from /user/worlds, /world/{id}, and related
world endpoints, supporting flexible evolution of API responses.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorldSummary(BaseModel):
    """Minimal world reference for granularity level 0.

    Lightweight world representation containing only essential identifiers.
    Used in list responses and as embedded references within larger
    API responses when minimal data is requested.

    Attributes:
        id: World unique identifier assigned by World Anvil.
        name: World name or title.

    Example:
        >>> worlds = await client.list_user_worlds(granularity="0")
        >>> for world in worlds:
        ...     print(f"World: {world.name} (ID: {world.id})")
    """

    id: str = Field(..., description="World unique identifier")
    name: str = Field(..., description="World name")

    model_config = ConfigDict(extra="allow")


class World(BaseModel):
    """Full world details with metadata for granularity levels 1-2.

    Complete world information including description, genre, category counts,
    RPG system information, timestamps, and owner details. Returned by
    /world/{id} and /user/worlds endpoints with full granularity.

    Attributes:
        id: World unique identifier assigned by World Anvil.
        name: World name or title.
        description: World description or summary text (granularity 1+).
        genre: World genre classification (granularity 1+).
        locale: World locale/language setting (granularity 1+).
        article_count: Number of articles in the world (granularity 1+).
        category_count: Number of categories in the world (granularity 1+).
        rpg_system: Linked RPG system or ruleset name.
        created_at: World creation timestamp in ISO 8601 format.
        updated_at: World last update timestamp in ISO 8601 format.
        owner: Nested dictionary containing world owner information.

    Example:
        >>> world = await client.get_world("world-id", granularity="2")
        >>> print(f"World: {world.name}")
        >>> print(f"Genre: {world.genre}")
        >>> print(f"Articles: {world.article_count}")
        >>> print(f"Categories: {world.category_count}")
        >>> if world.rpg_system:
        ...     print(f"RPG System: {world.rpg_system}")
    """

    id: str = Field(..., description="World unique identifier")
    name: str = Field(..., description="World name")
    description: str | None = Field(None, description="World description")
    genre: str | None = Field(None, description="World genre")
    locale: str | None = Field(None, description="World locale/language")
    article_count: int | None = Field(None, description="Number of articles in world")
    category_count: int | None = Field(None, description="Number of categories in world")
    rpg_system: str | None = Field(None, description="Linked RPG system")
    created_at: datetime | None = Field(None, description="World creation date")
    updated_at: datetime | None = Field(None, description="World last update date")
    owner: dict[str, Any] | None = Field(None, description="World owner information")

    model_config = ConfigDict(extra="allow")
