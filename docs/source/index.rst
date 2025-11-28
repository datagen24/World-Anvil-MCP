World Anvil MCP Server
======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   installation
   quickstart
   api/index
   workflows/index
   specs/index
   development/index
   architecture/index
   research/index

MCP server for World Anvil API integration to assist with D&D world development.

Overview
--------

The World Anvil MCP Server provides Claude Code with direct access to your
World Anvil worlds, enabling AI-assisted D&D campaign management through
natural language interactions.

**Key Features:**

- 🌍 Full CRUD operations for worlds, articles, categories, and more
- 📝 Session note-taking assistance during live gameplay
- 🎭 NPC and location generation with World Anvil integration
- 🗺️ Map management and marker operations
- ⚡ Optimized for real-time session support (<500ms response)
- 🔄 Intelligent caching and rate limiting

Quick Start
-----------

Installation::

    pip install world-anvil-mcp

Configuration::

    # Create .env file
    WORLD_ANVIL_API_KEY=your-application-key
    WORLD_ANVIL_USER_TOKEN=your-user-token

Usage::

    # Start MCP server
    world-anvil-mcp

    # Or with Claude Code
    # Add to your MCP settings:
    {
      "mcpServers": {
        "world-anvil": {
          "command": "world-anvil-mcp"
        }
      }
    }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
