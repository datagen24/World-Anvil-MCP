# World Anvil MCP Server - Workflow Documentation

**Version**: 1.0  
**Phase**: 0.2 - Example Workflows  
**Status**: Complete

---

## Overview

This document defines user workflows for the World Anvil MCP Server, mapping natural language interactions to MCP tool invocations for D&D campaign management and worldbuilding.

---

## Workflow Summary

| ID | Workflow | Category | Complexity | Description |
|----|----------|----------|------------|-------------|
| WF-001 | Campaign Setup | Campaign Mgmt | Medium | Initialize D&D campaign structure |
| WF-002 | Session Notes | Campaign Mgmt | High | Real-time note capture during play |
| WF-003 | NPC Generation | Content Creation | Medium | Create integrated NPCs |
| WF-004 | Location Dev | World Building | Medium | Develop settlements/dungeons |
| WF-005 | Quick NPC Lookup | Session Support | Low | Fast NPC reference during play |
| WF-006 | World Building | Content Creation | High | Lore, cultures, factions |
| WF-007 | Map Management | Organization | Medium | Geographic queries and travel |
| WF-008 | Quest/Plot Mgmt | Campaign Mgmt | Medium | Story thread tracking |
| WF-009 | Session Prep | Campaign Mgmt | High | Pre-session preparation |
| WF-010 | Content Search | Info Retrieval | Low | Find world content |

---

## Workflow Details

### WF-001: D&D Campaign Setup

**Purpose**: Set up a new D&D campaign with proper category structure

**Trigger Phrases**:
- "Set up a new D&D campaign"
- "Create a campaign for [name]"
- "Initialize my World Anvil for D&D"

**MCP Tools Used**:
```
list_worlds → get_world → list_categories
```

**Example Flow**:
```
User: Set up a new D&D 5e campaign called "Storm King's Thunder"

Claude: [list_worlds] → Shows available worlds
        [get_world] → Loads selected world details
        [list_categories] → Shows current structure
        
        Recommends category organization for D&D play
```

---

### WF-002: Session Note-Taking

**Purpose**: Capture session notes during live play without disrupting flow

**Trigger Phrases**:
- "Start session notes"
- "Log this encounter"
- "Note that the party met [NPC]"

**MCP Tools Used**:
```
get_world → list_articles → search_articles → get_article
```

**Real-Time Pattern**:
```
User: The party met an elf named Silvanus at the temple

Claude: [search_articles: "Silvanus"]
        📝 Noted: Party met Silvanus (elf) at temple
        Not in world yet - flagged for article creation
```

---

### WF-003: NPC Generation

**Purpose**: Create well-developed NPCs integrated with world content

**Trigger Phrases**:
- "Create an NPC"
- "I need a [role] NPC"
- "Make a shopkeeper for [location]"

**MCP Tools Used**:
```
search_articles → get_article → list_articles (for connections)
```

**Output Format**:
```markdown
# [NPC Name]
## Overview
## Appearance  
## Personality
## Motivations
## Connections (linked to existing content)
## Secrets (DM only)
```

---

### WF-004: Location Development

**Purpose**: Develop locations with gameplay-relevant details

**Trigger Phrases**:
- "Develop [location]"
- "Build out this town"
- "What's in [location]?"

**MCP Tools Used**:
```
search_articles → get_article → list_articles
```

**Output Types**:
- Full Settlement: Districts, NPCs, economy, government
- Session Focused: Just what party will encounter
- Adventure Site: Encounter zones, treasure, hazards

---

### WF-005: Quick NPC Lookup

**Purpose**: Instant NPC retrieval during active sessions

**Trigger Phrases**:
- "Who is [name]?"
- "Quick info on [NPC]"
- "Remind me about [character]"

**MCP Tools Used**:
```
search_articles → get_article
```

**Response Format** (optimized for speed):
```
📋 [NAME]
Race: X | Role: Y
PERSONALITY: [Key traits]
VOICE: [Speech pattern]
QUICK FACTS: [Bullet points]
```

**Target Response Time**: < 2 seconds

---

### WF-006: World Building

**Purpose**: Systematic lore and culture development

**Trigger Phrases**:
- "Help me worldbuild"
- "Develop the lore for [topic]"
- "Create a culture/religion"

**MCP Tools Used**:
```
get_world → list_articles → search_articles → get_article
```

**Topics Covered**:
- Pantheons and religions
- Cultures and societies
- Historical eras
- Magic systems
- Political factions

---

### WF-007: Map Management

**Purpose**: Geographic queries and travel planning

**Trigger Phrases**:
- "What's near [location]?"
- "Travel from [A] to [B]"
- "Show map pins in [area]"

**MCP Tools Used**:
```
list_maps → get_map → get_map_markers → get_article
```

**Capabilities**:
- Nearby location queries
- Travel time calculation
- Encounter zone mapping
- Pin/marker queries

---

### WF-008: Quest/Plot Management

**Purpose**: Track campaign storylines and quest progress

**Trigger Phrases**:
- "What quests are active?"
- "Update quest [name]"
- "Track this plot thread"

**MCP Tools Used**:
```
list_articles (Plot template) → get_article → search_articles
```

**Quest Status Types**:
- 🔘 Available
- 🔷 Active
- 🔶 On Hold
- ✅ Completed
- ❌ Failed
- ⬜ Abandoned

---

### WF-009: Session Prep

**Purpose**: Prepare materials for upcoming sessions

**Trigger Phrases**:
- "Help me prep for session [N]"
- "Prepare materials for [event]"
- "What do I need for next session?"

**MCP Tools Used**:
```
get_world → list_articles → get_article → search_articles
```

**Prep Package Includes**:
- Last session recap
- Party status and location
- Active quest threads
- NPC quick sheets
- Encounter preparations
- Session checklist

---

### WF-010: Content Search

**Purpose**: Find specific content within the world

**Trigger Phrases**:
- "Find [content]"
- "Search for [term]"
- "List all [category]"

**MCP Tools Used**:
```
search_articles → list_articles → get_article → list_categories
```

**Search Types**:
- Name search (exact match)
- Topic search (keyword)
- Category browse
- Template filter
- Tag search
- Connection traversal

---

## MCP Tool Requirements

### Phase 1 (Core)
| Tool | Type | Priority |
|------|------|----------|
| `list_worlds` | Read | Core |
| `get_world` | Read | Core |
| `list_articles` | Read | Core |
| `get_article` | Read | Core |
| `list_categories` | Read | Core |
| `get_category` | Read | Core |

### Phase 2 (Enhanced)
| Tool | Type | Priority |
|------|------|----------|
| `search_articles` | Read | High |
| `list_maps` | Read | High |
| `get_map` | Read | High |
| `get_map_markers` | Read | High |

### Phase 3 (Campaign)
| Tool | Type | Priority |
|------|------|----------|
| `get_campaign` | Read | Medium |
| `list_campaign_npcs` | Read | Medium |
| `get_campaign_npc` | Read | Medium |

### Future (Write API)
| Tool | Type | Priority |
|------|------|----------|
| `create_article` | Write | Critical |
| `update_article` | Write | High |
| `create_category` | Write | Medium |

---

## Design Principles

1. **Progressive Disclosure**: Quick summaries first, details on request
2. **Context Preservation**: Maintain session state across interactions
3. **Graceful Degradation**: Handle missing content, suggest alternatives
4. **Speed Priority**: Session-time responses must be fast
5. **DM-First Design**: Optimize for running games, separate player/DM info

---

## Related Documentation

- [Design Specification](DESIGN_SPECIFICATION.md) - Architecture and design
- [API Reference](API_REFERENCE.md) - Tool and resource documentation
- [Usage Examples](USAGE_EXAMPLES.md) - Common usage patterns

---

## Detailed Workflow Files

Complete workflow documentation with examples available in:
```
docs/workflows/
├── README.md                    # Workflow index
├── d-and-d-campaign-setup.md    # WF-001
├── session-note-taking.md       # WF-002
├── npc-generation.md            # WF-003
├── location-development.md      # WF-004
├── quick-npc-lookup.md          # WF-005
├── world-building.md            # WF-006
├── map-management.md            # WF-007
├── quest-plot-management.md     # WF-008
├── session-prep.md              # WF-009
└── content-search.md            # WF-010
```

