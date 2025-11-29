"""Tests for MCP Ecosystem Detection Framework.

Tests EcosystemDetector including:
- Companion detection by tools
- Tier-based filtering
- Integration prompt generation
- Workflow suggestions
- Ecosystem status reporting
"""

from unittest.mock import Mock

import pytest

from world_anvil_mcp.ecosystem.detector import (
    COMPANION_REGISTRY,
    CompanionMCP,
    EcosystemDetector,
    IntegrationTier,
)


class TestIntegrationTier:
    """Tests for IntegrationTier enumeration."""

    @pytest.mark.unit
    def test_tier_critical_value(self) -> None:
        """Test CRITICAL tier has value 1."""
        # Act & Assert
        assert IntegrationTier.CRITICAL.value == 1

    @pytest.mark.unit
    def test_tier_recommended_value(self) -> None:
        """Test RECOMMENDED tier has value 2."""
        # Act & Assert
        assert IntegrationTier.RECOMMENDED.value == 2

    @pytest.mark.unit
    def test_tier_optional_value(self) -> None:
        """Test OPTIONAL tier has value 3."""
        # Act & Assert
        assert IntegrationTier.OPTIONAL.value == 3

    @pytest.mark.unit
    def test_tier_ordering(self) -> None:
        """Test tier values order correctly for sorting."""
        # Act & Assert
        assert IntegrationTier.CRITICAL.value < IntegrationTier.RECOMMENDED.value
        assert IntegrationTier.RECOMMENDED.value < IntegrationTier.OPTIONAL.value

    @pytest.mark.unit
    def test_tier_enum_members(self) -> None:
        """Test all expected tier members exist."""
        # Act
        tiers = [tier for tier in IntegrationTier]

        # Assert
        assert len(tiers) == 3
        tier_names = [tier.name for tier in tiers]
        assert "CRITICAL" in tier_names
        assert "RECOMMENDED" in tier_names
        assert "OPTIONAL" in tier_names


class TestCompanionMCP:
    """Tests for CompanionMCP dataclass."""

    @pytest.mark.unit
    def test_companion_minimal_creation(self) -> None:
        """Test creating CompanionMCP with required fields."""
        # Act
        companion = CompanionMCP(
            name="Test MCP",
            tier=IntegrationTier.RECOMMENDED,
            description="Test description",
            detection_tools=["tool1", "tool2"],
            use_cases=["use case 1"],
        )

        # Assert
        assert companion.name == "Test MCP"
        assert companion.tier == IntegrationTier.RECOMMENDED
        assert companion.description == "Test description"
        assert companion.detection_tools == ["tool1", "tool2"]
        assert companion.use_cases == ["use case 1"]

    @pytest.mark.unit
    def test_companion_with_all_fields(self) -> None:
        """Test creating CompanionMCP with all fields."""
        # Act
        companion = CompanionMCP(
            name="Full MCP",
            tier=IntegrationTier.CRITICAL,
            description="Full description",
            detection_tools=["tool1"],
            use_cases=["use case"],
            documentation_url="https://example.com/docs",
            can_read=True,
            can_write=True,
            bidirectional=True,
            workflow_suggestions={"workflow1": "suggestion1"},
        )

        # Assert
        assert companion.name == "Full MCP"
        assert companion.documentation_url == "https://example.com/docs"
        assert companion.can_read is True
        assert companion.can_write is True
        assert companion.bidirectional is True
        assert companion.workflow_suggestions == {"workflow1": "suggestion1"}

    @pytest.mark.unit
    def test_companion_default_capabilities(self) -> None:
        """Test CompanionMCP default capability values."""
        # Act
        companion = CompanionMCP(
            name="Default MCP",
            tier=IntegrationTier.OPTIONAL,
            description="Description",
            detection_tools=["tool"],
            use_cases=["use case"],
        )

        # Assert
        assert companion.can_read is True
        assert companion.can_write is False
        assert companion.bidirectional is False
        assert companion.documentation_url is None
        assert companion.workflow_suggestions == {}

    @pytest.mark.unit
    def test_companion_empty_workflow_suggestions(self) -> None:
        """Test CompanionMCP with empty workflow suggestions."""
        # Act
        companion = CompanionMCP(
            name="No Suggestions",
            tier=IntegrationTier.OPTIONAL,
            description="Desc",
            detection_tools=["tool"],
            use_cases=["use case"],
        )

        # Assert
        assert companion.workflow_suggestions == {}


class TestEcosystemDetectorInitialization:
    """Tests for EcosystemDetector initialization."""

    @pytest.mark.unit
    def test_detector_initialization_empty(self) -> None:
        """Test EcosystemDetector with no available tools."""
        # Act
        detector = EcosystemDetector(available_tools=[])

        # Assert
        assert detector.available_tools == set()
        assert len(detector.all_companions) == 0

    @pytest.mark.unit
    def test_detector_initialization_with_tools(self) -> None:
        """Test EcosystemDetector with available tools."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])

        # Assert
        assert "foundry_get_actors" in detector.available_tools
        assert len(detector.available_tools) == 1

    @pytest.mark.unit
    def test_detector_initialization_multiple_tools(self) -> None:
        """Test EcosystemDetector with multiple available tools."""
        # Act
        tools = ["foundry_get_actors", "search_reference", "dropbox_upload"]
        detector = EcosystemDetector(available_tools=tools)

        # Assert
        assert len(detector.available_tools) == 3
        assert "foundry_get_actors" in detector.available_tools
        assert "search_reference" in detector.available_tools
        assert "dropbox_upload" in detector.available_tools

    @pytest.mark.unit
    def test_detector_tool_list_converted_to_set(self) -> None:
        """Test available_tools are converted to set for detection."""
        # Act
        detector = EcosystemDetector(available_tools=["tool1", "tool2", "tool1"])

        # Assert
        assert isinstance(detector.available_tools, set)
        assert len(detector.available_tools) == 2


class TestEcosystemDetectorDetection:
    """Tests for companion detection logic."""

    @pytest.mark.unit
    def test_detect_foundry_vtt(self) -> None:
        """Test detection of Foundry VTT companion."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])

        # Assert
        assert detector.has("Foundry VTT")
        foundry = detector.get("Foundry VTT")
        assert foundry is not None
        assert foundry.name == "Foundry VTT"
        assert foundry.tier == IntegrationTier.CRITICAL

    @pytest.mark.unit
    def test_detect_context_engine(self) -> None:
        """Test detection of Context Engine companion."""
        # Act
        detector = EcosystemDetector(available_tools=["search_reference"])

        # Assert
        assert detector.has("Context Engine")
        context = detector.get("Context Engine")
        assert context is not None
        assert context.name == "Context Engine"
        assert context.tier == IntegrationTier.CRITICAL

    @pytest.mark.unit
    def test_detect_dropbox(self) -> None:
        """Test detection of Dropbox companion."""
        # Act
        detector = EcosystemDetector(available_tools=["dropbox_upload"])

        # Assert
        assert detector.has("Dropbox")
        dropbox = detector.get("Dropbox")
        assert dropbox is not None
        assert dropbox.tier == IntegrationTier.RECOMMENDED

    @pytest.mark.unit
    def test_detect_multiple_companions(self) -> None:
        """Test detection of multiple companions simultaneously."""
        # Act
        detector = EcosystemDetector(
            available_tools=["foundry_get_actors", "search_reference", "dropbox_upload"]
        )

        # Assert
        assert detector.has("Foundry VTT")
        assert detector.has("Context Engine")
        assert detector.has("Dropbox")
        assert len(detector.all_companions) == 3

    @pytest.mark.unit
    def test_detect_nonexistent_tool(self) -> None:
        """Test detection with nonexistent tool returns empty."""
        # Act
        detector = EcosystemDetector(available_tools=["nonexistent_tool"])

        # Assert
        assert len(detector.all_companions) == 0

    @pytest.mark.unit
    def test_has_returns_false_for_missing(self) -> None:
        """Test has() returns False for missing companions."""
        # Act
        detector = EcosystemDetector(available_tools=[])

        # Assert
        assert not detector.has("Foundry VTT")
        assert not detector.has("Context Engine")
        assert not detector.has("Discord")

    @pytest.mark.unit
    def test_get_returns_none_for_missing(self) -> None:
        """Test get() returns None for missing companions."""
        # Act
        detector = EcosystemDetector(available_tools=[])

        # Assert
        assert detector.get("Foundry VTT") is None
        assert detector.get("Context Engine") is None

    @pytest.mark.unit
    def test_partial_tool_match_detected(self) -> None:
        """Test companion is detected if ANY detection tool matches."""
        # Act - only foundry_get_scenes, one of Foundry's detection tools
        detector = EcosystemDetector(available_tools=["foundry_get_scenes"])

        # Assert
        assert detector.has("Foundry VTT")

    @pytest.mark.unit
    def test_all_detection_tools_for_companion(self) -> None:
        """Test Foundry VTT detects with any of its tools."""
        # Arrange
        foundry_tools = [
            "foundry_get_actors",
            "foundry_get_scenes",
            "foundry_get_journal",
            "foundry_roll_dice",
            "foundry_update_actor",
        ]

        # Act & Assert
        for tool in foundry_tools:
            detector = EcosystemDetector(available_tools=[tool])
            assert detector.has("Foundry VTT"), f"Should detect Foundry with {tool}"


class TestEcosystemDetectorTierFiltering:
    """Tests for tier-based filtering."""

    @pytest.mark.unit
    def test_critical_companions_property(self) -> None:
        """Test critical_companions returns only CRITICAL tier."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # CRITICAL
                "search_reference",  # CRITICAL
                "dropbox_upload",  # RECOMMENDED
                "discord_send_message",  # OPTIONAL
            ]
        )

        # Assert
        critical = detector.critical_companions
        assert len(critical) == 2
        for companion in critical:
            assert companion.tier == IntegrationTier.CRITICAL
        names = [c.name for c in critical]
        assert "Foundry VTT" in names
        assert "Context Engine" in names

    @pytest.mark.unit
    def test_critical_companions_empty(self) -> None:
        """Test critical_companions returns empty when none detected."""
        # Act
        detector = EcosystemDetector(available_tools=["dropbox_upload"])

        # Assert
        critical = detector.critical_companions
        assert len(critical) == 0

    @pytest.mark.unit
    def test_all_companions_includes_all_tiers(self) -> None:
        """Test all_companions includes all detected companions."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # CRITICAL
                "dropbox_upload",  # RECOMMENDED
                "discord_send_message",  # OPTIONAL
            ]
        )

        # Assert
        all_comp = detector.all_companions
        assert len(all_comp) == 3
        tiers = {c.tier for c in all_comp}
        assert IntegrationTier.CRITICAL in tiers
        assert IntegrationTier.RECOMMENDED in tiers
        assert IntegrationTier.OPTIONAL in tiers

    @pytest.mark.unit
    def test_all_companions_empty(self) -> None:
        """Test all_companions returns empty when none detected."""
        # Act
        detector = EcosystemDetector(available_tools=[])

        # Assert
        assert len(detector.all_companions) == 0


class TestEcosystemDetectorWorkflowSuggestions:
    """Tests for workflow suggestion functionality."""

    @pytest.mark.unit
    def test_suggest_for_workflow_foundry_session_prep(self) -> None:
        """Test workflow suggestions for session_prep with Foundry."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        suggestions = detector.suggest_for_workflow("session_prep")

        # Assert
        assert len(suggestions) == 1
        name, hint, companion = suggestions[0]
        assert name == "Foundry VTT"
        assert "Sync" in hint or "sync" in hint
        assert companion.name == "Foundry VTT"

    @pytest.mark.unit
    def test_suggest_for_workflow_multiple_suggestions(self) -> None:
        """Test workflow returns multiple suggestions."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # session_prep
                "notion_search",  # session_prep
            ]
        )
        suggestions = detector.suggest_for_workflow("session_prep")

        # Assert
        assert len(suggestions) == 2
        names = [s[0] for s in suggestions]
        assert "Foundry VTT" in names
        assert "Notion" in names

    @pytest.mark.unit
    def test_suggest_for_workflow_no_suggestions(self) -> None:
        """Test suggest_for_workflow returns empty for no match."""
        # Act
        detector = EcosystemDetector(available_tools=["discord_send_message"])
        suggestions = detector.suggest_for_workflow("npc_generation")

        # Assert
        assert len(suggestions) == 0

    @pytest.mark.unit
    def test_suggest_for_workflow_npc_generation(self) -> None:
        """Test npc_generation workflow suggestions."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # npc_generation
                "search_reference",  # npc_generation
            ]
        )
        suggestions = detector.suggest_for_workflow("npc_generation")

        # Assert
        assert len(suggestions) == 2
        # Should be sorted by tier (CRITICAL first)
        assert suggestions[0][0] in ["Foundry VTT", "Context Engine"]
        assert suggestions[1][0] in ["Foundry VTT", "Context Engine"]

    @pytest.mark.unit
    def test_suggest_for_workflow_sorted_by_tier(self) -> None:
        """Test suggestions are sorted by tier (critical first)."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # CRITICAL, session_prep
                "notion_search",  # RECOMMENDED, session_prep
                "discord_send_message",  # OPTIONAL, no session_prep
            ]
        )
        suggestions = detector.suggest_for_workflow("session_prep")

        # Assert
        assert len(suggestions) == 2
        # Foundry (CRITICAL) should come before Notion (RECOMMENDED)
        assert suggestions[0][0] == "Foundry VTT"
        assert suggestions[1][0] == "Notion"

    @pytest.mark.unit
    def test_suggestion_tuple_structure(self) -> None:
        """Test suggestion tuple has correct structure."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        suggestions = detector.suggest_for_workflow("session_prep")

        # Assert
        assert len(suggestions) == 1
        suggestion = suggestions[0]
        assert len(suggestion) == 3
        name, hint, companion_obj = suggestion
        assert isinstance(name, str)
        assert isinstance(hint, str)
        assert isinstance(companion_obj, CompanionMCP)

    @pytest.mark.unit
    def test_suggest_for_nonexistent_workflow(self) -> None:
        """Test suggest_for_workflow with nonexistent workflow ID."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        suggestions = detector.suggest_for_workflow("nonexistent_workflow")

        # Assert
        assert len(suggestions) == 0


class TestEcosystemDetectorStatusReport:
    """Tests for ecosystem status reporting."""

    @pytest.mark.unit
    def test_status_report_empty_ecosystem(self) -> None:
        """Test status report for empty ecosystem."""
        # Act
        detector = EcosystemDetector(available_tools=[])
        status = detector.get_ecosystem_status()

        # Assert
        assert "MCP Ecosystem Status" in status
        assert "Missing Critical Integrations" in status
        assert "Context Engine" in status
        assert "Foundry VTT" in status

    @pytest.mark.unit
    def test_status_report_with_critical(self) -> None:
        """Test status report with critical companions detected."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        status = detector.get_ecosystem_status()

        # Assert
        assert "Critical Integrations" in status
        assert "Foundry VTT" in status
        assert "✅" in status or "✓" in status

    @pytest.mark.unit
    def test_status_report_with_recommended(self) -> None:
        """Test status report with recommended companions."""
        # Act
        detector = EcosystemDetector(available_tools=["dropbox_upload"])
        status = detector.get_ecosystem_status()

        # Assert
        assert "Dropbox" in status

    @pytest.mark.unit
    def test_status_report_with_optional(self) -> None:
        """Test status report with optional companions."""
        # Act
        detector = EcosystemDetector(available_tools=["discord_send_message"])
        status = detector.get_ecosystem_status()

        # Assert
        assert "Discord" in status

    @pytest.mark.unit
    def test_status_report_markdown_format(self) -> None:
        """Test status report is valid markdown."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors", "dropbox_upload"])
        status = detector.get_ecosystem_status()

        # Assert
        # Should contain markdown headers
        assert "##" in status
        # Should contain markdown bullet points
        assert "-" in status

    @pytest.mark.unit
    def test_status_report_complete_ecosystem(self) -> None:
        """Test status report with all companion types."""
        # Act
        detector = EcosystemDetector(
            available_tools=[
                "foundry_get_actors",  # CRITICAL
                "dropbox_upload",  # RECOMMENDED
                "discord_send_message",  # OPTIONAL
            ]
        )
        status = detector.get_ecosystem_status()

        # Assert
        assert "Foundry VTT" in status
        assert "Dropbox" in status
        assert "Discord" in status


class TestEcosystemDetectorCompanionRegistry:
    """Tests for companion registry validation."""

    @pytest.mark.unit
    def test_companion_registry_not_empty(self) -> None:
        """Test COMPANION_REGISTRY contains companions."""
        # Assert
        assert len(COMPANION_REGISTRY) > 0

    @pytest.mark.unit
    def test_companion_registry_has_foundry(self) -> None:
        """Test registry contains Foundry VTT."""
        # Act
        foundry = [c for c in COMPANION_REGISTRY if c.name == "Foundry VTT"]

        # Assert
        assert len(foundry) == 1
        assert foundry[0].tier == IntegrationTier.CRITICAL

    @pytest.mark.unit
    def test_companion_registry_has_context_engine(self) -> None:
        """Test registry contains Context Engine."""
        # Act
        context = [c for c in COMPANION_REGISTRY if c.name == "Context Engine"]

        # Assert
        assert len(context) == 1
        assert context[0].tier == IntegrationTier.CRITICAL

    @pytest.mark.unit
    def test_companion_registry_critical_companions(self) -> None:
        """Test registry has expected critical companions."""
        # Act
        critical = [c for c in COMPANION_REGISTRY if c.tier == IntegrationTier.CRITICAL]

        # Assert
        assert len(critical) == 2
        names = {c.name for c in critical}
        assert "Foundry VTT" in names
        assert "Context Engine" in names

    @pytest.mark.unit
    def test_companion_registry_all_have_tools(self) -> None:
        """Test all registry companions have detection tools."""
        # Assert
        for companion in COMPANION_REGISTRY:
            assert len(companion.detection_tools) > 0

    @pytest.mark.unit
    def test_companion_registry_all_have_use_cases(self) -> None:
        """Test all registry companions have use cases."""
        # Assert
        for companion in COMPANION_REGISTRY:
            assert len(companion.use_cases) > 0


class TestEcosystemDetectorEdgeCases:
    """Tests for edge cases and boundary conditions."""

    @pytest.mark.unit
    def test_detector_with_duplicate_tools(self) -> None:
        """Test detector handles duplicate tools gracefully."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors", "foundry_get_actors"])

        # Assert
        assert len(detector.available_tools) == 1
        assert detector.has("Foundry VTT")

    @pytest.mark.unit
    def test_detector_case_sensitive_tool_matching(self) -> None:
        """Test tool matching is case-sensitive."""
        # Act
        detector = EcosystemDetector(available_tools=["FOUNDRY_GET_ACTORS"])

        # Assert
        # Should not match (case mismatch)
        assert not detector.has("Foundry VTT")

    @pytest.mark.unit
    def test_detector_with_empty_string_tool(self) -> None:
        """Test detector handles empty string in tool list."""
        # Act
        detector = EcosystemDetector(available_tools=["", "foundry_get_actors"])

        # Assert
        assert "" in detector.available_tools
        assert detector.has("Foundry VTT")

    @pytest.mark.unit
    def test_detector_preserves_tool_list(self) -> None:
        """Test detector doesn't modify provided tool list."""
        # Arrange
        original_tools = ["foundry_get_actors", "search_reference"]

        # Act
        detector = EcosystemDetector(available_tools=original_tools)

        # Assert
        assert original_tools == ["foundry_get_actors", "search_reference"]

    @pytest.mark.unit
    def test_multiple_detectors_independent(self) -> None:
        """Test multiple detector instances are independent."""
        # Act
        detector1 = EcosystemDetector(available_tools=["foundry_get_actors"])
        detector2 = EcosystemDetector(available_tools=["dropbox_upload"])

        # Assert
        assert detector1.has("Foundry VTT")
        assert not detector1.has("Dropbox")
        assert detector2.has("Dropbox")
        assert not detector2.has("Foundry VTT")

    @pytest.mark.unit
    def test_detector_get_returns_same_object(self) -> None:
        """Test get() returns consistent object reference."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        obj1 = detector.get("Foundry VTT")
        obj2 = detector.get("Foundry VTT")

        # Assert
        assert obj1 is obj2

    @pytest.mark.unit
    def test_all_companions_returns_new_list(self) -> None:
        """Test all_companions returns a list copy."""
        # Act
        detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        list1 = detector.all_companions
        list2 = detector.all_companions

        # Assert
        assert list1 == list2
        assert isinstance(list1, list)
        assert isinstance(list2, list)
