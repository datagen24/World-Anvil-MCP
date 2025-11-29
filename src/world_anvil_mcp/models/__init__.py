"""Pydantic v2 models for World Anvil API responses.

This package provides type-safe data validation for all World Anvil API
responses. Models use Pydantic v2 syntax with strict field validation.

Exported Models:
    - Identity: User identity from /identity endpoint
    - User: User details from /user endpoint
    - WorldSummary: Minimal world reference (granularity 0)
    - World: Full world details (granularity 1-2)
"""

from .user import Identity, User
from .world import World, WorldSummary

__all__ = [
    "Identity",
    "User",
    "World",
    "WorldSummary",
]
