# World Anvil MCP Scripts

Utility scripts for development, testing, and maintenance.

## Live API Testing

### Prerequisites

1. **World Anvil Credentials**
   ```bash
   # Add to .env file:
   WORLD_ANVIL_APP_KEY=your-application-key
   WORLD_ANVIL_USER_TOKEN=your-user-token
   TEST_WORLD_ID=your-test-world-id  # Optional, can pass as argument
   ```

2. **Test World**
   - Use a dedicated test world for API validation
   - **⚠️ WARNING**: Tests will create and delete articles in this world
   - Do NOT use a production world with real content

3. **Environment Setup**
   ```bash
   # Ensure venv exists and dependencies installed
   uv venv --python 3.11 .venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

### Running Live API Tests

**Option 1: Using wrapper script (recommended)**
```bash
# With TEST_WORLD_ID in .env
./scripts/run_live_tests.sh

# Or pass world ID as argument
./scripts/run_live_tests.sh <your-world-id>
```

**Option 2: Direct Python execution**
```bash
export TEST_WORLD_ID=your-world-id
source .venv/bin/activate
python scripts/test_live_api.py
```

### Test Suite Coverage

The live API tests validate:

1. **World Read Access**
   - Verifies test world is accessible
   - Validates credentials work

2. **Article Creation (PUT)**
   - Creates test article with prefix "MCP-TEST-"
   - Validates response includes article ID
   - Tests success=false quirk handling

3. **Article Update (PATCH)**
   - Updates test article content
   - Validates cache invalidation

4. **Article Read Verification**
   - Reads article after creation/update
   - Confirms updates are reflected

5. **Article Deletion (DELETE)**
   - Deletes test article
   - Verifies 404 on subsequent read

6. **Error Handling**
   - Tests 404 handling (invalid article ID)
   - Validates exception types

### Test Artifacts

Test articles are:
- Named with clear prefix: `MCP-TEST-Article-{timestamp}`
- Created in draft state (not published)
- Automatically cleaned up after tests
- Deleted even if tests fail (cleanup in finally block)

### Expected Output

```
============================================================
World Anvil Live API Test Suite
============================================================
World ID: abc123
Timestamp: 2025-11-29T16:30:00
============================================================

📖 Test 1: World Read Access
------------------------------------------------------------
✅ World accessible: My Test World
   ID: abc123
   Articles: 0

➕ Test 2: Article Creation (PUT)
------------------------------------------------------------
✅ Article created successfully
   ID: xyz789
   Title: MCP-TEST-Article-20251129-163000

✏️  Test 3: Article Update (PATCH)
------------------------------------------------------------
✅ Article updated successfully
   ID: xyz789
   Updated content: Updated content at 2025-11-29T16:30:05

📖 Test 4: Article Read Verification
------------------------------------------------------------
✅ Article readable after update
   Title: MCP-TEST-Article-20251129-163000
   State: draft

🗑️  Test 5: Article Deletion (DELETE)
------------------------------------------------------------
✅ Article deleted successfully
   ID: xyz789
✅ Verified: Article returns 404 after deletion

🚨 Test 6: Error Handling
------------------------------------------------------------
✅ 404 handling: Correctly raises NotFoundError

🧹 Cleanup
------------------------------------------------------------
✅ No cleanup needed

============================================================
Test Summary
============================================================
Total Tests: 6
✅ Passed: 6
❌ Failed: 0
⚠️  Skipped: 0

✅ world_read: PASS
✅ article_create: PASS
✅ article_update: PASS
✅ article_read: PASS
✅ article_delete: PASS
✅ error_handling: PASS
============================================================
```

### Troubleshooting

**"Missing credentials" error**
- Verify .env file exists and contains WORLD_ANVIL_APP_KEY and WORLD_ANVIL_USER_TOKEN
- Check credentials are valid at https://www.worldanvil.com/api-keys

**"World not accessible" error**
- Verify TEST_WORLD_ID is correct
- Ensure user has access to the specified world
- Check world exists and is not deleted

**"Article creation failed" error**
- May indicate API endpoint changes
- Check World Anvil API documentation for current article creation endpoint
- Verify world allows article creation

**Tests hang or timeout**
- Check network connectivity to www.worldanvil.com
- Verify no rate limiting (60 requests/minute limit)
- Check for API service disruptions

### Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed or error occurred

### Safety Features

1. **Clear naming**: All test articles prefixed with "MCP-TEST-"
2. **Draft state**: Articles created as drafts (not published)
3. **Automatic cleanup**: Articles deleted after tests complete
4. **Error resilience**: Cleanup runs even if tests fail
5. **Read-only fallback**: If writes fail, tests skip gracefully

## Other Scripts

### md_to_rst.py

Converts markdown documentation to reStructuredText for Sphinx.

```bash
python scripts/md_to_rst.py
```

## Adding New Scripts

When adding new scripts:

1. **Location**: Place in `scripts/` directory
2. **Naming**: Use descriptive names with underscores (e.g., `test_live_api.py`)
3. **Shebang**: Include `#!/usr/bin/env python3` for Python scripts
4. **Documentation**: Add docstring and usage instructions
5. **Executable**: `chmod +x scripts/your_script.py`
6. **Update README**: Document new script in this file
