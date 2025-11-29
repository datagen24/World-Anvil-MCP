# World Anvil MCP Server - Development Environment Setup (PowerShell)
# Sets up Python virtual environment, installs dependencies, and configures pre-commit hooks
# Usage: PowerShell -ExecutionPolicy Bypass -File scripts/dev-setup.ps1

param(
    [switch]$NoInteractive = $false
)

# Error handling
$ErrorActionPreference = "Stop"

# Script configuration
$projectRoot = Split-Path -Parent $PSScriptRoot
$venvDir = Join-Path $projectRoot ".venv"
$pythonMinVersion = "3.11"

# Color helper functions
function Write-Header {
    param([string]$Message)
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

function Write-Step {
    param([string]$Message)
    Write-Host "✓" -ForegroundColor Green -NoNewline
    Write-Host " $Message"
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ" -ForegroundColor Yellow -NoNewline
    Write-Host " $Message"
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗" -ForegroundColor Red -NoNewline
    Write-Host " $Message" -ForegroundColor Red
}

function Confirm-Action {
    param([string]$Message)
    if ($NoInteractive) {
        return $true
    }
    $response = Read-Host "$Message (y/n)"
    return $response -eq "y" -or $response -eq "Y"
}

# Check system requirements
function Check-Requirements {
    Write-Header "Checking System Requirements"

    # Check for Python
    try {
        $pythonPath = (Get-Command python3 -ErrorAction Stop).Source
        Write-Step "Python 3 found at: $pythonPath"
    } catch {
        Write-Error-Custom "Python 3 is not installed or not in PATH"
        Write-Host "Please install Python 3.11 or later from https://www.python.org"
        exit 1
    }

    # Check Python version
    try {
        $pythonVersion = & python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))"

        # Version comparison (simple string comparison works for X.YY format)
        if ([version]$pythonVersion -lt [version]$pythonMinVersion) {
            Write-Error-Custom "Python 3.11+ is required, but Python $pythonVersion is installed"
            exit 1
        }
        Write-Step "Python $pythonVersion detected"
    } catch {
        Write-Error-Custom "Could not determine Python version: $_"
        exit 1
    }

    # Check for uv
    try {
        $uvPath = (Get-Command uv -ErrorAction Stop).Source
        Write-Step "uv package manager found at: $uvPath"
    } catch {
        Write-Error-Custom "uv package manager is not installed or not in PATH"
        Write-Host "Install uv from https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    }

    # Check for git (optional but recommended)
    try {
        $gitPath = (Get-Command git -ErrorAction Stop).Source
        Write-Step "git found at: $gitPath"
    } catch {
        Write-Info "git is not installed - you can still use the project, but version control features won't work"
    }
}

# Create virtual environment
function Setup-VirtualEnv {
    Write-Header "Setting Up Virtual Environment"

    if (Test-Path $venvDir) {
        Write-Info "Virtual environment already exists at $venvDir"

        if (-not $NoInteractive) {
            if (Confirm-Action "Do you want to recreate it?") {
                Remove-Item -Path $venvDir -Recurse -Force
                Write-Info "Removed existing virtual environment"
            } else {
                Write-Step "Using existing virtual environment"
                return
            }
        } else {
            Write-Step "Using existing virtual environment (non-interactive mode)"
            return
        }
    }

    try {
        Write-Info "Creating virtual environment at $venvDir..."
        & uv venv $venvDir --python 3.11
        Write-Step "Virtual environment created"
    } catch {
        Write-Error-Custom "Failed to create virtual environment: $_"
        exit 1
    }
}

# Install dependencies
function Install-Dependencies {
    Write-Header "Installing Dependencies"

    try {
        # Determine pip path
        $pipPath = Join-Path $venvDir "Scripts" "pip"

        if (-not (Test-Path $pipPath)) {
            Write-Error-Custom "pip not found at $pipPath"
            exit 1
        }

        Write-Info "Installing development dependencies (this may take a minute)..."
        & $pipPath install -e "$projectRoot[dev,test]" --quiet
        Write-Step "Development dependencies installed"

        Write-Info "Verifying core dependencies..."
        & $pipPath show mcp pydantic httpx tenacity cachetools | Out-Null
        Write-Host "  - Core dependencies: ✓" -ForegroundColor Green

        Write-Info "Verifying dev tools..."
        & $pipPath show ruff mypy | Out-Null
        Write-Host "  - Dev tools: ✓" -ForegroundColor Green

        Write-Info "Verifying test dependencies..."
        & $pipPath show pytest respx | Out-Null
        Write-Host "  - Test dependencies: ✓" -ForegroundColor Green

        Write-Step "All dependencies verified"
    } catch {
        Write-Error-Custom "Failed to install dependencies: $_"
        exit 1
    }
}

# Setup pre-commit hooks
function Setup-PreCommit {
    Write-Header "Installing Pre-commit Hooks"

    try {
        $preCommitPath = Join-Path $venvDir "Scripts" "pre-commit"

        if (-not (Test-Path $preCommitPath)) {
            Write-Error-Custom "pre-commit not found at $preCommitPath"
            exit 1
        }

        Write-Info "Installing pre-commit hooks..."
        & $preCommitPath install
        Write-Step "Pre-commit hooks installed"

        Write-Info "Installing commit-msg hooks..."
        & $preCommitPath install --hook-type commit-msg
        Write-Step "Commit-msg hooks installed"
    } catch {
        Write-Error-Custom "Failed to install pre-commit hooks: $_"
        exit 1
    }
}

# Check configuration
function Check-Configuration {
    Write-Header "Configuration Check"

    $envPath = Join-Path $projectRoot ".env"
    $envExamplePath = Join-Path $projectRoot ".env.example"

    if (Test-Path $envPath) {
        Write-Step ".env file found"
    } else {
        Write-Info ".env file not found"
        if (Test-Path $envExamplePath) {
            Write-Host ""
            Write-Host "To use the World Anvil API, you need to:"
            Write-Host "  1. Copy .env.example to .env"
            Write-Host "  2. Add your World Anvil API credentials"
            Write-Host ""
            Write-Host "Get your credentials from: https://www.worldanvil.com/api-keys"
        }
    }
}

# Print final summary
function Print-Summary {
    Write-Header "Setup Complete! 🎉"
    Write-Host ""
    Write-Host "Your development environment is ready. Next steps:"
    Write-Host ""

    Write-Host "  1. Activate the virtual environment:"
    Write-Host "     " -NoNewline
    Write-Host ".venv\Scripts\Activate.ps1" -ForegroundColor Green
    Write-Host ""

    Write-Host "  2. (Optional) Configure World Anvil API credentials:"
    Write-Host "     " -NoNewline
    Write-Host "Copy-Item .env.example .env" -ForegroundColor Green
    Write-Host "     Then edit .env and add your credentials from https://www.worldanvil.com/api-keys"
    Write-Host ""

    Write-Host "  3. Verify your setup with quality checks:"
    Write-Host "     " -NoNewline
    Write-Host "make quality" -ForegroundColor Green
    Write-Host ""

    Write-Host "  4. Run unit tests to confirm everything works:"
    Write-Host "     " -NoNewline
    Write-Host "make test-unit" -ForegroundColor Green
    Write-Host ""

    Write-Host "Useful development commands:"
    Write-Host "  " -NoNewline
    Write-Host "make help" -ForegroundColor Green
    Write-Host "              Show all available make targets"
    Write-Host "  " -NoNewline
    Write-Host "make quality" -ForegroundColor Green
    Write-Host "          Run all code quality checks (ruff + mypy)"
    Write-Host "  " -NoNewline
    Write-Host "make test" -ForegroundColor Green
    Write-Host "             Run all tests"
    Write-Host "  " -NoNewline
    Write-Host "make test-unit" -ForegroundColor Green
    Write-Host "        Run fast unit tests only"
    Write-Host "  " -NoNewline
    Write-Host "make test-cov" -ForegroundColor Green
    Write-Host "         Run tests with coverage report"
    Write-Host "  " -NoNewline
    Write-Host "make run" -ForegroundColor Green
    Write-Host "              Run the MCP server"
    Write-Host "  " -NoNewline
    Write-Host "make docs" -ForegroundColor Green
    Write-Host "             Build documentation"
    Write-Host ""
}

# Main execution
function Main {
    Write-Header "World Anvil MCP Server - Development Environment Setup"
    Write-Host ""
    Write-Host "This script will:"
    Write-Host "  • Check system requirements (Python 3.11+, uv)"
    Write-Host "  • Create a Python virtual environment at .venv\"
    Write-Host "  • Install all development and test dependencies"
    Write-Host "  • Configure pre-commit hooks"
    Write-Host ""

    try {
        Check-Requirements
        Setup-VirtualEnv
        Install-Dependencies
        Setup-PreCommit
        Check-Configuration
        Print-Summary
    } catch {
        Write-Error-Custom "Setup failed: $_"
        exit 1
    }
}

# Run main function
Main
