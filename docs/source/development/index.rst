Development Guide
=================

This guide covers contributing to the World Anvil MCP Server project.

.. toctree::
   :maxdepth: 2
   :caption: Development Topics:

   quality/index

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

**Required**:

- Python 3.11+
- Git
- World Anvil account with API credentials

**Recommended**:

- pyenv or similar for Python version management
- make for automation commands
- VS Code or PyCharm with Python extensions

Development Setup
~~~~~~~~~~~~~~~~~

1. **Clone the repository**:

.. code-block:: bash

    git clone https://github.com/yourusername/world-anvil-mcp.git
    cd world-anvil-mcp

2. **Install development dependencies**:

.. code-block:: bash

    pip install -e ".[dev,test,docs]"

This installs:

- **Core dependencies**: httpx, pydantic, mcp, etc.
- **Dev tools**: ruff, mypy, pre-commit
- **Test tools**: pytest, coverage, respx, faker
- **Docs tools**: sphinx, sphinx-rtd-theme, myst-parser

3. **Install pre-commit hooks**:

.. code-block:: bash

    pre-commit install

This automatically runs quality checks before every commit.

4. **Configure environment**:

Create ``.env`` file:

.. code-block:: bash

    WORLD_ANVIL_API_KEY=your-test-app-key
    WORLD_ANVIL_USER_TOKEN=your-test-user-token

⚠️ **Note**: Use test credentials, not production!

5. **Verify setup**:

.. code-block:: bash

    make quality  # Run all quality checks
    make test     # Run all tests
    make docs     # Build documentation

Development Workflow
--------------------

Standard Development Cycle
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Create feature branch**:

.. code-block:: bash

    git checkout -b feature/your-feature-name

2. **Make changes**:

   - Write code following style guide
   - Add tests for new functionality
   - Update documentation

3. **Run quality checks**:

.. code-block:: bash

    make quality  # Format, lint, typecheck

4. **Run tests**:

.. code-block:: bash

    make test-unit        # Fast unit tests
    make test-integration # Integration tests
    make test-cov         # With coverage report

5. **Commit changes**:

.. code-block:: bash

    git add .
    git commit -m "feat: add new feature"

Pre-commit hooks will automatically:

- Format code with ruff
- Lint with ruff
- Type-check with mypy
- Run unit tests

6. **Push and create PR**:

.. code-block:: bash

    git push origin feature/your-feature-name

Then create a pull request on GitHub.

Makefile Commands
~~~~~~~~~~~~~~~~~

Quick reference for ``make`` targets:

**Development**:

.. code-block:: bash

    make install        # Install package in editable mode
    make install-dev    # Install with dev dependencies
    make install-test   # Install with test dependencies
    make install-docs   # Install with docs dependencies
    make install-all    # Install with all dependencies

**Code Quality**:

.. code-block:: bash

    make format         # Format code with ruff
    make lint           # Lint code with ruff
    make typecheck      # Type-check with mypy
    make quality        # Run all quality checks

**Testing**:

.. code-block:: bash

    make test           # Run all tests
    make test-unit      # Run unit tests only (fast)
    make test-integration # Run integration tests
    make test-e2e       # Run e2e tests (requires live API)
    make test-cov       # Run tests with coverage report
    make test-watch     # Run tests in watch mode

**Documentation**:

.. code-block:: bash

    make docs           # Build Sphinx documentation
    make docs-serve     # Serve docs locally with live reload
    make docs-clean     # Clean documentation build
    make docs-linkcheck # Check for broken links

**Cleanup**:

.. code-block:: bash

    make clean          # Remove build artifacts
    make clean-pyc      # Remove Python cache files
    make clean-test     # Remove test artifacts

**Help**:

.. code-block:: bash

    make help           # Show all available targets

Code Quality Standards
----------------------

Formatting and Linting
~~~~~~~~~~~~~~~~~~~~~~~

We use **ruff** for both formatting and linting:

.. code-block:: bash

    make format  # Auto-format code
    make lint    # Check for issues

Ruff configuration is in ``pyproject.toml``:

- Line length: 100 characters
- Target: Python 3.11+
- Rules: Comprehensive set (see ``pyproject.toml``)

Type Checking
~~~~~~~~~~~~~

We use **mypy** with strict mode:

.. code-block:: bash

    make typecheck

All code must:

- Include type annotations
- Pass strict type checking
- Use Pydantic models for data

Exception: Tests can skip some annotations.

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

**Docstring Format**: Google-style

.. code-block:: python

    def get_article(article_id: str, granularity: str = "2") -> Article:
        """Get a specific article by ID.

        Args:
            article_id: UUID of the article to retrieve.
            granularity: Detail level ("0", "1", "2"). Defaults to "2".

        Returns:
            Article object with complete metadata and content.

        Raises:
            NotFoundError: Article doesn't exist.
            AuthenticationError: Invalid credentials.
            WorldAnvilAPIError: API request failed.

        Example:
            >>> client = WorldAnvilClient()
            >>> article = await client.articles.get("abc-123")
            >>> print(article.title)
        """

**Required for**:

- All public functions and methods
- All classes
- All modules

**Optional for**:

- Private methods (``_method``)
- Simple property getters
- Test functions

Testing Guide
-------------

Test Organization
~~~~~~~~~~~~~~~~~

Tests are organized in ``tests/`` directory:

.. code-block:: text

    tests/
    ├── conftest.py              # Shared fixtures
    ├── unit/                    # Unit tests (fast, no I/O)
    │   ├── test_client.py
    │   ├── test_cache.py
    │   └── test_rate_limiter.py
    ├── integration/             # Integration tests (mocked API)
    │   ├── test_endpoints.py
    │   └── test_error_handling.py
    └── e2e/                     # End-to-end tests (live API)
        └── test_workflows.py

Test Markers
~~~~~~~~~~~~

We use pytest markers to categorize tests:

.. code-block:: python

    @pytest.mark.unit
    def test_cache_basic():
        """Fast unit test with no I/O."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_article_endpoint():
        """Integration test with mocked API."""

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_real_api():
        """E2E test requiring live API."""

    @pytest.mark.slow
    def test_performance():
        """Test that takes >1 second."""

Run specific test types:

.. code-block:: bash

    pytest -m unit              # Only unit tests
    pytest -m integration       # Only integration tests
    pytest -m "not e2e"         # Skip e2e tests
    pytest -m "not slow"        # Skip slow tests

Writing Tests
~~~~~~~~~~~~~

**Unit Tests** - Test individual functions in isolation:

.. code-block:: python

    @pytest.mark.unit
    def test_cache_stores_value():
        """Cache should store and retrieve values."""
        cache = ResponseCache()
        cache.set("key", "value")
        assert cache.get("key") == "value"

**Integration Tests** - Test component interactions with mocked I/O:

.. code-block:: python

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_article_endpoint_success(respx_mock, mock_client_config):
        """ArticleEndpoint should fetch article from API."""
        # Mock API response
        respx_mock.get("/articles/abc-123").mock(
            return_value=httpx.Response(200, json={"id": "abc-123"})
        )

        client = WorldAnvilClient(**mock_client_config)
        article = await client.articles.get("abc-123")
        assert article.id == "abc-123"

**E2E Tests** - Test complete workflows with live API:

.. code-block:: python

    @pytest.mark.e2e
    @pytest.mark.asyncio
    async def test_list_worlds_real_api():
        """Should successfully list worlds from live API."""
        client = WorldAnvilClient()  # Uses real credentials
        worlds = await client.worlds.list()
        assert len(worlds) > 0
        assert all(isinstance(w, World) for w in worlds)

Shared Fixtures
~~~~~~~~~~~~~~~

Use shared fixtures from ``conftest.py``:

.. code-block:: python

    def test_with_faker(faker):
        """Use Faker fixture for test data."""
        name = faker.name()
        assert isinstance(name, str)

    def test_with_config(mock_client_config):
        """Use mock configuration."""
        client = WorldAnvilClient(**mock_client_config)
        assert client.app_key == "test-app-key-12345"

    def test_with_sample_data(sample_article_data):
        """Use sample article JSON."""
        article = Article(**sample_article_data)
        assert article.title

Coverage Requirements
~~~~~~~~~~~~~~~~~~~~~

We require **≥85% branch coverage**:

.. code-block:: bash

    make test-cov  # Run tests with coverage report

Coverage report shows:

- Line coverage percentage
- Missing lines
- Branch coverage
- HTML report in ``htmlcov/``

**Exemptions**:

- ``__init__.py`` files
- ``conftest.py`` files
- Unreachable defensive code (marked with ``# pragma: no cover``)

Git Workflow
------------

Branch Naming
~~~~~~~~~~~~~

Use descriptive branch names:

- ``feature/add-map-endpoints`` - New features
- ``fix/rate-limit-bug`` - Bug fixes
- ``docs/update-api-reference`` - Documentation
- ``test/improve-coverage`` - Test improvements
- ``refactor/simplify-cache`` - Refactoring

Commit Messages
~~~~~~~~~~~~~~~

Follow conventional commits:

.. code-block:: text

    <type>(<scope>): <description>

    [optional body]

    [optional footer]

**Types**:

- ``feat``: New feature
- ``fix``: Bug fix
- ``docs``: Documentation only
- ``test``: Test additions/changes
- ``refactor``: Code refactoring
- ``perf``: Performance improvement
- ``chore``: Build/tooling changes

**Examples**:

.. code-block:: text

    feat(endpoints): add map marker operations

    Implement create, update, and delete operations for map markers.
    Includes comprehensive tests and API documentation.

    Closes #42

.. code-block:: text

    fix(cache): handle None values correctly

    Cache was raising KeyError when None values were stored.
    Now properly handles None as valid cached value.

Pull Request Process
~~~~~~~~~~~~~~~~~~~~

1. **Ensure quality**:

   - All tests pass
   - Coverage ≥85%
   - No linting errors
   - Docs updated

2. **Create PR**:

   - Descriptive title
   - Clear description
   - Link related issues

3. **Code review**:

   - Address reviewer feedback
   - Update as needed

4. **Merge**:

   - Squash commits for clean history
   - Delete feature branch

Project Structure
-----------------

Understanding the Codebase
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    world-anvil-mcp/
    ├── src/
    │   └── world_anvil_mcp/
    │       ├── __init__.py          # Package exports
    │       ├── client.py            # WorldAnvilClient main class
    │       ├── endpoints/           # Endpoint implementations
    │       │   ├── base.py          # BaseEndpoint foundation
    │       │   ├── articles.py      # ArticleEndpoint
    │       │   ├── worlds.py        # WorldEndpoint
    │       │   └── ...
    │       ├── models/              # Pydantic data models
    │       │   ├── article.py       # Article model
    │       │   ├── world.py         # World model
    │       │   └── ...
    │       ├── cache.py             # ResponseCache
    │       ├── rate_limiter.py      # RateLimiter
    │       ├── exceptions.py        # Custom exceptions
    │       └── server.py            # MCP server implementation
    ├── tests/                       # Test suite
    ├── docs/                        # Documentation
    │   ├── source/                  # Sphinx source files
    │   ├── workflows/               # Workflow documentation
    │   └── quality/                 # Quality standards
    ├── pyproject.toml               # Project configuration
    ├── Makefile                     # Development automation
    └── .pre-commit-config.yaml      # Pre-commit hooks

Adding New Features
-------------------

Adding an Endpoint
~~~~~~~~~~~~~~~~~~

1. **Create endpoint class** in ``src/world_anvil_mcp/endpoints/``:

.. code-block:: python

    from .base import BaseEndpoint
    from ..models import MyModel

    class MyEndpoint(BaseEndpoint):
        """Handle operations for MyResource."""

        async def list(self) -> list[MyModel]:
            """List all resources."""
            response = await self._request("GET", "/my-resources")
            return [MyModel(**item) for item in response]

2. **Add model** in ``src/world_anvil_mcp/models/``:

.. code-block:: python

    from pydantic import BaseModel, Field

    class MyModel(BaseModel):
        """Represents a MyResource."""

        id: str = Field(..., description="Resource UUID")
        title: str = Field(..., description="Resource title")

3. **Add to client** in ``src/world_anvil_mcp/client.py``:

.. code-block:: python

    from .endpoints.my_endpoint import MyEndpoint

    class WorldAnvilClient:
        def __init__(self, ...):
            ...
            self.my_resources = MyEndpoint(self._session, ...)

4. **Write tests** in ``tests/unit/`` and ``tests/integration/``:

.. code-block:: python

    @pytest.mark.unit
    def test_my_model_validation():
        """MyModel should validate data correctly."""
        data = {"id": "123", "title": "Test"}
        model = MyModel(**data)
        assert model.id == "123"

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_my_endpoint_list(respx_mock):
        """MyEndpoint.list should fetch resources."""
        respx_mock.get("/my-resources").mock(...)
        client = WorldAnvilClient(...)
        resources = await client.my_resources.list()
        assert len(resources) > 0

5. **Update documentation** in ``docs/source/api/``.

Common Development Tasks
------------------------

Running Tests Locally
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Fast unit tests only
    make test-unit

    # All tests except e2e
    pytest -m "not e2e"

    # Specific test file
    pytest tests/unit/test_cache.py

    # Specific test function
    pytest tests/unit/test_cache.py::test_cache_stores_value

    # With verbose output
    pytest -v

    # With print statements
    pytest -s

Debugging Tests
~~~~~~~~~~~~~~~

Use ``pytest --pdb`` to drop into debugger on failure:

.. code-block:: bash

    pytest --pdb tests/unit/test_cache.py

Or add ``breakpoint()`` in code:

.. code-block:: python

    def test_something():
        result = compute_something()
        breakpoint()  # Debugger will stop here
        assert result == expected

Updating Dependencies
~~~~~~~~~~~~~~~~~~~~~

Update dependencies in ``pyproject.toml``:

.. code-block:: toml

    dependencies = [
        "httpx>=0.27.0",
        "pydantic>=2.6.0",
        "mcp>=1.0.0",
    ]

Then reinstall:

.. code-block:: bash

    pip install -e ".[dev,test,docs]"

Building Documentation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Build HTML docs
    make docs

    # Serve with live reload
    make docs-serve

    # Check for broken links
    make docs-linkcheck

    # Clean build artifacts
    make docs-clean

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Tests failing with authentication errors**:

- Verify ``.env`` file exists with valid credentials
- Use test credentials, not production
- Check that variables are loaded: ``python -c "import os; print(os.getenv('WORLD_ANVIL_API_KEY'))"``

**Pre-commit hooks failing**:

- Run manually: ``pre-commit run --all-files``
- Update hooks: ``pre-commit autoupdate``
- Skip hooks temporarily: ``git commit --no-verify`` (not recommended)

**Type checking errors**:

- Run mypy: ``make typecheck``
- Check ``pyproject.toml`` for mypy configuration
- Add type ignores only as last resort: ``# type: ignore[error-code]``

**Import errors in tests**:

- Ensure editable install: ``pip install -e .``
- Check ``PYTHONPATH``: ``echo $PYTHONPATH``
- Verify package structure with ``__init__.py`` files

Getting Help
~~~~~~~~~~~~

- **Documentation**: https://world-anvil-mcp.readthedocs.io
- **GitHub Issues**: https://github.com/yourusername/world-anvil-mcp/issues
- **Discussions**: https://github.com/yourusername/world-anvil-mcp/discussions

See Also
--------

- :doc:`testing` - Detailed testing guide
- :doc:`quality` - Code quality standards
- :doc:`contributing` - Contributing guidelines
- :doc:`../architecture/index` - Architecture details
