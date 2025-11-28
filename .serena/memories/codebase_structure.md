# Codebase Structure

## Directory Layout

```
world-anvil/
├── README.md                          # Project overview and setup
├── pyproject.toml                     # Python project configuration
├── .env.example                       # Environment variable template
├── openapi.yml                        # World Anvil API OpenAPI 3.0 spec
├── claudedocs/                        # Design and documentation
│   ├── DESIGN_SPECIFICATION.md        # Complete architecture design
│   ├── API_REFERENCE.md               # Tool and resource docs (TBD)
│   └── USAGE_EXAMPLES.md              # Common workflows (TBD)
├── src/world_anvil_mcp/               # Main source code
│   ├── __init__.py                    # Package initialization
│   ├── server.py                      # FastMCP server entry point
│   ├── api/                           # World Anvil API client
│   │   ├── __init__.py
│   │   ├── client.py                  # HTTP client wrapper (TBD)
│   │   ├── models.py                  # Pydantic models (TBD)
│   │   └── exceptions.py              # Custom exceptions (TBD)
│   ├── tools/                         # MCP tools
│   │   ├── __init__.py
│   │   ├── articles.py                # Article management (TBD)
│   │   ├── worlds.py                  # World management (TBD)
│   │   ├── categories.py              # Category tools (TBD)
│   │   ├── maps.py                    # Map tools (TBD)
│   │   └── dnd.py                     # D&D-specific tools (TBD)
│   ├── resources/                     # MCP resources
│   │   ├── __init__.py
│   │   ├── worlds.py                  # World resources (TBD)
│   │   ├── articles.py                # Article resources (TBD)
│   │   └── campaigns.py               # Campaign resources (TBD)
│   ├── prompts/                       # MCP prompts
│   │   ├── __init__.py
│   │   ├── creation.py                # Content creation prompts (TBD)
│   │   └── enhancement.py             # Enhancement prompts (TBD)
│   ├── templates/                     # D&D content templates
│   │   ├── __init__.py
│   │   ├── character.py               # Character template (TBD)
│   │   ├── location.py                # Location template (TBD)
│   │   ├── item.py                    # Item template (TBD)
│   │   └── session.py                 # Campaign session template (TBD)
│   └── utils/                         # Utilities
│       ├── __init__.py
│       ├── cache.py                   # Response caching (TBD)
│       ├── rate_limit.py              # Rate limiting (TBD)
│       └── formatting.py              # Content formatting (TBD)
└── tests/                             # Test suite
    ├── __init__.py
    ├── test_api_client.py             # API client tests (TBD)
    ├── test_tools.py                  # Tool tests (TBD)
    └── test_resources.py              # Resource tests (TBD)
```

## Key Components

### server.py
FastMCP server entry point. Currently implements:
- `get_api_status()` tool - Check API configuration
- `config://status` resource - Expose server config
- `main()` - Entry point for running server

### API Client (TBD)
Will handle all World Anvil API communication:
- Authentication with x-application-key and x-auth-token
- Rate limiting and retry logic
- Response caching
- Pydantic models for type safety

### Tools (TBD)
MCP tools for Claude to execute actions:
- Article CRUD operations
- World and category management
- Map and marker operations
- D&D content generation

### Resources (TBD)
MCP resources to expose World Anvil data:
- World contexts for AI
- Article content access
- Campaign state information

### Prompts (TBD)
Pre-built prompt templates:
- Character creation guidance
- Location design prompts
- Session recap templates
