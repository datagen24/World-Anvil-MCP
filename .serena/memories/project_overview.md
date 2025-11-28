# World Anvil MCP Server - Project Overview

## Purpose
MCP (Model Context Protocol) server for interfacing with World Anvil API to assist with D&D world development. Bridges Claude Code with the World Anvil platform for AI-assisted worldbuilding through structured tools, resources, and prompts.

## Target Users
- D&D Dungeon Masters managing campaigns
- Fantasy writers using World Anvil for worldbuilding
- Worldbuilders seeking AI assistance with content creation

## Key Features
- **Content Management**: Create and manage articles, blocks, categories, manuscripts
- **Map Integration**: Interactive maps with markers, layers, and marker groups
- **Campaign Tools**: RPG systems, timelines, histories, session logs
- **D&D Assistance**: NPC generation, location design, quest tracking
- **Notebook System**: Organized notes and documentation
- **Resource Exposure**: Make World Anvil data accessible as MCP resources for AI context

## Tech Stack
- **Language**: Python 3.11+
- **MCP Framework**: FastMCP (from @modelcontextprotocol/python-sdk)
- **HTTP Client**: httpx (async)
- **Data Validation**: Pydantic v2
- **Configuration**: python-dotenv
- **Reliability**: tenacity (retry logic)
- **Caching**: cachetools
- **API Spec**: OpenAPI 3.0.3 (Boromir v2)

## Authentication
- **Application Key**: `x-application-key` header (requires Grandmaster guild membership)
- **User Token**: `x-auth-token` header (per-user authentication)
- Both keys required for all API requests

## Project Status
🚧 Phase 1: Core Infrastructure - Initial setup complete, API client implementation next

## Development Environment
- **OS**: macOS (Darwin)
- **Package Manager**: uv (recommended) or pip
- **Python Version**: 3.11 minimum
