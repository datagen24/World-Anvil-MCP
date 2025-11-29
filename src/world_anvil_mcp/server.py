"""World Anvil MCP Server entry point.

This module initializes and runs the FastMCP server with World Anvil integration.
"""

import json
import os
from typing import Any

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP(
    name="World Anvil Assistant",
)


@mcp.tool()
async def get_api_status() -> dict[str, Any]:
    """Check World Anvil API connection status.

    Returns:
        Dictionary with API status information
    """
    app_key = os.getenv("WORLD_ANVIL_APP_KEY")
    user_token = os.getenv("WORLD_ANVIL_USER_TOKEN")

    return {
        "status": "ready" if (app_key and user_token) else "not_configured",
        "has_app_key": bool(app_key),
        "has_user_token": bool(user_token),
        "api_base": os.getenv(
            "WORLD_ANVIL_API_BASE", "https://www.worldanvil.com/api/external/boromir"
        ),
    }


@mcp.resource("config://status")
def get_config_status() -> str:
    """Expose server configuration status as a resource.

    Returns:
        JSON string with configuration details
    """
    app_key = os.getenv("WORLD_ANVIL_APP_KEY")
    user_token = os.getenv("WORLD_ANVIL_USER_TOKEN")

    status = {
        "server": "World Anvil MCP",
        "version": "0.1.0",
        "configured": bool(app_key and user_token),
        "api_base": os.getenv(
            "WORLD_ANVIL_API_BASE", "https://www.worldanvil.com/api/external/boromir"
        ),
    }

    return json.dumps(status, indent=2)


def main() -> None:
    """Run the MCP server."""
    # Check for required environment variables
    if not os.getenv("WORLD_ANVIL_APP_KEY"):
        print("Warning: WORLD_ANVIL_APP_KEY not set")
        print("Set it in .env or environment variables")

    if not os.getenv("WORLD_ANVIL_USER_TOKEN"):
        print("Warning: WORLD_ANVIL_USER_TOKEN not set")
        print("Set it in .env or environment variables")

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
