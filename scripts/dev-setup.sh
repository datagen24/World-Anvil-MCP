#!/bin/bash
# World Anvil MCP Server - Development Environment Setup
# Sets up Python virtual environment, installs dependencies, and configures pre-commit hooks
# Usage: bash scripts/dev-setup.sh

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Script variables
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"
PYTHON_MIN_VERSION="3.11"

# Helper functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_step() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${YELLOW}ℹ${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check for required tools
check_requirements() {
    print_header "Checking System Requirements"

    # Check for Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        echo "Please install Python 3.11 or later from https://www.python.org"
        exit 1
    fi

    # Check Python version
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [ "$(printf '%s\n' "$PYTHON_MIN_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$PYTHON_MIN_VERSION" ]; then
        print_error "Python 3.11+ is required, but Python $PYTHON_VERSION is installed"
        exit 1
    fi
    print_step "Python $PYTHON_VERSION detected"

    # Check for uv
    if ! command -v uv &> /dev/null; then
        print_error "uv package manager is not installed"
        echo "Install uv from https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
    print_step "uv package manager found"

    # Check for git (optional but recommended)
    if ! command -v git &> /dev/null; then
        print_info "git is not installed - you can still use the project, but version control features won't work"
    else
        print_step "git found"
    fi
}

# Create virtual environment
setup_venv() {
    print_header "Setting Up Virtual Environment"

    if [ -d "$VENV_DIR" ]; then
        print_info "Virtual environment already exists at $VENV_DIR"
        read -p "Do you want to recreate it? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
            print_info "Removed existing virtual environment"
        else
            print_step "Using existing virtual environment"
            return
        fi
    fi

    print_info "Creating virtual environment at $VENV_DIR..."
    uv venv "$VENV_DIR" --python 3.11
    print_step "Virtual environment created"
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"

    print_info "Activating virtual environment..."
    source "${VENV_DIR}/bin/activate"
    print_step "Virtual environment activated"

    print_info "Installing development dependencies (this may take a minute)..."
    pip install -e "${PROJECT_ROOT}[dev,test]" --quiet
    print_step "Development dependencies installed"

    print_info "Verifying installations..."
    python -c "import mcp, pydantic, httpx, tenacity, cachetools; print('  - Core dependencies: ✓')"
    python -c "import ruff, mypy; print('  - Dev tools: ✓')"
    python -c "import pytest, respx; print('  - Test dependencies: ✓')"
    print_step "All dependencies verified"
}

# Setup pre-commit hooks
setup_precommit() {
    print_header "Installing Pre-commit Hooks"

    source "${VENV_DIR}/bin/activate"

    print_info "Installing pre-commit hooks..."
    pre-commit install
    print_step "Pre-commit hooks installed"

    print_info "Installing commit-msg hooks..."
    pre-commit install --hook-type commit-msg
    print_step "Commit-msg hooks installed"
}

# Configuration check
check_configuration() {
    print_header "Configuration Check"

    if [ -f "${PROJECT_ROOT}/.env" ]; then
        print_step ".env file found"
    else
        if [ -f "${PROJECT_ROOT}/.env.example" ]; then
            print_info ".env file not found"
            echo "To use the World Anvil API, you need to:"
            echo "  1. Copy .env.example to .env"
            echo "  2. Add your World Anvil API credentials"
            echo ""
            echo "Get your credentials from: https://www.worldanvil.com/api-keys"
        else
            print_info "No .env configuration found"
        fi
    fi
}

# Final summary
print_summary() {
    print_header "Setup Complete! 🎉"

    echo ""
    echo "Your development environment is ready. Next steps:"
    echo ""
    echo "  1. Activate the virtual environment:"
    echo "     ${GREEN}source .venv/bin/activate${NC}"
    echo ""
    echo "  2. (Optional) Configure World Anvil API credentials:"
    echo "     ${GREEN}cp .env.example .env${NC}"
    echo "     Then edit .env and add your credentials from https://www.worldanvil.com/api-keys"
    echo ""
    echo "  3. Verify your setup with quality checks:"
    echo "     ${GREEN}make quality${NC}"
    echo ""
    echo "  4. Run unit tests to confirm everything works:"
    echo "     ${GREEN}make test-unit${NC}"
    echo ""
    echo "Useful development commands:"
    echo "  ${GREEN}make help${NC}              Show all available make targets"
    echo "  ${GREEN}make quality${NC}          Run all code quality checks (ruff + mypy)"
    echo "  ${GREEN}make test${NC}             Run all tests"
    echo "  ${GREEN}make test-unit${NC}        Run fast unit tests only"
    echo "  ${GREEN}make test-cov${NC}         Run tests with coverage report"
    echo "  ${GREEN}make run${NC}              Run the MCP server"
    echo "  ${GREEN}make docs${NC}             Build documentation"
    echo ""
}

# Main execution
main() {
    print_header "World Anvil MCP Server - Development Environment Setup"
    echo ""
    echo "This script will:"
    echo "  • Check system requirements (Python 3.11+, uv)"
    echo "  • Create a Python virtual environment at .venv/"
    echo "  • Install all development and test dependencies"
    echo "  • Configure pre-commit hooks"
    echo ""

    check_requirements
    setup_venv
    install_dependencies
    setup_precommit
    check_configuration
    print_summary
}

# Run main function
main
