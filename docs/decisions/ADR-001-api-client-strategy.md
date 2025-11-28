# ADR-001: API Client Strategy

**Status**: Proposed
**Date**: 2025-11-28
**Decider**: PM Agent + User
**Context**: Phase 0 - Architecture Decision

---

## Context and Problem Statement

We need to decide whether to use the existing `pywaclient` Python SDK or build our own World Anvil API client. This decision impacts development speed, maintainability, flexibility, and MCP integration.

**Existing SDK**: https://gitlab.com/SoulLink/world-anvil-api-client (pywaclient)

---

## Decision Drivers

### Must Have
- ✅ Full MCP Context integration (logging, progress, error reporting)
- ✅ Granularity-aware caching with custom TTLs
- ✅ Retry logic with exponential backoff
- ✅ Strict Pydantic type validation
- ✅ Coverage of all 34 endpoints we need

### Should Have
- 🎯 Fast time-to-market for MVP
- 🎯 Easy to debug and troubleshoot
- 🎯 Minimal external dependencies
- 🎯 Full control over error handling patterns

### Nice to Have
- 💡 Community validation of approach
- 💡 Reference implementation for complex endpoints
- 💡 Reduced testing burden

---

## Options Considered

### Option 1: Use pywaclient SDK Directly

**Approach**: Install pywaclient as dependency, wrap with thin MCP layer

**Pros**:
- ✅ **Fast start**: Already implemented, tested, working
- ✅ **Community validated**: Used by others, bugs likely found
- ✅ **All endpoints covered**: "wrapper for all the endpoints"
- ✅ **Less code to write**: Focus on MCP integration only
- ✅ **Reference available**: Can study their implementation
- ✅ **Maintenance burden shared**: Bug fixes from community

**Cons**:
- ❌ **External dependency risk**: Repository could be abandoned
- ❌ **Limited control**: Can't customize internal behavior easily
- ❌ **MCP integration harder**: Need to wrap every call for Context
- ❌ **Caching inflexible**: May not support our granularity-aware strategy
- ❌ **Error handling**: May not match our custom exception hierarchy
- ❌ **Pydantic models**: May not have strict models we want
- ❌ **Learning gap**: Less understanding of API internals
- ❌ **Version lock-in**: Breaking changes could disrupt us

**Code Example**:
```python
from pywaclient import WorldAnvilClient as WAClient
from mcp.server.fastmcp import Context

# Need to wrap every call
@mcp.tool()
async def get_article(world_id: str, article_id: str, ctx: Context):
    client = WAClient(app_key=..., user_token=...)

    # No built-in Context integration
    try:
        article = await client.get_article(world_id, article_id)
        # Manual logging
        await ctx.info(f"Retrieved article {article_id}")
        return article
    except Exception as e:
        # Manual error handling
        await ctx.error(f"Failed: {e}")
        raise
```

---

### Option 2: Build Custom Client (Recommended)

**Approach**: Write our own `WorldAnvilClient` with MCP-first design

**Pros**:
- ✅ **Full control**: Complete ownership of implementation
- ✅ **MCP-native**: Built-in Context, logging, progress reporting
- ✅ **Custom caching**: Granularity-aware with configurable TTLs
- ✅ **Tailored retry**: tenacity-based with our specific patterns
- ✅ **Strict types**: Pydantic models exactly as we need
- ✅ **No dependency risk**: No external maintenance concerns
- ✅ **Deep learning**: Full understanding of API behavior
- ✅ **Debugging ease**: Can trace through our own code
- ✅ **Optimization**: Can optimize for our specific use cases

**Cons**:
- ❌ **More upfront work**: Need to implement all endpoints
- ❌ **More testing**: Full test suite required
- ❌ **Reinventing wheels**: Some patterns already solved
- ❌ **Initial time investment**: Slower to first endpoint

**Code Example**:
```python
from world_anvil_mcp.api.client import WorldAnvilClient
from mcp.server.fastmcp import Context

# Client built for MCP
@mcp.tool()
async def get_article(world_id: str, article_id: str, ctx: Context):
    client = get_client(ctx)  # Context-aware client

    # Built-in logging, progress, caching, retry
    article = await client.get_article(world_id, article_id)
    # Context integration automatic
    return article.model_dump()

# Client implementation
class WorldAnvilClient:
    def __init__(self, ctx: Context = None):
        self.ctx = ctx
        self.cache = ResponseCache(ttl=3600)

    @retry(stop=stop_after_attempt(3))
    async def get_article(self, world_id: str, article_id: str,
                          granularity: int = 1) -> Article:
        # Auto-logging
        if self.ctx:
            await self.ctx.info(f"Fetching article {article_id}")

        # Cache with granularity
        cache_key = f"article:{world_id}:{article_id}:{granularity}"
        if cached := self.cache.get(cache_key):
            return Article.model_validate(cached)

        # HTTP call with retry
        response = await self.client.get(
            f"/article",
            params={"id": article_id, "granularity": granularity}
        )

        # Pydantic validation
        article = Article.model_validate(response)
        self.cache.set(cache_key, response)
        return article
```

---

### Option 3: Hybrid Approach

**Approach**: Use pywaclient as reference, build our own implementation

**Pros**:
- ✅ **Best of both**: Learn from their patterns, own our code
- ✅ **Validation**: Can compare our implementation to theirs
- ✅ **Learning accelerated**: See how they solved problems
- ✅ **MCP-optimized**: Build exactly what we need
- ✅ **Reference available**: Consult when stuck

**Cons**:
- ⚠️ **Still full implementation**: Same work as Option 2
- ⚠️ **Temptation to copy**: May not optimize for our needs

**Approach**:
1. Study pywaclient source code
2. Learn their endpoint patterns
3. Build our own client with MCP-first design
4. Reference theirs when uncertain
5. Compare implementations for validation

---

## Decision Outcome

**Recommended**: **Option 2 - Build Custom Client** with pywaclient as reference

**Rationale**:
1. **MCP Integration Critical**: Context, logging, progress reporting are core requirements
2. **Caching Strategy**: Need granularity-aware caching for performance
3. **Error Handling**: Custom exception hierarchy for MCP patterns
4. **Type Safety**: Strict Pydantic models for reliability
5. **Long-term Control**: No dependency on external maintenance
6. **Learning Value**: Deep API understanding helps debugging

**Implementation Strategy**:
1. **Phase 0.1**: Study pywaclient implementation patterns
2. **Phase 1.1**: Build foundation client with User/World endpoints
3. **Phase 1+**: Incrementally add endpoints, referencing pywaclient
4. **Testing**: Compare our results to pywaclient outputs (if available)

---

## Detailed Implementation Plan

### Phase 0.1 Enhancement: Study pywaclient

**Add to Phase 0.1 tasks**:

1. **Clone and Analyze pywaclient**
   ```bash
   git clone https://gitlab.com/SoulLink/world-anvil-api-client.git
   cd world-anvil-api-client
   ```

2. **Study Key Patterns**
   - How they structure API calls
   - Error handling patterns
   - Authentication flow
   - Response parsing
   - Endpoint parameter patterns

3. **Document Learnings**
   ```
   docs/research/pywaclient-analysis.md
   - Authentication approach
   - Error handling patterns
   - Caching (if any)
   - Endpoint organization
   - Response models
   ```

4. **Extract Useful Patterns**
   - Header structure
   - Common parameter patterns
   - Error response formats
   - API quirks and gotchas

### Our Custom Client Architecture

```python
# src/world_anvil_mcp/api/client.py

class WorldAnvilClient:
    """MCP-optimized World Anvil API client.

    Features:
    - Built-in Context integration for MCP logging
    - Granularity-aware caching with configurable TTLs
    - Automatic retry with exponential backoff
    - Strict Pydantic response validation
    - Progress reporting for long operations
    """

    def __init__(
        self,
        app_key: str,
        user_token: str,
        base_url: str = "https://www.worldanvil.com/api/external/boromir",
        ctx: Context | None = None,
        cache_ttl: int = 3600,
        rate_limit: int = 60
    ):
        self.app_key = app_key
        self.user_token = user_token
        self.base_url = base_url
        self.ctx = ctx

        # MCP-specific features
        self.cache = GranularityCache(ttl=cache_ttl)
        self.rate_limiter = RateLimiter(rate_limit)

        # HTTP client
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
        }

    async def _log(self, level: str, message: str):
        """Context-aware logging."""
        if self.ctx:
            if level == "info":
                await self.ctx.info(message)
            elif level == "error":
                await self.ctx.error(message)
            elif level == "warning":
                await self.ctx.warning(message)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, httpx.TimeoutException))
    )
    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        data: dict | None = None
    ) -> dict:
        """Make authenticated API request with retry and caching."""
        # Rate limiting
        await self.rate_limiter.acquire()

        # Make request
        response = await self.client.request(
            method,
            f"{self.base_url}{endpoint}",
            params=params,
            json=data
        )

        # Error handling
        if response.status_code == 401:
            raise AuthenticationError("Invalid API credentials")
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code == 404:
            raise NotFoundError(f"Resource not found: {endpoint}")

        response.raise_for_status()
        return response.json()

    # Endpoint methods (implement one by one)
    async def get_user(self) -> User:
        """Get current user information."""
        await self._log("info", "Fetching current user")
        data = await self._request("GET", "/user")
        return User.model_validate(data)

    async def get_world(self, world_id: str, granularity: int = 1) -> World:
        """Get world details with caching."""
        cache_key = f"world:{world_id}:{granularity}"

        # Check cache
        if cached := self.cache.get(cache_key):
            await self._log("info", f"World {world_id} from cache")
            return World.model_validate(cached)

        # Fetch from API
        await self._log("info", f"Fetching world {world_id}")
        data = await self._request(
            "GET",
            "/world",
            params={"id": world_id, "granularity": granularity}
        )

        # Cache and return
        self.cache.set(cache_key, data)
        return World.model_validate(data)
```

### Benefits vs pywaclient

| Feature | pywaclient | Our Client | Winner |
|---------|------------|------------|--------|
| MCP Context Integration | ❌ No | ✅ Built-in | **Ours** |
| Progress Reporting | ❌ No | ✅ Yes | **Ours** |
| Granularity Caching | ❓ Unknown | ✅ Yes | **Ours** |
| Custom Retry Logic | ⚠️ Basic | ✅ Advanced | **Ours** |
| Pydantic Models | ⚠️ Some | ✅ Strict | **Ours** |
| Error Hierarchy | ⚠️ Basic | ✅ Custom | **Ours** |
| Immediate Available | ✅ Yes | ❌ Need to build | **Theirs** |
| Community Validation | ✅ Yes | ❌ No | **Theirs** |
| Maintenance | ⚠️ External | ✅ Our control | **Ours** |

---

## Updated Phase 0 Timeline

### Phase 0.1: Tool Specifications + pywaclient Analysis (Day 1-2)

**Enhanced Tasks**:
1. Clone and study pywaclient (2-3 hours)
2. Document their patterns in `docs/research/pywaclient-analysis.md`
3. Create tool specifications using learnings
4. Define our client architecture

**Deliverables**:
- `docs/research/pywaclient-analysis.md` - Pattern analysis
- `docs/specs/tool-specifications.md` - Enhanced with pywaclient insights
- `docs/specs/client-architecture.md` - Our custom client design

### Updated Timeline Impact

**Before**: Phase 0 = 5 days
**After**: Phase 0 = 5 days (same, just enhanced research)

**Before**: Phase 1.1 User endpoints = 2 days
**After**: Phase 1.1 = 3 days (includes building client foundation)

**Overall Impact**: +1 day to project, but with:
- ✅ Better MCP integration
- ✅ Full control and flexibility
- ✅ Deep API understanding
- ✅ Optimized for our use cases

---

## Consequences

### Positive
- ✅ **MCP-native**: Perfect integration with Context, logging, progress
- ✅ **Optimized**: Exactly what we need, nothing we don't
- ✅ **Learning**: Deep understanding of World Anvil API
- ✅ **Control**: No dependency on external maintenance
- ✅ **Debugging**: Can trace through our own code
- ✅ **Reference available**: pywaclient for validation

### Negative
- ⚠️ **More work**: Need to implement all endpoints ourselves
- ⚠️ **More testing**: Full test coverage required
- ⚠️ **Initial delay**: +1 day to reach first working endpoint

### Mitigation
- Use pywaclient as reference to avoid mistakes
- Implement incrementally (endpoint-by-endpoint)
- Comprehensive testing at each step
- Pattern extraction for reuse across endpoints

---

## Validation

### How to Validate This Decision

1. **Phase 1.1 Completion**: If we successfully implement User/World endpoints with good MCP integration, decision validated
2. **Compare**: Run same requests through pywaclient and our client, compare results
3. **Performance**: Measure caching effectiveness and response times
4. **Developer Experience**: Evaluate ease of adding new endpoints

### Rollback Plan

If our custom client proves too difficult:
- Fall back to pywaclient wrapper approach
- Migrate existing tools to use pywaclient
- Accept MCP integration limitations

**Rollback Trigger**: If Phase 1.1 takes >5 days or quality issues emerge

---

## Next Steps

1. **Approve this ADR**: User confirms approach
2. **Start Phase 0.1**: Clone and study pywaclient
3. **Document patterns**: Extract useful patterns to docs/research/
4. **Design client**: Create detailed client architecture
5. **Begin implementation**: Phase 1.1 with custom client

---

**Decision**: ✅ **APPROVED - Build Custom Client**
**Date**: 2025-11-28
**Rationale**: MCP-first design, full control, no dependency risk, optimal integration

**Implementation**: Custom WorldAnvilClient using pywaclient as reference only
