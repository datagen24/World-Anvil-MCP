# GitHub Actions Workflow Reference

**File Location**: `.github/workflows/ci.yml`
**Status**: Production Ready
**Created**: 2025-11-29

---

## Complete Workflow Content

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

permissions:
  contents: read
  checks: write
  pull-requests: write

jobs:
  test:
    name: Test & Quality Gates
    runs-on: ubuntu-latest
    timeout-minutes: 30

    strategy:
      matrix:
        python-version: ['3.11']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies (dev + test)
        run: uv pip install -e ".[dev,test]" --system

      - name: Format check
        run: ruff format --check .

      - name: Lint check
        run: ruff check .

      - name: Type check (mypy strict)
        run: mypy src/world_anvil_mcp

      - name: Run tests with coverage
        run: |
          pytest \
            --cov=src/world_anvil_mcp \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=85 \
            --junit-xml=test-results.xml \
            -v

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}

      - name: Comment PR with coverage
        if: github.event_name == 'pull_request'
        uses: py-cov-action/python-coverage-comment-action@v3
        with:
          GITHUB_TOKEN: ${{ github.token }}
          MINIMUM_GREEN: 85
          MINIMUM_ORANGE: 70
```

---

## Workflow Line-by-Line Explanation

### Metadata Section
```yaml
name: CI
```
**Purpose**: Display name in GitHub Actions UI
**Visible in**: Repository → Actions tab, PR status checks

### Event Triggers
```yaml
on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
```
**What**: Triggers workflow when:
- Code is pushed to main branch
- Pull request is created/updated targeting main

**Why**: Catches issues immediately before merge

### Permissions (Least Privilege)
```yaml
permissions:
  contents: read      # Can read repository code
  checks: write       # Can write check results to PR
  pull-requests: write # Can comment on pull requests
```
**Security**: Minimal permissions needed only

### Job Configuration
```yaml
jobs:
  test:                           # Job ID
    name: Test & Quality Gates    # Display name
    runs-on: ubuntu-latest        # GitHub-hosted runner
    timeout-minutes: 30           # Safety limit
```
**What**: Single job with 7 sequential quality gates

### Python Version Matrix
```yaml
    strategy:
      matrix:
        python-version: ['3.11']
```
**What**: Can test multiple Python versions (currently just 3.11)
**Extensible**: Add '3.12', '3.13' to test multiple versions

### Step 1: Checkout Code
```yaml
      - name: Checkout code
        uses: actions/checkout@v4
```
**What**: Download repository code
**Why**: Needed before running any checks
**Version**: v4 (latest)

### Step 2: Setup Python
```yaml
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
```
**What**: Install Python 3.11 and enable pip caching
**Cache**: Stores pip packages from previous runs
**Benefit**: Reduces install time by ~60%
**Version**: v5 (latest)

### Step 3: Install uv
```yaml
      - name: Install uv
        run: pip install uv
```
**What**: Install uv package manager
**Why**: Faster than pip, better dependency resolution
**Time**: ~5 seconds

### Step 4: Install Dependencies
```yaml
      - name: Install dependencies (dev + test)
        run: uv pip install -e ".[dev,test]" --system
```
**What**: Install package in editable mode with extras
**Extras**:
- `dev`: ruff, mypy, pre-commit
- `test`: pytest, pytest-cov, respx, faker
**System**: Use system Python (not venv)
**Time**: 20-30 seconds (first run), 5 seconds (cached)

### Step 5: Format Check
```yaml
      - name: Format check
        run: ruff format --check .
```
**What**: Check code formatting (no auto-fix)
**Config**: `pyproject.toml` [tool.ruff.format]
- Line length: 100 characters
- Quote style: Double quotes
**Failure**: Returns exit code 1
**Auto-fix**: Run `ruff format .` locally
**Time**: ~5 seconds

### Step 6: Lint Check
```yaml
      - name: Lint check
        run: ruff check .
```
**What**: Lint code quality (with auto-fix available)
**Config**: `pyproject.toml` [tool.ruff.lint]
**Rules**: 25+ categories (security, naming, imports, etc.)
**Failure**: Returns exit code 1
**Auto-fix**: Run `ruff check . --fix` locally
**Time**: ~10 seconds

### Step 7: Type Check
```yaml
      - name: Type check (mypy strict)
        run: mypy src/world_anvil_mcp
```
**What**: Strict type checking
**Config**: `pyproject.toml` [tool.mypy]
**Settings**:
- `strict = true`: All functions must be typed
- `disallow_untyped_defs = true`: No implicit types
- `strict_equality = true`: Strict equality checks
**Coverage**: 100% of public APIs
**Failure**: Returns exit code 1
**Time**: ~15 seconds

### Step 8: Test Execution
```yaml
      - name: Run tests with coverage
        run: |
          pytest \
            --cov=src/world_anvil_mcp \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=85 \
            --junit-xml=test-results.xml \
            -v
```
**What**: Run all tests and measure coverage
**Options**:
- `--cov=src/world_anvil_mcp`: Measure this directory
- `--cov-report=xml`: Generate XML for Codecov
- `--cov-report=term-missing`: Show missing lines in terminal
- `--cov-fail-under=85`: Fail if <85% coverage
- `--junit-xml=test-results.xml`: Generate test results
- `-v`: Verbose output
**Failure**: Returns exit code 1 if:
- Any test fails
- Coverage below 85%
**Time**: 30-60 seconds (depends on test suite)

### Step 9: Upload Test Results
```yaml
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results.xml
```
**What**: Save test results as artifact
**When**: `if: always()` - Even if previous steps failed
**Format**: JUnit XML (compatible with CI tools)
**Retention**: 90 days (GitHub default)
**Access**: Actions tab → Run → Artifacts → test-results
**Why**: For analysis and debugging after run

### Step 10: Upload Coverage to Codecov
```yaml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: true
          token: ${{ secrets.CODECOV_TOKEN }}
```
**What**: Upload coverage report to codecov.io
**Setup Required**: Add CODECOV_TOKEN secret to repository
**Steps to Setup**:
1. Go to codecov.io
2. Connect GitHub
3. Copy repo token
4. Go to: Repository → Settings → Secrets → New repository secret
5. Create `CODECOV_TOKEN` with token value
**Options**:
- `file`: Coverage XML from pytest
- `flags`: Tag for organizing reports
- `name`: Report name in dashboard
- `fail_ci_if_error: true`: Fail if upload fails
- `token`: Repository secret
**Dashboard**: View trends at codecov.io/repositories
**Why**: Track coverage over time, prevent regressions

### Step 11: Comment PR with Coverage
```yaml
      - name: Comment PR with coverage
        if: github.event_name == 'pull_request'
        uses: py-cov-action/python-coverage-comment-action@v3
        with:
          GITHUB_TOKEN: ${{ github.token }}
          MINIMUM_GREEN: 85
          MINIMUM_ORANGE: 70
```
**What**: Post coverage summary as PR comment
**When**: `if: github.event_name == 'pull_request'` - Only on PRs
**Coverage Thresholds**:
- Green: ≥85% (target)
- Orange: 70-85% (warning)
- Red: <70% (alert)
**Information Shown**:
- Overall coverage %
- Changes in coverage vs base branch
- Missing lines
- File-by-file breakdown
**Automatic**: Appears within 1-2 minutes of push
**Why**: Quick feedback without checking Codecov separately

---

## Action Versions

| Action | Version | Status | Next Major |
|--------|---------|--------|-----------|
| checkout | v4 | Current | v5 (future) |
| setup-python | v5 | Current | v6 (future) |
| codecov-action | v4 | Current | v5 (future) |
| py-cov-action | v3 | Current | v4 (future) |
| upload-artifact | v4 | Current | v5 (future) |

**Update Policy**: Update within 30 days of major release

---

## Customization Examples

### Add Python 3.12 Testing
```yaml
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
```
Runs complete pipeline on both Python versions

### Make Coverage Optional (Not Recommended)
```yaml
- name: Upload coverage to Codecov
  # Remove: fail_ci_if_error: true
  # This allows pipeline to pass even if Codecov is down
```

### Skip E2E Tests in CI
```yaml
- name: Run tests with coverage
  run: |
    pytest \
      --cov=src/world_anvil_mcp \
      -m "not e2e" \  # Add this line
      ...
```

### Increase Test Timeout
```yaml
      - name: Run tests with coverage
        timeout-minutes: 60  # Change from 30
        run: |
          pytest ...
```

### Parallel Test Execution
```bash
# Add pytest-xdist to dev dependencies first
# Then modify workflow:
run: pytest -n auto --cov=src/world_anvil_mcp ...
```

---

## Troubleshooting

### Workflow Won't Run
**Issue**: No Actions tab visible
**Solution**: Ensure `.github/workflows/` directory exists with .yml file

### All Tests Pass Locally but Fail in CI
**Likely causes**:
- Python version mismatch (ensure 3.11)
- Missing environment variables
- Platform-specific code (Windows vs Unix)
- Import errors from dependencies

**Solution**:
```bash
# Test locally with same Python version
python --version  # Should be 3.11.x

# Install exact same dependencies
uv pip install -e ".[dev,test]"

# Run same commands as CI
pytest --cov=src/world_anvil_mcp --cov-fail-under=85
```

### Codecov Token Invalid
**Issue**: Codecov upload fails
**Solution**:
1. Go to codecov.io/repositories
2. Regenerate token
3. Update CODECOV_TOKEN secret in GitHub

### Coverage Threshold Not Enforced
**Issue**: Tests pass with 80% coverage
**Check**:
1. Verify `--cov-fail-under=85` in workflow
2. Check pytest.ini for conflicting settings
3. Ensure pyproject.toml has `coverage.run` section

---

## References

- **Official Docs**: https://docs.github.com/en/actions
- **Checkout Action**: https://github.com/actions/checkout
- **Setup Python**: https://github.com/actions/setup-python
- **Codecov Action**: https://github.com/codecov/codecov-action
- **Artifacts**: https://github.com/actions/upload-artifact

---

**Last Updated**: 2025-11-29
**Status**: Production Ready
