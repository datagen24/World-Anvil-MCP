Quick Start
===========

This guide demonstrates common usage patterns for the World Anvil MCP Server with Claude Code.

Prerequisites
-------------

- Completed :doc:`installation`
- World Anvil account with API credentials configured
- Claude Code with MCP server enabled

Basic Usage
-----------

Natural Language Queries
~~~~~~~~~~~~~~~~~~~~~~~~

The MCP server enables natural language interactions with World Anvil:

.. code-block:: text

    You: "Show me all my World Anvil worlds"
    Claude: [Fetches and displays your worlds using list_worlds tool]

    You: "Get details about my 'Forgotten Realms Campaign' world"
    Claude: [Uses search or get_world to retrieve world information]

    You: "List all NPCs in the 'Storm King's Thunder' world"
    Claude: [Uses list_articles with category filter for characters]

Direct Tool Usage
~~~~~~~~~~~~~~~~~

You can also request specific tool invocations:

.. code-block:: text

    You: "Use the get_article tool to fetch article ID abc-123"
    Claude: [Directly calls get_article with specified ID]

Common Workflows
----------------

Workflow 1: Session Note-Taking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**During a live D&D session**:

.. code-block:: text

    You: "Start session notes for Session 15"
    Claude: [Loads world context and recent sessions]

    You: "The party arrived at Goldenfields and met Naxene Drathkala"
    Claude: [Searches for Goldenfields and Naxene, provides quick reference]

    You: "Combat with 3 Hill Giants at the north gate"
    Claude: [Logs encounter details]

    You: "Wrap up session notes"
    Claude: [Generates structured session report with all events]

For detailed patterns, see :doc:`workflows/session-note-taking`.

Workflow 2: NPC Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Create a new NPC**:

.. code-block:: text

    You: "Generate a mysterious wizard NPC for my campaign"
    Claude: [Creates NPC with personality, backstory, and stats]

    You: "Add them to my 'Storm King's Thunder' world as an article"
    Claude: [Uses create_article to add NPC to World Anvil]

For detailed patterns, see :doc:`workflows/npc-generation`.

Workflow 3: Quick Reference Lookup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**During gameplay**:

.. code-block:: text

    You: "Who is Harshnag?"
    Claude: [Searches articles, provides quick summary]

    You: "Show me the stats for Harshnag"
    Claude: [Displays stat block from article content]

For detailed patterns, see :doc:`workflows/quick-npc-lookup`.

Programmatic Usage
------------------

Python Client (Without MCP)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the World Anvil client directly in Python:

.. code-block:: python

    import asyncio
    from world_anvil_mcp import WorldAnvilClient

    async def main():
        # Initialize client
        client = WorldAnvilClient(
            app_key="your-app-key",
            user_token="your-user-token"
        )

        # List all worlds
        worlds = await client.worlds.list()
        for world in worlds:
            print(f"World: {world.title} (ID: {world.id})")

        # Get a specific article
        article = await client.articles.get(article_id="abc-123")
        print(f"Article: {article.title}")
        print(f"Content: {article.content[:100]}...")

        # Search articles
        results = await client.articles.search(
            term="dragon",
            world_id="world-456"
        )
        print(f"Found {len(results)} articles about dragons")

    asyncio.run(main())

For complete API documentation, see :doc:`api/index`.

Available MCP Tools
-------------------

The MCP server exposes the following tools to Claude Code:

**Core Operations (Phase 1)**:

- ``list_worlds`` - List all accessible worlds
- ``get_world`` - Get detailed world information
- ``list_articles`` - List articles with optional filters
- ``get_article`` - Get detailed article information
- ``list_categories`` - List category hierarchy
- ``get_category`` - Get category details

**High Priority (Phase 2)**:

- ``search_articles`` - Full-text search across articles
- ``list_maps`` - List maps in a world
- ``get_map`` - Get map details
- ``get_map_markers`` - Get markers for a map

**Campaign Management (Phase 3)**:

- ``get_campaign`` - Get campaign details
- ``list_campaign_npcs`` - List NPCs in a campaign
- ``get_campaign_npc`` - Get campaign NPC details

**Future (Write Operations)**:

- ``create_article`` - Create new articles
- ``update_article`` - Update existing articles
- ``create_category`` - Create new categories
- ``create_map_marker`` - Add markers to maps

Understanding MCP Context
--------------------------

The MCP server maintains context across interactions:

**Caching**:
    Frequently accessed data is cached with TTL:

    - World metadata: 1 hour
    - Article content: 5 minutes
    - Category hierarchy: 15 minutes

**Rate Limiting**:
    Automatic rate limiting (60 requests/min) protects your API quota.
    The server queues requests when approaching limits.

**Error Handling**:
    Automatic retry with exponential backoff for transient failures.

Best Practices
--------------

Session Preparation
~~~~~~~~~~~~~~~~~~~

Before a D&D session:

.. code-block:: text

    You: "Load context for my 'Storm King's Thunder' campaign"
    Claude: [Pre-caches relevant NPCs, locations, and recent sessions]

This optimizes response time during live gameplay.

Content Organization
~~~~~~~~~~~~~~~~~~~~

Use consistent naming and categorization:

.. code-block:: text

    You: "Create category structure for my new campaign"
    Claude: [Suggests standard D&D categories: NPCs, Locations, Items, etc.]

Lore Consistency
~~~~~~~~~~~~~~~~

Check for conflicts before adding content:

.. code-block:: text

    You: "Before I create this NPC, check if they conflict with existing lore"
    Claude: [Searches for name conflicts and thematic inconsistencies]

Troubleshooting
---------------

Slow Responses
~~~~~~~~~~~~~~

If responses are slow during sessions:

1. **Pre-cache content**: Load world context before session starts
2. **Reduce scope**: Focus queries on specific categories or articles
3. **Check network**: Verify internet connectivity to World Anvil

Authentication Errors
~~~~~~~~~~~~~~~~~~~~~

If you see authentication failures:

1. **Verify credentials**: Check ``.env`` or MCP settings
2. **Lowercase headers**: Ensure using ``x-application-key`` and ``x-auth-token``
3. **Regenerate tokens**: Create new credentials in World Anvil settings

Tool Not Found Errors
~~~~~~~~~~~~~~~~~~~~~

If Claude reports a tool isn't available:

1. **Restart MCP server**: Reload Claude Code configuration
2. **Check installation**: Verify ``world-anvil-mcp`` is installed
3. **Review logs**: Check Claude Code logs for startup errors

Next Steps
----------

- **Explore Workflows**: See :doc:`workflows/index` for detailed use cases
- **API Reference**: Review :doc:`api/index` for programmatic usage
- **Development**: Contribute at :doc:`development/index`

Examples
--------

For complete workflow examples with detailed interactions, see:

- :doc:`workflows/d-and-d-campaign-setup`
- :doc:`workflows/session-note-taking`
- :doc:`workflows/npc-generation`
- :doc:`workflows/location-development`
- :doc:`workflows/session-prep`
