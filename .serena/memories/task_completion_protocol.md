# Task Completion Protocol

When completing any development task, follow this protocol to ensure code quality and consistency.

## Pre-Commit Checklist

### 1. Code Formatting
```bash
ruff format .
```
- Auto-formats all Python files to consistent style
- Must pass before committing

### 2. Linting
```bash
ruff check --fix .
```
- Checks code quality (E, F, I, N, W, UP rules)
- Auto-fixes issues where possible
- Review any remaining warnings

### 3. Type Checking
```bash
mypy src/world_anvil_mcp
```
- Verifies type hints are correct
- Must pass with strict mode enabled
- Fix any type errors before committing

### 4. Tests
```bash
pytest
```
- Run all tests to ensure no regressions
- All tests must pass
- Add tests for new functionality

### 5. Coverage Check
```bash
pytest --cov=world_anvil_mcp --cov-report=term
```
- Verify test coverage remains >80%
- Add tests if coverage drops

## Quick All-in-One Command

```bash
ruff format . && ruff check --fix . && mypy src/world_anvil_mcp && pytest --cov=world_anvil_mcp
```

If all commands succeed, code is ready to commit.

## Specific Task Types

### Adding a New Tool

1. **Implement tool function** in appropriate file (e.g., `tools/articles.py`)
   - Add type hints
   - Add docstring (Google style)
   - Use `@mcp.tool()` decorator
   - Make function async if needed

2. **Register in server.py** if not auto-discovered

3. **Add tests** in `tests/test_tools.py`
   - Test success cases
   - Test error cases
   - Mock API calls

4. **Update documentation** in `claudedocs/API_REFERENCE.md`

5. **Run checklist** (format, lint, type check, test)

### Adding a New Resource

1. **Implement resource function** in `resources/` directory
   - Use `@mcp.resource("uri://pattern")` decorator
   - Return string or structured data
   - Add proper error handling

2. **Add tests** in `tests/test_resources.py`

3. **Document resource** in API reference

4. **Run checklist**

### Adding API Client Method

1. **Define Pydantic model** in `api/models.py` for response type

2. **Implement client method** in `api/client.py`
   - Add type hints
   - Add retry logic with `@retry` decorator
   - Handle caching if appropriate
   - Add proper exception handling

3. **Add unit tests** in `tests/test_api_client.py`
   - Mock HTTP responses
   - Test error scenarios

4. **Run checklist**

### Updating OpenAPI Integration

1. **Review openapi.yml** for endpoint details

2. **Update models** to match API schema

3. **Update client methods** to use correct headers:
   - `x-application-key`: Application key
   - `x-auth-token`: User authentication token

4. **Test against real API** (if keys available)

5. **Run checklist**

## Documentation Updates

When adding features, update:
- `README.md` if user-facing changes
- `claudedocs/DESIGN_SPECIFICATION.md` if architecture changes
- `claudedocs/API_REFERENCE.md` for new tools/resources
- `claudedocs/USAGE_EXAMPLES.md` for new workflows

## Git Commit Standards

```bash
# Format: "Verb (present tense) + what"
git commit -m "Add article creation tool"
git commit -m "Fix authentication header bug"
git commit -m "Update design specification with OpenAPI details"

# Not: "Added", "Fixed", "Updated" (past tense)
```

## Pre-Push Checklist

1. ✅ All pre-commit checks pass
2. ✅ Documentation updated
3. ✅ Tests added for new functionality
4. ✅ No sensitive data (API keys) in code
5. ✅ Commit messages are descriptive
6. ✅ Branch is up to date with main

## Performance Considerations

- ⚡ Use caching for repeated API calls
- ⚡ Implement rate limiting to respect API limits
- ⚡ Batch operations when possible
- ⚡ Use async/await for concurrent operations

## Security Checks

- 🔒 Never commit API keys or tokens
- 🔒 Validate all user inputs
- 🔒 Sanitize error messages (no token exposure)
- 🔒 Use environment variables for secrets
