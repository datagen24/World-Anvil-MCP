API Reference
=============

This section provides complete API documentation for the World Anvil MCP Server.

.. toctree::
   :maxdepth: 2
   :caption: API Modules:

   client
   endpoints
   models
   cache
   rate_limiter
   exceptions

Overview
--------

The World Anvil MCP Server provides both:

1. **MCP Tools**: Claude Code integration via Model Context Protocol
2. **Python Client**: Direct programmatic access to World Anvil API

Core Components
---------------

WorldAnvilClient
~~~~~~~~~~~~~~~~

Main entry point for all World Anvil API operations.

**Note**: Auto-generated API documentation will appear here once implementation begins.
For design specifications, see :doc:`../specs/client-architecture`.

Endpoints
~~~~~~~~~

Specialized endpoint classes for different resource types:

- ``ArticleEndpoint`` - Article operations (list, get, search, create, update)
- ``WorldEndpoint`` - World operations (list, get)
- ``CategoryEndpoint`` - Category operations (list, get)
- ``MapEndpoint`` - Map operations (list, get, markers)
- ``CampaignEndpoint`` - Campaign operations (get, list NPCs)

**Note**: Auto-generated endpoint documentation will appear here once implementation begins.
For design specifications, see :doc:`../specs/client-architecture`.

Data Models
~~~~~~~~~~~

Pydantic v2 models for type-safe data handling:

- ``Article`` - Article metadata and content
- ``World`` - World metadata and settings
- ``Category`` - Category hierarchy information
- ``Map`` - Map metadata and configuration
- ``Campaign`` - Campaign information
- ``User`` - User profile data

**Note**: Auto-generated model documentation will appear here once implementation begins.
For model specifications, see :doc:`../specs/tool-specifications`.

Infrastructure
~~~~~~~~~~~~~~

Internal components for caching, rate limiting, and error handling:

- ``ResponseCache`` - TTL-based response caching
- ``RateLimiter`` - Token bucket rate limiter (60 req/min)
- ``RetryLogic`` - Exponential backoff retry handler
- ``Exceptions`` - Custom exception hierarchy

**Note**: Auto-generated infrastructure documentation will appear here once implementation begins.
For architecture details, see :doc:`../architecture/index`.

MCP Tools
---------

Tools exposed to Claude Code via Model Context Protocol.

World Operations
~~~~~~~~~~~~~~~~

.. function:: list_worlds() -> list[World]

   List all accessible World Anvil worlds.

   :returns: List of world objects with metadata
   :raises WorldAnvilAPIError: If API request fails

   **Example**:

   .. code-block:: text

       You: "List my worlds"
       Claude: [Calls list_worlds MCP tool]

.. function:: get_world(world_id: str) -> World

   Get detailed information about a specific world.

   :param world_id: UUID of the world
   :returns: Complete world object with all metadata
   :raises NotFoundError: If world doesn't exist
   :raises WorldAnvilAPIError: If API request fails

   **Example**:

   .. code-block:: text

       You: "Get details for world abc-123"
       Claude: [Calls get_world with world_id="abc-123"]

Article Operations
~~~~~~~~~~~~~~~~~~

.. function:: list_articles(world_id: str, category_id: str | None = None, **filters) -> list[Article]

   List articles in a world with optional filtering.

   :param world_id: UUID of the world
   :param category_id: Optional category filter
   :param filters: Additional filters (tags, state, etc.)
   :returns: List of article summaries
   :raises WorldAnvilAPIError: If API request fails

   **Example**:

   .. code-block:: text

       You: "List all NPCs in my Storm King's Thunder world"
       Claude: [Calls list_articles with category filter for characters]

.. function:: get_article(article_id: str, granularity: str = "2") -> Article

   Get detailed information about a specific article.

   :param article_id: UUID of the article
   :param granularity: Detail level ("0", "1", "2")
   :returns: Complete article with content
   :raises NotFoundError: If article doesn't exist
   :raises WorldAnvilAPIError: If API request fails

   **Example**:

   .. code-block:: text

       You: "Get the full article for Harshnag"
       Claude: [Searches for Harshnag, then calls get_article]

.. function:: search_articles(term: str, world_id: str | None = None) -> list[Article]

   Full-text search across articles.

   :param term: Search query
   :param world_id: Optional world restriction
   :returns: Matching articles sorted by relevance
   :raises WorldAnvilAPIError: If API request fails

   **Example**:

   .. code-block:: text

       You: "Find all articles about dragons"
       Claude: [Calls search_articles with term="dragons"]

Category Operations
~~~~~~~~~~~~~~~~~~~

.. function:: list_categories(world_id: str) -> list[Category]

   List category hierarchy for a world.

   :param world_id: UUID of the world
   :returns: Hierarchical category tree
   :raises WorldAnvilAPIError: If API request fails

.. function:: get_category(category_id: str) -> Category

   Get detailed category information.

   :param category_id: UUID of the category
   :returns: Category object with metadata
   :raises NotFoundError: If category doesn't exist
   :raises WorldAnvilAPIError: If API request fails

Map Operations
~~~~~~~~~~~~~~

.. function:: list_maps(world_id: str) -> list[Map]

   List maps in a world.

   :param world_id: UUID of the world
   :returns: List of map summaries
   :raises WorldAnvilAPIError: If API request fails

.. function:: get_map(map_id: str) -> Map

   Get detailed map information.

   :param map_id: UUID of the map
   :returns: Complete map object
   :raises NotFoundError: If map doesn't exist
   :raises WorldAnvilAPIError: If API request fails

.. function:: get_map_markers(map_id: str) -> list[MapMarker]

   Get markers for a specific map.

   :param map_id: UUID of the map
   :returns: List of map markers with coordinates
   :raises WorldAnvilAPIError: If API request fails

Python Client Usage
-------------------

Initialization
~~~~~~~~~~~~~~

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient

    # From environment variables
    client = WorldAnvilClient()

    # Explicit credentials
    client = WorldAnvilClient(
        app_key="your-app-key",
        user_token="your-user-token"
    )

    # Custom base URL
    client = WorldAnvilClient(
        app_key="your-app-key",
        user_token="your-user-token",
        base_url="https://custom-api-endpoint.com"
    )

Async Operations
~~~~~~~~~~~~~~~~

All client methods are async and must be awaited:

.. code-block:: python

    import asyncio
    from world_anvil_mcp import WorldAnvilClient

    async def main():
        client = WorldAnvilClient()

        # List worlds
        worlds = await client.worlds.list()

        # Get specific article
        article = await client.articles.get("article-id")

        # Search with filters
        results = await client.articles.search(
            term="dragon",
            world_id="world-id"
        )

    asyncio.run(main())

Context Manager
~~~~~~~~~~~~~~~

Use context manager for automatic cleanup:

.. code-block:: python

    async def main():
        async with WorldAnvilClient() as client:
            worlds = await client.worlds.list()
            # Client automatically closes on exit

Error Handling
~~~~~~~~~~~~~~

Handle specific exceptions:

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient
    from world_anvil_mcp.exceptions import (
        NotFoundError,
        AuthenticationError,
        RateLimitError,
        WorldAnvilAPIError
    )

    async def main():
        client = WorldAnvilClient()

        try:
            article = await client.articles.get("invalid-id")
        except NotFoundError:
            print("Article doesn't exist")
        except AuthenticationError:
            print("Invalid credentials")
        except RateLimitError:
            print("Rate limit exceeded, retry later")
        except WorldAnvilAPIError as e:
            print(f"API error: {e}")

Type Safety
~~~~~~~~~~~

All responses are typed with Pydantic models:

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient
    from world_anvil_mcp.models import Article, World

    async def main():
        client = WorldAnvilClient()

        # Type-safe responses
        worlds: list[World] = await client.worlds.list()
        article: Article = await client.articles.get("article-id")

        # IDE autocomplete and type checking
        print(article.title)  # ✓ Type-safe
        print(article.invalid_field)  # ✗ Type error

Advanced Usage
--------------

Custom Caching
~~~~~~~~~~~~~~

Override default cache TTLs:

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient
    from world_anvil_mcp.cache import ResponseCache

    # Custom cache configuration
    cache = ResponseCache(
        default_ttl=300,  # 5 minutes
        max_size=1000     # Max cached items
    )

    client = WorldAnvilClient(cache=cache)

Rate Limiting
~~~~~~~~~~~~~

Configure rate limiter:

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient
    from world_anvil_mcp.rate_limiter import RateLimiter

    # Custom rate limit (default: 60/min)
    rate_limiter = RateLimiter(
        rate=60,
        per=60.0  # seconds
    )

    client = WorldAnvilClient(rate_limiter=rate_limiter)

Retry Configuration
~~~~~~~~~~~~~~~~~~~

Customize retry behavior:

.. code-block:: python

    from world_anvil_mcp import WorldAnvilClient

    client = WorldAnvilClient(
        max_retries=5,
        retry_delay=1.0,
        backoff_factor=2.0
    )

See Also
--------

- :doc:`../workflows/index` - Usage patterns and examples
- :doc:`../development/index` - Contributing guide
- :doc:`../architecture/index` - System architecture details
