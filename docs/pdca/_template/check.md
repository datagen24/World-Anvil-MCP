# Check: [Endpoint/Feature Name]

**Date Completed**: YYYY-MM-DD
**Phase**: Phase X.Y
**Implementation Duration**: X days

---

## Results vs Expectations (評価)

### Functional Requirements

| Requirement | Expected | Actual | Status | Notes |
|-------------|----------|--------|--------|-------|
| Feature 1 | [Description] | [What was delivered] | ✅/⚠️/❌ | [Comments] |
| Feature 2 | [Description] | [What was delivered] | ✅/⚠️/❌ | [Comments] |
| Feature 3 | [Description] | [What was delivered] | ✅/⚠️/❌ | [Comments] |

**Overall Functional Success**: X/Y requirements met (Z%)

---

### Quality Metrics

| Metric | Target | Actual | Status | Gap Analysis |
|--------|--------|--------|--------|--------------|
| Test Coverage | ≥85% | X% | ✅/⚠️/❌ | [If gap, why?] |
| Client Coverage | ≥90% | X% | ✅/⚠️/❌ | [If gap, why?] |
| Tool Coverage | ≥85% | X% | ✅/⚠️/❌ | [If gap, why?] |
| Type Coverage | 100% | X% | ✅/⚠️/❌ | [If gap, why?] |
| Docstrings | 100% | X% | ✅/⚠️/❌ | [If gap, why?] |
| Performance | <500ms | Xms | ✅/⚠️/❌ | [If gap, why?] |
| Error Handling | All cases | X/Y cases | ✅/⚠️/❌ | [If gap, why?] |

**Overall Quality Success**: X/Y metrics met (Z%)

---

### Coverage Report

```bash
# Final coverage report
pytest --cov=world_anvil_mcp --cov-report=term

# Output:
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
src/world_anvil_mcp/api/client.py         150      5    97%
src/world_anvil_mcp/tools/[endpoint].py    75      8    89%
-----------------------------------------------------------
TOTAL                                     225     13    94%
```

**Analysis**:
- ✅ Exceeded target (94% vs 85%)
- Missing coverage: [Describe uncovered lines]
- Justification: [Why acceptable or plan to cover]

---

### Timeline Performance

| Phase | Estimated | Actual | Variance | Reason for Variance |
|-------|-----------|--------|----------|---------------------|
| Planning | 1-2h | Xh | +/- Y | [Explanation] |
| Implementation | 4-6h | Xh | +/- Y | [Explanation] |
| Testing | 2-3h | Xh | +/- Y | [Explanation] |
| Documentation | 1h | Xh | +/- Y | [Explanation] |
| **Total** | **1-1.5 days** | **X days** | **+/- Y** | [Overall analysis] |

**Timeline Success**: On time / Ahead / Behind

---

## What Worked Well (成功パターン)

### Technical Successes
1. **[Success 1]**
   - **What**: [What went well]
   - **Why**: [Reason it worked]
   - **Reusable**: Yes/No - [Explanation]

2. **[Success 2]**
   - **What**: [What went well]
   - **Why**: [Reason it worked]
   - **Reusable**: Yes/No - [Explanation]

### Process Successes
1. **[Success 1]**
   - **What**: [What went well]
   - **Impact**: [Benefit gained]
   - **Repeat**: [How to replicate]

2. **[Success 2]**
   - **What**: [What went well]
   - **Impact**: [Benefit gained]
   - **Repeat**: [How to replicate]

### Tool Effectiveness
| Tool | Effectiveness | Best Use Case | Learnings |
|------|---------------|---------------|-----------|
| context7 | ⭐⭐⭐⭐⭐ | [When most useful] | [What learned] |
| WebFetch | ⭐⭐⭐⭐⭐ | [When most useful] | [What learned] |
| Sequential | ⭐⭐⭐⭐⭐ | [When most useful] | [What learned] |

---

## What Failed / Challenges (失敗・課題)

### Technical Failures
1. **[Failure 1]**
   - **What Failed**: [Description]
   - **Root Cause**: [Why it failed]
   - **Impact**: High/Medium/Low
   - **Time Lost**: X hours
   - **Prevention**: [How to avoid in future]

2. **[Failure 2]**
   - **What Failed**: [Description]
   - **Root Cause**: [Why it failed]
   - **Impact**: High/Medium/Low
   - **Time Lost**: X hours
   - **Prevention**: [How to avoid in future]

### Process Failures
1. **[Failure 1]**
   - **What Failed**: [Description]
   - **Root Cause**: [Why it failed]
   - **Impact**: [Effect on project]
   - **Prevention**: [Process improvement]

### Unexpected Challenges
1. **[Challenge 1]**
   - **Description**: [What was unexpected]
   - **How Handled**: [Solution applied]
   - **Learning**: [What to know for next time]

---

## Hypothesis Validation (仮説の検証)

### Original Hypothesis
> [Quote from plan.md]

### Validation Results
- **Correct Assumptions**: [What was right]
- **Incorrect Assumptions**: [What was wrong]
- **Surprises**: [What was unexpected]

### Hypothesis Evolution
[How understanding changed during implementation]

---

## Quality Analysis

### Code Quality
- **Strengths**: [What's good about the code]
- **Weaknesses**: [What could be better]
- **Technical Debt**: [Any compromises made]
- **Refactoring Needed**: [Future improvements]

### Test Quality
- **Strengths**: [What's good about tests]
- **Gaps**: [What's missing]
- **Coverage Holes**: [Uncovered scenarios]
- **Improvement Plan**: [How to enhance]

### Documentation Quality
- **Completeness**: [What's documented well]
- **Gaps**: [What's missing]
- **Clarity**: [How understandable]
- **Improvement Plan**: [How to enhance]

---

## Performance Analysis

### Benchmarks
```python
# Performance test results
test_get_world: 145ms (target: <200ms) ✅
test_list_worlds: 320ms (target: <500ms) ✅
test_create_article: 280ms (target: <500ms) ✅
```

**Analysis**:
- All targets met ✅
- Optimization opportunities: [List if any]
- Caching effectiveness: [Measurement]

---

## Security & Error Handling

### Error Scenarios Tested
- [x] Invalid authentication
- [x] Rate limit exceeded
- [x] Network timeout
- [x] Invalid input data
- [x] Resource not found
- [ ] [Any not tested]

### Security Considerations
- **Authentication**: [How handled]
- **Input Validation**: [How validated]
- **Secrets Management**: [How protected]
- **Error Messages**: [Info exposure checked]

---

## Comparison with Similar Work

### Previous Similar Endpoints
| Endpoint | This Implementation | Comparison | Learning Applied |
|----------|---------------------|------------|------------------|
| [Previous] | [Current approach] | Better/Worse/Same | [What changed] |

### Pattern Consistency
- **Followed Existing Patterns**: [List]
- **New Patterns Introduced**: [List with justification]
- **Pattern Violations**: [List with justification]

---

## Learnings Summary (学び)

### Top 3 Technical Learnings
1. **[Learning 1]**: [Explanation and application]
2. **[Learning 2]**: [Explanation and application]
3. **[Learning 3]**: [Explanation and application]

### Top 3 Process Learnings
1. **[Learning 1]**: [Explanation and application]
2. **[Learning 2]**: [Explanation and application]
3. **[Learning 3]**: [Explanation and application]

### Reusable Patterns Identified
- [ ] Pattern 1: [Name] → Extract to docs/patterns/
- [ ] Pattern 2: [Name] → Extract to docs/patterns/
- [ ] Pattern 3: [Name] → Extract to docs/patterns/

---

## User Impact

### User Value Delivered
- **Functionality**: [What users can now do]
- **Workflows Enabled**: [Which workflows]
- **Pain Points Solved**: [What problems solved]

### User Experience
- **Ease of Use**: [How easy to use]
- **Documentation**: [How well documented]
- **Examples**: [How many examples provided]

---

## Recommendations

### For This Endpoint
- **Immediate**: [Must do before considering complete]
- **Short-term**: [Should do in next sprint]
- **Long-term**: [Nice to have improvements]

### For Future Endpoints
- **Do More Of**: [What to continue]
- **Do Less Of**: [What to reduce]
- **Start Doing**: [New practices to adopt]
- **Stop Doing**: [Practices to eliminate]

### For Process
- **Methodology**: [PDCA process improvements]
- **Tools**: [Tool usage improvements]
- **Documentation**: [Doc process improvements]

---

## Serena Memory Update

```python
write_memory("evaluation/[endpoint]/check", """
Status: ✅ Complete / ⚠️ Partial / ❌ Failed
Coverage: X%
Timeline: On time / Ahead / Behind (X days)
Quality: [Summary]

Success Patterns:
- [Pattern 1]
- [Pattern 2]

Failures:
- [Failure 1]
- [Failure 2]

Learnings:
- [Learning 1]
- [Learning 2]
""")
```

---

## Overall Assessment

### Success Rating
**Overall**: ⭐⭐⭐⭐⭐ (X/5 stars)

**Breakdown**:
- Functionality: ⭐⭐⭐⭐⭐ (X/5) - [Comment]
- Quality: ⭐⭐⭐⭐⭐ (X/5) - [Comment]
- Timeline: ⭐⭐⭐⭐⭐ (X/5) - [Comment]
- Documentation: ⭐⭐⭐⭐⭐ (X/5) - [Comment]
- Learning Value: ⭐⭐⭐⭐⭐ (X/5) - [Comment]

### Would We Approach Differently?
[If starting over, what would you change?]

### Ready for Next Phase?
**Status**: ✅ Yes / ⚠️ Needs work / ❌ Not ready

**Blockers for Next Phase**: [List any]

---

**Checked By**: PM Agent
**Check Date**: YYYY-MM-DD
**Next Action**: Proceed to act.md for formalization
