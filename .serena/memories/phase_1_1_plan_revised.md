# Phase 1.1 Plan - REVISED (User Feedback Incorporated)

**Date**: 2025-11-28
**Status**: ✅ Revised based on user feedback
**Timeline**: 7-8 days (extended from 5-7 for realism)
**Location**: `docs/pdca/phase-1.1-foundation/plan.md`

## Key Changes from Original Plan

### 1. CI/CD Moved to Day 1 (Mandatory)
**Was**: Optional task in Phase 1.4
**Now**: Mandatory Day 1 task (before first endpoint)

**Rationale**:
- Catches issues immediately from first endpoint
- Establishes quality baseline before implementation
- Enables confident iteration from Day 2
- GitHub Actions badge shows quality status

### 2. Full Day 1 for Foundation
**Was**: Days 1-2 for User endpoints + foundation
**Now**: Full Day 1 dedicated to foundation only

**Rationale**:
- WorldAnvilClient is architectural cornerstone (real complexity)
- Authentication patterns affect all future endpoints
- Retry/error logic must be solid before endpoints
- CI/CD setup needs proper time

**Day 1 Tasks**:
- WorldAnvilClient foundation (3-4 hours)
- Exception hierarchy & retry logic (2-3 hours)
- CI/CD pipeline (2 hours) - MANDATORY
- Dev setup script (1 hour)
- Getting Started docs (1 hour)

### 3. Write API Validation Spike (Days 6-7)
**Was**: Write API marked "Future" with uncertainty
**Now**: Dedicated Days 6-7 for validation spike

**Objective**: Confirm CRUD capabilities before Phase 2 commitment

**Test Cases**:
1. Can we update World metadata? (PUT /world/{id})
2. What permissions are required?
3. Which fields are updatable?
4. What error responses occur? (403? 405? etc.)

**Deliverable**: `docs/research/write-api-validation.md`
- Document all test results
- Code examples (successful and failed)
- Go/no-go decision for Phase 2 writes

**Outcomes**:
- ✅ Write works → Document patterns for Phase 2
- ❌ Write blocked → Document limitations, adjust Phase 2 scope
- ⚠️ Write partial → Document which operations work

### 4. Explicit Caching Decision (Day 4)
**Was**: Implicit caching implementation
**Now**: Explicit decision point with options analysis

**Options Considered**:
1. In-memory TTL cache (Recommended) ✅
   - Simple implementation (cachetools)
   - Session-scoped (acceptable for MCP)
   - Easy to extend later
2. File-based cache (Future)
   - Persistent across sessions
   - More complexity
3. No cache (Not recommended)
   - Slower operations
   - Need later anyway

**Decision**: In-memory TTL cache for Phase 1

### 5. Dev Setup Scripts (Day 1)
**Was**: Backlog, unscheduled
**Now**: Day 1 deliverable

**Script**: `scripts/dev-setup.sh`
```bash
#!/bin/bash
set -e
uv venv .venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
echo "✅ Ready! Run: source .venv/bin/activate"
```

**Purpose**: Unblock contributors immediately

### 6. Getting Started Docs (Day 1)
**Was**: Later documentation phase
**Now**: Day 1 deliverable

**Updates to**: `docs/source/installation.rst`
- Quickstart with `scripts/dev-setup.sh`
- Environment variable setup
- Troubleshooting section
- End-to-end validation

### 7. Timeline Extended (7-8 Days)
**Was**: 5-7 days
**Now**: 7-8 days (more realistic)

**Rationale**:
- Foundation work is real complexity
- Write API validation needs proper time
- Buffer for discovery and debugging
- No rushed corners for quality

## Revised Day Structure

**Day 1**: Foundation & CI (Critical Infrastructure)
- Client foundation
- Exception hierarchy & retry
- CI/CD pipeline (MANDATORY)
- Dev setup script
- Getting Started docs

**Days 2-3**: User & Identity Endpoints (Auth Validation)
- Pydantic models (Identity, User)
- BaseEndpoint generic
- Identity and User endpoints
- **Live API connectivity test** (Day 2 - CRITICAL)
- MCP tools
- Documentation

**Days 4-5**: World Endpoints (Core Content Access)
- **Caching decision** (Day 4 - EXPLICIT)
- ResponseCache implementation
- World models (WorldSummary, WorldDetail)
- World list and get endpoints
- RateLimiter implementation
- MCP tools and resources

**Days 6-7**: Write API Validation & Polish (Risk Mitigation)
- **Write API spike** (Day 6 - 4-5 hours)
- `docs/research/write-api-validation.md`
- Comprehensive testing
- Phase 1.1 retrospective
- Pattern extraction
- Documentation polish

## Updated Quality Gates

| Gate | Target | Validation |
|------|--------|------------|
| **CI Passing** | 100% | GitHub Actions green |
| **Test Coverage** | ≥90% | pytest-cov report |
| **Type Coverage** | 100% | mypy strict passes |
| **API Connectivity** | ✓ | Live credential test (Day 2) |
| **Docs Complete** | ✓ | Getting Started works |
| **Write API Assessed** | ✓ | Validation doc created |
| **Performance** | <500ms | Cached requests |
| **Code Quality** | Zero warnings | ruff check passes |

## Updated Risk Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **API credentials don't work** | High | Medium | Day 2 connectivity test before heavy implementation |
| **Write API not available** | Medium | Medium | Day 6-7 spike identifies before Phase 2 commitment |
| **2 days insufficient for foundation** | High | Low | Day 1 focuses only on foundation, not endpoints |
| **pywaclient patterns don't transfer** | Medium | Low | Already analyzed; patterns documented |

## User Feedback Addressed

✅ **Write API Uncertainty** → Days 6-7 validation spike with documented findings
✅ **CI/CD Optional** → Now mandatory on Day 1 (before first endpoint)
✅ **Backlog Unscheduled** → Getting Started docs, dev scripts explicitly on Day 1
✅ **Foundation Timing** → Full Day 1 dedicated (not rushed with endpoints)
✅ **Caching Decision** → Explicit Day 4 decision point (in-memory TTL)
✅ **Quality Gates** → Comprehensive table with all gates
✅ **Risk Mitigation** → Explicit strategies for all risks
✅ **Dev Setup** → `scripts/dev-setup.sh` on Day 1
✅ **Timeline** → Realistic 7-8 days (not optimistic 5-7)

## Critical Path

1. **Day 1**: Foundation & CI must be solid
2. **Day 2**: Auth connectivity test must pass before continuing
3. **Days 6-7**: Write API validation informs Phase 2 scope

## Next Steps

**After User Approval**:
1. Update Serena memory with final plan
2. Create `docs/pdca/phase-1.1-foundation/do.md`
3. Begin Day 1 implementation
4. Track progress with PDCA methodology

---

**Status**: ✅ Revised plan complete, awaiting user approval
**Quality**: Addresses all user feedback comprehensively
**Readiness**: Ready to begin implementation after approval
