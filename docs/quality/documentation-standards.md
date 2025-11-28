# Documentation Standards

**Phase**: 0.3 - Quality Standards
**Status**: Complete
**Date**: 2025-11-28

---

## Overview

This document establishes comprehensive documentation standards for the World Anvil MCP Server project, ensuring clear, consistent, and maintainable documentation across code, APIs, and user-facing materials.

---

## Documentation Philosophy

### Core Principles

1. **Clarity First**: Write for understanding, not cleverness
2. **Audience Awareness**: Tailor content to reader's knowledge level
3. **Examples Required**: Show, don't just tell
4. **Maintenance Mindset**: Keep docs current with code changes
5. **Discoverability**: Make information easy to find

### Documentation Types

| Type | Audience | Location | Update Frequency |
|------|----------|----------|------------------|
| Code Documentation | Developers | Inline docstrings | With code changes |
| API Reference | Integration developers | Auto-generated | Automated |
| User Guide | End users | `docs/` | Major releases |
| Developer Guide | Contributors | `docs/` | As needed |
| Architecture Decisions | Technical stakeholders | `docs/adr/` | Per decision |

---

## Docstring Standards

### Format: Google Style

We use Google-style docstrings as enforced by ruff's pydocstyle rules.

### Module Docstrings

**Location**: First line of every `.py` file
**Required**: Yes, for all non-test modules

```python
"""World Anvil API client implementation.

This module provides an async HTTP client for the World Anvil Boromir API v2,
with built-in caching, rate limiting, and retry logic optimized for MCP usage.

The WorldAnvilClient class serves as the main entry point for all API operations,
delegating to specialized endpoint classes for different resource types.

Typical usage example:

    from world_anvil_mcp.client import WorldAnvilClient

    async with WorldAnvilClient(app_key="...", user_token="...") as client:
        article = await client.articles.get("article-id")
        print(f"{article.title}: {article.content}")

See Also:
    - WorldAnvilClient: Main client class
    - endpoints.articles: Article endpoint operations
"""
```

### Class Docstrings

**Location**: Immediately after class definition
**Required**: Yes, for all public classes

```python
class WorldAnvilClient:
    """Async HTTP client for World Anvil Boromir API v2.

    Provides MCP-optimized access to World Anvil resources with built-in
    caching, rate limiting, and retry logic. Designed for use as an async
    context manager to ensure proper HTTP client lifecycle management.

    The client delegates to specialized endpoint classes for different
    resource types (users, worlds, articles, etc.), each providing
    type-safe methods for CRUD operations.

    Attributes:
        users: User endpoint operations (UserEndpoint).
        worlds: World endpoint operations (WorldEndpoint).
        articles: Article endpoint operations (ArticleEndpoint).
        categories: Category endpoint operations (CategoryEndpoint).
        ctx: Optional MCP Context for logging and progress reporting.
        cache: Response cache for reducing API calls.
        rate_limiter: Token bucket rate limiter (60 req/min default).

    Example:
        Basic usage with authentication:

        >>> async with WorldAnvilClient(
        ...     app_key="your-app-key",
        ...     user_token="your-user-token"
        ... ) as client:
        ...     user = await client.users.get_identity()
        ...     print(f"Logged in as {user.username}")

        With MCP Context for logging:

        >>> from mcp import Context
        >>> ctx = Context()
        >>> async with WorldAnvilClient(
        ...     app_key="...",
        ...     user_token="...",
        ...     ctx=ctx
        ... ) as client:
        ...     article = await client.articles.get("article-id")

    Note:
        Always use as async context manager to ensure HTTP client cleanup.
        The client will automatically handle retries for transient failures
        and respect rate limits.

    Raises:
        AuthenticationError: If credentials are invalid.
        ValueError: If required parameters are missing or invalid.
    """
```

### Function/Method Docstrings

**Location**: Immediately after function/method definition
**Required**: Yes, for all public functions and methods

```python
async def get_article(
    self,
    article_id: str,
    granularity: str = "1"
) -> Article:
    """Retrieve a single article by ID.

    Fetches article details from the World Anvil API with the specified
    level of detail. Higher granularity values return more information
    but may increase response time.

    Args:
        article_id: Unique identifier for the article. Must be a valid
            World Anvil article ID (e.g., "abc123def456").
        granularity: Detail level as string. Valid values are "-1", "0",
            "1", "2", "3". Higher values return more detail. Defaults to "1".
            - "-1": Minimal data (ID and title only)
            - "0": Basic metadata (no content)
            - "1": Standard metadata (default)
            - "2": Full content included
            - "3": Extended metadata and relationships

    Returns:
        Article object populated with data based on granularity level.
        The returned article will always include id, title, state, and url.
        Content field is only populated at granularity "2" or higher.

    Raises:
        NotFoundError: Article with the given ID does not exist.
        AuthenticationError: Invalid or missing authentication credentials.
        RateLimitError: Rate limit exceeded (60 requests per minute).
        ServerError: World Anvil API server error (500-599 status codes).
        ValidationError: Invalid article_id or granularity value format.

    Example:
        Basic retrieval with default granularity:

        >>> article = await client.articles.get("abc123")
        >>> print(f"{article.title} - {article.state}")

        Retrieve with full content:

        >>> article = await client.articles.get("abc123", granularity="2")
        >>> print(f"Content: {article.content}")

    Note:
        Responses are cached for 5 minutes. Subsequent calls with the same
        article_id and granularity will return cached data.

    See Also:
        - list_articles: Retrieve multiple articles
        - search_articles: Search for articles by query
    """
```

### Property Docstrings

**Location**: Immediately after property definition
**Required**: Yes, for non-trivial properties

```python
@property
def is_published(self) -> bool:
    """True if article state is 'public', False otherwise.

    Convenience property for checking publication status without
    needing to know the specific state values.

    Returns:
        bool: True if state == "public", False for draft/private/other.

    Example:
        >>> if article.is_published:
        ...     print("Article is live")
        ... else:
        ...     print("Article is not public")
    """
    return self.state == "public"
```

### Exception Docstrings

**Location**: Immediately after exception class definition
**Required**: Yes, for all custom exceptions

```python
class NotFoundError(WorldAnvilError):
    """Requested resource does not exist.

    Raised when an API request returns a 404 status code, indicating
    the specified resource (article, world, category, etc.) could not
    be found.

    Attributes:
        resource_type: Type of resource that was not found (e.g., "article").
        resource_id: ID of the resource that was requested.
        message: Human-readable error message.

    Example:
        >>> try:
        ...     article = await client.articles.get("invalid-id")
        ... except NotFoundError as e:
        ...     print(f"Article {e.resource_id} not found")
    """
```

---

## API Documentation

### Auto-Generated Documentation

We use **mkdocs** with **mkdocstrings** for automated API documentation generation.

### Configuration

**File**: `mkdocs.yml`

```yaml
site_name: World Anvil MCP Server
site_description: MCP server for World Anvil API integration
site_author: Steven Peterson
repo_url: https://github.com/yourusername/world-anvil-mcp
edit_uri: edit/main/docs/

theme:
  name: material
  palette:
    - scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - navigation.top
    - search.suggest
    - content.code.annotate

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true
            show_category_heading: true
            members_order: source
            group_by_category: true
            show_signature_annotations: true

nav:
  - Home: index.md
  - User Guide:
      - Installation: user-guide/installation.md
      - Quick Start: user-guide/quickstart.md
      - Configuration: user-guide/configuration.md
      - Workflows: user-guide/workflows.md
  - API Reference:
      - Client: api/client.md
      - Endpoints: api/endpoints.md
      - Models: api/models.md
      - Exceptions: api/exceptions.md
  - Developer Guide:
      - Contributing: dev/contributing.md
      - Architecture: dev/architecture.md
      - Testing: dev/testing.md
      - Quality Standards: dev/quality.md
  - Architecture:
      - Decisions: adr/index.md
      - Client Design: specs/client-architecture.md
      - Tool Specifications: specs/tool-specifications.md

markdown_extensions:
  - admonition
  - codehilite
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.tabbed:
      alternate_style: true
  - toc:
      permalink: true
```

### API Reference Pages

**File**: `docs/api/client.md`

```markdown
# Client API Reference

## WorldAnvilClient

::: world_anvil_mcp.client.WorldAnvilClient
    options:
      show_root_heading: true
      show_source: true
      members:
        - __init__
        - __aenter__
        - __aexit__
        - users
        - worlds
        - articles
        - categories

## Usage Examples

### Basic Authentication

```python
from world_anvil_mcp.client import WorldAnvilClient

async with WorldAnvilClient(
    app_key="your-app-key",
    user_token="your-user-token"
) as client:
    user = await client.users.get_identity()
    print(f"Logged in as {user.username}")
```

### With MCP Context

```python
from mcp import Context
from world_anvil_mcp.client import WorldAnvilClient

ctx = Context()
async with WorldAnvilClient(
    app_key="...",
    user_token="...",
    ctx=ctx
) as client:
    article = await client.articles.get("article-id", granularity="2")
    await ctx.info(f"Retrieved: {article.title}")
```
```

---

## README Structure

### Project README

**File**: `README.md` (root directory)

```markdown
# World Anvil MCP Server

> MCP server for World Anvil API integration to assist with D&D world development

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-1.0+-green.svg)](https://github.com/modelcontextprotocol/python-sdk)

## Overview

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

## Quick Start

### Installation

```bash
# Using pip
pip install world-anvil-mcp

# From source
git clone https://github.com/yourusername/world-anvil-mcp.git
cd world-anvil-mcp
pip install -e .
```

### Configuration

1. **Get your World Anvil API credentials**:
   - Application Key: [Get from World Anvil](https://www.worldanvil.com/api-keys)
   - User Token: [Your user authentication token]

2. **Create `.env` file**:

```env
WORLD_ANVIL_API_KEY=your-application-key
WORLD_ANVIL_USER_TOKEN=your-user-token
```

3. **Configure Claude Code**:

Add to your `mcp_config.json`:

```json
{
  "mcpServers": {
    "world-anvil": {
      "command": "python",
      "args": ["-m", "world_anvil_mcp"],
      "env": {
        "WORLD_ANVIL_API_KEY": "your-key",
        "WORLD_ANVIL_USER_TOKEN": "your-token"
      }
    }
  }
}
```

### Usage

Once configured, use natural language with Claude Code:

```
You: "Show me my World Anvil worlds"
Claude: *Uses list_worlds tool* You have 3 worlds: ...

You: "Get details about my 'Storm King's Thunder' campaign"
Claude: *Uses get_world and list_articles tools* ...

You: "Start session notes for tonight's game"
Claude: *Enters session note-taking workflow* ...
```

## Documentation

- **[User Guide](docs/user-guide/)**: Installation, configuration, workflows
- **[API Reference](docs/api/)**: Complete API documentation
- **[Developer Guide](docs/dev/)**: Contributing, architecture, testing
- **[Workflows](docs/workflows/)**: Example use cases and patterns

## Supported Workflows

- **[Session Note-Taking](docs/workflows/session-note-taking.md)**: Real-time note capture during play
- **[NPC Generation](docs/workflows/npc-generation.md)**: Create and track NPCs
- **[World Building](docs/workflows/world-building.md)**: Develop locations and lore
- **[Session Prep](docs/workflows/session-prep.md)**: Prepare for upcoming sessions
- **[Content Search](docs/workflows/content-search.md)**: Quick reference lookup

[See all 10 workflows →](docs/workflows/)

## Requirements

- Python 3.11+
- World Anvil account with API access
- Claude Code (for MCP integration)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/world-anvil-mcp.git
cd world-anvil-mcp

# Install with dev dependencies
pip install -e ".[dev,test]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# All tests with coverage
pytest --cov=src --cov-report=term-missing

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration
```

### Code Quality

```bash
# Format code
ruff format .

# Lint
ruff check --fix .

# Type check
mypy src/
```

## Architecture

The project follows a modular architecture optimized for MCP:

```
WorldAnvilClient (main entry point)
├── UserEndpoint
├── WorldEndpoint
├── ArticleEndpoint
├── CategoryEndpoint
└── ... (15+ endpoint classes)

Supporting Components:
├── ResponseCache (TTL-based caching)
├── RateLimiter (token bucket)
└── Context Integration (MCP logging)
```

See **[Architecture Documentation](docs/specs/client-architecture.md)** for details.

## Contributing

We welcome contributions! Please see **[Contributing Guide](docs/dev/contributing.md)**.

### Development Standards

- **Code Quality**: ruff (format + lint) + mypy (strict type checking)
- **Test Coverage**: ≥85% required
- **Documentation**: Google-style docstrings for all public APIs
- **Git Workflow**: Feature branches with meaningful commits

## License

BSD 3-Clause License - see **[LICENSE](LICENSE)** for details.

## Acknowledgments

- [World Anvil](https://www.worldanvil.com/) for the excellent world-building platform
- [pywaclient](https://gitlab.com/SoulLink/world-anvil-api-client) for API pattern reference
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for MCP framework

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/world-anvil-mcp/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/world-anvil-mcp/discussions)
- **Documentation**: [Full Documentation](https://yourusername.github.io/world-anvil-mcp/)

---

**Status**: Active Development | **Phase**: 0.3 (Quality Standards)
```

---

## User Guide Documentation

### Installation Guide

**File**: `docs/user-guide/installation.md`

```markdown
# Installation Guide

## Prerequisites

Before installing the World Anvil MCP Server, ensure you have:

- **Python 3.11 or higher**: [Download Python](https://www.python.org/downloads/)
- **World Anvil account**: [Sign up](https://www.worldanvil.com/register)
- **API credentials**: [Get API keys](https://www.worldanvil.com/api-keys)
- **Claude Code**: [Install Claude Code](https://claude.ai/code)

## Installation Methods

### Method 1: Using pip (Recommended)

```bash
pip install world-anvil-mcp
```

### Method 2: From Source

```bash
git clone https://github.com/yourusername/world-anvil-mcp.git
cd world-anvil-mcp
pip install -e .
```

### Method 3: Using pipx (Isolated Environment)

```bash
pipx install world-anvil-mcp
```

## Configuration

### 1. Obtain API Credentials

1. Log in to [World Anvil](https://www.worldanvil.com/)
2. Navigate to [API Keys](https://www.worldanvil.com/api-keys)
3. Create new application key
4. Copy your user authentication token

### 2. Set Environment Variables

Create `.env` file in your project directory:

```env
WORLD_ANVIL_API_KEY=your-application-key-here
WORLD_ANVIL_USER_TOKEN=your-user-token-here
```

**Security Note**: Never commit `.env` to version control!

### 3. Configure Claude Code

Add to `~/.claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "world-anvil": {
      "command": "python",
      "args": ["-m", "world_anvil_mcp"],
      "env": {
        "WORLD_ANVIL_API_KEY": "${WORLD_ANVIL_API_KEY}",
        "WORLD_ANVIL_USER_TOKEN": "${WORLD_ANVIL_USER_TOKEN}"
      }
    }
  }
}
```

## Verification

### Test Connection

```python
import asyncio
from world_anvil_mcp.client import WorldAnvilClient

async def test_connection():
    async with WorldAnvilClient(
        app_key="your-key",
        user_token="your-token"
    ) as client:
        user = await client.users.get_identity()
        print(f"Connected as: {user.username}")

asyncio.run(test_connection())
```

Expected output:
```
Connected as: YourUsername
```

## Troubleshooting

### Common Issues

**ImportError: No module named 'world_anvil_mcp'**

Solution: Ensure package is installed:
```bash
pip install world-anvil-mcp
# or
pip install -e .  # if installing from source
```

**AuthenticationError: Invalid credentials**

Solution: Verify your API credentials:
- Check `.env` file has correct values
- Ensure no extra spaces in keys
- Verify keys are active on World Anvil

**RateLimitError: Rate limit exceeded**

Solution: Default limit is 60 requests/minute:
- Wait 60 seconds and retry
- Reduce request frequency
- Enable caching (on by default)

## Next Steps

- **[Quick Start Guide](quickstart.md)**: First steps with the server
- **[Configuration Guide](configuration.md)**: Advanced configuration
- **[Workflows](../workflows/)**: Example use cases
```

---

## Developer Guide Documentation

### Contributing Guide

**File**: `docs/dev/contributing.md`

```markdown
# Contributing Guide

Thank you for your interest in contributing to the World Anvil MCP Server!

## Getting Started

### 1. Fork and Clone

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/world-anvil-mcp.git
cd world-anvil-mcp
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev,test]"

# Install pre-commit hooks
pre-commit install
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Workflow

### Code Quality Standards

All code must pass:

1. **ruff format**: Code formatting
2. **ruff check**: Linting
3. **mypy**: Type checking (strict mode)
4. **pytest**: All tests with ≥85% coverage

```bash
# Check everything
make quality

# Individual checks
ruff format .           # Format code
ruff check --fix .      # Lint and auto-fix
mypy src/               # Type check
pytest --cov=src        # Run tests with coverage
```

### Writing Code

Follow these standards:

- **Type hints**: All public functions fully annotated
- **Docstrings**: Google-style for all public APIs
- **Tests**: Unit tests for all new functionality
- **Coverage**: Maintain ≥85% test coverage

See:
- **[Code Quality Rules](../quality/code-quality-rules.md)**
- **[Testing Requirements](../quality/testing-requirements.md)**
- **[Documentation Standards](../quality/documentation-standards.md)**

### Commit Messages

Use conventional commit format:

```
type(scope): Brief description

Longer explanation if needed.

Fixes #123
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

Example:
```
feat(articles): Add support for article content updates

Implement PATCH endpoint for updating article content and metadata.
Includes validation, error handling, and comprehensive tests.

Fixes #42
```

## Pull Request Process

### 1. Ensure Quality

```bash
# All checks must pass
make quality

# Coverage must be ≥85%
pytest --cov=src --cov-fail-under=85
```

### 2. Update Documentation

- Add/update docstrings for new code
- Update relevant user/developer guides
- Add examples if introducing new features

### 3. Create Pull Request

1. Push to your fork
2. Create PR against `main` branch
3. Fill out PR template completely
4. Link related issues

### 4. Code Review

- Address reviewer feedback
- Keep PR focused and reasonably sized
- Maintain clean commit history

## Testing Guidelines

### Test Types

Write tests for all three levels:

1. **Unit Tests**: Test components in isolation
2. **Integration Tests**: Test component interactions (mocked API)
3. **E2E Tests**: Test against live API (optional, requires credentials)

Example:

```python
# tests/endpoints/test_articles.py

@pytest.mark.unit
def test_article_model_validation():
    """Article model validates required fields."""
    # Test Pydantic model validation
    ...

@pytest.mark.integration
@respx.mock
async def test_get_article_success():
    """Successfully retrieve article with mocked API."""
    # Test with mocked HTTP responses
    ...

@pytest.mark.e2e
@pytest.mark.skipif(not has_credentials, reason="No API credentials")
async def test_get_article_live():
    """Retrieve article from live API."""
    # Test with real World Anvil API
    ...
```

### Test Coverage

Aim for:
- ≥85% overall coverage
- 100% for error handling
- 100% for public API surface

## Documentation Guidelines

### Docstrings

Every public API needs comprehensive docstring:

```python
async def get_article(self, article_id: str, granularity: str = "1") -> Article:
    """Retrieve a single article by ID.

    Args:
        article_id: Unique identifier for the article.
        granularity: Detail level ("-1", "0", "1", "2", "3").

    Returns:
        Article object with details based on granularity.

    Raises:
        NotFoundError: Article does not exist.
        AuthenticationError: Invalid credentials.

    Example:
        >>> article = await client.articles.get("abc123", granularity="2")
        >>> print(article.title)
    """
```

See **[Documentation Standards](../quality/documentation-standards.md)** for complete guidelines.

## Questions?

- Open a **[Discussion](https://github.com/yourusername/world-anvil-mcp/discussions)**
- Ask in PR comments
- Review existing **[Issues](https://github.com/yourusername/world-anvil-mcp/issues)**

Thank you for contributing! 🎉
```

---

## Change Documentation

### CHANGELOG Format

**File**: `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Session note-taking workflow support
- NPC generation tools

### Changed
- Improved cache performance

### Deprecated
- None

### Removed
- None

### Fixed
- Rate limiting edge case

### Security
- None

## [0.1.0] - 2025-11-28

### Added
- Initial release
- Core WorldAnvilClient implementation
- Support for 34 World Anvil API endpoints
- MCP Context integration
- Caching and rate limiting
- Comprehensive test suite (≥85% coverage)
- Complete documentation

[Unreleased]: https://github.com/yourusername/world-anvil-mcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/world-anvil-mcp/releases/tag/v0.1.0
```

---

## Quality Checklist

### Documentation Review Checklist

Before merging documentation changes:

- [ ] All docstrings follow Google style
- [ ] Examples are tested and work
- [ ] No broken links
- [ ] Spelling and grammar checked
- [ ] Code blocks have correct syntax highlighting
- [ ] Screenshots/diagrams up to date
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated

---

## Tools and Automation

### Documentation Build

```bash
# Build documentation locally
mkdocs build

# Serve locally with live reload
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

### Link Checking

```bash
# Install markdown-link-check
npm install -g markdown-link-check

# Check all markdown files
find docs -name "*.md" -exec markdown-link-check {} \;
```

### Spell Checking

```bash
# Install codespell
pip install codespell

# Check spelling
codespell docs/ README.md
```

---

## References

- [Google Style Guide - Docstrings](https://google.github.io/styleguide/pyguide.html#383-functions-and-methods)
- [MkDocs Documentation](https://www.mkdocs.org/)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

**Status**: Complete ✅
**Next**: api-client-patterns.md
