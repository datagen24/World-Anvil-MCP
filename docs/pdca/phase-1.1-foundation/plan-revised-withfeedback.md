# Phase 1.1: Foundation - User & World Endpoints

**Phase**: 1.1  
**Duration**: 7-8 days  
**Status**: Planning  
**Priority**: Critical (blocks all subsequent work)

---

## Hypothesis

Building the WorldAnvilClient foundation with User and World endpoints will establish:
1. Authentication patterns that work with Grandmaster API credentials
2. Read AND write patterns for all supported operations
3. In-memory caching strategy for session performance
4. MCP ecosystem awareness (detecting companion tools like Notion)
5. Production-ready infrastructure (CI, dev setup, quality gates)

This foundation enables rapid implementation of all subsequent phases.

---

## Expected Outcomes

| Metric | Target | Validation |
|--------|--------|------------|
| Test Coverage | ≥90% | pytest-cov |
| Type Coverage | 100% | mypy --strict |
| CI Pipeline | Green | GitHub Actions |
| API Connectivity | ✓ | Live credential test |
| Write Operations | ✓ | Create/update world metadata |
| Caching | ✓ | In-memory TTL working |
| Dev Setup | <5 min | Fresh clone to running tests |

---

## Endpoints to Implement

### Read Operations
| Endpoint | Method | Tool Name | Priority |
|----------|--------|-----------|----------|
| `/identity` | GET | `get_identity` | Critical |
| `/user` | GET | `get_current_user` | Critical |
| `/user/{id}/worlds` | GET | `list_worlds` | Critical |
| `/world/{id}` | GET | `get_world` | Critical |

### Write Operations (Validate & Implement)
| Endpoint | Method | Tool Name | Priority |
|----------|--------|-----------|----------|
| `/world/{id}` | PATCH | `update_world` | High |

---

## Implementation Schedule

### Day 1: Infrastructure & Client Foundation

**Morning: CI/CD Pipeline**
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install uv
        run: pip install uv
      
      - name: Install dependencies
        run: uv pip install -e ".[dev]" --system
      
      - name: Format check
        run: ruff format --check .
      
      - name: Lint
        run: ruff check .
      
      - name: Type check
        run: mypy src/world_anvil_mcp
      
      - name: Test with coverage
        run: pytest --cov=src/world_anvil_mcp --cov-report=xml --cov-fail-under=85
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
```

**Morning: Dev Setup Scripts**
```bash
# scripts/dev-setup.sh
#!/bin/bash
set -e

echo "🔧 Setting up World Anvil MCP development environment..."

# Create virtual environment
uv venv .venv

# Activate (provide instructions since we can't source in script)
echo "📦 Installing dependencies..."
.venv/bin/pip install -e ".[dev]"

# Install pre-commit hooks
.venv/bin/pre-commit install

echo ""
echo "✅ Setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source .venv/bin/activate  # Linux/macOS"
echo "  .venv\\Scripts\\activate   # Windows"
echo ""
echo "Then verify with:"
echo "  make check  # Run all quality checks"
```

```powershell
# scripts/dev-setup.ps1
$ErrorActionPreference = "Stop"

Write-Host "🔧 Setting up World Anvil MCP development environment..." -ForegroundColor Cyan

# Create virtual environment
uv venv .venv

# Install dependencies
& .venv\Scripts\pip install -e ".[dev]"

# Install pre-commit hooks
& .venv\Scripts\pre-commit install

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment, run:"
Write-Host "  .venv\Scripts\activate"
Write-Host ""
Write-Host "Then verify with:"
Write-Host "  make check  # Run all quality checks"
```

**Afternoon: WorldAnvilClient Foundation**
```python
# src/world_anvil_mcp/api/client.py
"""World Anvil API Client with MCP integration."""

from __future__ import annotations

import asyncio
from typing import Any, TypeVar
from datetime import datetime, timedelta

import httpx
from pydantic import BaseModel

from world_anvil_mcp.api.exceptions import (
    WorldAnvilAuthError,
    WorldAnvilAPIError,
    WorldAnvilRateLimitError,
    WorldAnvilNotFoundError,
)
from world_anvil_mcp.api.cache import InMemoryCache

T = TypeVar("T", bound=BaseModel)


class WorldAnvilClient:
    """Async client for World Anvil Boromir API.
    
    Designed for MCP integration with:
    - Automatic retry with exponential backoff
    - In-memory caching with TTL
    - Granularity parameter support
    - Full CRUD operations where supported
    
    Args:
        app_key: World Anvil application key
        user_token: User authentication token
        base_url: API base URL (default: production)
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts
        cache_ttl: Default cache TTL in seconds
    """
    
    BASE_URL = "https://www.worldanvil.com/api/external/boromir"
    
    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        cache_ttl: int = 300,  # 5 minutes default
    ) -> None:
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout
        self.max_retries = max_retries
        self.cache = InMemoryCache(default_ttl=cache_ttl)
        
        self._client: httpx.AsyncClient | None = None
    
    @property
    def headers(self) -> dict[str, str]:
        """Authentication headers for all requests."""
        return {
            "x-application-key": self.app_key,
            "x-auth-token": self.user_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    
    async def __aenter__(self) -> WorldAnvilClient:
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
        )
        return self
    
    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            self._client = None
    
    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        cache_key: str | None = None,
        cache_ttl: int | None = None,
    ) -> dict[str, Any]:
        """Execute HTTP request with retry and caching.
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: API endpoint path
            params: Query parameters
            json: JSON body for POST/PATCH
            cache_key: Cache key (None to skip caching)
            cache_ttl: Cache TTL override
            
        Returns:
            Response JSON as dictionary
            
        Raises:
            WorldAnvilAuthError: Invalid credentials
            WorldAnvilRateLimitError: Rate limit exceeded
            WorldAnvilNotFoundError: Resource not found
            WorldAnvilAPIError: Other API errors
        """
        # Check cache for GET requests
        if method == "GET" and cache_key:
            cached = self.cache.get(cache_key)
            if cached is not None:
                return cached
        
        if not self._client:
            raise RuntimeError("Client not initialized. Use async context manager.")
        
        last_error: Exception | None = None
        
        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json,
                )
                
                # Handle response codes
                if response.status_code == 401:
                    raise WorldAnvilAuthError("Invalid API credentials")
                elif response.status_code == 403:
                    raise WorldAnvilAuthError("Insufficient permissions")
                elif response.status_code == 404:
                    raise WorldAnvilNotFoundError(f"Resource not found: {path}")
                elif response.status_code == 429:
                    retry_after = int(response.headers.get("Retry-After", 60))
                    raise WorldAnvilRateLimitError(
                        f"Rate limit exceeded. Retry after {retry_after}s",
                        retry_after=retry_after,
                    )
                elif response.status_code >= 400:
                    raise WorldAnvilAPIError(
                        f"API error {response.status_code}: {response.text}"
                    )
                
                data = response.json()
                
                # Cache successful GET responses
                if method == "GET" and cache_key:
                    self.cache.set(cache_key, data, ttl=cache_ttl)
                
                # Invalidate cache on writes
                if method in ("POST", "PATCH", "PUT", "DELETE"):
                    self.cache.invalidate_pattern(path.split("/")[1])
                
                return data
                
            except httpx.TimeoutException as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    
            except httpx.RequestError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        raise WorldAnvilAPIError(f"Request failed after {self.max_retries} attempts: {last_error}")
    
    # -------------------------------------------------------------------------
    # User & Identity Endpoints
    # -------------------------------------------------------------------------
    
    async def get_identity(self) -> dict[str, Any]:
        """Get current user identity.
        
        Returns:
            User identity information
        """
        return await self._request(
            "GET",
            "/identity",
            cache_key="identity",
            cache_ttl=3600,  # 1 hour - rarely changes
        )
    
    async def get_current_user(self, granularity: int = 1) -> dict[str, Any]:
        """Get current user details.
        
        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
            
        Returns:
            User details
        """
        return await self._request(
            "GET",
            "/user",
            params={"granularity": granularity},
            cache_key=f"user:self:{granularity}",
            cache_ttl=3600,
        )
    
    # -------------------------------------------------------------------------
    # World Endpoints
    # -------------------------------------------------------------------------
    
    async def list_worlds(self, granularity: int = 1) -> list[dict[str, Any]]:
        """List all worlds owned by authenticated user.
        
        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
            
        Returns:
            List of world objects
        """
        response = await self._request(
            "GET",
            "/user/worlds",  # Note: This might be /user/{id}/worlds
            params={"granularity": granularity},
            cache_key=f"worlds:list:{granularity}",
            cache_ttl=300,  # 5 minutes
        )
        return response.get("worlds", response) if isinstance(response, dict) else response
    
    async def get_world(self, world_id: str, granularity: int = 1) -> dict[str, Any]:
        """Get world details.
        
        Args:
            world_id: World identifier
            granularity: Detail level
            
        Returns:
            World details
        """
        return await self._request(
            "GET",
            f"/world/{world_id}",
            params={"granularity": granularity},
            cache_key=f"world:{world_id}:{granularity}",
            cache_ttl=300,
        )
    
    async def update_world(
        self,
        world_id: str,
        **updates: Any,
    ) -> dict[str, Any]:
        """Update world metadata.
        
        Args:
            world_id: World identifier
            **updates: Fields to update (name, description, etc.)
            
        Returns:
            Updated world details
        """
        return await self._request(
            "PATCH",
            f"/world/{world_id}",
            json=updates,
        )
```

**Afternoon: Cache Implementation**
```python
# src/world_anvil_mcp/api/cache.py
"""In-memory cache with TTL support."""

from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CacheEntry:
    """Single cache entry with expiration."""
    value: Any
    expires_at: float


class InMemoryCache:
    """Simple in-memory cache with TTL.
    
    Thread-safe for async operations (GIL protected).
    Designed for session-scoped caching during MCP operations.
    
    Args:
        default_ttl: Default time-to-live in seconds
        max_entries: Maximum cache entries (LRU eviction)
    """
    
    def __init__(
        self,
        default_ttl: int = 300,
        max_entries: int = 1000,
    ) -> None:
        self.default_ttl = default_ttl
        self.max_entries = max_entries
        self._cache: dict[str, CacheEntry] = {}
        self._access_order: list[str] = []
    
    def get(self, key: str) -> Any | None:
        """Get cached value if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if expired/missing
        """
        entry = self._cache.get(key)
        if entry is None:
            return None
        
        if time.time() > entry.expires_at:
            del self._cache[key]
            if key in self._access_order:
                self._access_order.remove(key)
            return None
        
        # Update access order for LRU
        if key in self._access_order:
            self._access_order.remove(key)
        self._access_order.append(key)
        
        return entry.value
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        """Set cache value with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (None for default)
        """
        # Evict if at capacity
        while len(self._cache) >= self.max_entries and self._access_order:
            oldest = self._access_order.pop(0)
            self._cache.pop(oldest, None)
        
        ttl = ttl if ttl is not None else self.default_ttl
        self._cache[key] = CacheEntry(
            value=value,
            expires_at=time.time() + ttl,
        )
        self._access_order.append(key)
    
    def invalidate(self, key: str) -> None:
        """Remove specific cache entry.
        
        Args:
            key: Cache key to invalidate
        """
        self._cache.pop(key, None)
        if key in self._access_order:
            self._access_order.remove(key)
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern.
        
        Args:
            pattern: Regex pattern or prefix to match
            
        Returns:
            Number of entries invalidated
        """
        regex = re.compile(pattern)
        keys_to_remove = [k for k in self._cache if regex.search(k)]
        
        for key in keys_to_remove:
            self.invalidate(key)
        
        return len(keys_to_remove)
    
    def clear(self) -> None:
        """Clear entire cache."""
        self._cache.clear()
        self._access_order.clear()
    
    def stats(self) -> dict[str, int]:
        """Get cache statistics.
        
        Returns:
            Dict with entries, max_entries, expired counts
        """
        now = time.time()
        expired = sum(1 for e in self._cache.values() if now > e.expires_at)
        
        return {
            "entries": len(self._cache),
            "max_entries": self.max_entries,
            "expired_pending": expired,
        }
```

**End of Day 1 Deliverables**:
- [ ] CI pipeline passing
- [ ] Dev setup scripts working
- [ ] WorldAnvilClient base class
- [ ] InMemoryCache implementation
- [ ] Exception types defined

---

### Day 2: Exception Types & MCP Ecosystem Detection

**Morning: Exception Hierarchy**
```python
# src/world_anvil_mcp/api/exceptions.py
"""World Anvil API exceptions."""

from __future__ import annotations


class WorldAnvilError(Exception):
    """Base exception for World Anvil API errors."""
    pass


class WorldAnvilAuthError(WorldAnvilError):
    """Authentication or authorization failure."""
    pass


class WorldAnvilAPIError(WorldAnvilError):
    """General API error."""
    
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class WorldAnvilRateLimitError(WorldAnvilError):
    """Rate limit exceeded."""
    
    def __init__(self, message: str, retry_after: int = 60) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class WorldAnvilNotFoundError(WorldAnvilError):
    """Resource not found."""
    pass


class WorldAnvilValidationError(WorldAnvilError):
    """Request validation failed."""
    pass
```

**Morning: MCP Ecosystem Detection**
```python
# src/world_anvil_mcp/ecosystem.py
"""MCP ecosystem detection and integration hints.

This module helps the MCP server detect and suggest complementary tools
that may be available in the user's MCP configuration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp.server import Server


@dataclass
class CompanionTool:
    """Represents a companion MCP tool that enhances World Anvil workflows."""
    
    name: str
    description: str
    use_cases: list[str]
    detection_tools: list[str]  # Tool names to check for
    
    
# Known companion MCPs that enhance World Anvil workflows
COMPANION_MCPS = [
    CompanionTool(
        name="Notion",
        description="Project and campaign planning outside World Anvil",
        use_cases=[
            "Track campaign prep tasks",
            "Player availability scheduling",
            "Session planning checklists",
            "Out-of-world meta notes",
            "Content creation backlog",
        ],
        detection_tools=["notion_search", "notion_create_page", "notion_query_database"],
    ),
    CompanionTool(
        name="Google Drive",
        description="Document storage and sharing",
        use_cases=[
            "Character sheet PDFs",
            "Handout documents",
            "Map image storage",
            "Session recordings",
        ],
        detection_tools=["gdrive_search", "gdrive_upload", "gdrive_read"],
    ),
    CompanionTool(
        name="Calendar",
        description="Session scheduling",
        use_cases=[
            "Schedule game sessions",
            "Track recurring games",
            "Player reminders",
        ],
        detection_tools=["calendar_create_event", "calendar_list_events"],
    ),
    CompanionTool(
        name="Discord",
        description="Player communication",
        use_cases=[
            "Session announcements",
            "Share World Anvil links",
            "Post session summaries",
        ],
        detection_tools=["discord_send_message", "discord_list_channels"],
    ),
]


class EcosystemDetector:
    """Detects available companion MCP tools.
    
    Used to suggest integrations and provide hints about available
    functionality that complements World Anvil.
    """
    
    def __init__(self, available_tools: list[str]) -> None:
        """Initialize with list of available tool names.
        
        Args:
            available_tools: List of tool names from MCP context
        """
        self.available_tools = set(available_tools)
        self._detected: dict[str, CompanionTool] = {}
        self._detect()
    
    def _detect(self) -> None:
        """Detect which companion MCPs are available."""
        for companion in COMPANION_MCPS:
            if any(tool in self.available_tools for tool in companion.detection_tools):
                self._detected[companion.name] = companion
    
    @property
    def available_companions(self) -> list[CompanionTool]:
        """List of detected companion MCPs."""
        return list(self._detected.values())
    
    def has(self, name: str) -> bool:
        """Check if a specific companion is available.
        
        Args:
            name: Companion name (e.g., "Notion")
            
        Returns:
            True if companion is detected
        """
        return name in self._detected
    
    def suggest_for_workflow(self, workflow: str) -> list[tuple[str, str]]:
        """Suggest companion tools for a workflow.
        
        Args:
            workflow: Workflow name (e.g., "session_prep")
            
        Returns:
            List of (tool_name, suggestion) tuples
        """
        suggestions = []
        
        workflow_hints = {
            "session_prep": [
                ("Notion", "Track prep tasks and player notes"),
                ("Google Drive", "Store handout documents"),
            ],
            "campaign_setup": [
                ("Notion", "Create campaign planning database"),
                ("Calendar", "Schedule Session 0"),
            ],
            "session_notes": [
                ("Notion", "Back up session notes"),
                ("Discord", "Post session summary"),
            ],
        }
        
        for tool_name, hint in workflow_hints.get(workflow, []):
            if self.has(tool_name):
                suggestions.append((tool_name, hint))
        
        return suggestions
    
    def get_integration_prompt(self) -> str:
        """Generate a prompt snippet describing available integrations.
        
        Returns:
            Markdown-formatted integration hints
        """
        if not self._detected:
            return ""
        
        lines = ["**Available Integrations:**"]
        for companion in self.available_companions:
            lines.append(f"- **{companion.name}**: {companion.description}")
        
        return "\n".join(lines)
```

**Afternoon: Pydantic Models**
```python
# src/world_anvil_mcp/models/user.py
"""User and Identity models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Identity(BaseModel):
    """User identity from /identity endpoint."""
    
    id: str = Field(..., description="User unique identifier")
    username: str = Field(..., description="Display username")
    
    class Config:
        extra = "allow"  # Allow additional fields from API


class User(BaseModel):
    """User details from /user endpoint."""
    
    id: str = Field(..., description="User unique identifier")
    username: str = Field(..., description="Display username")
    email: str | None = Field(None, description="User email")
    avatar: str | None = Field(None, description="Avatar URL")
    membership: str | None = Field(None, description="Guild membership level")
    created_at: datetime | None = Field(None, description="Account creation date")
    
    class Config:
        extra = "allow"


# src/world_anvil_mcp/models/world.py
"""World models."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WorldSummary(BaseModel):
    """Minimal world reference (granularity 0)."""
    
    id: str = Field(..., description="World unique identifier")
    name: str = Field(..., description="World name")
    
    class Config:
        extra = "allow"


class World(BaseModel):
    """Full world details (granularity 1-2)."""
    
    id: str = Field(..., description="World unique identifier")
    name: str = Field(..., description="World name")
    description: str | None = Field(None, description="World description")
    genre: str | None = Field(None, description="World genre")
    locale: str | None = Field(None, description="World locale/language")
    
    # Counts (granularity 1+)
    article_count: int | None = Field(None, description="Number of articles")
    category_count: int | None = Field(None, description="Number of categories")
    
    # System info
    rpg_system: str | None = Field(None, description="Linked RPG system")
    
    # Timestamps
    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
    
    # Owner reference
    owner: dict[str, Any] | None = Field(None, description="World owner info")
    
    class Config:
        extra = "allow"


class WorldList(BaseModel):
    """Response wrapper for world listing."""
    
    worlds: list[WorldSummary | World] = Field(default_factory=list)
    total: int | None = Field(None)
```

**End of Day 2 Deliverables**:
- [ ] Exception hierarchy complete
- [ ] MCP ecosystem detection working
- [ ] Pydantic models for User, Identity, World
- [ ] Unit tests for cache and exceptions

---

### Days 3-4: User & World Endpoints Implementation

**Day 3: Identity & User Tools**
```python
# src/world_anvil_mcp/tools/user.py
"""User and Identity MCP tools."""

from __future__ import annotations

from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent

from world_anvil_mcp.api.client import WorldAnvilClient
from world_anvil_mcp.models.user import Identity, User


def register_user_tools(server: Server, client: WorldAnvilClient) -> None:
    """Register user-related MCP tools.
    
    Args:
        server: MCP server instance
        client: World Anvil API client
    """
    
    @server.tool()
    async def get_identity() -> list[TextContent]:
        """Get the current authenticated user's identity.
        
        Returns basic identity information to verify API connectivity
        and authentication status.
        
        Returns:
            User identity with id and username
        """
        data = await client.get_identity()
        identity = Identity.model_validate(data)
        
        return [TextContent(
            type="text",
            text=f"Authenticated as: {identity.username} (ID: {identity.id})"
        )]
    
    @server.tool()
    async def get_current_user(
        granularity: int = 1,
    ) -> list[TextContent]:
        """Get detailed information about the current user.
        
        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
            
        Returns:
            User profile including membership level and stats
        """
        data = await client.get_current_user(granularity=granularity)
        user = User.model_validate(data)
        
        lines = [
            f"# User: {user.username}",
            f"- ID: {user.id}",
            f"- Membership: {user.membership or 'Free'}",
        ]
        
        if user.email:
            lines.append(f"- Email: {user.email}")
        
        return [TextContent(type="text", text="\n".join(lines))]
```

**Day 4: World Tools**
```python
# src/world_anvil_mcp/tools/world.py
"""World management MCP tools."""

from __future__ import annotations

from typing import Any

from mcp.server import Server
from mcp.types import Tool, TextContent, Resource

from world_anvil_mcp.api.client import WorldAnvilClient
from world_anvil_mcp.models.world import World, WorldSummary, WorldList


def register_world_tools(server: Server, client: WorldAnvilClient) -> None:
    """Register world-related MCP tools.
    
    Args:
        server: MCP server instance
        client: World Anvil API client
    """
    
    @server.tool()
    async def list_worlds(
        granularity: int = 1,
    ) -> list[TextContent]:
        """List all worlds owned by the authenticated user.
        
        Use this to discover available worlds before accessing
        specific world content.
        
        Args:
            granularity: Detail level (0=minimal, 1=standard, 2=full)
            
        Returns:
            List of worlds with IDs, names, and basic stats
        """
        data = await client.list_worlds(granularity=granularity)
        
        if not data:
            return [TextContent(
                type="text",
                text="No worlds found. Create a world at worldanvil.com first."
            )]
        
        lines = ["# Your Worlds\n"]
        for world_data in data:
            world = WorldSummary.model_validate(world_data)
            lines.append(f"- **{world.name}** (ID: `{world.id}`)")
        
        lines.append(f"\n*Total: {len(data)} worlds*")
        
        return [TextContent(type="text", text="\n".join(lines))]
    
    @server.tool()
    async def get_world(
        world_id: str,
        granularity: int = 1,
    ) -> list[TextContent]:
        """Get detailed information about a specific world.
        
        Args:
            world_id: World unique identifier
            granularity: Detail level (0=minimal, 1=standard, 2=full)
            
        Returns:
            World details including description, genre, and content counts
        """
        data = await client.get_world(world_id, granularity=granularity)
        world = World.model_validate(data)
        
        lines = [
            f"# {world.name}",
            "",
            f"**ID**: `{world.id}`",
            f"**Genre**: {world.genre or 'Not set'}",
        ]
        
        if world.description:
            lines.extend(["", "## Description", world.description])
        
        if world.article_count is not None:
            lines.extend([
                "",
                "## Content",
                f"- Articles: {world.article_count}",
                f"- Categories: {world.category_count or 0}",
            ])
        
        if world.rpg_system:
            lines.append(f"- RPG System: {world.rpg_system}")
        
        return [TextContent(type="text", text="\n".join(lines))]
    
    @server.tool()
    async def update_world(
        world_id: str,
        name: str | None = None,
        description: str | None = None,
        genre: str | None = None,
    ) -> list[TextContent]:
        """Update world metadata.
        
        Args:
            world_id: World unique identifier
            name: New world name (optional)
            description: New description (optional)
            genre: New genre (optional)
            
        Returns:
            Updated world information
        """
        updates = {}
        if name is not None:
            updates["name"] = name
        if description is not None:
            updates["description"] = description
        if genre is not None:
            updates["genre"] = genre
        
        if not updates:
            return [TextContent(
                type="text",
                text="No updates specified. Provide name, description, or genre to update."
            )]
        
        data = await client.update_world(world_id, **updates)
        world = World.model_validate(data)
        
        return [TextContent(
            type="text",
            text=f"✅ Updated world: **{world.name}** (`{world.id}`)"
        )]
    
    # -------------------------------------------------------------------------
    # MCP Resources
    # -------------------------------------------------------------------------
    
    @server.resource("world://{world_id}")
    async def world_resource(world_id: str) -> Resource:
        """MCP resource for world context.
        
        Provides world details as context for LLM operations.
        """
        data = await client.get_world(world_id, granularity=2)
        world = World.model_validate(data)
        
        return Resource(
            uri=f"world://{world_id}",
            name=world.name,
            description=world.description or f"World: {world.name}",
            mimeType="application/json",
            text=world.model_dump_json(indent=2),
        )
```

**End of Days 3-4 Deliverables**:
- [ ] 4 read tools implemented
- [ ] 1 write tool implemented (update_world)
- [ ] MCP resource for world context
- [ ] Integration tests passing
- [ ] Live API validation complete

---

### Days 5-6: Testing & Write API Validation

**Day 5: Comprehensive Testing**
```python
# tests/endpoints/test_user.py
"""Tests for user endpoints."""

import pytest
from httpx import Response

from world_anvil_mcp.api.client import WorldAnvilClient
from world_anvil_mcp.api.exceptions import WorldAnvilAuthError


class TestIdentityEndpoint:
    """Tests for /identity endpoint."""
    
    async def test_get_identity_success(self, mock_client, respx_mock):
        """Should return user identity."""
        respx_mock.get("/identity").mock(return_value=Response(
            200,
            json={"id": "123", "username": "testuser"}
        ))
        
        result = await mock_client.get_identity()
        
        assert result["id"] == "123"
        assert result["username"] == "testuser"
    
    async def test_get_identity_auth_error(self, mock_client, respx_mock):
        """Should raise auth error on 401."""
        respx_mock.get("/identity").mock(return_value=Response(401))
        
        with pytest.raises(WorldAnvilAuthError):
            await mock_client.get_identity()
    
    async def test_get_identity_cached(self, mock_client, respx_mock):
        """Should return cached result on second call."""
        respx_mock.get("/identity").mock(return_value=Response(
            200,
            json={"id": "123", "username": "testuser"}
        ))
        
        # First call
        await mock_client.get_identity()
        # Second call - should use cache
        result = await mock_client.get_identity()
        
        assert respx_mock.calls.call_count == 1  # Only one HTTP call
        assert result["id"] == "123"


# tests/endpoints/test_world.py
"""Tests for world endpoints."""

import pytest
from httpx import Response

from world_anvil_mcp.api.client import WorldAnvilClient


class TestListWorlds:
    """Tests for /user/worlds endpoint."""
    
    async def test_list_worlds_success(self, mock_client, respx_mock):
        """Should return list of worlds."""
        respx_mock.get("/user/worlds").mock(return_value=Response(
            200,
            json=[
                {"id": "w1", "name": "Test World 1"},
                {"id": "w2", "name": "Test World 2"},
            ]
        ))
        
        result = await mock_client.list_worlds()
        
        assert len(result) == 2
        assert result[0]["id"] == "w1"
    
    async def test_list_worlds_empty(self, mock_client, respx_mock):
        """Should handle empty world list."""
        respx_mock.get("/user/worlds").mock(return_value=Response(
            200,
            json=[]
        ))
        
        result = await mock_client.list_worlds()
        
        assert result == []


class TestUpdateWorld:
    """Tests for PATCH /world/{id} endpoint."""
    
    async def test_update_world_name(self, mock_client, respx_mock):
        """Should update world name."""
        respx_mock.patch("/world/w1").mock(return_value=Response(
            200,
            json={"id": "w1", "name": "Updated Name"}
        ))
        
        result = await mock_client.update_world("w1", name="Updated Name")
        
        assert result["name"] == "Updated Name"
    
    async def test_update_world_invalidates_cache(self, mock_client, respx_mock):
        """Should invalidate world cache after update."""
        respx_mock.get("/world/w1").mock(return_value=Response(
            200,
            json={"id": "w1", "name": "Original"}
        ))
        respx_mock.patch("/world/w1").mock(return_value=Response(
            200,
            json={"id": "w1", "name": "Updated"}
        ))
        
        # Cache the world
        await mock_client.get_world("w1")
        
        # Update should invalidate
        await mock_client.update_world("w1", name="Updated")
        
        # Next get should hit API, not cache
        await mock_client.get_world("w1")
        
        assert respx_mock.calls.call_count == 3
```

**Day 6: Live API Validation & Write API Confirmation**
```python
# tests/integration/test_live_api.py
"""Live API integration tests.

These tests require valid API credentials and hit the real World Anvil API.
Run with: pytest tests/integration/ -m live --run-live

Environment variables required:
  WORLD_ANVIL_APP_KEY
  WORLD_ANVIL_USER_TOKEN
"""

import os
import pytest

from world_anvil_mcp.api.client import WorldAnvilClient


# Skip all tests in this module if credentials not available
pytestmark = pytest.mark.live


@pytest.fixture
async def live_client():
    """Create client with real credentials."""
    app_key = os.environ.get("WORLD_ANVIL_APP_KEY")
    user_token = os.environ.get("WORLD_ANVIL_USER_TOKEN")
    
    if not app_key or not user_token:
        pytest.skip("Live API credentials not configured")
    
    async with WorldAnvilClient(
        app_key=app_key,
        user_token=user_token,
    ) as client:
        yield client


class TestLiveAPI:
    """Live API validation tests."""
    
    async def test_identity_endpoint(self, live_client):
        """Verify /identity endpoint works with real credentials."""
        result = await live_client.get_identity()
        
        assert "id" in result
        assert "username" in result
        print(f"✅ Authenticated as: {result['username']}")
    
    async def test_list_worlds(self, live_client):
        """Verify world listing works."""
        result = await live_client.list_worlds(granularity=0)
        
        assert isinstance(result, list)
        print(f"✅ Found {len(result)} worlds")
        
        if result:
            print(f"   First world: {result[0].get('name', 'Unknown')}")
    
    async def test_get_world_detail(self, live_client):
        """Verify world detail retrieval."""
        worlds = await live_client.list_worlds(granularity=0)
        
        if not worlds:
            pytest.skip("No worlds available for testing")
        
        world_id = worlds[0]["id"]
        result = await live_client.get_world(world_id, granularity=2)
        
        assert "id" in result
        assert "name" in result
        print(f"✅ Retrieved world: {result['name']}")
    
    async def test_write_api_availability(self, live_client):
        """Test if write API is available (non-destructive)."""
        worlds = await live_client.list_worlds(granularity=0)
        
        if not worlds:
            pytest.skip("No worlds available for testing")
        
        world_id = worlds[0]["id"]
        original = await live_client.get_world(world_id)
        original_name = original["name"]
        
        # Try to update with same name (no actual change)
        try:
            result = await live_client.update_world(
                world_id,
                name=original_name,  # Same name = no-op
            )
            print(f"✅ Write API available! Updated world: {result.get('name')}")
            assert True
        except Exception as e:
            if "403" in str(e) or "405" in str(e):
                print(f"⚠️ Write API not available: {e}")
                pytest.skip("Write API not available for this endpoint")
            raise


# Document findings
"""
# Write API Validation Results

## Endpoint: PATCH /world/{id}

### Test Date: [Date of test]

### Result: [PASS/FAIL/NOT_AVAILABLE]

### Notes:
- 
- 
- 

### Permissions Required:
- 

### Observed Behavior:
- 
"""
```

**End of Days 5-6 Deliverables**:
- [ ] Unit tests: 90%+ coverage
- [ ] Integration tests passing
- [ ] Live API validation passing
- [ ] Write API documented (availability, permissions)
- [ ] `docs/research/write-api-validation.md` created

---

### Days 7-8: Polish & Phase Completion

**Day 7: Documentation & Getting Started**
```markdown
# docs/GETTING_STARTED.md

# Getting Started with World Anvil MCP

This guide will get you from zero to a working development environment in under 5 minutes.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- World Anvil account with Grandmaster guild membership
- World Anvil API credentials

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/datagen24/World-Anvil-MCP.git
cd World-Anvil-MCP
```

### 2. Run Setup Script

**Linux/macOS:**
```bash
./scripts/dev-setup.sh
source .venv/bin/activate
```

**Windows:**
```powershell
.\scripts\dev-setup.ps1
.venv\Scripts\activate
```

### 3. Configure Credentials

Create a `.env` file:
```bash
WORLD_ANVIL_APP_KEY=your_application_key_here
WORLD_ANVIL_USER_TOKEN=your_user_token_here
```

Get your credentials:
- **Application Key**: [Request via World Anvil](https://www.worldanvil.com/api/auth/key)
- **User Token**: [Generate in your account](https://www.worldanvil.com/api/auth/key)

### 4. Verify Installation

```bash
# Run all quality checks
make check

# Run tests
make test

# Verify API connectivity
make test-live  # Requires .env credentials
```

## Common Commands

| Command | Description |
|---------|-------------|
| `make check` | Run all quality checks (format, lint, typecheck) |
| `make test` | Run unit tests |
| `make test-cov` | Run tests with coverage report |
| `make format` | Auto-format code |
| `make lint` | Run linter with auto-fix |

## Using the MCP Server

### With Claude Desktop

Add to your MCP settings:
```json
{
  "mcpServers": {
    "world-anvil": {
      "command": "world-anvil-mcp",
      "env": {
        "WORLD_ANVIL_APP_KEY": "your_key",
        "WORLD_ANVIL_USER_TOKEN": "your_token"
      }
    }
  }
}
```

### Standalone

```bash
# Start MCP server
world-anvil-mcp

# Or with Python
python -m world_anvil_mcp.server
```

## Troubleshooting

### "Invalid API credentials"
- Verify your `.env` file exists and contains valid credentials
- Check that you have Grandmaster guild membership or above

### "Rate limit exceeded"
- The client automatically retries with exponential backoff
- If persistent, wait 60 seconds before retrying

### Tests failing
```bash
# Check specific test
pytest tests/path/to/test.py -v

# Run with debug output
pytest -v --tb=long
```

## Next Steps

- Read the [API Reference](claudedocs/API_REFERENCE.md)
- Explore [Workflows](docs/workflows/README.md)
- Check the [Architecture](claudedocs/DESIGN_SPECIFICATION.md)
```

**Day 8: Retrospective & Phase 1.2 Prep**

Create Phase 1.1 retrospective and prepare for Articles & Categories.

**End of Days 7-8 Deliverables**:
- [ ] GETTING_STARTED.md complete
- [ ] All documentation updated
- [ ] Phase 1.1 retrospective complete
- [ ] Phase 1.2 plan drafted
- [ ] Patterns extracted to docs/patterns/

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API credentials invalid | Low | Critical | Day 2 live validation test |
| Write API not available | Medium | High | Day 6 validation; fallback to read-only MVP |
| Rate limiting during tests | Medium | Medium | Mock API for unit tests; throttle live tests |
| pywaclient patterns don't transfer | Low | Medium | Patterns already documented in Phase 0 |
| Endpoint paths differ from docs | Medium | Medium | Live validation confirms actual paths |

---

## Success Criteria

### Phase 1.1 Complete When:

- [ ] CI pipeline green on every push
- [ ] 4 read tools + 1 write tool implemented
- [ ] Test coverage ≥ 90%
- [ ] Type coverage: 100% (mypy --strict passes)
- [ ] Live API validation passing
- [ ] Write API capabilities documented
- [ ] Getting Started guide works for fresh clone
- [ ] MCP ecosystem detection working
- [ ] Phase 1.1 retrospective complete
- [ ] Phase 1.2 plan created

### Metrics to Track:

| Metric | Target | Actual |
|--------|--------|--------|
| Test Coverage | ≥90% | TBD |
| Type Coverage | 100% | TBD |
| CI Build Time | <5min | TBD |
| API Latency (cached) | <50ms | TBD |
| API Latency (uncached) | <500ms | TBD |
| Dev Setup Time | <5min | TBD |

---

## Appendix: MCP Ecosystem Integration Pattern

```python
# Example: Using ecosystem detection in a tool

@server.tool()
async def prepare_session(world_id: str) -> list[TextContent]:
    """Prepare materials for an upcoming D&D session.
    
    Gathers world content and suggests companion tool integrations.
    """
    # Load world content
    world = await client.get_world(world_id, granularity=2)
    
    # Check for companion tools
    ecosystem = EcosystemDetector(available_tools)
    suggestions = ecosystem.suggest_for_workflow("session_prep")
    
    lines = [
        f"# Session Prep: {world['name']}",
        "",
        "## World Content Loaded",
        f"- Articles: {world.get('article_count', 0)}",
        f"- Categories: {world.get('category_count', 0)}",
    ]
    
    if suggestions:
        lines.extend([
            "",
            "## 💡 Available Integrations",
            "",
        ])
        for tool_name, hint in suggestions:
            lines.append(f"- **{tool_name}**: {hint}")
    
    return [TextContent(type="text", text="\n".join(lines))]
```

This pattern allows the World Anvil MCP to suggest (but not require) companion integrations, keeping the core functionality independent while enabling powerful compositions.
