# World Anvil API Coverage Analysis

## API Surface Overview

Based on the OpenAPI 3.0.3 specification in `openapi.yml`, the World Anvil Boromir API v2 provides access to **26 major resource types** organized into **8 functional areas**.

## Functional Areas

### 1. Core Content Management (High Priority for D&D)
- ✅ **Articles** - Primary content type for NPCs, locations, items, lore
- ✅ **Categories** - Hierarchical organization of content
- ⚠️ **Blocks** - Reusable content snippets (medium priority)
- ⚠️ **Block Folders** - Block organization (medium priority)
- ⚠️ **Block Templates** - Custom content templates (lower priority)

**D&D Use Case**: Articles for characters, locations, items. Categories for organization.

### 2. Maps & Geography (High Priority for D&D)
- ✅ **Maps** - World maps, regional maps, dungeon maps
- ✅ **Layers** - Map layers for different information types
- ✅ **Markers** - Points of interest on maps
- ✅ **Marker Groups** - Organized marker collections
- ✅ **Marker Types** - Pin types and icons

**D&D Use Case**: Campaign world geography, dungeon layouts, tactical maps with markers for encounters.

### 3. Campaign Timeline (High Priority for D&D)
- ✅ **Timelines** - Campaign chronology
- ✅ **Histories** - Historical events
- ⚠️ **Chronicles** - (Commented out in spec - may be deprecated)

**D&D Use Case**: Track campaign progression, historical events, timeline of world history.

### 4. RPG Systems (Critical for D&D)
- ✅ **RPG Systems** - D&D 5e, Pathfinder, etc.

**D&D Use Case**: Link world to specific RPG system rules.

### 5. Note-Taking & Session Management (High Priority for D&D)
- ✅ **Notebooks** - Campaign notebooks
- ✅ **Note Sections** - Organized sections
- ✅ **Notes** - Individual notes for sessions, ideas, NPCs

**D&D Use Case**: Session notes, DM prep, campaign planning, quick NPC notes.

### 6. Writing & Publishing (Lower Priority for D&D)
- ⚠️ **Manuscripts** - Book/story writing
- ⚠️ **Manuscript Beats** - Story structure
- ⚠️ **Manuscript Bookmarks** - Navigation
- ⚠️ **Manuscript Parts** - Chapters/sections
- ⚠️ **Manuscript Versions** - Version control
- ⚠️ **Manuscript Tags** - Organization
- ⚠️ **Manuscript Stats** - Writing statistics
- ⚠️ **Manuscript Labels** - Categorization
- ⚠️ **Manuscript Plots** - Plot threads

**D&D Use Case**: Publishing campaign settings, writing novels in the world. Not critical for active campaigns.

### 7. Media & Visuals (Medium Priority)
- ⚠️ **Images** - Image assets
- ⚠️ **Canvas** - Visual design and layouts

**D&D Use Case**: Character portraits, location art, maps. Important but not core functionality.

### 8. Access Control & Advanced (Lower Priority)
- ⚠️ **Secrets** - Hidden DM-only content
- ⚠️ **Subscriber Groups** - Access control for subscribers
- ⚠️ **Variables** - Template variables
- ⚠️ **Variable Collections** - Variable sets

**D&D Use Case**: Secrets for hidden info, but simpler than full implementation.

### 9. User & World Management (Critical Foundation)
- ✅ **User** - User profile and authentication
- ✅ **Identity** - User identity details
- ✅ **World** - World details and settings

**D&D Use Case**: Essential for all operations.

## Implementation Priority

### Phase 1: Core Foundation (Week 1-2)
**Essential for MVP**
- ✅ User & World management
- ✅ Articles (read/write)
- ✅ Categories (read/list)
- Authentication and API client
- Basic error handling and caching

**Deliverable**: Can read and create basic content

### Phase 2: D&D Campaign Features (Week 3-4)
**High-value D&D functionality**
- ✅ Notebooks and Notes (session logs)
- ✅ Timelines and Histories (campaign chronology)
- ✅ RPG Systems (link to D&D 5e)
- D&D-specific generators (NPCs, locations)

**Deliverable**: Full campaign management

### Phase 3: Maps & Geography (Week 5-6)
**Tactical and world maps**
- ✅ Maps (read/list)
- ✅ Markers and Marker Groups
- ✅ Layers (map organization)
- Interactive map integration

**Deliverable**: Complete map support

### Phase 4: Advanced Content (Week 7-8)
**Nice-to-have features**
- ⚠️ Blocks and Block Templates
- ⚠️ Secrets (DM-only content)
- ⚠️ Images and Canvas
- Advanced organization

**Deliverable**: Full-featured MCP server

### Phase 5: Publishing Features (Future)
**For content creators**
- ⚠️ Manuscripts and all sub-resources
- ⚠️ Variables and collections
- ⚠️ Subscriber groups
- Publishing workflows

**Deliverable**: Complete World Anvil integration

## Resource Complexity Analysis

### Simple Resources (Easy to Implement)
- User, World, Identity
- RPG Systems (mostly read-only)
- Basic article read operations

**Effort**: 1-2 days per resource type

### Medium Resources (Moderate Complexity)
- Articles (full CRUD)
- Categories (hierarchical)
- Notebooks/Notes (hierarchical)
- Timelines/Histories

**Effort**: 3-5 days per resource type

### Complex Resources (High Complexity)
- Maps with Layers, Markers, Groups
- Block system with Templates
- Manuscripts with all sub-resources

**Effort**: 1-2 weeks per resource type

## API Limitations & Unknowns

### Known Limitations
- OpenAPI spec shows mostly GET operations
- Write/Update/Delete operations not fully documented
- `parts/` directory schemas not available (referenced but missing)
- Chronicle endpoints commented out (may be deprecated)

### Requires Investigation
- ❓ Full CRUD support for each resource
- ❓ Granularity support (0/1/2) for all endpoints
- ❓ Rate limiting specifics
- ❓ Pagination patterns
- ❓ Search and filtering capabilities
- ❓ Webhook/notification support
- ❓ Bulk operation support

### Next Steps
1. Test API with real credentials to verify CRUD operations
2. Request `parts/` directory schemas from World Anvil team
3. Document actual rate limits through testing
4. Confirm granularity support per endpoint

## Recommended MCP Tool Coverage

### High Priority Tools (Phase 1-2)
1. `list_worlds` - List user's worlds
2. `get_world` - Get world details
3. `list_articles` - List articles with filtering
4. `get_article` - Get article content
5. `create_article` - Create new article
6. `update_article` - Update existing article
7. `list_categories` - List category hierarchy
8. `create_notebook` - Create campaign notebook
9. `create_note` - Add session notes
10. `link_rpg_system` - Connect world to D&D 5e

### Medium Priority Tools (Phase 3)
11. `list_maps` - List world maps
12. `get_map` - Get map with markers
13. `add_marker` - Add location marker
14. `create_timeline` - Create campaign timeline
15. `add_history_entry` - Add historical event

### Lower Priority Tools (Phase 4-5)
16. `manage_secrets` - DM-only content
17. `upload_image` - Add character art
18. `create_manuscript` - Start publishing project
19. `manage_blocks` - Reusable content

## API Coverage Summary

| Area | Resources | Priority | Complexity | Phase |
|------|-----------|----------|------------|-------|
| Core Content | 5 | High | Medium | 1-2 |
| Maps | 5 | High | High | 3 |
| Timeline | 2 | High | Medium | 2 |
| RPG Systems | 1 | Critical | Low | 1 |
| Notebooks | 3 | High | Medium | 2 |
| Writing | 9 | Low | High | 5 |
| Media | 2 | Medium | Medium | 4 |
| Access | 4 | Low | Medium | 4 |
| Foundation | 3 | Critical | Low | 1 |

**Total API Surface**: 34 distinct endpoints across 26 resource types

**Recommended MVP Coverage**: ~15 endpoints (44% of API surface)
**Full D&D Coverage**: ~25 endpoints (74% of API surface)
**Complete Coverage**: 34 endpoints (100% of API surface)
