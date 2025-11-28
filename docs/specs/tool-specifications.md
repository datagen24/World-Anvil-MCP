# World Anvil MCP Tool Specifications

**Date**: 2025-11-28
**Status**: Phase 0.1 - Complete Tool Specifications
**Based On**:
- pywaclient analysis (docs/research/pywaclient-analysis.md)
- Workflow tool mappings (docs/workflows/README.md)
- OpenAPI specification (openapi.yml)

---

## Overview

This document specifies all 34 MCP tools for the World Anvil MCP server, organized by implementation priority based on workflow analysis.

**Tool Priority Matrix** (from workflow analysis):
- **Critical** (10+ workflows): `list_articles`, `get_article`, `search_articles`
- **High** (5-9 workflows): `get_world`, `list_categories`, `get_category`
- **Medium** (2-4 workflows): `list_maps`, `get_map`, campaign tools
- **Low** (1 workflow): Specialized tools

---

## Table of Contents

1. [Tool Naming Conventions](#tool-naming-conventions)
2. [Common Patterns](#common-patterns)
3. [Critical Tools](#critical-tools-phase-1)
4. [High Priority Tools](#high-priority-tools-phase-2)
5. [Medium Priority Tools](#medium-priority-tools-phase-3-6)
6. [Low Priority Tools](#low-priority-tools-phase-7-9)
7. [Pydantic Models](#pydantic-models)
8. [Error Handling](#error-handling)
9. [Caching Strategy](#caching-strategy)

---

## Tool Naming Conventions

### Pattern
```
{action}_{resource}[_qualifier]
```

### Actions
- `get`: Retrieve single resource by ID
- `list`: Retrieve collection of resources
- `search`: Query resources with filters
- `create`: Create new resource (write API)
- `update`: Modify existing resource (write API)
- `delete`: Remove resource (write API)

### Examples
- `get_article`: Get single article
- `list_articles`: List articles (optionally filtered)
- `search_articles`: Search articles by text
- `list_world_articles`: List all articles in a world
- `get_user_identity`: Get authenticated user

---

## Common Patterns

### Granularity Parameter
All `get_*` tools support granularity levels:
```python
granularity: int = 1  # Default: standard detail
# 0: Preview (minimal data)
# 1: Standard (full metadata)
# 2: Extended (includes content, where applicable)
```

### Pagination Parameters
All `list_*` tools support pagination:
```python
limit: int = 50    # Max 50
offset: int = 0    # Starting position
```

### Common Response Structure
```json
{
  "success": true,
  "data": {...},       // Single resource
  "entities": [...],   // Collection
  "meta": {
    "total": 100,
    "offset": 0,
    "limit": 50
  }
}
```

---

## Critical Tools (Phase 1)

### 1. `get_article`

**Priority**: Critical (9/10 workflows)
**Endpoint**: `GET /article`
**Cache**: Yes (TTL: 1 hour, granularity-aware)

**Description**: Retrieve a single article with specified detail level.

**Parameters**:
```python
article_id: str           # Article identifier (required)
granularity: int = 1      # Detail level: 0=preview, 1=standard, 2=extended
```

**Returns**: `Article` (Pydantic model)

**Example**:
```python
@mcp.tool()
async def get_article(article_id: str, granularity: int = 1, ctx: Context) -> dict:
    """
    Get article details from World Anvil.

    Use granularity to control detail level:
    - 0: Preview (title, state, basic metadata)
    - 1: Standard (full metadata, no content)
    - 2: Extended (includes full article content)

    Args:
        article_id: Article UUID
        granularity: Detail level (0-2)

    Returns:
        Article data with title, content, world, category, etc.
    """
    client = get_client(ctx)
    article = await client.articles.get(article_id, granularity)
    return article.model_dump()
```

**Response Model**:
```python
class Article(BaseModel):
    id: str
    title: str
    state: str  # "public" | "private" | "draft"
    content: str | None = None  # Only at granularity=2
    url: str
    tags: list[str] = []
    is_wip: bool = False
    update_date: dict
    world: dict  # {id, name, url}
    category: dict | None = None
    template: str | None = None
```

**Errors**:
- `404`: Article not found
- `403`: No access to article (private/guild)
- `401`: Invalid authentication

**Caching**:
```python
cache_key = f"article:{article_id}:{granularity}"
ttl = 3600  # 1 hour
```

---

### 2. `list_articles`

**Priority**: Critical (10/10 workflows)
**Endpoint**: `POST /world/articles`
**Cache**: Yes (TTL: 15 minutes)

**Description**: List articles in a world, optionally filtered by category.

**Parameters**:
```python
world_id: str                    # World identifier (required)
category_id: str | None = None   # Filter by category ("-1" for uncategorized)
limit: int = 50                  # Results per page (max 50)
offset: int = 0                  # Pagination offset
```

**Returns**: `list[ArticleReference]`

**Example**:
```python
@mcp.tool()
async def list_articles(
    world_id: str,
    category_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    List articles in a world, optionally filtered by category.

    Use category_id="-1" to get uncategorized articles (no category or parent).

    Args:
        world_id: World UUID
        category_id: Optional category filter
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of article references with metadata
    """
    client = get_client(ctx)
    articles = await client.worlds.articles(
        world_id,
        category_id=category_id,
        limit=limit,
        offset=offset
    )
    return {"entities": [a.model_dump() for a in articles]}
```

**Response Model**:
```python
class ArticleReference(BaseModel):
    id: str
    title: str
    state: str
    url: str
    excerpt: str | None = None
    update_date: dict
```

**Errors**:
- `404`: World not found
- `403`: No access to world

**Caching**:
```python
cache_key = f"world:{world_id}:articles:{category_id}:{limit}:{offset}"
ttl = 900  # 15 minutes
```

---

### 3. `search_articles`

**Priority**: Critical (8/10 workflows)
**Endpoint**: `POST /article/search` (assumed from workflows)
**Cache**: Yes (TTL: 5 minutes)

**Description**: Search articles by text query across title, content, tags.

**Parameters**:
```python
query: str                       # Search query (required)
world_id: str | None = None      # Optional world filter
limit: int = 50                  # Results per page
offset: int = 0                  # Pagination offset
```

**Returns**: `list[ArticleSearchResult]`

**Example**:
```python
@mcp.tool()
async def search_articles(
    query: str,
    world_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    Search articles by text query.

    Searches across article titles, content, and tags.
    Optionally filter to a specific world.

    Args:
        query: Search text
        world_id: Optional world filter
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of matching articles with relevance scores
    """
    client = get_client(ctx)
    results = await client.articles.search(
        query,
        world_id=world_id,
        limit=limit,
        offset=offset
    )
    return {"entities": [r.model_dump() for r in results]}
```

**Response Model**:
```python
class ArticleSearchResult(BaseModel):
    id: str
    title: str
    excerpt: str
    url: str
    relevance: float  # 0.0-1.0
    world: dict
```

**Errors**:
- `400`: Invalid search query

**Caching**:
```python
cache_key = f"search:articles:{hash(query)}:{world_id}:{limit}:{offset}"
ttl = 300  # 5 minutes
```

---

### 4. `get_world`

**Priority**: Critical (5/10 workflows)
**Endpoint**: `GET /world`
**Cache**: Yes (TTL: 1 hour)

**Description**: Retrieve world metadata and configuration.

**Parameters**:
```python
world_id: str             # World identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `World`

**Example**:
```python
@mcp.tool()
async def get_world(world_id: str, granularity: int = 1, ctx: Context) -> dict:
    """
    Get world details and metadata.

    Args:
        world_id: World UUID
        granularity: Detail level (0-1)

    Returns:
        World data with name, description, configuration, etc.
    """
    client = get_client(ctx)
    world = await client.worlds.get(world_id, granularity)
    return world.model_dump()
```

**Response Model**:
```python
class World(BaseModel):
    id: str
    title: str
    description: str | None = None
    url: str
    is_public: bool
    followers: int = 0
    article_count: int = 0
    map_count: int = 0
    tags: list[str] = []
    configuration: dict = {}
```

---

### 5. `list_categories`

**Priority**: High (3/10 workflows)
**Endpoint**: `POST /world/categories`
**Cache**: Yes (TTL: 30 minutes)

**Description**: List all categories in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[CategoryReference]`

**Example**:
```python
@mcp.tool()
async def list_categories(
    world_id: str,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    List all categories in a world.

    Args:
        world_id: World UUID
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of category references
    """
    client = get_client(ctx)
    categories = await client.worlds.categories(
        world_id,
        limit=limit,
        offset=offset
    )
    return {"entities": [c.model_dump() for c in categories]}
```

**Response Model**:
```python
class CategoryReference(BaseModel):
    id: str
    title: str
    icon: str | None = None
    article_count: int = 0
```

---

### 6. `get_category`

**Priority**: High (3/10 workflows)
**Endpoint**: `GET /category`
**Cache**: Yes (TTL: 30 minutes)

**Description**: Get category details and metadata.

**Parameters**:
```python
category_id: str          # Category identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Category`

**Example**:
```python
@mcp.tool()
async def get_category(category_id: str, granularity: int = 1, ctx: Context) -> dict:
    """
    Get category details.

    Args:
        category_id: Category UUID
        granularity: Detail level (0-1)

    Returns:
        Category data with title, icon, article count, etc.
    """
    client = get_client(ctx)
    category = await client.categories.get(category_id, granularity)
    return category.model_dump()
```

**Response Model**:
```python
class Category(BaseModel):
    id: str
    title: str
    icon: str | None = None
    article_count: int = 0
    world: dict
```

---

### 7. `get_user_identity`

**Priority**: Critical (Session initialization)
**Endpoint**: `GET /identity`
**Cache**: Yes (TTL: 1 day)

**Description**: Get authenticated user information.

**Parameters**: None (uses authentication token)

**Returns**: `User`

**Example**:
```python
@mcp.tool()
async def get_user_identity(ctx: Context) -> dict:
    """
    Get the authenticated user's information.

    Uses the authentication token to identify the user.

    Returns:
        User data with id, username, worlds, etc.
    """
    client = get_client(ctx)
    user = await client.users.identity()
    return user.model_dump()
```

**Response Model**:
```python
class User(BaseModel):
    id: str
    username: str
    profile_url: str
    avatar_url: str | None = None
    is_guild: bool = False
    world_count: int = 0
```

---

### 8. `list_user_worlds`

**Priority**: Critical (Session initialization)
**Endpoint**: `POST /user/worlds`
**Cache**: Yes (TTL: 1 hour)

**Description**: List all worlds owned by a user.

**Parameters**:
```python
user_id: str | None = None   # User ID (default: authenticated user)
limit: int = 50              # Results per page
offset: int = 0              # Pagination offset
```

**Returns**: `list[WorldReference]`

**Example**:
```python
@mcp.tool()
async def list_user_worlds(
    user_id: str | None = None,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    List worlds owned by a user.

    If user_id is not provided, lists authenticated user's worlds.

    Args:
        user_id: Optional user UUID (default: current user)
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of world references
    """
    client = get_client(ctx)
    if user_id is None:
        identity = await client.users.identity()
        user_id = identity.id

    worlds = await client.users.worlds(user_id, limit=limit, offset=offset)
    return {"entities": [w.model_dump() for w in worlds]}
```

**Response Model**:
```python
class WorldReference(BaseModel):
    id: str
    title: str
    url: str
    is_public: bool
    followers: int = 0
```

---

## High Priority Tools (Phase 2)

### 9. `list_maps`

**Priority**: Medium (1/10 workflows - Map Management)
**Endpoint**: `POST /world/maps`
**Cache**: Yes (TTL: 30 minutes)

**Description**: List all maps in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[MapReference]`

**Example**:
```python
@mcp.tool()
async def list_maps(
    world_id: str,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    List all maps in a world.

    Args:
        world_id: World UUID
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of map references
    """
    client = get_client(ctx)
    maps = await client.worlds.maps(world_id, limit=limit, offset=offset)
    return {"entities": [m.model_dump() for m in maps]}
```

**Response Model**:
```python
class MapReference(BaseModel):
    id: str
    title: str
    image_url: str | None = None
    marker_count: int = 0
```

---

### 10. `get_map`

**Priority**: Medium (1/10 workflows)
**Endpoint**: `GET /map`
**Cache**: Yes (TTL: 30 minutes)

**Description**: Get map details including markers.

**Parameters**:
```python
map_id: str               # Map identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Map`

**Example**:
```python
@mcp.tool()
async def get_map(map_id: str, granularity: int = 1, ctx: Context) -> dict:
    """
    Get map details and configuration.

    Args:
        map_id: Map UUID
        granularity: Detail level (0-1)

    Returns:
        Map data with title, image, markers, etc.
    """
    client = get_client(ctx)
    map_data = await client.maps.get(map_id, granularity)
    return map_data.model_dump()
```

**Response Model**:
```python
class Map(BaseModel):
    id: str
    title: str
    image_url: str
    world: dict
    markers: list[dict] = []  # At granularity=1
```

---

### 11. `get_map_markers`

**Priority**: Medium
**Endpoint**: `GET /map/{id}/markers` (assumed)
**Cache**: Yes (TTL: 15 minutes)

**Description**: Get all markers for a specific map.

**Parameters**:
```python
map_id: str          # Map identifier (required)
limit: int = 50      # Results per page
offset: int = 0      # Pagination offset
```

**Returns**: `list[MapMarker]`

**Example**:
```python
@mcp.tool()
async def get_map_markers(
    map_id: str,
    limit: int = 50,
    offset: int = 0,
    ctx: Context
) -> dict:
    """
    Get all markers on a map.

    Args:
        map_id: Map UUID
        limit: Results per page (1-50)
        offset: Pagination offset

    Returns:
        List of map markers with positions and linked articles
    """
    client = get_client(ctx)
    markers = await client.maps.markers(map_id, limit=limit, offset=offset)
    return {"entities": [m.model_dump() for m in markers]}
```

**Response Model**:
```python
class MapMarker(BaseModel):
    id: str
    label: str
    latitude: float
    longitude: float
    icon: str | None = None
    linked_article: dict | None = None  # {id, title, url}
```

---

## Medium Priority Tools (Phase 3-6)

### Campaign & Session Tools

#### 12. `get_campaign`

**Priority**: Medium (2/10 workflows)
**Endpoint**: `GET /campaign` (assumed)
**Cache**: Yes (TTL: 1 hour)

**Description**: Get campaign details and configuration.

**Parameters**:
```python
campaign_id: str          # Campaign identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Campaign`

**Response Model**:
```python
class Campaign(BaseModel):
    id: str
    name: str
    description: str | None = None
    world: dict
    participants: list[dict] = []
    session_count: int = 0
```

---

#### 13. `list_campaign_npcs`

**Priority**: Medium (2/10 workflows)
**Endpoint**: `POST /campaign/{id}/npcs` (assumed)
**Cache**: Yes (TTL: 15 minutes)

**Description**: List NPCs in a campaign.

**Parameters**:
```python
campaign_id: str      # Campaign identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[CampaignNPC]`

**Response Model**:
```python
class CampaignNPC(BaseModel):
    id: str
    name: str
    article_id: str
    role: str | None = None  # "ally", "enemy", "neutral"
    status: str | None = None  # "alive", "dead", "unknown"
```

---

#### 14. `get_campaign_npc`

**Priority**: Medium
**Endpoint**: `GET /campaign/npc/{id}` (assumed)
**Cache**: Yes (TTL: 30 minutes)

**Description**: Get campaign NPC details.

**Parameters**:
```python
npc_id: str               # NPC identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `CampaignNPCDetail`

---

### Secret Management Tools

#### 15. `list_secrets`

**Priority**: Low
**Endpoint**: `POST /world/secrets`
**Cache**: No (sensitive data)

**Description**: List secrets (DM-only content) in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[SecretReference]`

**Response Model**:
```python
class SecretReference(BaseModel):
    id: str
    title: str
    article_id: str | None = None
```

---

#### 16. `get_secret`

**Priority**: Low
**Endpoint**: `GET /secret`
**Cache**: No (sensitive data)

**Description**: Get secret content (DM-only).

**Parameters**:
```python
secret_id: str            # Secret identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Secret`

**Response Model**:
```python
class Secret(BaseModel):
    id: str
    title: str
    content: str | None = None
    article: dict | None = None
```

---

### Timeline & History Tools

#### 17. `list_timelines`

**Priority**: Low
**Endpoint**: `POST /world/timelines`
**Cache**: Yes (TTL: 30 minutes)

**Description**: List timelines in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[TimelineReference]`

---

#### 18. `get_timeline`

**Priority**: Low
**Endpoint**: `GET /timeline`
**Cache**: Yes (TTL: 30 minutes)

**Description**: Get timeline details and events.

**Parameters**:
```python
timeline_id: str          # Timeline identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Timeline`

---

#### 19. `list_histories`

**Priority**: Low
**Endpoint**: `POST /world/histories`
**Cache**: Yes (TTL: 30 minutes)

**Description**: List historical eras in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[HistoryReference]`

---

#### 20. `get_history`

**Priority**: Low
**Endpoint**: `GET /history`
**Cache**: Yes (TTL: 30 minutes)

**Description**: Get historical era details.

**Parameters**:
```python
history_id: str           # History identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `History`

---

### Image Management Tools

#### 21. `list_images`

**Priority**: Low
**Endpoint**: `POST /world/images`
**Cache**: Yes (TTL: 1 hour)

**Description**: List images in a world.

**Parameters**:
```python
world_id: str         # World identifier (required)
limit: int = 50       # Results per page
offset: int = 0       # Pagination offset
```

**Returns**: `list[ImageReference]`

---

#### 22. `get_image`

**Priority**: Low
**Endpoint**: `GET /image`
**Cache**: Yes (TTL: 1 day)

**Description**: Get image metadata and URL.

**Parameters**:
```python
image_id: str             # Image identifier (required)
granularity: int = 1      # Detail level
```

**Returns**: `Image`

---

## Low Priority Tools (Phase 7-9)

### Additional Resource Types

The following tools follow the same patterns as above:

23. `list_chronicles` / `get_chronicle` (World events/logs)
24. `list_canvases` / `get_canvas` (Visual content)
25. `list_notebooks` / `get_notebook` (Personal notes)
26. `list_manuscripts` / `get_manuscript` (Documents)
27. `list_blocks` / `get_block` (Stat blocks)
28. `list_block_folders` / `get_block_folder` (Stat block organization)
29. `list_block_templates` / `get_block_template` (Templates)
30. `list_variables` / `get_variable` (Custom fields)
31. `list_variable_collections` / `get_variable_collection` (Field groups)
32. `list_subscriber_groups` / `get_subscriber_group` (Access control)
33. `list_rpg_systems` / `get_rpg_system` (Game systems)
34. `list_eras` / `get_era` (Time periods)

---

## Pydantic Models

### Base Models

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class BaseReference(BaseModel):
    """Base class for resource references."""
    id: str
    title: str
    url: str

class BaseResource(BaseReference):
    """Base class for full resources."""
    state: str = "public"  # "public" | "private" | "draft"
    update_date: dict
    world: dict | None = None

    @field_validator('update_date')
    @classmethod
    def parse_date(cls, v):
        """Convert World Anvil date format to structured data."""
        return v
```

### Article Models

```python
class ArticleReference(BaseReference):
    """Article list item."""
    state: str
    excerpt: str | None = None
    update_date: dict

class Article(BaseResource):
    """Full article with content."""
    content: str | None = None  # Only at granularity=2
    tags: list[str] = Field(default_factory=list)
    is_wip: bool = False
    category: dict | None = None
    template: str | None = None
    sections: dict = Field(default_factory=dict)
    cover_image: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "The Dragon's Keep",
                "state": "public",
                "content": "A mighty fortress...",
                "url": "https://www.worldanvil.com/w/myworld/a/dragons-keep",
                "tags": ["location", "fortress", "dragons"],
                "world": {"id": "world-123", "name": "My World"}
            }]
        }
    }
```

### World Models

```python
class WorldReference(BaseReference):
    """World list item."""
    is_public: bool
    followers: int = 0

class World(BaseResource):
    """Full world details."""
    description: str | None = None
    is_public: bool
    followers: int = 0
    article_count: int = 0
    map_count: int = 0
    category_count: int = 0
    tags: list[str] = Field(default_factory=list)
    configuration: dict = Field(default_factory=dict)
    genre: str | None = None
    setting: str | None = None
```

### Category Models

```python
class CategoryReference(BaseReference):
    """Category list item."""
    icon: str | None = None
    article_count: int = 0

class Category(BaseResource):
    """Full category details."""
    icon: str | None = None
    article_count: int = 0
    parent_category: dict | None = None
    subcategories: list[dict] = Field(default_factory=list)
```

### User Models

```python
class User(BaseModel):
    """Authenticated user."""
    id: str
    username: str
    profile_url: str
    avatar_url: str | None = None
    is_guild: bool = False
    world_count: int = 0
    subscriber_tier: str | None = None
```

### Map Models

```python
class MapReference(BaseReference):
    """Map list item."""
    image_url: str | None = None
    marker_count: int = 0

class Map(BaseResource):
    """Full map details."""
    image_url: str
    markers: list[dict] = Field(default_factory=list)
    width: int | None = None
    height: int | None = None

class MapMarker(BaseModel):
    """Map marker/pin."""
    id: str
    label: str
    latitude: float
    longitude: float
    icon: str | None = None
    linked_article: dict | None = None
    description: str | None = None
```

---

## Error Handling

### Exception Hierarchy

```python
class WorldAnvilError(Exception):
    """Base exception for all World Anvil errors."""
    pass

class APIError(WorldAnvilError):
    """API-level errors."""
    def __init__(self, status: int, message: str, path: str):
        self.status = status
        self.message = message
        self.path = path
        super().__init__(f"{status}: {message} (path: {path})")

class AuthenticationError(APIError):
    """401 - Invalid or missing credentials."""
    def __init__(self, path: str):
        super().__init__(401, "Invalid authentication credentials", path)

class AuthorizationError(APIError):
    """403 - No access to resource."""
    def __init__(self, path: str):
        super().__init__(403, "Access forbidden", path)

class NotFoundError(APIError):
    """404 - Resource not found."""
    def __init__(self, path: str):
        super().__init__(404, "Resource not found", path)

class ValidationError(APIError):
    """422 - Invalid request data."""
    def __init__(self, path: str, details: dict):
        self.details = details
        super().__init__(422, "Validation failed", path)

class RateLimitError(APIError):
    """429 - Rate limit exceeded."""
    def __init__(self, path: str, retry_after: int | None = None):
        self.retry_after = retry_after
        super().__init__(429, "Rate limit exceeded", path)

class ServerError(APIError):
    """500+ - Server-side errors."""
    def __init__(self, status: int, path: str):
        super().__init__(status, "Server error", path)
```

### Error Response Handling

```python
async def _parse_response(response: httpx.Response, path: str) -> dict:
    """
    Parse World Anvil API response.

    Critical: Check 'success' flag, not just status code!
    API returns 200 OK with {"success": false} for some errors.
    """
    if response.status_code == 401:
        raise AuthenticationError(path)
    elif response.status_code == 403:
        raise AuthorizationError(path)
    elif response.status_code == 404:
        raise NotFoundError(path)
    elif response.status_code == 422:
        data = response.json()
        raise ValidationError(path, data.get('error', {}))
    elif response.status_code == 429:
        retry_after = response.headers.get('Retry-After')
        raise RateLimitError(path, int(retry_after) if retry_after else None)
    elif response.status_code >= 500:
        raise ServerError(response.status_code, path)

    # Check 200 OK responses for success flag
    if response.status_code == 200:
        data = response.json()
        if 'success' not in data:
            raise APIError(200, "Response missing success flag", path)
        if not data['success']:
            error_msg = data.get('error', 'Unknown error')
            raise APIError(200, f"API returned success=false: {error_msg}", path)
        return data

    # Unexpected status
    raise APIError(response.status_code, response.reason_phrase, path)
```

---

## Caching Strategy

### Cache Configuration

```python
from cachetools import TTLCache
from typing import TypeVar, Callable

T = TypeVar('T')

class ResponseCache:
    """Granularity-aware response cache."""

    def __init__(self, maxsize: int = 1000):
        # Different TTLs for different resource types
        self.caches = {
            'article': TTLCache(maxsize=maxsize, ttl=3600),      # 1 hour
            'world': TTLCache(maxsize=100, ttl=3600),             # 1 hour
            'category': TTLCache(maxsize=500, ttl=1800),          # 30 minutes
            'map': TTLCache(maxsize=200, ttl=1800),               # 30 minutes
            'user': TTLCache(maxsize=50, ttl=86400),              # 1 day
            'search': TTLCache(maxsize=500, ttl=300),             # 5 minutes
            'list': TTLCache(maxsize=1000, ttl=900),              # 15 minutes
        }

    def get_cache(self, resource_type: str) -> TTLCache:
        """Get cache for resource type."""
        return self.caches.get(resource_type, self.caches['list'])

    def build_key(self, resource_type: str, resource_id: str, **kwargs) -> str:
        """
        Build cache key with granularity awareness.

        Examples:
        - article:123:2 (article 123 at granularity 2)
        - world:456:articles:category-789:50:0 (world 456 articles, category 789, limit 50, offset 0)
        - search:articles:hash(dragon):world-123:50:0
        """
        parts = [resource_type, resource_id]
        for k, v in sorted(kwargs.items()):
            if v is not None:
                parts.append(f"{k}-{v}")
        return ":".join(parts)

    def get(self, key: str, resource_type: str = 'list') -> dict | None:
        """Get cached response."""
        cache = self.get_cache(resource_type)
        return cache.get(key)

    def set(self, key: str, value: dict, resource_type: str = 'list'):
        """Cache response."""
        cache = self.get_cache(resource_type)
        cache[key] = value

    def invalidate(self, resource_type: str, resource_id: str):
        """Invalidate all cache entries for a resource."""
        cache = self.get_cache(resource_type)
        prefix = f"{resource_type}:{resource_id}"
        keys_to_delete = [k for k in cache.keys() if k.startswith(prefix)]
        for key in keys_to_delete:
            del cache[key]
```

### Cache Usage in Client

```python
class WorldAnvilClient:
    def __init__(self, ctx: Context = None):
        self.cache = ResponseCache(maxsize=1000)

    async def get_article(self, article_id: str, granularity: int = 1) -> Article:
        """Get article with caching."""
        cache_key = self.cache.build_key(
            'article',
            article_id,
            granularity=granularity
        )

        # Check cache
        cached = self.cache.get(cache_key, 'article')
        if cached:
            if self.ctx:
                await self.ctx.info(f"Cache hit: {cache_key}")
            return Article.model_validate(cached)

        # Fetch from API
        if self.ctx:
            await self.ctx.info(f"Fetching article {article_id}")

        data = await self._request('GET', '/article', params={
            'id': article_id,
            'granularity': str(granularity)
        })

        # Cache response
        self.cache.set(cache_key, data, 'article')

        return Article.model_validate(data)
```

### Cache Invalidation Strategy

**On Write Operations** (future):
```python
async def update_article(self, article_id: str, updates: dict) -> Article:
    """Update article and invalidate cache."""
    result = await self._request('PATCH', '/article', ...)

    # Invalidate all cached versions of this article
    self.cache.invalidate('article', article_id)

    # Also invalidate list caches that might contain this article
    # (More sophisticated strategy needed)

    return Article.model_validate(result)
```

---

## Implementation Priority Summary

### Phase 1.1: User & World (Week 1)
- `get_user_identity`
- `list_user_worlds`
- `get_world`

### Phase 1.2: Articles & Categories (Week 2)
- `get_article` ⭐ Critical
- `list_articles` ⭐ Critical
- `search_articles` ⭐ Critical
- `list_categories`
- `get_category`

### Phase 2: Maps & Search (Week 3)
- `list_maps`
- `get_map`
- `get_map_markers`

### Phase 3-6: Campaign & Timeline Tools (Weeks 4-7)
- Campaign management tools
- Timeline/history tools
- Secret management
- Image management

### Phase 7-9: Remaining Resources (Weeks 8-10)
- Chronicles, canvases, notebooks
- Blocks and templates
- Variables and subscriber groups
- RPG systems and eras

---

**Status**: ✅ Tool Specifications Complete
**Date**: 2025-11-28
**Next**: Client Architecture Design
