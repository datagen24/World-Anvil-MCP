# World Anvil MCP Server - Design Specification

**Version**: 1.0
**Date**: 2025-11-28
**Purpose**: MCP server for interfacing with World Anvil API to assist with D&D world development

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [API Analysis](#api-analysis)
4. [MCP Server Components](#mcp-server-components)
5. [D&D-Specific Features](#dd-specific-features)
6. [Authentication & Security](#authentication--security)
7. [Implementation Roadmap](#implementation-roadmap)
8. [Technical Specifications](#technical-specifications)

---

## Executive Summary

### Project Goal
Build an MCP (Model Context Protocol) server that bridges Claude Code with World Anvil's API (v2 Boromir), enabling AI-assisted D&D world building through structured tools, resources, and prompts.

### Key Capabilities
- **Content Management**: Create, read, update, and organize articles, worlds, and categories
- **D&D Assistance**: Specialized tools for campaign management, NPC generation, location design
- **Contextual Resources**: Expose world data as MCP resources for AI context
- **Workflow Prompts**: Pre-built prompt templates for common worldbuilding tasks

### Technology Stack
- **Language**: Python 3.11+
- **Framework**: FastMCP (MCP Python SDK)
- **API Client**: Custom wrapper around World Anvil Boromir API v2
- **Transport**: stdio (default), streamable-http (optional for OAuth)
- **Authentication**: API key-based (user tokens)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Claude Code   │
│   (MCP Client)  │
└────────┬────────┘
         │ MCP Protocol (stdio/http)
         │
┌────────▼────────────────────────────┐
│   World Anvil MCP Server            │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  FastMCP Layer               │  │
│  │  • Tools                     │  │
│  │  • Resources                 │  │
│  │  • Prompts                   │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │  World Anvil Client Layer    │  │
│  │  • API wrapper               │  │
│  │  • Rate limiting             │  │
│  │  • Error handling            │  │
│  │  • Response caching          │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│  ┌──────────▼───────────────────┐  │
│  │  D&D Domain Logic            │  │
│  │  • Template system           │  │
│  │  • Content generators        │  │
│  │  • Relationship management   │  │
│  └──────────────────────────────┘  │
└─────────────┬───────────────────────┘
              │ HTTPS/JSON
              │
┌─────────────▼───────────────────┐
│   World Anvil API (Boromir v2)  │
│   • /worlds                     │
│   • /articles                   │
│   • /categories                 │
│   • /user                       │
└─────────────────────────────────┘
```

### Component Layers

#### 1. **MCP Interface Layer** (FastMCP)
- Handles MCP protocol communication
- Exposes tools, resources, and prompts to Claude
- Manages server lifecycle and context

#### 2. **World Anvil Client Layer**
- API request/response handling
- Authentication token management
- Rate limiting and retry logic
- Response caching for performance
- Granularity level management (0, 1, 2)

#### 3. **D&D Domain Layer**
- Article templates for D&D content types
- Content validation and enhancement
- Relationship tracking (NPCs, locations, items)
- Campaign organization utilities

#### 4. **Data Persistence Layer** (Optional)
- Local cache for API responses
- Session state management
- Template storage
- Query history

---

## API Analysis

### World Anvil Boromir API v2

**Base URL**: `https://www.worldanvil.com/api/external/boromir`

**Authentication**: Custom headers (NOT Bearer token)
```
x-application-key: <application_key>
x-auth-token: <user_authentication_token>
```

**Important**: Headers are lowercase `x-application-key` and `x-auth-token`, not `Authorization: Bearer`

**Content Type**: `application/json` for all requests/responses

### Core Endpoints (Based on OpenAPI 3.0.3 Spec)

#### World & User
```
GET    /world                   # Get world details
GET    /user/worlds             # List user's worlds
GET    /user                    # Get current user info
GET    /identity                # Get user identity
```

#### Articles & Content
```
GET    /article                 # Get article
GET    /world/articles          # List articles in world
```

#### Blocks & Templates
```
GET    /block                   # Get block
GET    /blockfolder/blocks      # List blocks in folder
GET    /blockfolder             # Get block folder
GET    /world/blockfolders      # List block folders
GET    /blocktemplate           # Get block template
GET    /user/blocktemplates     # List user's block templates
GET    /blocktemplatepart       # Get block template part
GET    /blocktemplate/blocktemplateparts  # List parts
```

#### Categories
```
GET    /category                # Get category
GET    /world/categories        # List categories in world
```

#### Maps & Geography
```
GET    /map                     # Get map
GET    /world/maps              # List maps in world
GET    /layer                   # Get map layer
GET    /map/layers              # List layers on map
GET    /marker                  # Get marker
GET    /map/markers             # List markers on map
GET    /markergroup             # Get marker group
GET    /map/markergroups        # List marker groups
GET    /markergroup/markers     # List markers in group
GET    /markertype              # Get marker type (pin)
GET    /markertypes             # List marker types
```

#### Timelines & History
```
GET    /timeline                # Get timeline
GET    /world/timelines         # List timelines
GET    /history                 # Get history entry
GET    /world/histories         # List histories
# /chronicle endpoints commented out in spec
```

#### RPG Systems
```
GET    /rpgsystem               # Get RPG system
GET    /rpgsystems              # List RPG systems
```

#### Manuscripts & Writing
```
GET    /manuscript              # Get manuscript
GET    /world/manuscripts       # List manuscripts
GET    /manuscript_beat         # Get manuscript beat
GET    /manuscript_part/manuscript_beats  # List beats by part
GET    /manuscript_bookmark     # Get bookmark
GET    /manuscript/manuscript_bookmarks   # List bookmarks
GET    /manuscript_part         # Get manuscript part
GET    /manuscript_version/manuscript_parts  # List parts
GET    /manuscript_version      # Get manuscript version
GET    /manuscript/manuscript_versions    # List versions
GET    /manuscript_tag          # Get manuscript tag
GET    /manuscript/manuscript_tags        # List tags
GET    /manuscript_stat         # Get manuscript stat
GET    /manuscript_version/manuscript_stats  # List stats
GET    /manuscript_label        # Get manuscript label
GET    /manuscript/manuscript_labels      # List labels
GET    /manuscript_plot         # Get manuscript plot
GET    /manuscript_version/manuscript_plots  # List plots
```

#### Notebooks & Notes
```
GET    /notebook                # Get notebook
GET    /world/notebooks         # List notebooks
GET    /notesection             # Get note section
GET    /notebook/notesections   # List note sections
GET    /note                    # Get note
GET    /notesection/notes       # List notes in section
```

#### Media
```
GET    /image                   # Get image
GET    /world/images            # List images
GET    /canvas                  # Get canvas
GET    /world/canvases          # List canvases
```

#### Access Control
```
GET    /secret                  # Get secret
GET    /world/secrets           # List secrets
GET    /subscribergroup         # Get subscriber group
GET    /world/subscribergroups  # List subscriber groups
```

#### Variables
```
GET    /variable                # Get variable
GET    /variable_collection/variables  # List variables
GET    /variable_collection     # Get variable collection
GET    /world/variablecollections      # List collections
```

**Note**: The OpenAPI spec includes references to `parts/` directory files with detailed schemas for each endpoint. Write/Update/Delete operations may be available but are not fully detailed in the main spec file.

### Granularity Levels

All GET endpoints support `?granularity=<level>`:

- **0**: Minimum display object (preview/choice data)
- **1**: Principal display object (standard display)
- **2**: Detailed object (full data with relationships)

### Rate Limiting

- Expected limits apply (check API documentation)
- Implement exponential backoff for 429 responses
- Cache responses aggressively to minimize API calls

### API Constraints

- **Read-Only Focus**: Current public API is primarily read-focused
- **Write Endpoints**: Limited write capabilities (check current API status)
- **Guild Requirement**: Grandmaster rank required for application key
- **User Tokens**: Guild member required for user API tokens

---

## MCP Server Components

### 1. Tools

MCP tools are executable functions that Claude can call to perform actions.

#### Article Management Tools

##### `create_article`
```python
@mcp.tool()
async def create_article(
    world_id: str,
    title: str,
    content: str,
    category_id: str | None = None,
    template: str = "generic",
    tags: list[str] | None = None,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Create a new article in World Anvil.

    Args:
        world_id: Target world ID
        title: Article title
        content: Article content (supports BBCode/Markdown)
        category_id: Optional category to organize article
        template: Article template type (character, location, item, etc.)
        tags: Optional tags for categorization

    Returns:
        Created article details including ID and URL
    """
```

##### `get_article`
```python
@mcp.tool()
async def get_article(
    world_id: str,
    article_id: str,
    granularity: int = 1,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Retrieve article details from World Anvil.

    Args:
        world_id: World containing the article
        article_id: Article identifier
        granularity: Detail level (0=preview, 1=standard, 2=detailed)

    Returns:
        Article content and metadata
    """
```

##### `update_article`
```python
@mcp.tool()
async def update_article(
    world_id: str,
    article_id: str,
    title: str | None = None,
    content: str | None = None,
    tags: list[str] | None = None,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Update existing article in World Anvil.

    Args:
        world_id: World containing the article
        article_id: Article to update
        title: New title (optional)
        content: New content (optional)
        tags: Updated tags (optional)

    Returns:
        Updated article details
    """
```

##### `search_articles`
```python
@mcp.tool()
async def search_articles(
    world_id: str,
    query: str | None = None,
    category_id: str | None = None,
    tags: list[str] | None = None,
    limit: int = 20,
    ctx: Context = None
) -> list[dict[str, Any]]:
    """
    Search articles within a world.

    Args:
        world_id: World to search
        query: Text search query
        category_id: Filter by category
        tags: Filter by tags
        limit: Maximum results to return

    Returns:
        List of matching articles
    """
```

#### World Management Tools

##### `list_worlds`
```python
@mcp.tool()
async def list_worlds(
    ctx: Context = None
) -> list[dict[str, Any]]:
    """
    List all worlds owned by the authenticated user.

    Returns:
        List of world summaries with IDs, names, and URLs
    """
```

##### `get_world`
```python
@mcp.tool()
async def get_world(
    world_id: str,
    granularity: int = 1,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Get detailed information about a world.

    Args:
        world_id: World identifier
        granularity: Detail level (0=preview, 1=standard, 2=detailed)

    Returns:
        World details including settings and statistics
    """
```

#### Category Management Tools

##### `list_categories`
```python
@mcp.tool()
async def list_categories(
    world_id: str,
    ctx: Context = None
) -> list[dict[str, Any]]:
    """
    List all categories in a world.

    Args:
        world_id: World to query

    Returns:
        List of categories with hierarchy
    """
```

##### `create_category`
```python
@mcp.tool()
async def create_category(
    world_id: str,
    name: str,
    parent_id: str | None = None,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Create a new category for organizing articles.

    Args:
        world_id: World to create category in
        name: Category name
        parent_id: Optional parent category for hierarchy

    Returns:
        Created category details
    """
```

#### D&D-Specific Tools

##### `generate_npc`
```python
@mcp.tool()
async def generate_npc(
    world_id: str,
    name: str,
    race: str | None = None,
    class_name: str | None = None,
    level: int | None = None,
    alignment: str | None = None,
    description: str | None = None,
    save: bool = True,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Generate a D&D NPC character with World Anvil article.

    Args:
        world_id: World to create NPC in
        name: Character name
        race: D&D race (Human, Elf, Dwarf, etc.)
        class_name: D&D class (Fighter, Wizard, etc.)
        level: Character level
        alignment: Alignment (LG, NG, CG, etc.)
        description: Additional character description
        save: Whether to save to World Anvil immediately

    Returns:
        NPC details including generated backstory and stats
    """
```

##### `generate_location`
```python
@mcp.tool()
async def generate_location(
    world_id: str,
    name: str,
    location_type: str,
    size: str | None = None,
    population: int | None = None,
    government: str | None = None,
    description: str | None = None,
    save: bool = True,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Generate a D&D location with World Anvil article.

    Args:
        world_id: World to create location in
        name: Location name
        location_type: Type (city, town, dungeon, wilderness, etc.)
        size: Size category
        population: Estimated population
        government: Government type
        description: Additional description
        save: Whether to save to World Anvil immediately

    Returns:
        Location details with generated content
    """
```

##### `generate_campaign_session`
```python
@mcp.tool()
async def generate_campaign_session(
    world_id: str,
    session_number: int,
    title: str,
    summary: str,
    participants: list[str] | None = None,
    locations: list[str] | None = None,
    npcs: list[str] | None = None,
    save: bool = True,
    ctx: Context = None
) -> dict[str, Any]:
    """
    Create a campaign session log with World Anvil article.

    Args:
        world_id: Campaign world
        session_number: Session sequence number
        title: Session title
        summary: Session summary/notes
        participants: Player character names/IDs
        locations: Visited location IDs
        npcs: Encountered NPC IDs
        save: Whether to save to World Anvil immediately

    Returns:
        Session log article with formatted content
    """
```

---

### 2. Resources

MCP resources expose World Anvil data as readable context for Claude.

#### World Resources

##### `world://{world_id}`
```python
@mcp.resource("world://{world_id}")
async def get_world_resource(world_id: str) -> str:
    """
    Expose world details as a resource.

    Returns formatted world information including:
    - World name and description
    - Total articles count
    - Category structure
    - Recent activity
    """
```

##### `world://{world_id}/summary`
```python
@mcp.resource("world://{world_id}/summary")
async def get_world_summary(world_id: str) -> str:
    """
    Provide concise world summary for context.

    Returns:
    - World overview
    - Key locations
    - Major NPCs
    - Active campaigns
    """
```

#### Article Resources

##### `article://{world_id}/{article_id}`
```python
@mcp.resource("article://{world_id}/{article_id}")
async def get_article_resource(world_id: str, article_id: str) -> str:
    """
    Expose article content as a resource.

    Returns:
    - Article title and content
    - Category and tags
    - Related articles
    - Metadata (author, dates, views)
    """
```

#### Category Resources

##### `category://{world_id}/{category_id}`
```python
@mcp.resource("category://{world_id}/{category_id}")
async def get_category_resource(world_id: str, category_id: str) -> str:
    """
    Expose category structure and contents.

    Returns:
    - Category name and hierarchy
    - Articles in category
    - Subcategories
    """
```

#### D&D Campaign Resources

##### `campaign://{world_id}/active`
```python
@mcp.resource("campaign://{world_id}/active")
async def get_active_campaign(world_id: str) -> str:
    """
    Provide context about active D&D campaign.

    Returns:
    - Campaign overview
    - Current party composition
    - Recent session summaries
    - Active plot threads
    - Key NPCs and locations
    """
```

---

### 3. Prompts

MCP prompts provide pre-built templates for common worldbuilding tasks.

#### Content Creation Prompts

##### `create_character`
```python
@mcp.prompt()
def create_character_prompt(
    name: str,
    role: str = "NPC",
    campaign_context: str | None = None
) -> str:
    """
    Generate prompt for creating a D&D character.

    Returns structured prompt guiding character creation with:
    - Physical description
    - Personality traits
    - Background and motivations
    - Abilities and skills
    - Role in the world/campaign
    """
```

##### `create_location`
```python
@mcp.prompt()
def create_location_prompt(
    location_type: str,
    setting_context: str | None = None
) -> str:
    """
    Generate prompt for creating a location.

    Returns structured prompt covering:
    - Physical description
    - History and significance
    - Key features and landmarks
    - Inhabitants and culture
    - Adventure hooks
    """
```

##### `write_session_recap`
```python
@mcp.prompt()
def write_session_recap_prompt(
    session_number: int,
    key_events: list[str] | None = None
) -> str:
    """
    Generate prompt for writing campaign session recap.

    Returns structured prompt for:
    - Session summary
    - Key events and decisions
    - Character development
    - Plot progression
    - Cliffhangers and next steps
    """
```

#### Content Enhancement Prompts

##### `expand_description`
```python
@mcp.prompt()
def expand_description_prompt(
    content_type: str,
    current_text: str
) -> str:
    """
    Generate prompt for expanding existing content.

    Returns prompt to enhance:
    - Sensory details
    - Historical context
    - Cultural elements
    - Narrative hooks
    """
```

##### `create_connections`
```python
@mcp.prompt()
def create_connections_prompt(
    article_id: str,
    world_context: str
) -> str:
    """
    Generate prompt for identifying connections.

    Returns prompt to find:
    - Related NPCs
    - Connected locations
    - Historical ties
    - Plot threads
    """
```

---

## D&D-Specific Features

### Article Templates

Pre-defined templates for common D&D content types:

#### Character Template
```python
CHARACTER_TEMPLATE = {
    "sections": [
        {"name": "Quick Reference", "fields": ["race", "class", "level", "alignment"]},
        {"name": "Physical Description", "fields": ["appearance", "distinctive_features"]},
        {"name": "Personality", "fields": ["traits", "ideals", "bonds", "flaws"]},
        {"name": "Background", "fields": ["backstory", "motivations"]},
        {"name": "Abilities", "fields": ["stats", "skills", "special_abilities"]},
        {"name": "Relationships", "fields": ["allies", "enemies", "affiliations"]},
    ],
    "metadata": {
        "category": "Characters",
        "tags": ["npc", "character"]
    }
}
```

#### Location Template
```python
LOCATION_TEMPLATE = {
    "sections": [
        {"name": "Overview", "fields": ["type", "size", "population", "government"]},
        {"name": "Description", "fields": ["appearance", "atmosphere"]},
        {"name": "History", "fields": ["founding", "major_events"]},
        {"name": "Geography", "fields": ["terrain", "climate", "resources"]},
        {"name": "Culture", "fields": ["customs", "religions", "economy"]},
        {"name": "Notable Features", "fields": ["landmarks", "districts"]},
        {"name": "Notable Residents", "fields": ["leaders", "merchants", "npcs"]},
        {"name": "Adventure Hooks", "fields": ["quests", "rumors", "threats"]},
    ],
    "metadata": {
        "category": "Locations",
        "tags": ["location", "settlement"]
    }
}
```

#### Item Template
```python
ITEM_TEMPLATE = {
    "sections": [
        {"name": "Properties", "fields": ["type", "rarity", "requires_attunement"]},
        {"name": "Description", "fields": ["appearance", "material"]},
        {"name": "Abilities", "fields": ["magical_properties", "mechanics"]},
        {"name": "History", "fields": ["origin", "previous_owners"]},
        {"name": "Lore", "fields": ["legends", "significance"]},
    ],
    "metadata": {
        "category": "Items",
        "tags": ["item", "magic_item"]
    }
}
```

#### Campaign Session Template
```python
SESSION_TEMPLATE = {
    "sections": [
        {"name": "Session Info", "fields": ["number", "date", "title"]},
        {"name": "Summary", "fields": ["overview"]},
        {"name": "Events", "fields": ["key_events", "combat_encounters"]},
        {"name": "Participants", "fields": ["players", "characters"]},
        {"name": "NPCs Encountered", "fields": ["npcs"]},
        {"name": "Locations Visited", "fields": ["locations"]},
        {"name": "Items Acquired", "fields": ["loot", "rewards"]},
        {"name": "Plot Development", "fields": ["revelations", "decisions"]},
        {"name": "Next Session", "fields": ["cliffhanger", "preparations"]},
    ],
    "metadata": {
        "category": "Campaign Logs",
        "tags": ["session", "campaign"]
    }
}
```

### Content Generators

#### NPC Generator
- Random name generation (race-appropriate)
- Personality trait selection from D&D tables
- Background and motivation generation
- Stat block creation (optional)
- Voice/mannerism suggestions
- Plot hook generation

#### Location Generator
- Settlement name generation
- Population and government structure
- Notable NPC residents
- Key locations within settlement
- Local customs and culture
- Adventure hooks and rumors

#### Quest Generator
- Quest type selection (rescue, retrieval, investigation, etc.)
- Quest giver NPC generation
- Objective and obstacles
- Rewards (treasure, XP, story progression)
- Complications and twists

### Relationship Tracking

Maintain connections between articles:
- NPC relationships (allies, enemies, family)
- Location hierarchies (cities → districts → buildings)
- Item ownership and history
- Quest participants and locations
- Campaign timeline connections

---

## Authentication & Security

### Authentication Flow

#### Application Key (Server-Level)
```python
# Stored in environment variables or config file
APPLICATION_KEY = os.getenv("WORLD_ANVIL_APP_KEY")
```

#### User API Token (User-Level)
```python
# Provided at server initialization or via prompt
USER_API_TOKEN = os.getenv("WORLD_ANVIL_USER_TOKEN")

# Or collected at runtime:
@mcp.tool()
async def authenticate(api_token: str) -> dict[str, str]:
    """Store user API token for session."""
    # Validate token by making test request
    # Store in session context
```

### Request Authentication

All API requests include these headers:
```python
headers = {
    "x-application-key": APPLICATION_KEY,
    "x-auth-token": USER_API_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

**Critical**: Use lowercase header names `x-application-key` and `x-auth-token`, NOT `Authorization: Bearer`

### Security Considerations

1. **Token Storage**:
   - Never log tokens
   - Store encrypted in config files
   - Support environment variables
   - Clear from memory on session end

2. **API Key Protection**:
   - Application key separate from user tokens
   - Require Grandmaster guild status confirmation
   - Document token generation process

3. **Rate Limiting**:
   - Respect API rate limits
   - Implement exponential backoff
   - Cache responses aggressively
   - Queue requests if necessary

4. **Error Handling**:
   - Sanitize error messages (remove tokens)
   - Handle 401/403 gracefully
   - Provide clear authentication guidance

---

## Implementation Roadmap

### Phase 1: Core Infrastructure (Week 1)

**Goals**: Basic MCP server with World Anvil API integration

**Tasks**:
1. **Project Setup**
   - Initialize Python project with `uv`
   - Install FastMCP and dependencies
   - Create project structure

2. **World Anvil API Client**
   - Implement base HTTP client
   - Add authentication handling
   - Create response models (Pydantic)
   - Implement rate limiting

3. **Basic MCP Server**
   - Initialize FastMCP server
   - Implement stdio transport
   - Add health check tool
   - Test with Claude Code

**Deliverables**:
- Working MCP server skeleton
- Authenticated API client
- Basic tool (`list_worlds`, `get_world`)

### Phase 2: Article Management (Week 2)

**Goals**: Full CRUD operations for articles

**Tasks**:
1. **Article Tools**
   - `get_article` with granularity support
   - `create_article` with template support
   - `update_article` with partial updates
   - `search_articles` with filters

2. **Article Resources**
   - `article://{world_id}/{article_id}` resource
   - Article content formatting
   - Metadata extraction

3. **Testing**
   - Unit tests for API client
   - Integration tests with real API
   - MCP protocol tests

**Deliverables**:
- Complete article management suite
- Article resources for Claude context
- Test coverage >80%

### Phase 3: D&D Content Generation (Week 3)

**Goals**: D&D-specific tools and templates

**Tasks**:
1. **Template System**
   - Implement template engine
   - Create D&D article templates
   - Add template validation

2. **Content Generators**
   - NPC generator with D&D tables
   - Location generator
   - Basic quest generator

3. **D&D Tools**
   - `generate_npc` tool
   - `generate_location` tool
   - `generate_campaign_session` tool

**Deliverables**:
- D&D template library
- Content generation tools
- Example generated content

### Phase 4: Campaign Management (Week 4)

**Goals**: Campaign-focused features

**Tasks**:
1. **Campaign Resources**
   - `campaign://{world_id}/active` resource
   - Campaign timeline tracking
   - Session log management

2. **Relationship Tracking**
   - Article relationship system
   - NPC relationship graphs
   - Location hierarchies

3. **Prompts**
   - Character creation prompts
   - Location design prompts
   - Session recap prompts

**Deliverables**:
- Campaign management suite
- Relationship tracking system
- Prompt library

### Phase 5: Enhancement & Polish (Week 5)

**Goals**: Performance, UX, documentation

**Tasks**:
1. **Performance**
   - Response caching
   - Request batching
   - Lazy loading

2. **User Experience**
   - Better error messages
   - Progress reporting for long operations
   - Interactive authentication flow

3. **Documentation**
   - API documentation
   - Usage examples
   - Troubleshooting guide

**Deliverables**:
- Optimized server performance
- Comprehensive documentation
- Production-ready v1.0

---

## Technical Specifications

### Project Structure

```
world-anvil/
├── README.md                 # Project overview and setup
├── pyproject.toml            # Python project configuration
├── .env.example              # Environment variable template
├── claudedocs/
│   ├── DESIGN_SPECIFICATION.md
│   ├── API_REFERENCE.md
│   └── USAGE_EXAMPLES.md
├── src/
│   └── world_anvil_mcp/
│       ├── __init__.py
│       ├── server.py         # FastMCP server entry point
│       ├── api/
│       │   ├── __init__.py
│       │   ├── client.py     # World Anvil API client
│       │   ├── models.py     # Pydantic models for API responses
│       │   └── exceptions.py # Custom exceptions
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── articles.py   # Article management tools
│       │   ├── worlds.py     # World management tools
│       │   ├── categories.py # Category tools
│       │   └── dnd.py        # D&D-specific tools
│       ├── resources/
│       │   ├── __init__.py
│       │   ├── worlds.py     # World resources
│       │   ├── articles.py   # Article resources
│       │   └── campaigns.py  # Campaign resources
│       ├── prompts/
│       │   ├── __init__.py
│       │   ├── creation.py   # Content creation prompts
│       │   └── enhancement.py # Enhancement prompts
│       ├── templates/
│       │   ├── __init__.py
│       │   ├── character.py  # Character template
│       │   ├── location.py   # Location template
│       │   ├── item.py       # Item template
│       │   └── session.py    # Campaign session template
│       └── utils/
│           ├── __init__.py
│           ├── cache.py      # Response caching
│           ├── rate_limit.py # Rate limiting
│           └── formatting.py # Content formatting
├── tests/
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_tools.py
│   ├── test_resources.py
│   └── test_templates.py
└── examples/
    ├── basic_usage.py
    ├── npc_generation.py
    └── campaign_management.py
```

### Dependencies

```toml
[project]
name = "world-anvil-mcp"
version = "1.0.0"
requires-python = ">=3.11"
dependencies = [
    "mcp>=1.0.0",                # MCP SDK
    "pydantic>=2.0.0",           # Data validation
    "httpx>=0.27.0",             # Async HTTP client
    "python-dotenv>=1.0.0",      # Environment variables
    "tenacity>=8.0.0",           # Retry logic
    "cachetools>=5.0.0",         # Response caching
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.3.0",               # Linting
    "mypy>=1.8.0",               # Type checking
]

[project.scripts]
world-anvil-mcp = "world_anvil_mcp.server:main"
```

### Configuration

#### Environment Variables
```bash
# Required
WORLD_ANVIL_APP_KEY=your_application_key_here
WORLD_ANVIL_USER_TOKEN=your_user_api_token_here

# Optional
WORLD_ANVIL_API_BASE=https://www.worldanvil.com/api/external/boromir
WORLD_ANVIL_CACHE_TTL=3600
WORLD_ANVIL_RATE_LIMIT=60
WORLD_ANVIL_DEBUG=false
```

#### Server Configuration
```python
# server.py configuration options
SERVER_CONFIG = {
    "name": "World Anvil Assistant",
    "version": "1.0.0",
    "api_base": os.getenv("WORLD_ANVIL_API_BASE", "https://www.worldanvil.com/api/external/boromir"),
    "cache_ttl": int(os.getenv("WORLD_ANVIL_CACHE_TTL", "3600")),
    "rate_limit": int(os.getenv("WORLD_ANVIL_RATE_LIMIT", "60")),
    "debug": os.getenv("WORLD_ANVIL_DEBUG", "false").lower() == "true",
    "transport": "stdio",  # or "streamable-http" for OAuth
}
```

### API Client Implementation

```python
# api/client.py structure
class WorldAnvilClient:
    """Async client for World Anvil Boromir API v2."""

    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str = "https://www.worldanvil.com/api/external/boromir",
        rate_limit: int = 60,
        cache_ttl: int = 3600
    ):
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url
        self.rate_limiter = RateLimiter(rate_limit)
        self.cache = ResponseCache(ttl=cache_ttl)
        self.client = httpx.AsyncClient(
            headers=self._build_headers(),
            timeout=30.0
        )

    def _build_headers(self) -> dict[str, str]:
        """Build request headers with authentication."""
        return {
            "x-application-key": self.app_key,
            "x-auth-token": self.user_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "World Anvil MCP/1.0.0"
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    async def get(self, endpoint: str, params: dict | None = None) -> dict:
        """Make GET request with caching and retry."""
        cache_key = f"{endpoint}:{params}"

        # Check cache first
        if cached := self.cache.get(cache_key):
            return cached

        # Rate limit
        await self.rate_limiter.acquire()

        # Make request
        response = await self.client.get(
            f"{self.base_url}{endpoint}",
            params=params
        )
        response.raise_for_status()

        data = response.json()
        self.cache.set(cache_key, data)
        return data

    # Specific endpoint methods
    async def get_world(self, world_id: str, granularity: int = 1) -> World:
        """Get world details."""
        data = await self.get(f"/world/{world_id}", {"granularity": granularity})
        return World.model_validate(data)

    async def list_articles(
        self,
        world_id: str,
        category_id: str | None = None,
        limit: int = 20
    ) -> list[Article]:
        """List articles in world."""
        params = {"limit": limit}
        if category_id:
            params["categoryId"] = category_id

        data = await self.get(f"/world/{world_id}/articles", params)
        return [Article.model_validate(item) for item in data]

    # ... more methods
```

### Error Handling Strategy

```python
# api/exceptions.py
class WorldAnvilError(Exception):
    """Base exception for World Anvil API errors."""
    pass

class AuthenticationError(WorldAnvilError):
    """Authentication failed (401, 403)."""
    pass

class RateLimitError(WorldAnvilError):
    """Rate limit exceeded (429)."""
    pass

class NotFoundError(WorldAnvilError):
    """Resource not found (404)."""
    pass

class ValidationError(WorldAnvilError):
    """Request validation failed (400)."""
    pass

# Error handling in tools
@mcp.tool()
async def get_article(world_id: str, article_id: str, ctx: Context) -> dict:
    try:
        client = ctx.fastmcp.lifespan_context["client"]
        article = await client.get_article(world_id, article_id)
        return article.model_dump()
    except AuthenticationError:
        await ctx.error("Authentication failed. Check your API tokens.")
        raise
    except NotFoundError:
        await ctx.warning(f"Article {article_id} not found in world {world_id}")
        return {"error": "not_found", "message": "Article not found"}
    except RateLimitError:
        await ctx.warning("Rate limit exceeded. Retrying after delay...")
        # Will be retried automatically by @retry decorator
        raise
    except WorldAnvilError as e:
        await ctx.error(f"World Anvil API error: {str(e)}")
        raise
```

### Testing Strategy

```python
# tests/test_api_client.py example
import pytest
from world_anvil_mcp.api.client import WorldAnvilClient
from world_anvil_mcp.api.exceptions import AuthenticationError

@pytest.mark.asyncio
async def test_get_world_success(mock_api):
    """Test successful world retrieval."""
    client = WorldAnvilClient(
        app_key="test_app_key",
        user_token="test_user_token"
    )

    mock_api.get("/world/123").respond(200, json={
        "id": "123",
        "name": "Test World",
        "description": "A test world"
    })

    world = await client.get_world("123")
    assert world.id == "123"
    assert world.name == "Test World"

@pytest.mark.asyncio
async def test_authentication_failure(mock_api):
    """Test authentication error handling."""
    client = WorldAnvilClient(
        app_key="invalid",
        user_token="invalid"
    )

    mock_api.get("/world/123").respond(401)

    with pytest.raises(AuthenticationError):
        await client.get_world("123")
```

---

## Usage Examples

### Example 1: Creating an NPC

```python
# User interaction with Claude Code
User: "Create a new NPC named 'Thaldrin Ironforge', a dwarf blacksmith in my campaign world"

# Claude uses the generate_npc tool
await generate_npc(
    world_id="campaign_world_123",
    name="Thaldrin Ironforge",
    race="Dwarf",
    class_name="Blacksmith",
    description="Gruff but skilled artisan known for magical weapons",
    save=True
)

# Result: Article created in World Anvil with:
# - Character template structure
# - Generated backstory
# - Personality traits
# - Skill suggestions
# - Plot hooks
```

### Example 2: Session Recap

```python
# User provides session notes
User: "Write a recap for session 15. The party infiltrated the thieves' guild and discovered the Shadow Crown artifact."

# Claude uses prompt + tool
prompt = create_session_recap_prompt(
    session_number=15,
    key_events=["Thieves' guild infiltration", "Shadow Crown discovery"]
)

# Claude generates content using prompt
# Then saves to World Anvil
await generate_campaign_session(
    world_id="campaign_world_123",
    session_number=15,
    title="The Shadow Crown Revealed",
    summary=generated_content,
    save=True
)
```

### Example 3: World Context for Planning

```python
# User asks for campaign planning help
User: "Help me plan the next adventure arc in my Forgotten Realms campaign"

# Claude reads world context via resources
world_info = await read_resource("world://campaign_world_123/summary")
active_campaign = await read_resource("campaign://campaign_world_123/active")

# Claude uses context to provide relevant suggestions based on:
# - Current campaign state
# - Active NPCs and locations
# - Previous session events
# - Established plot threads
```

---

## Performance Considerations

### Caching Strategy
- Cache API responses for 1 hour by default
- Invalidate cache on write operations
- Cache search results separately (5 minute TTL)
- Implement LRU cache with size limits

### Rate Limiting
- Respect World Anvil API limits (check documentation)
- Implement token bucket algorithm
- Queue requests when limit approached
- Exponential backoff for 429 responses

### Optimization Techniques
- Batch article requests when possible
- Use granularity=0 for list operations
- Lazy load article content
- Parallel requests for independent operations
- Connection pooling for HTTP client

---

## Security & Privacy

### Token Management
- Never log API tokens
- Store encrypted in configuration
- Support environment variables
- Prompt for tokens if not configured
- Clear tokens on session end

### Data Privacy
- Respect World Anvil's terms of service
- Don't cache sensitive user data longer than necessary
- Implement secure token storage
- Sanitize error messages

### API Usage
- Stay within rate limits
- Implement circuit breaker for API failures
- Handle degraded service gracefully
- Respect user's guild status requirements

---

## Future Enhancements

### Phase 2 Features (Post-MVP)
- **Advanced Templates**: More D&D content types (organizations, religions, events)
- **Batch Operations**: Bulk article creation/updates
- **Version Control**: Track article changes over time
- **Export/Import**: Backup and restore world data
- **Collaboration**: Multi-user campaign management

### Integration Opportunities
- **D&D Beyond**: Import character data
- **Roll20/Foundry VTT**: Export maps and tokens
- **AI Content Generation**: Enhanced description generation
- **Image Integration**: DALL-E for location/character art
- **PDF Export**: Generate campaign documents

### Advanced Features
- **Relationship Graphs**: Visual network of connections
- **Timeline Management**: Chronicle events chronologically
- **Quest Tracking**: Manage active and completed quests
- **Loot Tables**: Random treasure generation
- **Random Encounters**: Location-based encounter tables

---

## References & Resources

### Official Documentation
- [World Anvil API v2 (Boromir) Documentation](https://www.worldanvil.com/api/external/boromir/documentation)
- [World Anvil User API Tokens](https://www.worldanvil.com/api/auth/key)
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)

### Community Resources
- [World Anvil API Python Client (GitLab)](https://gitlab.com/SoulLink/world-anvil-api-client)
- [World Anvil Codex - Articles & Categories](https://www.worldanvil.com/w/WorldAnvilCodex/a/articles-categories-manager)
- [Foundry VTT World Anvil Integration](https://github.com/foundryvtt/world-anvil)

### Technical References
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md)
- [World Anvil Feature Requests - API Editing](https://www.worldanvil.com/community/voting/suggestion/4cbaaa25-8d3b-4603-8dd3-207873a73bce/view)

---

## Appendix: API Endpoint Reference

Based on OpenAPI 3.0.3 specification (openapi.yml)

### World & User Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/world` | Get world details | Supports granularity |
| `/user/worlds` | List user's worlds | Supports granularity |
| `/user` | Get current user info | User profile |
| `/identity` | Get user identity | Identity details |

### Content Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/article` | Get article | Core content type |
| `/world/articles` | List articles in world | Filterable |
| `/category` | Get category | Organization |
| `/world/categories` | List categories | Hierarchical |
| `/block` | Get content block | Reusable content |
| `/blockfolder` | Get block folder | Block organization |
| `/world/blockfolders` | List block folders | World-scoped |

### Map Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/map` | Get map | Geographic maps |
| `/world/maps` | List maps | World-scoped |
| `/layer` | Get map layer | Map layers |
| `/map/layers` | List layers on map | Hierarchical |
| `/marker` | Get map marker | POI markers |
| `/map/markers` | List markers | Map-scoped |
| `/markergroup` | Get marker group | Marker organization |
| `/map/markergroups` | List marker groups | Grouping |
| `/markergroup/markers` | List markers in group | Group members |
| `/markertype` | Get marker type | Pin types |
| `/markertypes` | List marker types | Global types |

### Timeline Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/timeline` | Get timeline | Campaign timelines |
| `/world/timelines` | List timelines | World-scoped |
| `/history` | Get history entry | Historical events |
| `/world/histories` | List histories | World-scoped |

### RPG System Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/rpgsystem` | Get RPG system | D&D, Pathfinder, etc. |
| `/rpgsystems` | List RPG systems | Global list |

### Manuscript Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/manuscript` | Get manuscript | Writing projects |
| `/world/manuscripts` | List manuscripts | World-scoped |
| `/manuscript_beat` | Get manuscript beat | Story beats |
| `/manuscript_bookmark` | Get bookmark | Navigation |
| `/manuscript_part` | Get manuscript part | Chapters/sections |
| `/manuscript_version` | Get version | Version control |
| `/manuscript_tag` | Get tag | Tagging system |
| `/manuscript_stat` | Get stat | Statistics |
| `/manuscript_label` | Get label | Organization |
| `/manuscript_plot` | Get plot | Plot threads |

### Notebook Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/notebook` | Get notebook | Note organization |
| `/world/notebooks` | List notebooks | World-scoped |
| `/notesection` | Get note section | Notebook sections |
| `/notebook/notesections` | List sections | Hierarchical |
| `/note` | Get note | Individual notes |
| `/notesection/notes` | List notes | Section-scoped |

### Media Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/image` | Get image | Image assets |
| `/world/images` | List images | World-scoped |
| `/canvas` | Get canvas | Visual design |
| `/world/canvases` | List canvases | World-scoped |

### Access Control Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/secret` | Get secret | Hidden content |
| `/world/secrets` | List secrets | DM-only info |
| `/subscribergroup` | Get subscriber group | Access control |
| `/world/subscribergroups` | List groups | Permission groups |

### Template & Variable Endpoints
| Endpoint | Description | Notes |
|----------|-------------|-------|
| `/blocktemplate` | Get block template | Custom templates |
| `/user/blocktemplates` | List user templates | User-scoped |
| `/blocktemplatepart` | Get template part | Template components |
| `/variable` | Get variable | Template variables |
| `/variable_collection` | Get variable collection | Variable sets |
| `/world/variablecollections` | List collections | World-scoped |

**Note**: Most endpoints support granularity parameter (0=preview, 1=standard, 2=detailed). Detailed schemas are in `parts/` directory files referenced by openapi.yml.

---

**End of Design Specification**

*This document provides comprehensive guidance for implementing the World Anvil MCP server. For implementation details, refer to the codebase and follow the roadmap outlined above.*

**Sources**:
- [World Anvil API Documentation - v.2 (Boromir)](https://www.worldanvil.com/api/external/boromir/documentation)
- [World Anvil API Python Client - GitLab](https://gitlab.com/SoulLink/world-anvil-api-client)
- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk)
