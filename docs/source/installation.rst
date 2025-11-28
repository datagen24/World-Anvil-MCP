Installation
============

This guide covers installing the World Anvil MCP Server for use with Claude Code.

Prerequisites
-------------

**System Requirements**:

- Python 3.11 or higher
- pip (Python package installer)
- Git (for development installation)

**World Anvil API Credentials**:

You'll need two credentials from World Anvil:

1. **Application Key** (``x-application-key``): Your app's API key
2. **User Token** (``x-auth-token``): Your personal authentication token

To obtain these credentials:

1. Log in to `World Anvil <https://www.worldanvil.com>`_
2. Navigate to your `API settings <https://www.worldanvil.com/api-settings>`_
3. Generate or copy your application key and user token

⚠️ **Security Note**: Never commit these credentials to version control.

Installation Methods
--------------------

Standard Installation
~~~~~~~~~~~~~~~~~~~~~

Install from PyPI (recommended for users):

.. code-block:: bash

    pip install world-anvil-mcp

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

Install from source (recommended for contributors):

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/yourusername/world-anvil-mcp.git
    cd world-anvil-mcp

    # Install in editable mode with all dependencies
    pip install -e ".[dev,test,docs]"

    # Install pre-commit hooks
    pre-commit install

This installs:

- **Core package**: The MCP server and World Anvil client
- **Dev tools**: ruff, mypy, pre-commit
- **Test tools**: pytest, coverage, respx, faker
- **Docs tools**: sphinx, sphinx-rtd-theme, myst-parser

Configuration
-------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Create a ``.env`` file in your project root:

.. code-block:: bash

    # World Anvil API credentials
    WORLD_ANVIL_API_KEY=your-application-key-here
    WORLD_ANVIL_USER_TOKEN=your-user-token-here

    # Optional: Custom base URL (defaults to official API)
    # WORLD_ANVIL_BASE_URL=https://www.worldanvil.com/api/external/boromir

Claude Code Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the MCP server to your Claude Code settings:

**File**: ``~/.claude/mcp_settings.json`` (or your Claude Code config location)

.. code-block:: json

    {
      "mcpServers": {
        "world-anvil": {
          "command": "world-anvil-mcp",
          "env": {
            "WORLD_ANVIL_API_KEY": "your-application-key-here",
            "WORLD_ANVIL_USER_TOKEN": "your-user-token-here"
          }
        }
      }
    }

Alternatively, use environment variables from your shell:

.. code-block:: json

    {
      "mcpServers": {
        "world-anvil": {
          "command": "world-anvil-mcp"
        }
      }
    }

Then set environment variables in your shell:

.. code-block:: bash

    export WORLD_ANVIL_API_KEY="your-application-key-here"
    export WORLD_ANVIL_USER_TOKEN="your-user-token-here"

Verification
------------

Test Basic Installation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Start the MCP server (for testing)
    world-anvil-mcp

    # Or verify the package is importable
    python -c "from world_anvil_mcp import WorldAnvilClient; print('✓ Installation successful')"

Test with Claude Code
~~~~~~~~~~~~~~~~~~~~~

1. Start Claude Code
2. The World Anvil MCP server should auto-start
3. Test with a simple query:

.. code-block:: text

    You: "List my World Anvil worlds"
    Claude: [Uses world-anvil MCP server to fetch your worlds]

Development Setup
-----------------

For Development Installation Only
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After installing with ``pip install -e ".[dev,test,docs]"``:

.. code-block:: bash

    # Run all quality checks
    make quality

    # Run tests
    make test

    # Build documentation
    make docs

    # See all available commands
    make help

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Error: No module named 'world_anvil_mcp'**
    - Ensure installation completed: ``pip show world-anvil-mcp``
    - Try reinstalling: ``pip install --upgrade --force-reinstall world-anvil-mcp``

**Authentication Failed**
    - Verify credentials are correct in ``.env`` or MCP settings
    - Check that credentials use lowercase headers:
      - ``x-application-key`` (not ``X-Application-Key``)
      - ``x-auth-token`` (not ``X-Auth-Token``)

**MCP Server Not Starting**
    - Check Claude Code logs for error messages
    - Verify ``world-anvil-mcp`` command is in PATH: ``which world-anvil-mcp``
    - Try running manually: ``world-anvil-mcp`` (should start server)

**Rate Limiting Errors**
    - The server automatically handles rate limiting (60 req/min)
    - If you see frequent rate limit errors, reduce request frequency
    - Check if multiple MCP instances are running

Getting Help
~~~~~~~~~~~~

- **Documentation**: https://world-anvil-mcp.readthedocs.io
- **GitHub Issues**: https://github.com/yourusername/world-anvil-mcp/issues
- **World Anvil API Docs**: https://www.worldanvil.com/api/external/boromir/documentation

Next Steps
----------

Once installed, see the :doc:`quickstart` guide for usage examples.
