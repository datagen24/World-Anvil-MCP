"""MCP Ecosystem Detection Framework.

This module implements the World Anvil MCP ecosystem integration pattern,
detecting and managing companion MCPs that enhance worldbuilding workflows.

Full specification: docs/specs/MCP-ECOSYSTEM-SPEC.md

IMPORTANT: Context Engine is a SEPARATE MCP server project (not part of this codebase).
It provides semantic search over TTRPG reference materials. For details, see:
docs/specs/CONTEXT-ENGINE-SPEC.md

Example:
    >>> detector = EcosystemDetector(available_tools=["foundry_get_actors", "search_reference"])
    >>> detector.critical_companions  # [Foundry VTT, Context Engine]
    >>> detector.has("Foundry VTT")  # True
    >>> suggestions = detector.suggest_for_workflow("session_prep")
    >>> # [("Foundry VTT", "Sync tonight's NPCs to Foundry", companion_obj), ...]
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class IntegrationTier(Enum):
    """Integration priority tiers for companion MCPs.

    Attributes:
        CRITICAL: Must detect, enables core workflows (Foundry VTT, Context Engine)
        RECOMMENDED: Should detect, enhances experience (Dropbox, Notion)
        OPTIONAL: May detect, nice to have (Discord, Calendar)
    """

    CRITICAL = 1  # Must detect, enables core workflows
    RECOMMENDED = 2  # Should detect, enhances experience
    OPTIONAL = 3  # May detect, nice to have


@dataclass
class CompanionMCP:
    """Specification for a companion MCP integration.

    Defines how to detect and integrate with companion MCPs in the ecosystem.

    Attributes:
        name: Human-readable companion name
        tier: Integration priority tier
        description: Brief description of companion's role
        detection_tools: Tool names used to detect this MCP
        use_cases: List of common use cases
        documentation_url: Optional URL to integration documentation
        can_read: Whether companion can read data
        can_write: Whether companion can write data
        bidirectional: Whether companion supports bidirectional sync
        workflow_suggestions: Dict mapping workflow IDs to suggestion text

    Example:
        >>> foundry = CompanionMCP(
        ...     name="Foundry VTT",
        ...     tier=IntegrationTier.CRITICAL,
        ...     description="Virtual tabletop",
        ...     detection_tools=["foundry_get_actors"],
        ...     use_cases=["Sync NPCs to actors"],
        ...     bidirectional=True,
        ... )
    """

    name: str
    tier: IntegrationTier
    description: str
    detection_tools: list[str]
    use_cases: list[str]
    documentation_url: str | None = None

    # Integration capabilities
    can_read: bool = True
    can_write: bool = False
    bidirectional: bool = False

    # Workflow hints
    workflow_suggestions: dict[str, str] = field(default_factory=dict)


# Registry of known companion MCPs
COMPANION_REGISTRY: list[CompanionMCP] = [
    # Tier 1: Critical - Must detect, enables core workflows
    CompanionMCP(
        name="Foundry VTT",
        tier=IntegrationTier.CRITICAL,
        description="Virtual tabletop for live gameplay execution",
        detection_tools=[
            "foundry_get_actors",
            "foundry_get_scenes",
            "foundry_get_journal",
            "foundry_roll_dice",
            "foundry_update_actor",
        ],
        use_cases=[
            "Sync NPCs to Foundry actors",
            "Import locations as scenes",
            "Capture session logs from chat",
            "Live lookup during play",
        ],
        documentation_url="https://foundryvtt.com/packages/foundry-mcp-bridge",
        can_read=True,
        can_write=True,
        bidirectional=True,
        workflow_suggestions={
            "session_prep": "Sync tonight's NPCs and locations to Foundry",
            "session_notes": "Import combat log from Foundry session",
            "npc_generation": "Push new NPC to Foundry as actor",
        },
    ),
    CompanionMCP(
        name="Context Engine",
        tier=IntegrationTier.CRITICAL,
        description="Semantic search over TTRPG reference materials (SEPARATE PROJECT)",
        detection_tools=[
            "search_reference",
            "get_srd_content",
            "find_similar",
            "generate_inspiration",
        ],
        use_cases=[
            "Research D&D lore while creating content",
            "Find similar NPCs/locations for inspiration",
            "Verify rule accuracy",
            "Generate culturally consistent names",
        ],
        documentation_url=None,  # Our own MCP (separate project)
        can_read=True,
        can_write=True,  # User corpus
        workflow_suggestions={
            "npc_generation": "Search reference for cultural details",
            "world_building": "Find historical parallels",
            "location_development": "Get genre-appropriate inspiration",
        },
    ),
    # Tier 2: Recommended - Should detect, enhances experience
    CompanionMCP(
        name="Dropbox",
        tier=IntegrationTier.RECOMMENDED,
        description="Cloud storage for maps, handouts, and assets",
        detection_tools=[
            "dropbox_upload",
            "dropbox_download",
            "dropbox_list_folder",
            "dropbox_search",
        ],
        use_cases=[
            "Store high-res battle maps",
            "Share handout documents",
            "Backup world exports",
            "Organize campaign audio",
        ],
        can_read=True,
        can_write=True,
        workflow_suggestions={
            "location_development": "Upload map to Dropbox, link in article",
            "session_prep": "Gather handouts from Dropbox",
        },
    ),
    CompanionMCP(
        name="Notion",
        tier=IntegrationTier.RECOMMENDED,
        description="Project management for campaign meta-planning",
        detection_tools=[
            "notion_search",
            "notion_create_page",
            "notion_query_database",
        ],
        use_cases=[
            "Track session prep checklists",
            "Manage content creation backlog",
            "Coordinate player schedules",
            "Store out-of-world notes",
        ],
        can_read=True,
        can_write=True,
        workflow_suggestions={
            "session_prep": "Check prep checklist in Notion",
            "campaign_setup": "Create campaign tracker database",
        },
    ),
    # Tier 3: Optional - May detect, nice to have
    CompanionMCP(
        name="Discord",
        tier=IntegrationTier.OPTIONAL,
        description="Player communication and announcements",
        detection_tools=[
            "discord_send_message",
            "discord_list_channels",
        ],
        use_cases=[
            "Announce session times",
            "Share World Anvil links",
            "Post session summaries",
        ],
        can_write=True,
        workflow_suggestions={
            "session_notes": "Post summary to Discord channel",
        },
    ),
    CompanionMCP(
        name="Calendar",
        tier=IntegrationTier.OPTIONAL,
        description="Session scheduling",
        detection_tools=[
            "calendar_create_event",
            "calendar_list_events",
        ],
        use_cases=[
            "Schedule game sessions",
            "Send reminders",
        ],
        can_write=True,
        workflow_suggestions={
            "campaign_setup": "Schedule Session 0",
        },
    ),
]


class EcosystemDetector:
    """Detects and manages companion MCP integrations.

    Implements the ecosystem detection framework from MCP-ECOSYSTEM-SPEC.md.
    Provides intelligent integration suggestions based on available companion MCPs.

    The detector operates in three phases:
    1. Initialization: Accept available tool list from MCP context
    2. Detection: Match tools against companion registrations
    3. Query: Provide companion information and workflow suggestions

    Attributes:
        available_tools: Set of tool names available in current MCP context
        _detected: Dict mapping companion names to CompanionMCP objects

    Example:
        >>> detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        >>> detector.critical_companions  # [Foundry VTT]
        >>> print(detector.get_ecosystem_status())  # Markdown status report
    """

    def __init__(self, available_tools: list[str]) -> None:
        """Initialize detector with available tool names.

        Args:
            available_tools: List of tool names from MCP server context.
                These are the tools available across all registered MCPs.

        Example:
            >>> tools = ["foundry_get_actors", "search_reference", "dropbox_upload"]
            >>> detector = EcosystemDetector(available_tools=tools)
            >>> len(detector.all_companions)
            3
        """
        self.available_tools = set(available_tools)
        self._detected: dict[str, CompanionMCP] = {}
        self._detect_all()

    def _detect_all(self) -> None:
        """Detect all available companion MCPs by matching tools against registry."""
        for companion in COMPANION_REGISTRY:
            if self._is_available(companion):
                self._detected[companion.name] = companion

    def _is_available(self, companion: CompanionMCP) -> bool:
        """Check if companion MCP is available based on tool presence.

        A companion is considered available if ANY of its detection tools
        are present in the available tools set.

        Args:
            companion: CompanionMCP to check availability

        Returns:
            True if at least one detection tool is available
        """
        return any(tool in self.available_tools for tool in companion.detection_tools)

    @property
    def critical_companions(self) -> list[CompanionMCP]:
        """Get detected critical tier companions only.

        Critical companions (Foundry VTT, Context Engine) are required
        for core workflows. Missing critical companions should trigger
        warnings or installation prompts.

        Returns:
            List of CRITICAL tier companions that were detected

        Example:
            >>> detector = EcosystemDetector(["foundry_get_actors", "search_reference"])
            >>> len(detector.critical_companions)
            2
            >>> detector.critical_companions[0].name
            'Foundry VTT'
        """
        return [c for c in self._detected.values() if c.tier == IntegrationTier.CRITICAL]

    @property
    def all_companions(self) -> list[CompanionMCP]:
        """Get all detected companions across all tiers.

        Returns:
            List of all detected CompanionMCP objects (CRITICAL, RECOMMENDED, OPTIONAL)
        """
        return list(self._detected.values())

    def has(self, name: str) -> bool:
        """Check if specific companion is available.

        Args:
            name: Companion name (e.g., "Foundry VTT", "Context Engine")

        Returns:
            True if companion is detected and available

        Example:
            >>> detector = EcosystemDetector(["foundry_get_actors"])
            >>> detector.has("Foundry VTT")
            True
            >>> detector.has("Context Engine")
            False
        """
        return name in self._detected

    def get(self, name: str) -> CompanionMCP | None:
        """Get companion by name.

        Args:
            name: Companion name to retrieve

        Returns:
            CompanionMCP object if detected, None otherwise

        Example:
            >>> detector = EcosystemDetector(["foundry_get_actors"])
            >>> foundry = detector.get("Foundry VTT")
            >>> foundry.bidirectional
            True
        """
        return self._detected.get(name)

    def suggest_for_workflow(
        self,
        workflow: str,
    ) -> list[tuple[str, str, CompanionMCP]]:
        """Get integration suggestions for a workflow.

        Returns all detected companions that have suggestions for the
        given workflow, sorted by tier (CRITICAL first, then RECOMMENDED,
        then OPTIONAL).

        Args:
            workflow: Workflow identifier (e.g., "session_prep", "npc_generation")

        Returns:
            List of (companion_name, suggestion_text, companion_object) tuples,
            sorted by integration tier (critical first)

        Example:
            >>> detector = EcosystemDetector(["foundry_get_actors", "notion_search"])
            >>> suggestions = detector.suggest_for_workflow("session_prep")
            >>> for name, hint, companion in suggestions:
            ...     print(f"{name}: {hint}")
            Foundry VTT: Sync tonight's NPCs to Foundry
            Notion: Check prep checklist in Notion
        """
        suggestions = []
        for companion in self._detected.values():
            if workflow in companion.workflow_suggestions:
                suggestions.append(
                    (
                        companion.name,
                        companion.workflow_suggestions[workflow],
                        companion,
                    )
                )

        # Sort by tier (critical first)
        suggestions.sort(key=lambda x: x[2].tier.value)
        return suggestions

    def get_ecosystem_status(self) -> str:
        """Generate markdown status report of detected ecosystem.

        Creates a comprehensive status report showing:
        - Detected CRITICAL integrations (with success indicator)
        - Missing CRITICAL integrations (with warning and install links)
        - Available RECOMMENDED integrations
        - Available OPTIONAL integrations

        Returns:
            Markdown-formatted status string with tier-based sections

        Example:
            >>> detector = EcosystemDetector(["foundry_get_actors"])
            >>> print(detector.get_ecosystem_status())
            ## 🔌 MCP Ecosystem Status

            ### ✅ Critical Integrations
            - **Foundry VTT**: Virtual tabletop for live gameplay execution

            ### ⚠️ Missing Critical Integrations
            - **Context Engine**: Semantic search over TTRPG reference materials
        """
        lines = ["## 🔌 MCP Ecosystem Status\n"]

        # Critical companions (detected and missing)
        critical = [c for c in self._detected.values() if c.tier == IntegrationTier.CRITICAL]
        missing_critical = [
            c
            for c in COMPANION_REGISTRY
            if c.tier == IntegrationTier.CRITICAL and c.name not in self._detected
        ]

        if critical:
            lines.append("### ✅ Critical Integrations")
            for c in critical:
                lines.append(f"- **{c.name}**: {c.description}")

        if missing_critical:
            lines.append("\n### ⚠️ Missing Critical Integrations")
            for c in missing_critical:
                lines.append(f"- **{c.name}**: {c.description}")
                if c.documentation_url:
                    lines.append(f"  - Install: {c.documentation_url}")

        # Recommended companions
        recommended = [c for c in self._detected.values() if c.tier == IntegrationTier.RECOMMENDED]
        if recommended:
            lines.append("\n### 📦 Available Integrations")
            for c in recommended:
                lines.append(f"- **{c.name}**: {c.description}")

        # Optional companions
        optional = [c for c in self._detected.values() if c.tier == IntegrationTier.OPTIONAL]
        if optional:
            lines.append("\n### 🔧 Optional Integrations")
            for c in optional:
                lines.append(f"- **{c.name}**: {c.description}")

        return "\n".join(lines)
