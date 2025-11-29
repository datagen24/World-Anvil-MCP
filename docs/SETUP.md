# Development Environment Setup

This guide walks you through setting up the World Anvil MCP Server development environment. We provide automated setup scripts for both Linux/macOS and Windows.

## Prerequisites

Before running the setup scripts, ensure you have:

- **Python 3.11 or later** - Download from https://www.python.org
- **uv package manager** - Install from https://docs.astral.sh/uv/getting-started/installation/
- **Git** (recommended, optional) - Download from https://git-scm.com

## Quick Setup

### Linux/macOS

```bash
# Make the script executable (if not already)
chmod +x scripts/dev-setup.sh

# Run the setup script
bash scripts/dev-setup.sh
```

### Windows (PowerShell)

```powershell
# Run the setup script
PowerShell -ExecutionPolicy Bypass -File scripts/dev-setup.ps1
```

For automated setup without prompts:

```powershell
PowerShell -ExecutionPolicy Bypass -File scripts/dev-setup.ps1 -NoInteractive
```

## What the Setup Scripts Do

Both `dev-setup.sh` (Linux/macOS) and `dev-setup.ps1` (Windows) automate these tasks:

1. **Verify System Requirements**
   - Checks Python 3.11+ is installed
   - Confirms uv is available
   - Validates git is installed (optional)

2. **Create Virtual Environment**
   - Creates `.venv/` directory at project root
   - Initializes Python virtual environment using uv
   - Offers to recreate if already exists

3. **Install Dependencies**
   - Installs core dependencies (mcp, pydantic, httpx, etc.)
   - Installs dev tools (ruff, mypy)
   - Installs test dependencies (pytest, respx, faker, etc.)
   - Verifies all installations

4. **Configure Pre-commit Hooks**
   - Installs pre-commit hooks for quality checks
   - Sets up commit-msg hooks
   - Ensures code quality on every commit

5. **Environment Validation**
   - Checks for `.env` configuration file
   - Provides instructions for World Anvil API credentials

## Manual Setup (If Scripts Don't Work)

If you prefer manual setup or the scripts don't work on your system:

### 1. Create Virtual Environment

```bash
# Linux/macOS
uv venv .venv --python 3.11
source .venv/bin/activate

# Windows PowerShell
uv venv .venv --python 3.11
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
# With dev and test dependencies
pip install -e ".[dev,test]"

# Or just dev
pip install -e ".[dev]"

# Or production only
pip install -e .
```

### 3. Install Pre-commit Hooks

```bash
pre-commit install
pre-commit install --hook-type commit-msg
```

### 4. Verify Installation

```bash
# Test imports
python -c "import mcp, pydantic, httpx; print('Core dependencies OK')"

# Run quality checks
make quality

# Run tests
make test-unit
```

## Environment Configuration

### World Anvil API Credentials

To interact with the World Anvil API, you need credentials:

1. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```

2. Add your World Anvil credentials:
   - Get API keys from https://www.worldanvil.com/api-keys
   - Edit `.env` and add:
     ```
     WORLD_ANVIL_APP_KEY=your_application_key
     WORLD_ANVIL_USER_TOKEN=your_user_token
     ```

3. Never commit `.env` (it's in `.gitignore`)

## Verify Setup

After setup completes, verify everything works:

```bash
# Activate virtual environment (if not already activated)
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Run quality checks
make quality

# Run fast unit tests
make test-unit

# View all available commands
make help
```

## Common Commands

Once your environment is set up, here are frequently used commands:

### Development

```bash
make quality          # Run all quality checks (format, lint, typecheck)
make format           # Format code with ruff
make lint             # Lint code and auto-fix issues
make typecheck        # Type check with mypy
```

### Testing

```bash
make test             # Run all tests
make test-unit        # Run unit tests only (fast, <1 minute)
make test-integration # Run integration tests (mocked API)
make test-cov         # Run tests with coverage report
```

### Running the Server

```bash
make run              # Run the MCP server
make run-dev          # Run with debug logging
```

### Documentation

```bash
make docs             # Build Sphinx documentation
make docs-serve       # Build and serve docs with live reload
```

### Project Maintenance

```bash
make clean            # Remove all build and cache files
make help             # Show all available commands
```

## Troubleshooting

### Python Not Found

**Error**: `python3: command not found`

**Solution**:
- Install Python 3.11+ from https://www.python.org
- Make sure Python is in your system PATH
- Try `python --version` if `python3` doesn't work

### uv Not Found

**Error**: `uv: command not found`

**Solution**:
- Install uv from https://docs.astral.sh/uv/getting-started/installation/
- On macOS: `brew install uv`
- On Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Permission Denied (Linux/macOS)

**Error**: `Permission denied: scripts/dev-setup.sh`

**Solution**:
```bash
chmod +x scripts/dev-setup.sh
bash scripts/dev-setup.sh
```

### Virtual Environment Already Exists

**Error**: Setup script asks if you want to recreate venv

**Options**:
- Press `y` to recreate (deletes old one)
- Press `n` to use existing venv
- For non-interactive: `scripts/dev-setup.ps1 -NoInteractive` (PowerShell)

### Pre-commit Hooks Fail

**Error**: Commits are blocked by pre-commit hooks

**Solution**: This is expected behavior - hooks ensure code quality:
```bash
# Fix issues
make quality

# Manually run hooks
make pre-commit

# Commit once hooks pass
git commit -m "message"
```

### Import Errors in IDE

**Error**: IDE can't find imports, "module not found"

**Solution**:
- Ensure virtual environment is activated
- Select `.venv/bin/python` (Linux/macOS) or `.venv\Scripts\python.exe` (Windows) as interpreter
- In VS Code: Open command palette → "Python: Select Interpreter" → choose `.venv`
- Restart IDE

## Environment Details

### Virtual Environment Location

```
project_root/
└── .venv/               # Virtual environment (created by setup scripts)
    ├── bin/             # Executable scripts (Linux/macOS)
    │   ├── python
        │   ├── pip
    │   └── ...
    ├── Scripts/         # Executable scripts (Windows)
    │   ├── python.exe
    │   ├── pip.exe
    │   └── ...
    └── lib/             # Installed packages
        └── python3.11/
            └── site-packages/
```

### Installed Tool Locations

After setup, tools are available:

```bash
# Linux/macOS
.venv/bin/ruff          # Code formatter/linter
.venv/bin/mypy          # Type checker
.venv/bin/pytest        # Test runner
.venv/bin/pre-commit    # Git hooks manager

# Windows PowerShell
.venv\Scripts\ruff.exe
.venv\Scripts\mypy.exe
.venv\Scripts\pytest.exe
.venv\Scripts\pre-commit.exe
```

Or via `make` targets (recommended):

```bash
make format
make typecheck
make test
make pre-commit
```

## Next Steps

After setup:

1. **Read the Architecture**: See `docs/specs/client-architecture.md`
2. **Review Specifications**: See `docs/specs/tool-specifications.md`
3. **Check Quality Standards**: See `docs/quality/api-client-patterns.md`
4. **Explore Workflows**: See `docs/workflows/` for example D&D use cases
5. **Start Contributing**: Create a feature branch and begin development

## Getting Help

- **Installation Issues**: Check Prerequisites section above
- **Tool Questions**: Run `make help` for available commands
- **Development Guide**: See `CLAUDE.md` in project root
- **Architecture**: See `docs/specs/client-architecture.md`
- **Workflow Examples**: See `docs/workflows/` directory

## See Also

- [CLAUDE.md](../CLAUDE.md) - Project development guide
- [Makefile](../Makefile) - Development targets
- [pyproject.toml](../pyproject.toml) - Project configuration
- [.pre-commit-config.yaml](../.pre-commit-config.yaml) - Pre-commit configuration
