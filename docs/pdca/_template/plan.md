# Plan: [Endpoint/Feature Name]

**Date**: YYYY-MM-DD
**Phase**: Phase X.Y
**Estimated Duration**: X days
**Assignee**: PM Agent → [Specialist Agent]

---

## Hypothesis (仮説)

### What to Implement
[Describe the endpoint or feature being implemented]

### Why This Approach
[Explain the reasoning behind the chosen implementation strategy]

### Key Decisions
- **Architecture**: [Design decisions]
- **Technology**: [Tools/libraries chosen]
- **Patterns**: [Design patterns to apply]

---

## Expected Outcomes (定量的目標)

### Functional Requirements
- [ ] Feature 1: [Specific capability]
- [ ] Feature 2: [Specific capability]
- [ ] Feature 3: [Specific capability]

### Quality Metrics
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Test Coverage | ≥85% | pytest --cov |
| Type Coverage | 100% | mypy strict |
| Documentation | 100% | Docstring check |
| Performance | <500ms | Benchmark tests |
| Error Handling | All scenarios | Error test cases |

### Success Criteria
- ✅ All functional requirements met
- ✅ All quality metrics achieved
- ✅ Documentation complete
- ✅ PDCA cycle documented

---

## Implementation Approach (実装計画)

### Step-by-Step Plan
1. **Define Models** (30 min)
   - Create Pydantic models for request/response
   - Add validation rules
   - Write model tests

2. **Implement API Client Method** (1-2 hours)
   - Add method to WorldAnvilClient
   - Implement retry logic
   - Add caching if appropriate
   - Error handling for all scenarios

3. **Create MCP Tool** (1 hour)
   - Wrap client method with @mcp.tool()
   - Add Context parameter
   - Implement progress reporting
   - Add logging (ctx.info, ctx.error)

4. **Write Tests** (2-3 hours)
   - Unit tests for client method
   - Integration tests for tool
   - Error scenario tests
   - Performance benchmarks

5. **Documentation** (1 hour)
   - Update API reference
   - Add usage examples
   - Update workflows if needed

### Dependencies
- **Blocked By**: [List prerequisites]
- **Blocks**: [List dependent work]
- **Related**: [List related endpoints]

---

## Risks & Mitigation (リスク対策)

### Technical Risks
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to prevent/handle] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to prevent/handle] |

### Process Risks
| Risk | Impact | Probability | Mitigation Strategy |
|------|--------|-------------|---------------------|
| Scope creep | Medium | Medium | Strict adherence to spec |
| Testing gaps | High | Low | Comprehensive test plan |

---

## Research & Investigation

### Questions to Answer
- [ ] Question 1: [What needs clarification?]
- [ ] Question 2: [What needs investigation?]

### Resources to Consult
- [ ] `context7`: [Specific documentation needed]
- [ ] `WebFetch`: [External resources to check]
- [ ] `Read`: [Local files to review]

### Prior Art
- Similar endpoints already implemented: [List]
- Reusable patterns: [Reference docs/patterns/]
- Learnings from previous phases: [Reference]

---

## Acceptance Criteria

### Definition of Done
- [ ] Code passes `ruff format --check`
- [ ] Code passes `ruff check`
- [ ] Code passes `mypy` strict mode
- [ ] All tests pass (`pytest`)
- [ ] Coverage target met (≥85%)
- [ ] Documentation complete
- [ ] API reference updated
- [ ] PDCA cycle complete

### Validation Method
```bash
# Quality gate command
ruff format . && \
ruff check --fix . && \
mypy src/world_anvil_mcp && \
pytest --cov=world_anvil_mcp --cov-report=term --cov-fail-under=85
```

---

## Timeline Estimate

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Research & Planning | 1-2 hours | This plan document |
| Implementation | 4-6 hours | Working code |
| Testing | 2-3 hours | Test suite |
| Documentation | 1 hour | Complete docs |
| **Total** | **1-1.5 days** | **Complete feature** |

---

## Serena Memory

**Write at Start**:
```python
write_memory("plan/[endpoint]/hypothesis", """
[Summary of this plan]
Expected: [Key metrics]
Approach: [Core strategy]
""")
```

**Track During**:
- Update `execution/[endpoint]/do` with progress
- Log errors immediately in `execution/[endpoint]/errors`
- Document solutions in `execution/[endpoint]/solutions`

---

## Next Steps

After plan approval:
1. Create `docs/pdca/[endpoint]/do.md`
2. Begin implementation following step-by-step plan
3. Update do.md continuously during work
4. Track all errors with root cause analysis
5. Checkpoint every 30 minutes

**Plan Approved By**: [Name/Date]
**Implementation Start**: [Date/Time]
