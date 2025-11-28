# Code Style and Conventions

## Language
Python 3.11+ with type hints

## Style Standards

### General
- **Line Length**: 100 characters (configured in pyproject.toml)
- **Formatter**: ruff
- **Linter**: ruff (E, F, I, N, W, UP rules enabled)
- **Type Checker**: mypy (strict mode)

### Naming Conventions
- **Functions/Methods**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private members**: `_leading_underscore`
- **Module names**: `snake_case.py`

### Type Hints
- **Required**: All function signatures must have type hints
- **Return types**: Always specify, use `None` for no return
- **Async functions**: Use `async def` with proper return type hints
- **Generic types**: Import from `typing` module

### Docstrings
- **Format**: Google style docstrings
- **Required for**: All public functions, classes, modules
- **Structure**:
  ```python
  """Short description.

  Longer description if needed.

  Args:
      param1: Description
      param2: Description

  Returns:
      Description of return value

  Raises:
      ExceptionType: When this exception occurs
  """
  ```

### Import Organization
- **Order**: Standard library → Third party → Local
- **Sorting**: Alphabetical within each group
- **Style**: One import per line for clarity
- **Tool**: ruff handles import sorting (I rule)

### Async Code
- **Prefer**: `async`/`await` over callbacks
- **HTTP**: Use `httpx.AsyncClient` for API calls
- **MCP**: All tools should be async-capable

### Error Handling
- **Custom Exceptions**: Define in `api/exceptions.py`
- **Hierarchy**: Inherit from base `WorldAnvilError`
- **Context**: Include helpful error messages
- **Logging**: Use `ctx.error()`, `ctx.warning()`, `ctx.info()` in MCP tools

### Example Function
```python
async def get_article(
    world_id: str,
    article_id: str,
    granularity: int = 1,
    ctx: Context | None = None
) -> dict[str, Any]:
    """Retrieve article details from World Anvil.

    Args:
        world_id: World containing the article
        article_id: Article identifier
        granularity: Detail level (0=preview, 1=standard, 2=detailed)
        ctx: MCP context for logging and progress

    Returns:
        Article content and metadata as dictionary

    Raises:
        AuthenticationError: If API authentication fails
        NotFoundError: If article doesn't exist
    """
    try:
        client = get_api_client()
        article = await client.get_article(world_id, article_id, granularity)
        if ctx:
            await ctx.info(f"Retrieved article: {article.title}")
        return article.model_dump()
    except Exception as e:
        if ctx:
            await ctx.error(f"Failed to get article: {str(e)}")
        raise
```

## Testing Standards
- **Framework**: pytest with pytest-asyncio
- **Coverage**: Target 80%+ coverage
- **Async tests**: Use `@pytest.mark.asyncio` decorator
- **Mocking**: Mock external API calls
- **Fixtures**: Define reusable test fixtures

## Git Conventions
- **Commits**: Descriptive messages, present tense
- **Branches**: `feature/name`, `fix/name`, `docs/name`
- **Format**: "Add X", "Fix Y", "Update Z" (not "Added", "Fixed")
