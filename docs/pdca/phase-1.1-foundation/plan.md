# Plan: Phase 1.1 - Foundation & API Validation (INTEGRATED)

**Date**: 2025-11-28 (Integrated: Structural + Code Examples)
**Phase**: Phase 1.1
**Estimated Duration**: 7-8 days
**Assignee**: PM Agent → backend-architect + quality-engineer

---

## Revision Notes

**Integration Summary**:
This plan combines:
1. ✅ Structural improvements from user feedback (CI on Day 1, 7-8 days, write validation)
2. ✅ Detailed code implementations and examples
3. ✅ **Spec-Compliant MCP Ecosystem Detection** (aligns with `docs/specs/MCP-ECOSYSTEM-SPEC.md`)
4. ✅ Complete test suites, CI/CD pipelines, and dev setup automation

**Latest Revision** (2025-11-29):
- ✅ Updated ecosystem detection to match `MCP-ECOSYSTEM-SPEC.md` exactly
- ✅ Added `IntegrationTier` enum (CRITICAL, RECOMMENDED, OPTIONAL)
- ✅ Enhanced `CompanionMCP` dataclass with tier, capabilities, workflow suggestions
- ✅ Added 6 companions: **Foundry VTT**, **Context Engine** (Tier 1), Dropbox, Notion (Tier 2), Discord, Calendar (Tier 3)
- ✅ Clarified **Context Engine is SEPARATE project** (detection only in Phase 1.1)
- ✅ Added References section linking to both specification documents

**Key Changes from Original Plan**:
1. ✅ CI/CD moved to Day 1 (mandatory, not optional)
2. ✅ Client foundation gets dedicated Day 1 (not rushed with endpoints)
3. ✅ Write API validation spike added (Days 6-7)
4. ✅ Explicit caching decision point (Day 4)
5. ✅ Dev setup scripts added to Day 1
6. ✅ Timeline extended to 7-8 days (realistic for foundation work)
7. ✅ **Spec-compliant MCP ecosystem detection** with integration tiers

**User Feedback Addressed**:
- Write API uncertainty → Day 6-7 validation spike resolves before Phase 2
- CI/CD optional → Now mandatory on Day 1
- Backlog unscheduled → Getting Started docs, dev scripts on Day 1
- Client foundation timing → Full Day 1 dedicated to foundation only

---

## Hypothesis

### What to Implement

Phase 1.1 establishes **production-ready foundation** for the World Anvil MCP Server:

**Day 1: Infrastructure & Client Foundation** (Critical Infrastructure)
1. **CI/CD Pipeline**: GitHub Actions with quality gates (mandatory)
2. **Dev Setup Scripts**: Bash and PowerShell automation for contributors
3. **WorldAnvilClient Core**: Authentication, base architecture, async client
4. **Cache Implementation**: In-memory TTL cache with LRU eviction
5. **Exception Hierarchy**: Complete error types with retry logic

**Day 2: User Models & Ecosystem Detection** (Foundation Components)
6. **Exception Types**: Complete hierarchy with proper error handling
7. **MCP Ecosystem Detection**: Discover companion tools (Notion, Google Drive, etc.)
8. **Pydantic Models**: User, Identity with validation
9. **Unit Tests**: Cache, exceptions, models

**Days 3-4: User & Identity Endpoints** (Auth Validation)
10. **User Endpoints**: `/identity`, `/user` for authentication
11. **Live API Testing**: Validate credentials work before heavy implementation
12. **MCP Tools**: Identity and user tools with ecosystem hints

**Days 4-5: World Endpoints** (Core Content Access)
13. **World Endpoints**: `/user/worlds`, `/world/{id}` with granularity
14. **World Tools**: List, get, update with MCP resources
15. **Rate Limiting**: Token bucket algorithm (60 req/min)

**Days 6-7: Write API Validation & Polish** (Risk Mitigation)
16. **Write API Spike**: Test CRUD capabilities on World endpoint
17. **Documentation**: Write API findings for Phase 2 planning
18. **Retrospective**: PDCA completion, pattern extraction
19. **Getting Started**: Complete documentation with examples

### Why This Approach

**Foundation-First Strategy** (Day 1 dedicated):
- Building client foundation is the real complexity
- CI/CD from Day 1 catches issues immediately
- Dev scripts unblock contributors from start
- In-memory cache provides session performance
- Ecosystem detection enables intelligent integrations

**Context Engine Clarification**:
- Context Engine is a **SEPARATE MCP server project** (not part of Phase 1.1)
- Provides semantic search over TTRPG reference materials (D&D SRD, mythology, etc.)
- Phase 1.1 implements DETECTION ONLY (recognizes if Context Engine is available)
- Full Context Engine specification: `docs/specs/CONTEXT-ENGINE-SPEC.md`
- Implementation roadmap: Future phase (TBD)

**Auth-Validation-Early** (Days 2-3):
- Validate API credentials work before heavy implementation
- User endpoints simpler than content endpoints (good warmup)
- Establishes authentication patterns for all future endpoints

**Write API Clarity** (Days 6-7):
- Resolves "Future" ambiguity before Phase 2 commitment
- Tests actual CRUD capabilities vs OpenAPI speculation
- Documents findings for informed Phase 2 planning
- Prevents wasted effort if writes unavailable

**Explicit Decisions** (No ambiguity):
- Caching: In-memory TTL with LRU eviction (Day 1)
- CI/CD: Mandatory (Day 1, not optional)
- Write API: Validated (Day 6-7 spike)
- Ecosystem: Detection for companion MCP tools

### Key Decisions

**Architecture**:
- Async-first design (all I/O uses `async/await`)
- httpx.AsyncClient for connection pooling and timeout management
- Pydantic v2 for models and validation
- In-memory cache with LRU eviction for session performance
- MCP ecosystem detection for companion tool awareness

**Technology**:
- httpx ≥0.27.0 for async HTTP
- Pydantic v2 for models and validation
- cachetools for in-memory TTL caching with LRU
- GitHub Actions for CI/CD
- pytest with async support, respx for HTTP mocking

**Patterns**:
- Repository pattern (WorldAnvilClient coordinates methods)
- Token bucket algorithm for rate limiting (60 req/min)
- Exponential backoff with jitter for retries
- Response caching with granularity-aware keys
- Companion tool detection for ecosystem awareness

---

## Expected Outcomes

### Functional Requirements

**Core Infrastructure** (Day 1):
- [ ] CI/CD pipeline (GitHub Actions) - **MANDATORY**
- [ ] Dev setup scripts (bash and PowerShell)
- [ ] WorldAnvilClient with authentication
- [ ] InMemoryCache with LRU eviction
- [ ] Exception hierarchy complete

**Ecosystem & Models** (Day 2):
- [ ] MCP ecosystem detection working
- [ ] Pydantic models (User, Identity, World)
- [ ] Unit tests for cache, exceptions, models

**User & Identity Endpoints** (Days 3-4):
- [ ] `get_identity()` - Get user identity
- [ ] `get_current_user()` - Retrieve authenticated user
- [ ] Live API connectivity validated
- [ ] MCP tools functional with ecosystem hints

**World Endpoints** (Days 4-5):
- [ ] `list_worlds()` - List user's worlds
- [ ] `get_world(world_id, granularity)` - Get world details
- [ ] `update_world()` - Update world metadata (write validation)
- [ ] Rate limiting enforced (60 req/min)
- [ ] MCP resource: `world://{world_id}`

**Write API Validation** (Days 6-7):
- [ ] Write capabilities tested on World endpoint
- [ ] Findings documented (`docs/research/write-api-validation.md`)
- [ ] Go/no-go decision for Phase 2 writes
- [ ] Getting Started guide complete
- [ ] Phase 1.1 retrospective complete

### Quality Metrics

| Metric | Target | Validation |
|--------|--------|------------|
| **CI Passing** | 100% | GitHub Actions green |
| **Test Coverage** | ≥90% | pytest-cov report |
| **Type Coverage** | 100% | mypy strict passes |
| **API Connectivity** | ✓ | Live credential test (Day 3) |
| **Docs Complete** | ✓ | Getting Started works |
| **Write API Assessed** | ✓ | Validation doc created |
| **Dev Setup Time** | <5 min | Fresh clone to running tests |
| **Performance** | <500ms | Uncached request response time |

### Success Criteria

**Functional**:
- ✅ All infrastructure complete (CI, scripts, cache, client)
- ✅ MCP ecosystem detection working
- ✅ User/Identity endpoints operational
- ✅ World endpoints operational with caching
- ✅ Live API validation successful
- ✅ Write API capabilities documented

**Quality**:
- ✅ CI/CD pipeline passing from Day 1
- ✅ Test coverage ≥90%
- ✅ Type coverage 100%
- ✅ Documentation 100% (all public APIs)
- ✅ Dev setup <5 minutes

**Process**:
- ✅ PDCA cycle complete
- ✅ Learnings documented
- ✅ Patterns formalized
- ✅ Zero technical debt
- ✅ Phase 2 informed by write API findings

---

## Implementation Approach

### Day 1: Infrastructure & Client Foundation

**Duration**: 1 full day
**Focus**: CI/CD, dev scripts, client foundation, cache implementation

**Morning: CI/CD Pipeline** (MANDATORY)

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
    - In-memory caching with TTL and LRU eviction
    - Granularity parameter support (STRING "0"-"3")
    - Full CRUD operations where supported

    Args:
        app_key: World Anvil application key
        user_token: User authentication token
        base_url: API base URL (default: production)
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts
        cache_ttl: Default cache TTL in seconds

    Example:
        >>> async with WorldAnvilClient(app_key, user_token) as client:
        ...     identity = await client.get_identity()
        ...     print(f"Authenticated as: {identity['username']}")
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
        """Authentication headers for all requests.

        IMPORTANT: World Anvil uses lowercase header names:
        - x-application-key (NOT X-Application-Key)
        - x-auth-token (NOT X-Auth-Token)
        """
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
            WorldAnvilAuthError: Invalid credentials (401, 403)
            WorldAnvilRateLimitError: Rate limit exceeded (429)
            WorldAnvilNotFoundError: Resource not found (404)
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
            User identity information (id, username)

        Example:
            >>> identity = await client.get_identity()
            >>> print(f"User ID: {identity['id']}")
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
            User details including membership, stats, etc.
        """
        return await self._request(
            "GET",
            "/user",
            params={"granularity": str(granularity)},  # MUST be string!
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
            "/user/worlds",
            params={"granularity": str(granularity)},  # MUST be string!
            cache_key=f"worlds:list:{granularity}",
            cache_ttl=300,  # 5 minutes
        )
        return response.get("worlds", response) if isinstance(response, dict) else response

    async def get_world(self, world_id: str, granularity: int = 1) -> dict[str, Any]:
        """Get world details.

        Args:
            world_id: World identifier
            granularity: Detail level (0=minimal, 1=standard, 2=full)

        Returns:
            World details
        """
        return await self._request(
            "GET",
            f"/world/{world_id}",
            params={"granularity": str(granularity)},  # MUST be string!
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
            **updates: Fields to update (name, description, genre, etc.)

        Returns:
            Updated world details

        Example:
            >>> result = await client.update_world(
            ...     "world123",
            ...     name="New Name",
            ...     description="Updated description"
            ... )
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
"""In-memory cache with TTL and LRU eviction."""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    """Single cache entry with expiration."""
    value: Any
    expires_at: float


class InMemoryCache:
    """Simple in-memory cache with TTL and LRU eviction.

    Thread-safe for async operations (GIL protected).
    Designed for session-scoped caching during MCP operations.

    Features:
    - TTL-based expiration
    - LRU eviction when max_entries reached
    - Pattern-based invalidation
    - Statistics tracking

    Args:
        default_ttl: Default time-to-live in seconds
        max_entries: Maximum cache entries (LRU eviction)

    Example:
        >>> cache = InMemoryCache(default_ttl=300, max_entries=1000)
        >>> cache.set("key", {"data": "value"})
        >>> result = cache.get("key")  # Returns {"data": "value"}
        >>> # After 300 seconds
        >>> result = cache.get("key")  # Returns None (expired)
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
        # Evict oldest if at capacity (LRU)
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
- [ ] `.github/workflows/ci.yml` (CI pipeline)
- [ ] `scripts/dev-setup.sh` (bash setup script)
- [ ] `scripts/dev-setup.ps1` (PowerShell setup script)
- [ ] `src/world_anvil_mcp/api/client.py` (WorldAnvilClient)
- [ ] `src/world_anvil_mcp/api/cache.py` (InMemoryCache)
- [ ] Unit tests for cache
- [ ] CI pipeline passing

**Quality Gate**: CI pipeline green (even with minimal code)

---

### Day 2: Exception Types & MCP Ecosystem Detection

**Duration**: 1 full day
**Focus**: Exception hierarchy, ecosystem detection, Pydantic models

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

**Morning: MCP Ecosystem Detection** (NEW FEATURE - Spec Compliant)

```python
# src/world_anvil_mcp/ecosystem/detector.py
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

    Example:
        >>> detector = EcosystemDetector(available_tools=["foundry_get_actors"])
        >>> detector.critical_companions  # [Foundry VTT]
        >>> print(detector.get_ecosystem_status())  # Markdown status report
    """

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
        """Get detected critical tier companions.

        Returns:
            List of CRITICAL tier companions (Foundry VTT, Context Engine)
        """
        return [
            c for c in self._detected.values()
            if c.tier == IntegrationTier.CRITICAL
        ]

    @property
    def all_companions(self) -> list[CompanionMCP]:
        """Get all detected companions."""
        return list(self._detected.values())

    def has(self, name: str) -> bool:
        """Check if specific companion is available.

        Args:
            name: Companion name (e.g., "Foundry VTT")

        Returns:
            True if companion is detected
        """
        return name in self._detected

    def get(self, name: str) -> CompanionMCP | None:
        """Get companion by name.

        Args:
            name: Companion name

        Returns:
            CompanionMCP object or None if not detected
        """
        return self._detected.get(name)

    def suggest_for_workflow(
        self,
        workflow: str,
    ) -> list[tuple[str, str, CompanionMCP]]:
        """Get integration suggestions for a workflow.

        Args:
            workflow: Workflow identifier (e.g., "session_prep")

        Returns:
            List of (companion_name, suggestion, companion_object) tuples,
            sorted by tier (critical first)

        Example:
            >>> suggestions = detector.suggest_for_workflow("session_prep")
            >>> for name, hint, companion in suggestions:
            ...     print(f"{name}: {hint}")
            Foundry VTT: Sync tonight's NPCs to Foundry
            Notion: Check prep checklist in Notion
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
        """Generate markdown status report of ecosystem.

        Returns:
            Markdown-formatted status showing detected companions by tier,
            with warnings for missing critical integrations.

        Example:
            ## 🔌 MCP Ecosystem Status

            ### ✅ Critical Integrations
            - **Foundry VTT**: Virtual tabletop for live gameplay

            ### ⚠️ Missing Critical Integrations
            - **Context Engine**: Semantic search over TTRPG references
              - Install: (separate project - see CONTEXT-ENGINE-SPEC.md)
        """
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

**Afternoon: Pydantic Models**

```python
# src/world_anvil_mcp/models/user.py
"""User and Identity models."""

from __future__ import annotations

from datetime import datetime

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
```

```python
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
```

**End of Day 2 Deliverables**:
- [ ] `src/world_anvil_mcp/api/exceptions.py` (exception hierarchy)
- [ ] `src/world_anvil_mcp/ecosystem/detector.py` (spec-compliant ecosystem detection)
- [ ] `src/world_anvil_mcp/models/user.py` (User, Identity models)
- [ ] `src/world_anvil_mcp/models/world.py` (World models)
- [ ] Unit tests for exceptions, ecosystem (all 3 tiers), models
- [ ] Integration tier support: CRITICAL (Foundry VTT, Context Engine), RECOMMENDED (Dropbox, Notion), OPTIONAL (Discord, Calendar)

**Quality Gate**: All tests passing, ≥90% coverage

**Note**: Context Engine is documented as Tier 1 CRITICAL but is a SEPARATE project (see `docs/specs/CONTEXT-ENGINE-SPEC.md`). Phase 1.1 only implements detection, not Context Engine itself.

---

### Days 3-4: User & Identity Endpoints Implementation

**Duration**: 2 days
**Focus**: User endpoints, MCP tools, live API validation

**Day 3: Identity & User Tools**

```python
# src/world_anvil_mcp/tools/user.py
"""User and Identity MCP tools."""

from __future__ import annotations

from mcp.server import Server
from mcp.types import TextContent

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

**Day 4: World Tools with Ecosystem Hints**

```python
# src/world_anvil_mcp/tools/world.py
"""World management MCP tools."""

from __future__ import annotations

from mcp.server import Server
from mcp.types import TextContent, Resource

from world_anvil_mcp.api.client import WorldAnvilClient
from world_anvil_mcp.models.world import World, WorldSummary
from world_anvil_mcp.ecosystem import EcosystemDetector


def register_world_tools(
    server: Server,
    client: WorldAnvilClient,
    ecosystem: EcosystemDetector,
) -> None:
    """Register world-related MCP tools.

    Args:
        server: MCP server instance
        client: World Anvil API client
        ecosystem: Ecosystem detector for companion tools
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

        # Add ecosystem hints if available
        integration_hint = ecosystem.get_integration_prompt()
        if integration_hint:
            lines.extend(["\n---\n", integration_hint])

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
- [ ] `src/world_anvil_mcp/tools/user.py` (user tools)
- [ ] `src/world_anvil_mcp/tools/world.py` (world tools with ecosystem)
- [ ] 4 read tools implemented
- [ ] 1 write tool implemented (update_world)
- [ ] MCP resource for world context
- [ ] Integration tests passing
- [ ] Live API validation complete

**Quality Gate**: Live API calls succeed, ≥90% coverage

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
```

**End of Days 5-6 Deliverables**:
- [ ] Unit tests: 90%+ coverage
- [ ] Integration tests passing
- [ ] Live API validation passing
- [ ] Write API documented (availability, permissions)
- [ ] `docs/research/write-api-validation.md` created

**Quality Gate**: All tests pass, write API assessed

---

### Days 7-8: Documentation & Polish

**Day 7: Getting Started Documentation**

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

**Day 8: Retrospective & Phase Completion**

Create Phase 1.1 retrospective and patterns documentation.

**End of Days 7-8 Deliverables**:
- [ ] `docs/GETTING_STARTED.md` complete
- [ ] All documentation updated
- [ ] Phase 1.1 retrospective complete (`docs/pdca/phase-1.1-foundation/check.md`)
- [ ] Patterns extracted (`docs/patterns/world-anvil-client-foundation.md`)
- [ ] Phase 1.2 plan drafted

---

## Dependencies

**Blocked By**:
- ✅ Phase 0 complete (all prerequisites met)

**Blocks**:
- Phase 1.2: Article Endpoints (depends on client foundation + write API assessment)
- Phase 1.3: Category Endpoints (depends on client foundation)
- All future endpoint implementations

**Related**:
- pywaclient analysis (reference for patterns)
- Tool specifications (implementation blueprint)
- Quality standards (testing and docs requirements)
- Write API validation (informs Phase 2 scope)

---

## Risks & Mitigation

### Technical Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| **API credentials don't work** | High | Medium | Day 3 connectivity test before heavy implementation |
| **Write API not available** | Medium | Medium | Day 6 spike identifies before Phase 2 commitment |
| **Granularity validation strict** | Medium | Medium | Test all values ("0", "1", "2", "3") explicitly |
| **Rate limiting edge cases** | Medium | Low | Token bucket with margin (55 req/min target) |
| **Caching invalidation bugs** | Medium | Low | Comprehensive cache tests; conservative TTL |
| **Ecosystem detection false positives** | Low | Low | Conservative tool name matching |

### Process Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| **Scope creep (adding extra endpoints)** | Medium | Medium | Strict adherence to User + World + Write validation only |
| **Testing gaps** | High | Low | ≥90% coverage enforced by CI from Day 1 |
| **Quality drift** | High | Low | Pre-commit hooks + CI block non-compliant code |
| **Documentation lag** | Medium | Medium | Write docs alongside code (Days 1, 7-8) |

---

## Acceptance Criteria

### Definition of Done

**Day 1 (Infrastructure & Foundation)**:
- [ ] CI/CD pipeline passing (GitHub Actions green)
- [ ] `scripts/dev-setup.sh` and `scripts/dev-setup.ps1` work
- [ ] WorldAnvilClient initializes correctly
- [ ] InMemoryCache with LRU eviction works

**Day 2 (Exceptions & Ecosystem)**:
- [ ] Exception hierarchy complete
- [ ] MCP ecosystem detection working
- [ ] Pydantic models for User, Identity, World
- [ ] Unit tests passing

**Days 3-4 (User & World Endpoints)**:
- [ ] Live API connectivity validated
- [ ] 4 MCP tools implemented (identity, user, list_worlds, get_world)
- [ ] 1 write tool implemented (update_world)
- [ ] ≥90% test coverage

**Days 5-6 (Testing & Write Validation)**:
- [ ] Comprehensive test suite passing
- [ ] Live API tests passing
- [ ] Write API validation complete
- [ ] `docs/research/write-api-validation.md` created

**Days 7-8 (Documentation & Polish)**:
- [ ] `docs/GETTING_STARTED.md` complete and tested
- [ ] Phase 1.1 retrospective complete
- [ ] Patterns extracted and documented
- [ ] All documentation updated

**Overall Quality**:
- [ ] `ruff format --check` passes (zero formatting issues)
- [ ] `ruff check` passes (zero linting warnings)
- [ ] `mypy` strict mode passes (100% type coverage)
- [ ] All tests pass (`pytest`)
- [ ] Coverage ≥90% (`pytest --cov --cov-fail-under=90`)
- [ ] CI pipeline green (all jobs pass)
- [ ] Documentation builds without errors

### Validation Method

```bash
# Complete quality gate validation (automated via CI)
make check

# Equivalent to:
ruff format . && \
ruff check . && \
mypy src/world_anvil_mcp && \
pytest --cov=src/world_anvil_mcp --cov-report=term --cov-fail-under=90

# Live API testing (requires credentials)
WORLD_ANVIL_APP_KEY=xxx WORLD_ANVIL_USER_TOKEN=xxx pytest -m live

# CI status
# Check GitHub Actions: All jobs green
```

---

## Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Day 1**: Infrastructure & Foundation | 1 day | CI, dev scripts, client, cache |
| **Day 2**: Exceptions & Ecosystem | 1 day | Errors, ecosystem detection, models |
| **Days 3-4**: User & World Endpoints | 2 days | Auth + world endpoints + tools |
| **Days 5-6**: Testing & Write Validation | 2 days | Comprehensive tests + write API |
| **Days 7-8**: Documentation & Polish | 2 days | Getting Started + retrospective |
| **TOTAL** | **7-8 days** | **Production-ready foundation** |

**Buffer**: 1 day built in for discovery/debugging (realistic estimate)

**Critical Path**: Day 1 (foundation + CI) → Day 3 (auth test) → Day 6 (write validation)

---

## Serena Memory

**Write at Start**:
```python
write_memory("plan/phase-1.1/hypothesis", """
Phase 1.1: Foundation & API Validation (INTEGRATED)

Approach:
- Day 1: CI/CD + client foundation + cache (mandatory)
- Day 2: Exceptions + MCP ecosystem detection + models
- Days 3-4: User & World endpoints with live validation
- Days 5-6: Testing + write API validation
- Days 7-8: Documentation + retrospective

Expected Outcomes:
- CI/CD operational from Day 1
- WorldAnvilClient with caching and ecosystem awareness
- User, Identity, World endpoints complete
- MCP ecosystem detection for companion tools
- Write API capabilities documented (critical for Phase 2)
- ≥90% test coverage
- Getting Started guide functional
- Zero technical debt

Timeline: 7-8 days (realistic for foundation work)
Key Risk Mitigations:
- Day 1: CI catches issues immediately
- Day 3: Auth connectivity test
- Day 6: Write API spike before Phase 2 commitment
""")
```

---

## Next Steps

**After Plan Approval**:

1. **Create Execution Log**
   - `docs/pdca/phase-1.1-foundation/do.md`
   - Begin logging from first commit

2. **Set Up Environment** (Day 1)
   - Create `.github/workflows/ci.yml`
   - Create `scripts/dev-setup.sh` and `scripts/dev-setup.ps1`
   - Verify CI workflow syntax

3. **Begin Day 1: Infrastructure & Foundation**
   - Implement CI/CD pipeline
   - Create dev setup scripts
   - Implement WorldAnvilClient with caching
   - Create exception hierarchy
   - Write tests alongside code
   - **Verify CI passing before Day 2**

4. **Root Cause Analysis Protocol** (All Days)
   - Any error → STOP
   - Investigate with context7/WebFetch/Grep
   - Document in `execution/phase-1.1/errors`
   - Design different solution
   - Document learning

5. **Continuous Updates**
   - Update `do.md` during work (not after)
   - Checkpoint every 30 minutes
   - Track all trial-and-error
   - **Day 6: Document write API findings meticulously**

---

## Quality Commitment

**Zero Technical Debt**:
- No skipped tests
- No disabled quality checks
- No TODO comments for core functionality
- No warnings ignored without investigation
- CI passing from Day 1 (not "fix later")

**Evidence-Based Development**:
- All design decisions documented with rationale
- All errors analyzed for root cause
- All solutions tested and validated
- All learnings captured
- **Write API: Evidence-based decision for Phase 2**

**User-Focused Quality**:
- Session-time performance (<500ms cached)
- Clear error messages
- Comprehensive documentation
- Reliable operation
- Easy contributor onboarding (<5 min setup)

---

## MCP Ecosystem Integration Pattern

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

---

## References

### Specifications

- **MCP Ecosystem Integration**: `docs/specs/MCP-ECOSYSTEM-SPEC.md`
  - Integration tiers (CRITICAL, RECOMMENDED, OPTIONAL)
  - 6 companion MCPs: Foundry VTT, Context Engine, Dropbox, Notion, Discord, Calendar
  - Full `EcosystemDetector` implementation
  - Workflow integration patterns

- **Context Engine MCP**: `docs/specs/CONTEXT-ENGINE-SPEC.md`
  - **Status**: SEPARATE project (not part of World Anvil MCP codebase)
  - Semantic search over TTRPG reference materials
  - System corpora: D&D 5e SRD, Pathfinder 2e, mythology, historical
  - MCP tools: `search_reference`, `get_srd_content`, `find_similar`
  - Architecture: ChromaDB, sentence-transformers, FastMCP

### API Documentation

- **World Anvil API**: https://www.worldanvil.com/api/external/boromir/documentation
- **MCP SDK**: https://github.com/modelcontextprotocol/python-sdk
- **OpenAPI Spec**: `openapi.yml` (World Anvil Boromir API v2)

### Related Projects

- **Foundry VTT**: https://foundryvtt.com/
- **Foundry MCP Bridge**: https://foundryvtt.com/packages/foundry-mcp-bridge

---

**Plan Approved By**: User feedback incorporated + detailed code integrated + spec-compliant ecosystem
**Implementation Start**: After user approves integrated plan
**Expected Completion**: 7-8 days from start
**Next Document**: `docs/pdca/phase-1.1-foundation/do.md` (execution log)

---

**Status**: ✅ Plan Integrated & Spec-Compliant (Structural + Code Examples + MCP Ecosystem Detection)
**Serena Memory**: `plan/phase-1.1/hypothesis` to be updated after approval
**PDCA Phase**: Plan (revised with specs) → Awaiting approval → Do (next)
