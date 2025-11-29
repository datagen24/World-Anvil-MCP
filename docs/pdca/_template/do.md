# Do: [Endpoint/Feature Name]

**Date Started**: YYYY-MM-DD HH:MM
**Phase**: Phase X.Y
**Current Status**: [In Progress / Blocked / Complete]

---

## Implementation Log

### YYYY-MM-DD

#### HH:MM - Session Start
- Restored context from `session/checkpoint`
- Current plan: [Link to plan.md]
- Today's goal: [Specific objective]

#### HH:MM - [Task Name]
**What**: [What was attempted]
**Result**: [Success/Failure/Partial]
**Notes**: [Important observations]

```python
# Code snippet if relevant
```

#### HH:MM - Error Encountered
**Error**: `[Error message or description]`

**Symptoms**:
- [What happened]
- [Expected vs actual behavior]

**Root Cause Investigation**:
1. **Hypothesis**: [Initial guess about cause]
2. **Research**:
   - `context7`: [What documentation says]
   - `WebFetch`: [Stack Overflow/GitHub issues found]
   - `Read`: [Related code examined]
3. **Root Cause**: [Actual cause identified]
4. **Evidence**: [Why this is the cause]

**Solution Attempt #1**:
- **Approach**: [What was tried]
- **Result**: [Worked/Failed]
- **Reason**: [Why it worked or didn't]

**Final Solution**:
- **Approach**: [Successful solution]
- **Implementation**:
```python
# Working code
```
- **Validation**: [How verified it works]

**Learning**: [What to remember for future]

#### HH:MM - Checkpoint
- Progress: [What's complete]
- Next: [What's next]
- Blockers: [Any issues]

```python
write_memory("execution/[endpoint]/do", """
Progress: [Current state]
Completed: [List]
Next: [List]
Blockers: [List]
""")
```

---

## Trial and Error Log

### Approach 1: [Description]
- **Tried**: YYYY-MM-DD HH:MM
- **Hypothesis**: [Why this should work]
- **Result**: ❌ Failed / ⚠️ Partial / ✅ Success
- **Learning**: [What was learned]

### Approach 2: [Description]
- **Tried**: YYYY-MM-DD HH:MM
- **Hypothesis**: [Why this should work]
- **Result**: ❌ Failed / ⚠️ Partial / ✅ Success
- **Learning**: [What was learned]

---

## Research & Investigation Notes

### Official Documentation (context7)
**Query**: [What was searched]
**Finding**: [What was learned]
**Applied**: [How it helped implementation]

### Community Resources (WebFetch)
**URL**: [Link to resource]
**Finding**: [What was learned]
**Applied**: [How it helped implementation]

### Codebase Patterns (Grep/Read)
**Location**: [File:line]
**Pattern**: [What pattern was found]
**Applied**: [How pattern was reused]

---

## Code Evolution

### Initial Implementation
```python
# First attempt
[Code]
```
**Issues**: [What was wrong]

### Iteration 2
```python
# Improved version
[Code]
```
**Improvements**: [What changed and why]

### Final Implementation
```python
# Production-ready code
[Code]
```
**Why This Works**: [Explanation]

---

## Test Development

### Test Cases Written
1. **Happy Path**: [Description]
2. **Error Case 1**: [Description]
3. **Error Case 2**: [Description]
4. **Edge Case**: [Description]

### Coverage Progress
| Component | Initial | Current | Target |
|-----------|---------|---------|--------|
| Client Method | 0% | X% | 90% |
| MCP Tool | 0% | Y% | 85% |
| Overall | 0% | Z% | 85% |

---

## Challenges Encountered

### Challenge 1: [Description]
**Impact**: High/Medium/Low
**Time Lost**: X hours
**Resolution**: [How solved]
**Prevention**: [How to avoid in future]

### Challenge 2: [Description]
**Impact**: High/Medium/Low
**Time Lost**: X hours
**Resolution**: [How solved]
**Prevention**: [How to avoid in future]

---

## Learnings During Implementation

### Technical Learnings
- 💡 [Learning 1]: [Explanation]
- 💡 [Learning 2]: [Explanation]

### Process Learnings
- 📝 [Learning 1]: [Explanation]
- 📝 [Learning 2]: [Explanation]

### Tool Usage
- 🔧 **context7**: [How effective, what to search differently]
- 🔧 **WebFetch**: [Best resources found]
- 🔧 **Sequential**: [When it helped with reasoning]

---

## Progress Metrics

### Time Tracking
| Task | Estimated | Actual | Variance |
|------|-----------|--------|----------|
| Models | 30min | Xmin | +/- Y |
| Client Method | 1-2h | Xh | +/- Y |
| MCP Tool | 1h | Xh | +/- Y |
| Tests | 2-3h | Xh | +/- Y |
| Docs | 1h | Xh | +/- Y |

### Quality Metrics
| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Test Coverage | ≥85% | X% | 🔴/🟡/🟢 |
| Type Coverage | 100% | X% | 🔴/🟡/🟢 |
| Docstrings | 100% | X% | 🔴/🟡/🟢 |

---

## Session End Notes

### What Was Completed Today
- [List accomplishments]

### What's Next
- [List next steps]

### Blockers
- [List any blockers]

### Checkpoint Save
```python
write_memory("session/checkpoint", """
Completed: [List]
Next: [List]
Blockers: [List]
Coverage: X%
Status: [In Progress/Blocked/Complete]
""")
```

---

## Notes for Future Self

### What Worked Well
- [Things that went smoothly]

### What to Do Differently
- [Improvements for next time]

### Reusable Patterns
- [Patterns worth extracting to docs/patterns/]

---

**Last Updated**: YYYY-MM-DD HH:MM
**Next Session Start**: Read this file + session/checkpoint
