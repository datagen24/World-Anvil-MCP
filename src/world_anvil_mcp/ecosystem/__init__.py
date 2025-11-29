"""MCP Ecosystem detection and integration framework.

This module provides detection and management for companion MCPs that enhance
World Anvil workflows. See docs/specs/MCP-ECOSYSTEM-SPEC.md for complete
specification.

Key Components:
    - EcosystemDetector: Detects available companion MCPs
    - IntegrationTier: Priority levels (CRITICAL, RECOMMENDED, OPTIONAL)
    - CompanionMCP: Specification for companion integrations
    - COMPANION_REGISTRY: Registry of known companions (6 total)

Example:
    >>> from world_anvil_mcp.ecosystem import EcosystemDetector, IntegrationTier
    >>> detector = EcosystemDetector(available_tools=["foundry_get_actors"])
    >>> detector.has("Foundry VTT")
    True
    >>> len(detector.critical_companions)
    1
"""

from world_anvil_mcp.ecosystem.detector import (
    COMPANION_REGISTRY,
    CompanionMCP,
    EcosystemDetector,
    IntegrationTier,
)

__all__ = [
    "COMPANION_REGISTRY",
    "CompanionMCP",
    "EcosystemDetector",
    "IntegrationTier",
]
