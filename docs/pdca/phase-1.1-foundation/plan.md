# Plan: Phase 1.1 - User & World Endpoints Foundation

**Date**: 2025-11-28 (Planning Phase)
**Phase**: Phase 1.1
**Estimated Duration**: 5-7 days
**Assignee**: PM Agent → backend-architect + quality-engineer

---

## Hypothesis (仮説)

### What to Implement

Phase 1.1 establishes the foundational infrastructure for the World Anvil MCP Server by implementing:

1. **WorldAnvilClient Core**: Main client class with authentication, rate limiting, and caching
2. **BaseEndpoint Generic**: Reusable endpoint base class with retry logic and error handling
3. **User Endpoints**: `/user/profile` and `/user/worlds` for authentication validation
4. **World Endpoints**: `/world/{id}` for basic world information retrieval

### Why This Approach

**Foundation-First Strategy**:
- User endpoints validate authentication before other endpoints
- World endpoints are prerequisite for all content operations
- BaseEndpoint provides patterns for all future endpoints
- Early validation against live API exposes quirks

**MCP-First Design**:
- Client designed specifically for MCP Context integration
- Tools wrap client methods with progress reporting
- Error handling optimized for Claude interaction
- Caching tuned for session-time workflows

**Test-Driven Approach**:
- Tests written alongside implementation (not after)
- ≥90% coverage target for core client code
- All three test levels (unit, integration, e2e)
- Quality gates enforced from first commit

### Key Decisions

**Architecture**:
- Async-first design (all I/O uses `async/await`)
- Generic `BaseEndpoint[T]` for type-safe endpoint classes
- Composition over inheritance (client delegates to endpoints)
- httpx.AsyncClient for connection pooling

**Technology**:
- httpx ≥0.27.0 for async HTTP
- Pydantic v2 for models and validation
- tenacity ≥8.0.0 for retry logic
- cachetools ≥5.0.0 for TTL caching

**Patterns**:
- Repository pattern (WorldAnvilClient coordinates endpoints)
- Token bucket algorithm for rate limiting (60 req/min)
- Exponential backoff with jitter for retries
- Response caching with granularity-aware keys

---

## Expected Outcomes (定量的目標)

### Functional Requirements

**Core Infrastructure**:
- [x] WorldAnvilClient with authentication
- [x] BaseEndpoint with retry and caching
- [x] RateLimiter with token bucket (60 req/min)
- [x] ResponseCache with TTL and granularity keys

**User Endpoints**:
- [x] `get_user_profile()` - Retrieve authenticated user
- [x] `list_user_worlds()` - List worlds user can access

**World Endpoints**:
- [x] `get_world(world_id, granularity)` - Get world details
- [x] Validate granularity parameter (STRING "0"-"3")

**MCP Tools**:
- [x] `get_user_profile` tool
- [x] `list_user_worlds` tool
- [x] `get_world` tool

### Quality Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Test Coverage | ≥90% | `pytest --cov=src/world_anvil_mcp --cov-fail-under=90` |
| Type Coverage | 100% | `mypy src/world_anvil_mcp` (strict mode) |
| Documentation | 100% | All public APIs have Google-style docstrings |
| Performance | <500ms | Response time for cached requests |
| Error Handling | All scenarios | Test all exception types |
| Code Quality | Zero warnings | `ruff check --select ALL` passes |

### Success Criteria

- ✅ All functional requirements implemented
- ✅ All quality metrics achieved
- ✅ Live API validation successful (with test credentials)
- ✅ Pre-commit hooks passing
- ✅ Documentation complete and built
- ✅ PDCA cycle documented

---

## Implementation Approach (実装計画)

### Step 1: Core Infrastructure (Day 1-2)

**Duration**: 1.5-2 days

**Tasks**:
1. **WorldAnvilClient Foundation** (4-6 hours)
   - Initialize httpx.AsyncClient with timeouts
   - Implement authentication header injection
   - Add environment variable validation
   - Create client context manager (`async with`)
   - Write unit tests for initialization

2. **BaseEndpoint Generic** (3-4 hours)
   - Define `BaseEndpoint[T]` with Pydantic response type
   - Implement `_request()` method with retry logic
   - Add MCP Context logging (ctx.info, ctx.error)
   - Create abstract response parsing
   - Write unit tests for retry behavior

3. **RateLimiter** (2-3 hours)
   - Token bucket algorithm (60 tokens/min, burst 10)
   - Async sleep when tokens depleted
   - Thread-safe implementation
   - Write unit tests for rate limiting

4. **ResponseCache** (2-3 hours)
   - TTL cache with granularity-aware keys
   - Cache key generation (endpoint + params + granularity)
   - Invalidation strategies
   - Write unit tests for caching

**Deliverables**:
- `src/world_anvil_mcp/client.py`
- `src/world_anvil_mcp/endpoints/base.py`
- `src/world_anvil_mcp/rate_limit.py`
- `src/world_anvil_mcp/cache.py`
- `tests/test_client.py`
- `tests/endpoints/test_base.py`
- `tests/test_rate_limit.py`
- `tests/test_cache.py`

### Step 2: User Endpoints (Day 3)

**Duration**: 1 day

**Tasks**:
1. **User Pydantic Models** (1-2 hours)
   - `UserProfile` model (id, username, email, etc.)
   - `World` model (id, name, description, etc.)
   - Validation rules
   - Write model unit tests

2. **UserEndpoint Class** (2-3 hours)
   - Inherit from `BaseEndpoint[UserProfile]`
   - `get_profile()` method
   - `list_worlds()` method
   - Error handling for auth failures
   - Write endpoint unit tests

3. **Integration with Client** (1 hour)
   - Add `user` property to WorldAnvilClient
   - Lazy initialization of UserEndpoint
   - Write integration tests

4. **MCP Tools** (2 hours)
   - `@mcp.tool()` for `get_user_profile`
   - `@mcp.tool()` for `list_user_worlds`
   - Context progress reporting
   - Write tool integration tests

**Deliverables**:
- `src/world_anvil_mcp/models/user.py`
- `src/world_anvil_mcp/endpoints/user.py`
- `tests/models/test_user.py`
- `tests/endpoints/test_user.py`
- Updated `src/world_anvil_mcp/server.py`

### Step 3: World Endpoints (Day 4)

**Duration**: 1 day

**Tasks**:
1. **World Pydantic Models** (1-2 hours)
   - `WorldDetail` model (complete world info)
   - Granularity-specific field validation
   - Write model unit tests

2. **WorldEndpoint Class** (2-3 hours)
   - Inherit from `BaseEndpoint[WorldDetail]`
   - `get(world_id, granularity)` method
   - Granularity parameter validation (STRING "0"-"3")
   - Cache key includes granularity
   - Write endpoint unit tests

3. **Integration with Client** (1 hour)
   - Add `worlds` property to WorldAnvilClient
   - Write integration tests

4. **MCP Tools** (2 hours)
   - `@mcp.tool()` for `get_world`
   - Granularity parameter in tool signature
   - Write tool integration tests

**Deliverables**:
- `src/world_anvil_mcp/models/world.py`
- `src/world_anvil_mcp/endpoints/world.py`
- `tests/models/test_world.py`
- `tests/endpoints/test_world.py`
- Updated `src/world_anvil_mcp/server.py`

### Step 4: Testing & Quality (Day 5-6)

**Duration**: 1.5-2 days

**Tasks**:
1. **Comprehensive Test Suite** (4-6 hours)
   - Unit tests for all components
   - Integration tests with mocked API (respx)
   - E2E tests with live API (skip in CI)
   - Error scenario coverage
   - Performance benchmarks

2. **Quality Gate Validation** (2-3 hours)
   - Run full test suite (`make test`)
   - Verify coverage ≥90% (`make coverage`)
   - Type check passes (`make typecheck`)
   - Linting passes (`make lint`)
   - Pre-commit hooks pass

3. **Live API Testing** (3-4 hours)
   - Test with real World Anvil credentials
   - Validate authentication flow
   - Test granularity parameter
   - Document any API quirks discovered
   - Verify rate limiting behavior

**Deliverables**:
- Comprehensive test suite (≥90% coverage)
- Test report with coverage analysis
- API quirks documentation
- Performance benchmark results

### Step 5: Documentation (Day 7)

**Duration**: 0.5-1 day

**Tasks**:
1. **API Reference** (2-3 hours)
   - Update Sphinx API docs (auto-generated)
   - Add usage examples to docstrings
   - Build and verify documentation
   - Fix any Sphinx warnings

2. **User Guide Updates** (2 hours)
   - Update quickstart with real examples
   - Document authentication setup
   - Add troubleshooting section

3. **PDCA Documentation** (2 hours)
   - Complete `docs/pdca/phase-1.1-foundation/do.md`
   - Complete `docs/pdca/phase-1.1-foundation/check.md`
   - Complete `docs/pdca/phase-1.1-foundation/act.md`

**Deliverables**:
- Updated Sphinx documentation
- User guide with examples
- Complete PDCA cycle

### Dependencies

**Blocked By**:
- ✅ Phase 0 complete (all prerequisites met)

**Blocks**:
- Phase 1.2: Article Endpoints (depends on client foundation)
- Phase 1.3: Category Endpoints (depends on client foundation)
- All future endpoint implementations

**Related**:
- pywaclient analysis (reference for patterns)
- Tool specifications (implementation blueprint)
- Quality standards (testing and docs requirements)

---

## Risks & Mitigation (リスク対策)

### Technical Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| API authentication differs from docs | High | Medium | Study pywaclient implementation first; test early |
| Granularity validation strict | Medium | Medium | Test all values ("0", "1", "2", "3") explicitly |
| Rate limiting edge cases | Medium | Low | Implement token bucket with margin (55 req/min target) |
| Caching invalidation bugs | Medium | Low | Comprehensive cache tests; conservative TTL |
| MCP Context integration issues | High | Low | Reference official MCP SDK examples closely |

### Process Risks

| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Scope creep (adding extra endpoints) | Medium | Medium | Strict adherence to User + World only |
| Testing gaps | High | Low | ≥90% coverage enforced by CI |
| Quality drift | High | Low | Pre-commit hooks block non-compliant commits |
| Documentation lag | Medium | Medium | Write docs alongside code, not after |
| Live API credentials issues | Medium | High | Document setup clearly; provide test account info |

---

## Research & Investigation

### Questions to Answer

- [x] How does World Anvil authentication work? (pywaclient analysis)
- [x] What are valid granularity values? (STRING "0"-"3")
- [x] What rate limits apply? (60 requests/minute)
- [ ] How does caching affect real workflows?
- [ ] What are common API error responses?
- [ ] How should retries be configured (max attempts, delays)?

### Resources to Consult

**Already Consulted**:
- [x] `docs/research/pywaclient-analysis.md` - Authentication patterns
- [x] `docs/specs/client-architecture.md` - Design blueprint
- [x] `docs/specs/tool-specifications.md` - User and World tools

**To Consult During Implementation**:
- [ ] `context7`: httpx async patterns, Pydantic v2 validation
- [ ] `WebFetch`: World Anvil official API docs (edge cases)
- [ ] `Read`: pywaclient source for retry logic patterns

### Prior Art

**Similar Components Already Designed**:
- Tool specifications (complete blueprint)
- Client architecture (detailed design)
- Quality standards (testing patterns)

**Reusable Patterns**:
- `docs/quality/api-client-patterns.md` - Async patterns
- `docs/quality/testing-requirements.md` - Test strategies
- Pre-commit hooks (already configured)

**Learnings from Phase 0**:
- Planning thoroughness prevents rework
- Quality gates from start = zero debt
- Documentation alongside work = better docs
- User feedback valuable (stay open to suggestions)

---

## Acceptance Criteria

### Definition of Done

**Code Quality**:
- [ ] `ruff format --check` passes (zero formatting issues)
- [ ] `ruff check` passes (zero linting warnings)
- [ ] `mypy` strict mode passes (100% type coverage)
- [ ] All tests pass (`pytest`)
- [ ] Coverage ≥90% (`pytest --cov --cov-fail-under=90`)

**Functionality**:
- [ ] User profile retrieval works
- [ ] User worlds listing works
- [ ] World detail retrieval works
- [ ] All granularity levels tested
- [ ] Rate limiting enforced correctly
- [ ] Caching reduces API calls

**Documentation**:
- [ ] All public APIs have docstrings (Google style)
- [ ] API reference auto-generated and accurate
- [ ] Usage examples in docstrings
- [ ] Quickstart updated with real code
- [ ] PDCA cycle complete

**Integration**:
- [ ] Pre-commit hooks pass
- [ ] Live API testing successful
- [ ] MCP tools work in Claude interaction
- [ ] No regression in existing tests

### Validation Method

```bash
# Complete quality gate validation
make dev-check

# Equivalent to:
ruff format . && \
ruff check . && \
mypy src/world_anvil_mcp && \
pytest --cov=src/world_anvil_mcp --cov-report=term --cov-fail-under=90

# Documentation build
make docs

# Live API testing (requires credentials)
WORLD_ANVIL_APP_KEY=xxx WORLD_ANVIL_USER_TOKEN=xxx pytest -m e2e
```

---

## Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Step 1**: Core Infrastructure | 1.5-2 days | Client, BaseEndpoint, RateLimiter, Cache |
| **Step 2**: User Endpoints | 1 day | UserEndpoint + MCP tools |
| **Step 3**: World Endpoints | 1 day | WorldEndpoint + MCP tools |
| **Step 4**: Testing & Quality | 1.5-2 days | Full test suite ≥90% coverage |
| **Step 5**: Documentation | 0.5-1 day | API docs + PDCA complete |
| **TOTAL** | **5.5-7 days** | **Production-ready foundation** |

**Buffer**: 1.5 days built in for discovery/debugging

---

## Serena Memory

**Write at Start**:
```python
write_memory("plan/phase-1.1/hypothesis", """
Phase 1.1: User & World Endpoints Foundation

Approach:
- Foundation-first (client, base endpoint, rate limit, cache)
- Test-driven (≥90% coverage target)
- MCP-optimized design

Expected Outcomes:
- WorldAnvilClient operational
- User and World endpoints complete
- ≥90% test coverage
- Live API validation successful
- Zero technical debt

Timeline: 5-7 days
""")

write_memory("plan/phase-1.1/rationale", """
Why Foundation-First:
- User endpoints validate auth before content operations
- World endpoints prerequisite for all content
- BaseEndpoint provides pattern for 30+ future endpoints
- Early API validation exposes quirks

Why Test-Driven:
- Prevents regression during rapid development
- Coverage enforced from first commit
- Quality gates block bad code
- Documentation quality higher
""")
```

**Track During**:
```python
# Updated continuously in do.md
write_memory("execution/phase-1.1/do", execution_log)

# Checkpoint every 30 minutes
write_memory("session/checkpoint", current_state)

# Log errors immediately
write_memory("execution/phase-1.1/errors", error_log)

# Document solutions
write_memory("execution/phase-1.1/solutions", solution_log)
```

---

## Next Steps

**After Plan Approval**:

1. **Create Execution Log**
   - `docs/pdca/phase-1.1-foundation/do.md`
   - Begin logging from first commit

2. **Set Up Environment**
   - Verify `uv venv` activated
   - Install dependencies (`uv pip install -e ".[dev]"`)
   - Verify pre-commit hooks (`pre-commit install`)

3. **Begin Step 1: Core Infrastructure**
   - Create `src/world_anvil_mcp/client.py`
   - Implement WorldAnvilClient
   - Write tests alongside code
   - Commit incrementally

4. **Root Cause Analysis Protocol**
   - Any error → STOP
   - Investigate with context7/WebFetch/Grep
   - Document in `execution/phase-1.1/errors`
   - Design different solution
   - Document learning

5. **Continuous Updates**
   - Update `do.md` during work (not after)
   - Checkpoint every 30 minutes
   - Track all trial-and-error
   - Log all errors with root causes

---

## Quality Commitment

**Zero Technical Debt**:
- No skipped tests
- No disabled quality checks
- No TODO comments for core functionality
- No warnings ignored without investigation

**Evidence-Based Development**:
- All design decisions documented with rationale
- All errors analyzed for root cause
- All solutions tested and validated
- All learnings captured

**User-Focused Quality**:
- Session-time performance (<500ms cached)
- Clear error messages
- Comprehensive documentation
- Reliable operation

---

**Plan Approved By**: PM Agent
**Implementation Start**: After Phase 0.5 completion
**Expected Completion**: 5-7 days from start
**Next Document**: `docs/pdca/phase-1.1-foundation/do.md` (execution log)

---

**Status**: ✅ Plan Complete, Ready for Execution
**Serena Memory**: `plan/phase-1.1/hypothesis` written
**PDCA Phase**: Plan → Do (next)
