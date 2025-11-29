#!/bin/bash
# Live API Test Execution Wrapper
#
# This script runs the World Anvil live API tests with proper environment setup.
#
# Prerequisites:
#   1. World Anvil credentials set in .env:
#      - WORLD_ANVIL_APP_KEY
#      - WORLD_ANVIL_USER_TOKEN
#   2. Test world ID (will prompt if not set)
#
# Usage:
#   ./scripts/run_live_tests.sh [world-id]

set -e  # Exit on error

# Load environment variables from .env
if [ -f .env ]; then
    echo "📝 Loading credentials from .env..."
    export $(grep -v '^#' .env | xargs)
else
    echo "⚠️  Warning: .env file not found"
fi

# Check credentials
if [ -z "$WORLD_ANVIL_APP_KEY" ] || [ -z "$WORLD_ANVIL_USER_TOKEN" ]; then
    echo "❌ Error: Missing World Anvil credentials"
    echo ""
    echo "Please set in .env:"
    echo "  WORLD_ANVIL_APP_KEY=your-app-key"
    echo "  WORLD_ANVIL_USER_TOKEN=your-user-token"
    exit 1
fi

# Get test world ID
if [ -z "$1" ]; then
    if [ -z "$TEST_WORLD_ID" ]; then
        echo "❌ Error: Test world ID required"
        echo ""
        echo "Usage:"
        echo "  ./scripts/run_live_tests.sh <world-id>"
        echo ""
        echo "Or set TEST_WORLD_ID in .env:"
        echo "  TEST_WORLD_ID=your-test-world-id"
        exit 1
    fi
    WORLD_ID="$TEST_WORLD_ID"
else
    WORLD_ID="$1"
fi

export TEST_WORLD_ID="$WORLD_ID"

echo "🚀 Starting Live API Tests"
echo "=========================="
echo "World ID: $WORLD_ID"
echo ""

# Activate venv and run tests
if [ ! -d .venv ]; then
    echo "❌ Error: Virtual environment not found at .venv"
    echo "Run: uv venv --python 3.11 .venv"
    exit 1
fi

source .venv/bin/activate

# Run the test script
echo "Running tests..."
python scripts/test_live_api.py

echo ""
echo "✅ Test execution complete"
