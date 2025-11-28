# pywaclient Implementation Analysis

**Date**: 2025-11-28
**Repository**: https://gitlab.com/SoulLink/world-anvil-api-client
**Version Analyzed**: Latest (Boromir v2 compatible)
**Purpose**: Extract implementation patterns for our custom MCP-optimized client

---

## Executive Summary

pywaclient is a synchronous, delegation-based API client with comprehensive error handling but lacking async support, caching, retry logic, and type safety features we need for MCP integration.

**Key Takeaways**:
- ✅ **Use**: Authentication patterns, error handling hierarchy, endpoint organization
- ⚠️ **Adapt**: Pagination strategy (scroll collection pattern)
- ❌ **Don't Use**: Synchronous requests, dict-based responses, lack of caching

---

## Architecture Overview

### Project Structure
```
pywaclient/
├── __init__.py              # Package exports
├── api.py                   # Main BoromirApiClient class
├── endpoints/               # Modular endpoint implementations
│   ├── __init__.py         # BasicEndpoint, CrudEndpoint base classes
│   ├── articles.py         # ArticleCrudEndpoint
│   ├── worlds.py           # WorldCrudEndpoint (with list methods)
│   ├── users.py            # UserCrudEndpoint (with identity)
│   ├── categories.py       # CategoryCrudEndpoint
│   └── ...                 # 18 more endpoint files
└── exceptions/             # Error handling
    └── __init__.py         # Exception hierarchy
```

### Design Pattern: **Delegation-Based Architecture**

**Main Client** (`BoromirApiClient`):
- Instantiates all endpoint objects
- Stores authentication headers
- Provides base URL
- Endpoints access client via `self.client`

**Example**:
```python
class BoromirApiClient:
    def __init__(self, name, url, version, application_key, authentication_token):
        self.headers = {
            'x-auth-token': authentication_token,
            'x-application-key': application_key,
            'Accept': 'application/json',
            'User-Agent': f'{name} ({url}, {version})'
        }
        self.base_url = 'https://www.worldanvil.com/api/external/boromir/'

        # Endpoint delegation
        self.article = ArticleCrudEndpoint(self)
        self.world = WorldCrudEndpoint(self)
        self.user = UserCrudEndpoint(self)
        # ... 15 more endpoints
```

---

## Authentication Implementation

### Header-Based Authentication
```python
self.headers = {
    'x-auth-token': authentication_token,      # User authentication
    'x-application-key': application_key,      # Application key
    'Accept': 'application/json',              # Response format
    'User-Agent': f'{name} ({url}, {version})' # Application identification
}

# For POST/PUT/PATCH requests
self.headers_post = self.headers.copy()
self.headers_post['Content-type'] = 'application/json'
```

**Our MCP Client Should**:
- ✅ Use same header names: `x-auth-token`, `x-application-key` (lowercase!)
- ✅ Include User-Agent with app identification
- ✅ Separate headers for GET vs POST/PUT/PATCH
- ➕ Add async context manager for header management

---

## Error Handling Patterns

### Exception Hierarchy
```
WorldAnvilClientException (base)
└── WorldAnvilServerException
    ├── ConnectionException (503)
    ├── UnauthorizedRequest (401)
    ├── AccessForbidden (403)
    ├── ResourceNotFound (404)
    ├── UnprocessableDataProvided (422)
    ├── InternalServerException (500)
    ├── UnexpectedStatusException (other)
    └── FailedRequest (success=false)
```

### Response Parsing Logic
```python
def _parse_response(path, response, params, content):
    if response.ok:
        data = response.json()
        # Check for 'success' flag in response
        if 'success' not in data:
            raise UnexpectedStatusException(...)
        if data['success']:
            return data
        else:
            raise FailedRequest(...)  # API returned success=false
    elif response.status_code == 401:
        raise UnauthorizedRequest(...)
    elif response.status_code == 403:
        raise AccessForbidden(...)
    elif response.status_code == 404:
        raise ResourceNotFound(...)
    elif response.status_code == 422:
        raise UnprocessableDataProvided(...)
    elif response.status_code == 500:
        raise InternalServerException(...)
    else:
        raise UnexpectedStatusException(...)
```

**Key Insight**: World Anvil API returns 200 OK with `{"success": false, "error": "..."}` for some failures!

**Our MCP Client Should**:
- ✅ Adopt similar exception hierarchy
- ✅ Check `success` flag in responses, not just status codes
- ➕ Add MCP Context integration for error logging
- ➕ Add retry logic for transient errors (429, 503, timeouts)

---

## Endpoint Organization

### Base Classes

**BasicEndpoint** (`endpoints/__init__.py`):
```python
class BasicEndpoint:
    def __init__(self, client, base_path):
        self.client = client
        self.path = base_path

    def _get_request(self, path, params):
        response = requests.get(
            self.client.base_url + path,
            params=params,
            headers=self.client.headers
        )
        return _parse_response(path, response, params, {})

    def _post_request(self, path, params, content):
        response = requests.post(
            self.client.base_url + path,
            params=params,
            json=content,
            headers=self.client.headers_post
        )
        return _parse_response(path, response, params, content)

    # Also: _put_request, _patch_request, _delete_request

    def get(self, identifier, granularity):
        return self._get_request(self.path, {
            'id': identifier,
            'granularity': str(granularity)  # Passed as STRING!
        })
```

**CrudEndpoint** (inherits BasicEndpoint):
```python
class CrudEndpoint(BasicEndpoint):
    def put(self, content):        # Create
        return self._put_request(self.path, content)

    def patch(self, identifier, content):  # Update
        return self._patch_request(self.path, {'id': identifier}, content)

    def delete(self, identifier):  # Delete
        self._delete_request(self.path, {'id': identifier})
```

### Endpoint Inheritance Patterns

**Simple CRUD** (most endpoints):
```python
class ArticleCrudEndpoint(CrudEndpoint):
    def __init__(self, client):
        super().__init__(client, 'article')
```

**Complex with List Methods** (worlds, users, etc.):
```python
class WorldCrudEndpoint(CrudEndpoint):
    def __init__(self, client):
        super().__init__(client, 'world')
        # Additional paths for list endpoints
        self.path_articles = f'{self.path}/articles'
        self.path_categories = f'{self.path}/categories'
        # ... 12 more list paths

    def articles(self, world_id, category_id=None, complete=True, limit=50, offset=0):
        if complete:
            return self._scroll_collection(
                self.path_articles,
                {'id': world_id},
                'entities',
                'category', category_id
            )
        else:
            request_body = {'limit': limit, 'offset': offset}
            if category_id:
                request_body['category'] = {'id': category_id}
            return self._post_request(...)['entities']
```

**Our MCP Client Should**:
- ✅ Use similar base class pattern (BasicEndpoint → CrudEndpoint)
- ✅ Organize endpoints by resource type
- ➕ Make async (httpx instead of requests)
- ➕ Add Pydantic models for responses
- ➕ Add caching at base class level

---

## Pagination Strategy

### Scroll Collection Pattern
```python
def _scroll_collection(self, path, params, collection_tag, parentName='', parentId=''):
    limit = 50  # Fixed batch size
    offset = 0

    # Build request body
    if parentName:
        content = {'limit': limit, 'offset': offset, parentName: {'id': parentId}}
    else:
        content = {'limit': limit, 'offset': offset}

    # First request
    collection = self._post_request(path, params, content)

    if collection['success']:
        items = collection[collection_tag]  # e.g., 'entities'
        while len(items) > 0:
            # Yield all items from current batch
            for item in items:
                yield item

            # Fetch next batch
            offset = offset + limit
            content['offset'] = offset
            collection = self._post_request(path, params, content)
            items = collection[collection_tag]
```

**Usage Pattern**:
```python
# Get all articles (fetches in 50-item batches)
for article in client.world.articles(world_id, complete=True):
    process(article)

# Get paginated results manually
articles = client.world.articles(world_id, complete=False, limit=20, offset=0)
```

**Our MCP Client Should**:
- ✅ Support similar pagination with `limit` and `offset`
- ✅ Provide iterator for complete collections
- ➕ Make async iterator (`async for`)
- ➕ Cache batch results
- ➕ Add progress reporting via MCP Context

---

## Granularity Handling

### Granularity Levels (from pywaclient)
```python
# Granularity passed as STRING parameter
def get(self, identifier, granularity):
    return self._get_request(self.path, {
        'id': identifier,
        'granularity': str(granularity)  # Important: STRING!
    })

# Example usage from README
article = client.article.get(articles[0]['id'], 2)      # Full content
category = client.category.get(categories[0]['id'], 1)  # Standard detail
```

**Documented Levels**:
- `-1`: Reference only
- `0`: Default/preview
- `1`: Full/standard detail
- `2`: Extended detail (for articles)
- `3`: Special (rare, not well documented)

**Our MCP Client Should**:
- ✅ Pass granularity as string parameter
- ➕ Use Enum for type safety (GranularityLevel.STANDARD → "1")
- ➕ Cache responses with granularity in cache key
- ➕ Default to granularity=1 for most operations

---

## HTTP Client Implementation

### Current (pywaclient): Synchronous with `requests`
```python
import requests

def _get_request(self, path, params):
    try:
        response = requests.get(
            self.client.base_url + path,
            params=params,
            headers=self.client.headers
        )
        return _parse_response(path, response, params, {})
    except RequestException as err:
        raise ConnectionException(str(err))
```

**Limitations**:
- ❌ Synchronous only (blocks thread)
- ❌ No connection pooling
- ❌ No retry logic
- ❌ No timeout configuration
- ❌ No rate limiting

### Our MCP Client: Async with `httpx`
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class WorldAnvilClient:
    def __init__(self, ctx: Context = None):
        self.client = httpx.AsyncClient(
            headers=self._build_headers(),
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_connections=10)
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def _get_request(self, path, params):
        try:
            response = await self.client.get(
                f"{self.base_url}{path}",
                params=params
            )
            return await self._parse_response(response)
        except httpx.TimeoutException as err:
            await self._log_error(f"Timeout: {err}")
            raise
```

**Advantages**:
- ✅ Async/await for MCP compatibility
- ✅ Connection pooling
- ✅ Automatic retry with exponential backoff
- ✅ Configurable timeouts
- ✅ Rate limiting capabilities

---

## What pywaclient is Missing (Our Opportunities)

### 1. Caching
**pywaclient**: None
**Our Client**: Granularity-aware caching with TTL
```python
from cachetools import TTLCache

class WorldAnvilClient:
    def __init__(self):
        self.cache = TTLCache(maxsize=1000, ttl=3600)

    async def get_article(self, article_id, granularity=1):
        cache_key = f"article:{article_id}:{granularity}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        data = await self._get_request('article', {
            'id': article_id,
            'granularity': str(granularity)
        })
        self.cache[cache_key] = data
        return data
```

### 2. Type Safety
**pywaclient**: Returns `Dict[str, Any]`
**Our Client**: Pydantic v2 models
```python
from pydantic import BaseModel

class Article(BaseModel):
    id: str
    title: str
    content: str | None = None
    state: str
    world: dict
    # ... with strict validation

async def get_article(self, article_id: str, granularity: int = 1) -> Article:
    data = await self._get_request(...)
    return Article.model_validate(data)
```

### 3. MCP Context Integration
**pywaclient**: No logging integration
**Our Client**: Built-in Context support
```python
from mcp.server.fastmcp import Context

class WorldAnvilClient:
    def __init__(self, ctx: Context | None = None):
        self.ctx = ctx

    async def get_article(self, article_id: str) -> Article:
        if self.ctx:
            await self.ctx.info(f"Fetching article {article_id}")

        try:
            article = await self._fetch_article(article_id)
            if self.ctx:
                await self.ctx.info(f"Retrieved: {article.title}")
            return article
        except Exception as e:
            if self.ctx:
                await self.ctx.error(f"Failed to fetch article: {e}")
            raise
```

### 4. Retry Logic
**pywaclient**: None
**Our Client**: Tenacity-based retry with exponential backoff
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((RateLimitError, httpx.TimeoutException))
)
async def _request(self, method, endpoint, **kwargs):
    # Retry on rate limits and timeouts
    ...
```

### 5. Rate Limiting
**pywaclient**: None
**Our Client**: Token bucket algorithm
```python
from asyncio import Semaphore
import time

class RateLimiter:
    def __init__(self, rate_limit: int = 60):  # 60 requests per minute
        self.semaphore = Semaphore(rate_limit)
        self.reset_time = time.time() + 60

    async def acquire(self):
        if time.time() >= self.reset_time:
            self.reset_time = time.time() + 60
            # Reset semaphore
        await self.semaphore.acquire()
```

---

## API Quirks and Gotchas

### 1. Success Flag Pattern
**Issue**: API returns 200 OK with `{"success": false}` for some errors
```json
{
  "success": false,
  "error": "Invalid world ID"
}
```
**Solution**: Always check `success` flag, not just status code

### 2. Granularity as String
**Issue**: API expects granularity as string, not integer
```python
# Correct
params = {'id': '123', 'granularity': '1'}

# Wrong (will fail)
params = {'id': '123', 'granularity': 1}
```

### 3. Nested ID Objects
**Issue**: List endpoints expect nested ID objects
```python
# Correct for filtering by category
request_body = {
    'limit': 50,
    'offset': 0,
    'category': {'id': '456'}  # Nested object!
}

# Wrong
request_body = {
    'limit': 50,
    'offset': 0,
    'category_id': '456'
}
```

### 4. Different Granularity Limits
**Issue**: Not all resources support granularity=2
```python
# Articles support 0, 1, 2
article = client.article.get(id, 2)  # ✅ Works

# Categories only support 0, 1
category = client.category.get(id, 2)  # ❌ May fail or return same as 1
```

---

## Recommendations for Our Client

### Architecture
✅ **Adopt**:
- Delegation pattern with endpoint classes
- Base class hierarchy (BasicEndpoint → CrudEndpoint)
- Modular endpoint organization

➕ **Enhance**:
- Make fully async with httpx
- Add MCP Context integration at base class
- Implement granularity-aware caching

### Error Handling
✅ **Adopt**:
- Exception hierarchy
- Success flag checking
- Status code mapping

➕ **Enhance**:
- Add retry logic for transient errors
- MCP Context logging for all errors
- Better error messages with context

### Pagination
✅ **Adopt**:
- Scroll collection pattern concept
- limit/offset parameters

➕ **Enhance**:
- Async iterators
- Progress reporting via Context
- Batch caching

### Type Safety
❌ **Don't Adopt**:
- Dict-based responses

➕ **Use Instead**:
- Pydantic v2 models
- Strict type hints
- Runtime validation

---

## Implementation Priority

### Phase 1: Foundation (Custom Client Base)
1. **AsyncClient with httpx**
   - Connection pooling
   - Timeout configuration
   - Proper headers (x-auth-token, x-application-key)

2. **Error Handling**
   - Exception hierarchy (adapted from pywaclient)
   - Success flag checking
   - Status code mapping

3. **Base Classes**
   - BasicEndpoint (async version)
   - CrudEndpoint (async version)
   - MCP Context integration

### Phase 2: Core Features
1. **Caching**
   - TTLCache with granularity awareness
   - Cache key generation

2. **Retry Logic**
   - Tenacity integration
   - Exponential backoff

3. **Rate Limiting**
   - Token bucket or semaphore-based

### Phase 3: Endpoint Implementation
1. **User & World** (Phase 1.1)
   - UserEndpoint with identity()
   - WorldEndpoint with get()

2. **Articles & Categories** (Phase 1.2)
   - ArticleEndpoint
   - CategoryEndpoint
   - List methods with pagination

3. **Continue** through remaining endpoints

---

## Code Examples Comparison

### pywaclient Style
```python
# Synchronous, dict-based
from pywaclient.api import BoromirApiClient

client = BoromirApiClient(
    'MyApp', 'https://example.com', '1.0.0',
    app_key, auth_token
)

user = client.user.identity()
worlds = list(client.user.worlds(user['id']))
article_dict = client.article.get(article_id, 2)
print(article_dict['title'])
```

### Our MCP Client Style
```python
# Async, type-safe, MCP-integrated
from world_anvil_mcp.client import WorldAnvilClient
from mcp.server.fastmcp import Context

async def get_article_info(ctx: Context):
    client = WorldAnvilClient(
        app_key=app_key,
        user_token=auth_token,
        ctx=ctx
    )

    async with client:
        user = await client.user.identity()
        worlds = [w async for w in client.user.worlds(user.id)]
        article = await client.article.get(article_id, granularity=2)

        await ctx.info(f"Retrieved: {article.title}")
        return article.model_dump()
```

---

## Conclusion

pywaclient provides valuable reference patterns for:
- ✅ Authentication header structure
- ✅ Error handling hierarchy
- ✅ Endpoint organization
- ✅ API quirks and gotchas

However, we need to build our own client to achieve:
- ➕ Async/await for MCP compatibility
- ➕ Type safety with Pydantic
- ➕ Caching with granularity awareness
- ➕ Retry logic with exponential backoff
- ➕ MCP Context integration
- ➕ Rate limiting
- ➕ Progress reporting

**Next Steps**:
1. Design our custom client architecture (docs/specs/client-architecture.md)
2. Create tool specifications using patterns learned here
3. Implement Phase 1.1 with User & World endpoints

---

**Status**: ✅ Analysis Complete
**Date**: 2025-11-28
**Next**: Client Architecture Design
