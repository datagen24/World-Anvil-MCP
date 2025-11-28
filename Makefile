# Makefile for World Anvil MCP Server development automation
.PHONY: help install install-dev install-test install-pre-commit \
        format lint typecheck test test-unit test-integration test-e2e \
        test-cov quality clean clean-pyc clean-test clean-build \
        docs docs-serve pre-commit run

# Default target
.DEFAULT_GOAL := help

##@ General

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Installation

install: ## Install package in production mode
	pip install -e .

install-dev: ## Install package with dev dependencies
	pip install -e ".[dev]"

install-test: ## Install package with test dependencies
	pip install -e ".[test]"

install-pre-commit: install-dev ## Install and setup pre-commit hooks
	pre-commit install
	pre-commit install --hook-type commit-msg

##@ Code Quality

format: ## Format code with ruff
	ruff format .
	@echo "✓ Code formatted"

lint: ## Lint code with ruff (auto-fix where possible)
	ruff check --fix .
	@echo "✓ Linting complete"

typecheck: ## Type check with mypy
	mypy src/
	@echo "✓ Type checking complete"

quality: format lint typecheck ## Run all code quality checks
	@echo "✓ All quality checks passed"

##@ Testing

test: ## Run all tests
	pytest

test-unit: ## Run unit tests only (fast)
	pytest -m unit -v

test-integration: ## Run integration tests (mocked API)
	pytest -m integration -v

test-e2e: ## Run end-to-end tests (requires live API credentials)
	pytest -m e2e -v

test-cov: ## Run tests with coverage report
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "✓ Coverage report generated in htmlcov/"

test-cov-fail: ## Run tests with coverage, fail if below 85%
	pytest --cov=src --cov-report=term-missing --cov-fail-under=85

##@ Pre-commit

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

##@ Running

run: ## Run the MCP server
	world-anvil-mcp

run-dev: ## Run the MCP server with development logging
	LOGLEVEL=DEBUG world-anvil-mcp

##@ Documentation

install-docs: ## Install documentation dependencies
	pip install -e ".[docs]"

docs-sync: ## Sync markdown files to RST for Sphinx
	python scripts/md_to_rst.py

docs: docs-sync ## Build Sphinx documentation for Read the Docs
	sphinx-build -b html docs/source docs/build/html
	@echo "✓ Documentation built in docs/build/html/"

docs-serve: docs-sync ## Serve documentation locally with live reload
	sphinx-autobuild docs/source docs/build/html --open-browser

docs-clean: ## Clean documentation build artifacts
	rm -rf docs/build/
	rm -rf docs/source/workflows/*.rst
	rm -rf docs/source/development/quality/
	rm -rf docs/source/research/
	rm -rf docs/source/specs/
	@echo "✓ Documentation build and generated RST files cleaned"

docs-linkcheck: docs-sync ## Check for broken links in documentation
	sphinx-build -b linkcheck docs/source docs/build/linkcheck
	@echo "✓ Link check complete"

##@ Cleanup

clean: clean-pyc clean-test clean-build ## Remove all build, test, and cache files

clean-pyc: ## Remove Python cache files
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '*.egg-info' -exec rm -rf {} +

clean-test: ## Remove test and coverage artifacts
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	rm -f coverage.xml

clean-build: ## Remove build artifacts
	rm -rf build/
	rm -rf dist/

##@ Development Workflow

dev-setup: install-dev install-test install-pre-commit ## Complete development setup
	@echo "✓ Development environment ready"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Copy .env.example to .env and add your World Anvil credentials"
	@echo "  2. Run 'make test-unit' to verify setup"
	@echo "  3. Run 'make quality' before committing changes"

dev-check: quality test-unit ## Quick development check (quality + unit tests)
	@echo "✓ Development checks passed - ready to commit"

ci: quality test-cov-fail ## Run CI checks locally (quality + tests with coverage)
	@echo "✓ CI checks passed"
