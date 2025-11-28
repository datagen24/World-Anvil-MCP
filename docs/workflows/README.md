# World Anvil MCP Server - Workflow Documentation Index

**Phase**: 0.2 - Example Workflows  
**Status**: Complete  
**Date**: 2025-11-28

---

## Overview

This documentation captures user workflows for the World Anvil MCP Server, mapping natural language interactions to MCP tool invocations for D&D campaign management.

---

## Workflow Inventory

| ID | Name | Category | Complexity | Status |
|----|------|----------|------------|--------|
| WF-001 | [D&D Campaign Setup](d-and-d-campaign-setup.md) | Campaign Management | Medium | ✅ |
| WF-002 | [Session Note-Taking](session-note-taking.md) | Campaign Management | High | ✅ |
| WF-003 | [NPC Generation](npc-generation.md) | Content Creation | Medium | ✅ |
| WF-004 | [Location Development](location-development.md) | World Building | Medium | ✅ |
| WF-005 | [Quick NPC Lookup](quick-npc-lookup.md) | Session Support | Low | ✅ |
| WF-006 | [World Building](world-building.md) | Content Creation | High | ✅ |
| WF-007 | [Map Management](map-management.md) | World Organization | Medium | ✅ |
| WF-008 | [Quest/Plot Management](quest-plot-management.md) | Campaign Management | Medium | ✅ |
| WF-009 | [Session Prep](session-prep.md) | Campaign Management | High | ✅ |
| WF-010 | [Content Search](content-search.md) | Information Retrieval | Low | ✅ |

---

## Workflow Categories

### Campaign Management
Workflows for running D&D campaigns:
- Campaign Setup (WF-001)
- Session Note-Taking (WF-002)
- Quest/Plot Management (WF-008)
- Session Prep (WF-009)

### Content Creation
Workflows for building world content:
- NPC Generation (WF-003)
- Location Development (WF-004)
- World Building (WF-006)

### Session Support
Real-time support during gameplay:
- Quick NPC Lookup (WF-005)
- Content Search (WF-010)

### World Organization
Managing world structure:
- Map Management (WF-007)

---

## MCP Tools Referenced

### Core (Phase 1) - Required for MVP
| Tool | Type | Workflows |
|------|------|-----------|
| `list_worlds` | Read | WF-001 |
| `get_world` | Read | WF-001, WF-002, WF-006, WF-009 |
| `list_articles` | Read | WF-001, WF-002, WF-003, WF-004, WF-005, WF-006, WF-008, WF-009, WF-010 |
| `get_article` | Read | WF-002, WF-003, WF-004, WF-005, WF-006, WF-007, WF-008, WF-009, WF-010 |
| `list_categories` | Read | WF-001, WF-002, WF-010 |
| `get_category` | Read | WF-010 |

### High Priority (Phase 2)
| Tool | Type | Workflows |
|------|------|-----------|
| `search_articles` | Read | WF-002, WF-003, WF-004, WF-005, WF-006, WF-007, WF-008, WF-010 |
| `list_maps` | Read | WF-007 |
| `get_map` | Read | WF-007 |
| `get_map_markers` | Read | WF-007 |

### Campaign-Specific (Phase 3)
| Tool | Type | Workflows |
|------|------|-----------|
| `get_campaign` | Read | WF-009 |
| `list_campaign_npcs` | Read | WF-005, WF-009 |
| `get_campaign_npc` | Read | WF-005 |

### Future (Write API - When Available)
| Tool | Type | Workflows |
|------|------|-----------|
| `create_article` | Write | WF-002, WF-003, WF-004, WF-006, WF-008 |
| `update_article` | Write | WF-008 |
| `create_category` | Write | WF-001 |
| `create_campaign_npc` | Write | WF-003 |
| `create_map_marker` | Write | WF-007 |

---

## Workflow Design Principles

### 1. Progressive Disclosure
- Quick summaries first
- Detailed information on request
- Don't overwhelm with data

### 2. Context Preservation
- Load relevant context at start
- Maintain session state
- Remember recent lookups

### 3. Graceful Degradation
- Handle missing content
- Suggest alternatives
- Create content if needed

### 4. Speed Priority
- Session-time responses must be fast
- Pre-cache when possible
- Minimize API calls

### 5. DM-First Design
- Optimize for running games
- Separate player-safe from DM-only
- Support improvisation

---

## Cross-Cutting Concerns

### Authentication
All workflows require valid API credentials:
- `x-application-key`: Application key
- `x-auth-token`: User authentication token

### Error Handling
Common error scenarios:
- Authentication failure
- Content not found
- Rate limiting
- Network issues

### Caching Strategy
- Cache frequently accessed content
- Invalidate on updates
- Pre-load for sessions

---

## Next Steps (Phase 0.3+)

1. **Tool Specifications** (Phase 0.1)
   - Define complete MCP tool interfaces
   - Pydantic models for responses
   - Error handling patterns

2. **Quality Standards** (Phase 0.3)
   - Code quality rules
   - Testing requirements
   - Documentation standards

3. **Implementation** (Phase 1+)
   - Build core read endpoints
   - Add search functionality
   - Implement caching

---

## Research References

- [World Anvil Platform Summary](../research/world-anvil-platform-summary.md)
- [World Anvil API Documentation](https://www.worldanvil.com/api/external/boromir/documentation)
- [Swagger Documentation](https://www.worldanvil.com/api/external/boromir/swagger-documentation)
- [pywaclient Python Client](https://gitlab.com/SoulLink/world-anvil-api-client)
