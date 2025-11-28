# Suggested Commands

## Development Setup

### Initial Setup
```bash
# Install dependencies with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"

# Create .env file from template
cp .env.example .env
# Then edit .env with your API keys
```

### Environment Configuration
```bash
# Required environment variables
export WORLD_ANVIL_APP_KEY=your_application_key
export WORLD_ANVIL_USER_TOKEN=your_user_token

# Or edit .env file:
# WORLD_ANVIL_APP_KEY=your_application_key
# WORLD_ANVIL_USER_TOKEN=your_user_token
```

## Running the Server

### Start MCP Server
```bash
# Run with entry point
world-anvil-mcp

# Or run directly
python -m world_anvil_mcp.server

# Run from source
python src/world_anvil_mcp/server.py
```

## Code Quality

### Linting
```bash
# Run ruff linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Check specific file
ruff check src/world_anvil_mcp/server.py
```

### Formatting
```bash
# Format code with ruff
ruff format .

# Check formatting without changes
ruff format --check .
```

### Type Checking
```bash
# Run mypy type checker
mypy src/world_anvil_mcp

# Check specific file
mypy src/world_anvil_mcp/server.py
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=world_anvil_mcp

# Run specific test file
pytest tests/test_api_client.py

# Run with verbose output
pytest -v

# Run async tests specifically
pytest -v -k async
```

### Coverage Report
```bash
# Generate coverage report
pytest --cov=world_anvil_mcp --cov-report=html

# View report
open htmlcov/index.html
```

## Task Completion Checklist

### Before Committing
```bash
# 1. Format code
ruff format .

# 2. Lint code
ruff check --fix .

# 3. Type check
mypy src/world_anvil_mcp

# 4. Run tests
pytest

# 5. Check coverage
pytest --cov=world_anvil_mcp --cov-report=term
```

### All-in-One Check
```bash
# Run all checks in sequence
ruff format . && ruff check --fix . && mypy src/world_anvil_mcp && pytest --cov=world_anvil_mcp
```

## Project Commands

### Package Management
```bash
# Add dependency
uv pip install package-name

# Add dev dependency
uv pip install --dev package-name

# Update dependencies
uv pip install --upgrade -e ".[dev]"
```

### Git Operations (macOS/Darwin)
```bash
# Standard git commands work on macOS
git status
git add .
git commit -m "message"
git push

# macOS-specific: Use 'open' instead of 'xdg-open'
open file.txt
```

## Debugging

### Check API Status
```bash
# Test API configuration
python -c "from world_anvil_mcp.server import mcp; import asyncio; print(asyncio.run(mcp.tools[0]()))"
```

### View OpenAPI Spec
```bash
# View API specification
cat openapi.yml

# Search for specific endpoint
grep -r "article" openapi.yml
```

## macOS-Specific Commands

### File Operations
```bash
# List files (BSD ls on macOS)
ls -la

# Find files
find . -name "*.py"

# Search in files
grep -r "pattern" src/

# Open files with default app
open README.md
```

### System Info
```bash
# Check Python version
python3 --version

# Check available Python versions
which -a python3

# System info
uname -a
sw_vers
```
