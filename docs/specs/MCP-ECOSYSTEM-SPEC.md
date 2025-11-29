# MCP Ecosystem Integration Specification

**Version**: 1.0  
**Status**: Draft  
**Created**: 2025-11-28  
**Purpose**: Define companion MCP integrations that enhance World Anvil workflows

---

## Executive Summary

The World Anvil MCP operates within a broader ecosystem of tools that together form a complete TTRPG worldbuilding and gameplay platform. Rather than reimplementing functionality, we detect and compose with companion MCPs to create powerful workflows.

**Core Principle**: World Anvil is the **canonical source of truth** for world content. Companion tools handle execution, storage, and reference - they consume from or enhance World Anvil, never replace it.

---

## Ecosystem Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MCP Ecosystem                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────┐      ┌──────────────────┐                     │
│  │  Context Engine  │      │   World Anvil    │                     │
│  │  (Reference)     │─────▶│   (Canonical)    │                     │
│  │                  │      │                  │                     │
│  │  • D&D SRD       │      │  • Articles      │                     │
│  │  • Genre Lore    │      │  • Maps          │                     │
│  │  • Historical    │      │  • Timelines     │                     │
│  │  • Custom Corpus │      │  • Campaigns     │                     │
│  └──────────────────┘      └────────┬─────────┘                     │
│                                     │                                │
│                                     │ Sync/Export                    │
│                                     ▼                                │
│                            ┌──────────────────┐                     │
│                            │   Foundry VTT    │                     │
│                            │   (Execution)    │                     │
│                            │                  │                     │
│                            │  • Live Play     │                     │
│                            │  • Combat        │                     │
│                            │  • Character     │                     │
│                            │    Sheets        │                     │
│                            └──────────────────┘                     │
│                                                                      │
│  ┌──────────────────┐      ┌──────────────────┐                     │
│  │     Dropbox      │      │     Notion       │                     │
│  │    (Storage)     │      │   (Planning)     │                     │
│  │                  │      │                  │                     │
│  │  • Maps/Images   │      │  • Session Prep  │                     │
│  │  • Handouts      │      │  • Player Notes  │                     │
│  │  • Audio         │      │  • Meta Tasks    │                     │
│  │  • Backups       │      │  • Scheduling    │                     │
│  └──────────────────┘      └──────────────────┘                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Integration Tiers

### Tier 1: Critical (Must Detect)

| Integration | Role | Why Critical |
|-------------|------|--------------|
| **Foundry VTT** | Gameplay Execution | Native WA integration; actual play happens here |
| **Context Engine** | Reference & Inspiration | Enables informed worldbuilding |

### Tier 2: Recommended (Should Detect)

| Integration | Role | Why Recommended |
|-------------|------|-----------------|
| **Dropbox** | Asset Storage | Maps, handouts, audio files |
| **Notion** | Meta-Planning | Session prep, player coordination |

### Tier 3: Optional (May Detect)

| Integration | Role | Notes |
|-------------|------|-------|
| **Discord** | Communication | Session announcements |
| **Calendar** | Scheduling | Session booking |
| **Obsidian** | Personal Notes | Some users prefer local-first |

---

## Integration Specifications

### 1. Foundry VTT Integration

**Priority**: Tier 1 - Critical  
**Type**: Bidirectional Sync  
**MCP Bridge**: https://foundryvtt.com/packages/foundry-mcp-bridge  
**API**: https://foundryvtt.com/api/

#### Why Foundry?

1. **Native World Anvil Integration**: Foundry has built-in WA import
2. **Execution Layer**: Where actual gameplay happens
3. **Character Sheets**: Live character data during play
4. **Combat Tracker**: Real-time encounter management
5. **Scene Management**: Maps with tokens, lighting, walls

#### Detection

```python
FOUNDRY_DETECTION_TOOLS = [
    "foundry_get_actors",
    "foundry_get_scenes", 
    "foundry_get_journal",
    "foundry_roll_dice",
    "foundry_update_actor",
    "foundry_create_journal_entry",
]
```

#### Integration Points

| World Anvil | Direction | Foundry VTT | Use Case |
|-------------|-----------|-------------|----------|
| Character Article | → | Actor | NPC import to Foundry |
| Location Article | → | Scene | Map with description |
| Session Report | ← | Chat Log | Session transcript |
| Item Article | → | Item | Magic item with stats |
| Organization | → | Journal Entry | Faction reference |

#### Workflows Enabled

**Pre-Session Sync**:
```
1. User: "Prepare Foundry for tonight's session in Phandalin"
2. World Anvil MCP: Load Phandalin article, NPCs, current quests
3. Foundry MCP: Create/update Journal entries, verify actors exist
4. Result: Foundry ready with current WA content
```

**Post-Session Capture**:
```
1. User: "Log tonight's session from Foundry"
2. Foundry MCP: Extract chat log, combat summaries, dice rolls
3. World Anvil MCP: Create Session Report article
4. Result: Session documented in canonical source
```

**Live Play Support**:
```
1. User: "What do I know about this NPC?" (during Foundry session)
2. Foundry MCP: Identify current scene/actor context
3. World Anvil MCP: Retrieve full article with secrets
4. Result: DM gets full context without leaving VTT
```

#### Data Mapping

```yaml
# World Anvil → Foundry Type Mapping
character_article:
  foundry_type: Actor
  fields:
    name: name
    description: biography
    portrait: img
    # Stats require RPG system-specific mapping

location_article:
  foundry_type: Scene
  fields:
    name: name
    description: notes
    map_image: background.src

item_article:
  foundry_type: Item
  fields:
    name: name
    description: description
    # D&D 5e specific fields...

organization_article:
  foundry_type: JournalEntry
  fields:
    name: name
    content: content_parsed
```

---

### 2. Context Engine Integration

**Priority**: Tier 1 - Critical  
**Type**: Reference Provider  
**Status**: New MCP Required  
**Full Specification**: See `CONTEXT-ENGINE-SPEC.md`

#### Purpose

The Context Engine provides **semantic search over reference materials** that inform worldbuilding. This is NOT World Anvil content - it's external knowledge that helps CREATE World Anvil content.

#### Why Critical?

1. **Semantic Search**: Find conceptually related content, not just keyword matches
2. **Curated Corpus**: Controlled, legal reference materials (SRD, public domain)
3. **Domain Expertise**: TTRPG, fantasy, historical knowledge
4. **Inspiration Generation**: "NPCs like X" or "Locations similar to Y"

#### Key Tools

| Tool | Purpose |
|------|---------|
| `search_reference` | Semantic search across corpora |
| `get_srd_content` | Direct SRD lookup (monsters, spells, etc.) |
| `find_similar` | Find content similar to provided text |
| `get_inspiration` | Contextual inspiration for content creation |
| `generate_names` | Culturally appropriate name generation |

#### Corpora (Pre-loaded)

| Corpus | Content |
|--------|---------|
| `dnd5e_srd` | D&D 5e System Reference Document |
| `pathfinder2e_srd` | Pathfinder 2e SRD |
| `fantasy_tropes` | Genre conventions and archetypes |
| `medieval_history` | Historical reference (feudal society, warfare) |
| `mythology_public` | Public domain myths and legends |
| `naming_patterns` | Cultural naming conventions |
| `user_*` | User-uploaded custom content |

#### Integration Pattern

```
1. User: "Create a dwarven blacksmith NPC"
2. World Anvil MCP: Checks existing world content
3. Context Engine MCP: 
   - Searches dwarven culture in SRD
   - Finds medieval blacksmith details
   - Gets fantasy profession tropes
4. World Anvil MCP: Creates informed NPC article
5. Result: Culturally consistent, lore-accurate NPC
```

#### Detection

```python
CONTEXT_ENGINE_DETECTION_TOOLS = [
    "search_reference",
    "get_srd_content",
    "find_similar",
    "get_inspiration",
    "generate_names",
]
```

> **Note**: Full technical specification including architecture, MCP interface, corpus details, and implementation roadmap in separate document.

---

### 3. Dropbox Integration

**Priority**: Tier 2 - Recommended  
**Type**: Asset Storage  
**MCP**: Standard Dropbox MCP (if available) or filesystem MCP

#### Purpose

Store and retrieve binary assets that complement World Anvil content:
- Battle maps (high-resolution images)
- Handout documents (PDFs, images)
- Audio files (ambient sounds, music)
- Backup exports

#### Detection

```python
DROPBOX_DETECTION_TOOLS = [
    "dropbox_upload",
    "dropbox_download",
    "dropbox_list_folder",
    "dropbox_search",
    "dropbox_get_link",
]
```

#### Integration Points

| World Anvil Content | Dropbox Asset | Link Type |
|---------------------|---------------|-----------|
| Location Article | Battle map image | Embed URL |
| Handout Document | PDF file | Share link |
| Session Report | Recording | Reference |
| World | Full backup | Archive |

#### Folder Structure Convention

```
/World Anvil/
├── {world_name}/
│   ├── Maps/
│   │   ├── Regional/
│   │   ├── City/
│   │   ├── Dungeon/
│   │   └── Battle/
│   ├── Handouts/
│   │   ├── Letters/
│   │   ├── Documents/
│   │   └── Images/
│   ├── Audio/
│   │   ├── Ambient/
│   │   └── Music/
│   └── Exports/
│       └── {date}_backup.zip
```

---

### 4. Notion Integration

**Priority**: Tier 2 - Recommended  
**Type**: Meta-Planning  
**MCP**: Official Notion MCP

#### Purpose

Handle planning and coordination that lives OUTSIDE the game world:
- Session preparation checklists
- Player availability tracking
- Campaign meta-notes (what's working, what isn't)
- Content creation backlog

#### Detection

```python
NOTION_DETECTION_TOOLS = [
    "notion_search",
    "notion_create_page",
    "notion_update_page",
    "notion_query_database",
    "notion_create_database",
]
```

#### Suggested Database Structure

**Campaign Tracker Database**:
```yaml
properties:
  - name: Session Number
    type: number
  - name: Date
    type: date
  - name: Status
    type: select
    options: [Planned, Prepped, Played, Logged]
  - name: World Anvil Session
    type: url  # Link to WA session report
  - name: Prep Checklist
    type: relation  # To prep items
  - name: Notes
    type: rich_text
```

**Content Backlog Database**:
```yaml
properties:
  - name: Content Type
    type: select
    options: [NPC, Location, Item, Quest, Lore]
  - name: Priority
    type: select
    options: [High, Medium, Low]
  - name: Status
    type: select
    options: [Idea, Drafting, In World Anvil, Done]
  - name: World Anvil Link
    type: url
  - name: Notes
    type: rich_text
```

#### Integration Workflow

```
1. User: "What do I need to prep for next session?"
2. Notion MCP: Query session tracker, get prep checklist
3. World Anvil MCP: Check content status for checklist items
4. Result: Unified prep status across both systems
```

---

## Detection Framework

### EcosystemDetector Implementation

```python
# src/world_anvil_mcp/ecosystem/detector.py
"""MCP Ecosystem Detection Framework."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class IntegrationTier(Enum):
    """Integration priority tiers."""
    CRITICAL = 1      # Must detect, enables core workflows
    RECOMMENDED = 2   # Should detect, enhances experience
    OPTIONAL = 3      # May detect, nice to have


@dataclass
class CompanionMCP:
    """Specification for a companion MCP integration."""
    
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
    # Tier 1: Critical
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
        description="Semantic search over TTRPG reference materials",
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
        documentation_url=None,  # Our own MCP
        can_read=True,
        can_write=True,  # User corpus
        workflow_suggestions={
            "npc_generation": "Search reference for cultural details",
            "world_building": "Find historical parallels",
            "location_development": "Get genre-appropriate inspiration",
        },
    ),
    
    # Tier 2: Recommended
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
    
    # Tier 3: Optional
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
    """Detects and manages companion MCP integrations."""
    
    def __init__(self, available_tools: list[str]) -> None:
        """Initialize detector with available tool names.
        
        Args:
            available_tools: List of tool names from MCP server context
        """
        self.available_tools = set(available_tools)
        self._detected: dict[str, CompanionMCP] = {}
        self._detect_all()
    
    def _detect_all(self) -> None:
        """Detect all available companion MCPs."""
        for companion in COMPANION_REGISTRY:
            if self._is_available(companion):
                self._detected[companion.name] = companion
    
    def _is_available(self, companion: CompanionMCP) -> bool:
        """Check if companion MCP is available."""
        return any(
            tool in self.available_tools 
            for tool in companion.detection_tools
        )
    
    @property
    def critical_companions(self) -> list[CompanionMCP]:
        """Get detected critical tier companions."""
        return [
            c for c in self._detected.values() 
            if c.tier == IntegrationTier.CRITICAL
        ]
    
    @property
    def all_companions(self) -> list[CompanionMCP]:
        """Get all detected companions."""
        return list(self._detected.values())
    
    def has(self, name: str) -> bool:
        """Check if specific companion is available."""
        return name in self._detected
    
    def get(self, name: str) -> CompanionMCP | None:
        """Get companion by name."""
        return self._detected.get(name)
    
    def suggest_for_workflow(
        self, 
        workflow: str,
    ) -> list[tuple[str, str, CompanionMCP]]:
        """Get integration suggestions for a workflow.
        
        Args:
            workflow: Workflow identifier
            
        Returns:
            List of (companion_name, suggestion, companion) tuples
        """
        suggestions = []
        for companion in self._detected.values():
            if workflow in companion.workflow_suggestions:
                suggestions.append((
                    companion.name,
                    companion.workflow_suggestions[workflow],
                    companion,
                ))
        
        # Sort by tier (critical first)
        suggestions.sort(key=lambda x: x[2].tier.value)
        return suggestions
    
    def get_ecosystem_status(self) -> str:
        """Generate markdown status report of ecosystem."""
        lines = ["## 🔌 MCP Ecosystem Status\n"]
        
        # Critical
        critical = [c for c in self._detected.values() 
                   if c.tier == IntegrationTier.CRITICAL]
        missing_critical = [c for c in COMPANION_REGISTRY 
                          if c.tier == IntegrationTier.CRITICAL 
                          and c.name not in self._detected]
        
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
        
        # Recommended
        recommended = [c for c in self._detected.values() 
                      if c.tier == IntegrationTier.RECOMMENDED]
        if recommended:
            lines.append("\n### 📦 Available Integrations")
            for c in recommended:
                lines.append(f"- **{c.name}**: {c.description}")
        
        # Optional
        optional = [c for c in self._detected.values() 
                   if c.tier == IntegrationTier.OPTIONAL]
        if optional:
            lines.append("\n### 🔧 Optional Integrations")
            for c in optional:
                lines.append(f"- **{c.name}**: {c.description}")
        
        return "\n".join(lines)
```

---

## Implementation Roadmap

### Phase 1.1: Detection Framework Only
- Implement `EcosystemDetector`
- Add to World Anvil MCP startup
- Log detected companions
- Include in status/diagnostic tools

### Phase 2.x: Foundry VTT Integration
- Define sync data models
- Implement bidirectional workflows
- Test with Foundry MCP Bridge

### Phase 3.x: Context Engine MCP
- Separate project: `context-engine-mcp`
- Core embedding infrastructure
- Initial corpus (D&D 5e SRD)
- Integration with World Anvil MCP

### Phase 4.x: Storage & Planning
- Dropbox integration (if MCP available)
- Notion integration patterns
- Cross-tool workflows

---

## Open Questions

1. **Context Engine Hosting**: Local embeddings vs cloud service?
   - Local: sentence-transformers, ChromaDB/FAISS
   - Cloud: OpenAI embeddings, Pinecone

2. **Corpus Licensing**: Which content can we legally include?
   - SRD: Clear (OGL/CC)
   - Historical: Mostly safe (public domain)
   - User content: User's responsibility

3. **Foundry VTT MCP Bridge**: Is it actively maintained? Capabilities?

4. **Sync Conflict Resolution**: When WA and Foundry diverge, which wins?
   - Proposal: WA is canonical, Foundry pulls from WA

---

## Appendix: Tool Detection Reference

### How to Get Available Tools

```python
# In MCP server initialization
from mcp.server import Server

server = Server("world-anvil")

@server.list_tools()
async def list_tools():
    # This is called by client to discover tools
    # We can also introspect what other tools exist
    pass

# Detection happens at runtime when we can query
# the MCP host for available tools from other servers
```

### MCP Host Query Pattern

The exact mechanism for querying other MCPs depends on the host (Claude Desktop, etc.), but typically involves checking the tool registry or making capability queries.

---

## References

- [Foundry VTT API](https://foundryvtt.com/api/)
- [Foundry MCP Bridge](https://foundryvtt.com/packages/foundry-mcp-bridge)
- [World Anvil Foundry Integration](https://www.worldanvil.com/learn/rpg/foundry-vtt)
- [D&D 5e SRD](https://dnd.wizards.com/resources/systems-reference-document)
- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://www.trychroma.com/)
