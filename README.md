# World Anvil MCP Server

MCP (Model Context Protocol) server for interfacing with World Anvil API to assist with D&D world development.

## Overview

This MCP server bridges Claude Code with the World Anvil platform, enabling AI-assisted worldbuilding through structured tools, resources, and prompts. Designed specifically for D&D campaign management and creative writing.

## Features

- **Content Management**: Articles, blocks, categories, manuscripts
- **Map Integration**: Interactive maps with markers and layers
- **Campaign Tools**: RPG systems, timelines, session notes
- **D&D Assistance**: NPC generation, location design, quest tracking
- **Notebook System**: Organized notes and documentation

## Prerequisites

- Python 3.11+
- World Anvil account with Grandmaster guild membership
- World Anvil API application key
- World Anvil user authentication token

## Installation

```bash
# Clone repository
cd world-anvil

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

## Configuration

Create a `.env` file:

```env
WORLD_ANVIL_APP_KEY=your_application_key_here
WORLD_ANVIL_USER_TOKEN=your_user_token_here
```

## Usage

### Running the Server

```bash
# Start MCP server with stdio transport
world-anvil-mcp

# Or run directly with Python
python -m world_anvil_mcp.server
```

### With Claude Code

Add to your MCP settings:

```json
{
  "mcpServers": {
    "world-anvil": {
      "command": "world-anvil-mcp"
    }
  }
}
```

## Documentation

- [Design Specification](claudedocs/DESIGN_SPECIFICATION.md) - Complete architecture and design
- [API Reference](claudedocs/API_REFERENCE.md) - Tool and resource documentation
- [Usage Examples](claudedocs/USAGE_EXAMPLES.md) - Common workflows

## Project Status

🚧 **In Development** - Phase 1 (Core Infrastructure)

See [Design Specification](claudedocs/DESIGN_SPECIFICATION.md) for roadmap.

## License

MIT License - See LICENSE file for details

## Resources

- [World Anvil API Documentation](https://www.worldanvil.com/api/external/boromir/documentation)
- [Model Context Protocol](https://modelcontextprotocol.io)
