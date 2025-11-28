Overview
========

The World Anvil MCP Server provides Claude Code with direct access to your World Anvil worlds,
enabling AI-assisted D&D campaign management through natural language interactions.

What is World Anvil?
--------------------

`World Anvil <https://www.worldanvil.com>`_ is a comprehensive world-building platform designed
for tabletop RPG creators, novelists, and game designers. It provides tools for organizing:

- 🌍 **Worlds**: Campaign settings and fictional universes
- 📝 **Articles**: Lore, NPCs, locations, items, and more
- 🗺️ **Maps**: Interactive maps with markers and layers
- 🎭 **Campaigns**: D&D session management and player tracking
- 📚 **Categories**: Hierarchical organization of content

What is MCP?
------------

The **Model Context Protocol (MCP)** is an open standard that enables AI assistants like Claude
to interact with external systems through a standardized interface. MCP servers expose:

- **Tools**: Callable functions (e.g., ``get_article``, ``create_world``)
- **Resources**: Accessible data (e.g., world schemas, article templates)
- **Prompts**: Reusable conversation starters

Key Features
------------

🔄 **Full CRUD Operations**
    Complete create, read, update, and delete support for all World Anvil resources:

    - Worlds and articles
    - Categories and tags
    - Maps and markers
    - Campaigns and NPCs

📝 **Session Note-Taking**
    Real-time assistance during live D&D gameplay:

    - Quick NPC lookups without disrupting play
    - Automatic cross-referencing with existing content
    - Structured session report generation
    - New content flagging for later development

🎭 **Content Generation**
    AI-powered world-building assistance:

    - NPC generation with personality and backstory
    - Location development with thematic consistency
    - Quest and plot management
    - Lore consistency checking

🗺️ **Map Management**
    Interactive map operations:

    - Marker creation and updates
    - Layer management
    - Geographic relationship tracking

⚡ **Performance Optimized**
    Built for real-time gameplay:

    - <500ms response target for session-critical operations
    - Intelligent TTL-based caching (5min-1hour)
    - Rate limiting (60 requests/min) with token bucket
    - Automatic retry with exponential backoff

🔐 **Type-Safe & Tested**
    Production-ready code quality:

    - Pydantic v2 models with strict validation
    - ≥85% branch coverage requirement
    - Async/await throughout with httpx
    - Comprehensive error handling

Use Cases
---------

**For Dungeon Masters**
    - Prepare session content with AI assistance
    - Take notes during live gameplay without disrupting flow
    - Generate NPCs and locations on-the-fly
    - Maintain campaign continuity and consistency

**For World-Builders**
    - Develop rich, interconnected lore
    - Maintain internal consistency across articles
    - Organize complex world hierarchies
    - Generate content ideas and expand existing lore

**For API Developers**
    - Reference implementation of World Anvil Boromir API v2
    - Async Python patterns with httpx
    - Type-safe data models with Pydantic
    - Error handling and retry patterns

Architecture
------------

The server follows a clean layered architecture::

    WorldAnvilClient (main entry point)
      └─> Endpoint Classes (ArticleEndpoint, WorldEndpoint, etc.)
           └─> BaseEndpoint (generic request handling)
                ├─> ResponseCache (TTL-based caching)
                ├─> RateLimiter (token bucket, 60 req/min)
                └─> Retry Logic (tenacity with exponential backoff)

    FastMCP Server (MCP protocol layer)
      └─> Tool Handlers (route MCP calls to client methods)

For detailed architecture documentation, see :doc:`architecture/index`.

Getting Started
---------------

1. **Installation**: :doc:`installation`
2. **Quick Start**: :doc:`quickstart`
3. **API Reference**: :doc:`api/index`
4. **Workflows**: :doc:`workflows/index`

Development
-----------

For contributing to the project, see :doc:`development/index`.

License
-------

BSD 3-Clause License - see LICENSE file for details.

Copyright (c) 2025, Steven Peterson
