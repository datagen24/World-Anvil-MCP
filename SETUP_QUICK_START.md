# Quick Start: Development Setup

## 60-Second Setup

### macOS/Linux
```bash
bash scripts/dev-setup.sh
source .venv/bin/activate
make quality
```

### Windows PowerShell
```powershell
PowerShell -ExecutionPolicy Bypass -File scripts/dev-setup.ps1
.venv\Scripts\Activate.ps1
make quality
```

## What You Need First

- Python 3.11+ → https://www.python.org
- uv package manager → https://docs.astral.sh/uv/
- Git (optional) → https://git-scm.com

## After Setup

```bash
# Verify everything works
make test-unit

# See all commands
make help

# Configure API credentials (optional)
cp .env.example .env
# Edit .env and add your World Anvil API keys from https://www.worldanvil.com/api-keys
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `python3: command not found` | Install Python 3.11+ from https://www.python.org |
| `uv: command not found` | Install uv from https://docs.astral.sh/uv/getting-started/installation/ |
| `Permission denied` | Run `chmod +x scripts/dev-setup.sh` |
| IDE can't find modules | Select `.venv/bin/python` as interpreter in IDE |
| Pre-commit blocks commits | Run `make quality` to fix issues |

## Full Setup Guide

See [docs/SETUP.md](docs/SETUP.md) for comprehensive setup instructions and troubleshooting.
