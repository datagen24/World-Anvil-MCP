# Act: [Endpoint/Feature Name]

**Date**: YYYY-MM-DD
**Phase**: Phase X.Y
**Status**: ✅ Success / ⚠️ Partial / ❌ Failed

---

## Action Summary (改善アクション)

### Overall Outcome
[Brief summary of what was achieved and what needs improvement]

### Key Decisions Made
1. **[Decision 1]**: [What was decided and why]
2. **[Decision 2]**: [What was decided and why]
3. **[Decision 3]**: [What was decided and why]

---

## Success Pattern Formalization (成功パターン化)

### Patterns Worth Extracting

#### Pattern 1: [Pattern Name]
**Extract To**: `docs/patterns/[pattern-name].md`

**Description**: [What pattern was successful]

**When to Use**: [Conditions where pattern applies]

**Implementation**:
```python
# Example code showing pattern
```

**Benefits**:
- [Benefit 1]
- [Benefit 2]

**Risks**:
- [Potential issue 1]
- [Potential issue 2]

**Related Patterns**: [Links to similar patterns]

---

#### Pattern 2: [Pattern Name]
[Same structure as above]

---

### Global Best Practices → CLAUDE.md

**Additions to CLAUDE.md**:
```markdown
## [New Section or Update]

[Content to add to global best practices]

Rationale: [Why this is globally applicable]
Evidence: [What proved this works]
```

---

## Failure Documentation (失敗の記録)

### Mistakes to Document

#### Mistake 1: [Error Description]
**Document In**: `docs/mistakes/[endpoint]-[date].md`

**What Went Wrong**: [Description]

**Root Cause**: [Why it happened]

**Impact**:
- Time Lost: X hours
- Quality Impact: [Description]
- User Impact: [Description]

**Prevention Checklist**:
- [ ] Check 1: [Validation step]
- [ ] Check 2: [Validation step]
- [ ] Check 3: [Validation step]

**Early Warning Signs**:
- [Signal 1 that indicates this issue]
- [Signal 2 that indicates this issue]

**Quick Fix Guide**:
```bash
# If this error occurs again
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Knowledge Base Updates

### Learnings to Preserve

#### Learning 1: [Topic]
**Category**: Technical / Process / Tool Usage

**What We Learned**: [Description]

**Why Important**: [Significance]

**How to Apply**: [Practical application]

**Serena Memory**:
```python
write_memory("learning/[category]/[topic]", """
Learning: [Summary]
Context: [When applicable]
Application: [How to use]
Evidence: [What proved this]
""")
```

---

## Checklist Updates

### Quality Gate Additions

**Add to Quality Gates** (`docs/quality/testing-requirements.md`):
```markdown
## [New Section or Update]

### [Checkpoint Name]
- [ ] [New validation step]
- [ ] [New validation step]

Rationale: [Why this check is needed]
Based on: [What experience led to this]
```

### Pre-commit Hook Updates

**Add to Pre-commit** (if needed):
```yaml
- id: [new-check-name]
  name: [Description]
  entry: [Command]
  language: system
  types: [python]
```

### Testing Checklist Updates

**Add to Test Requirements**:
- [ ] [New test type or scenario]
- [ ] [New test type or scenario]

Based on: [What gaps were discovered]

---

## Process Improvements

### PDCA Methodology Updates

**What Worked**:
- [Process element that worked well]
- [Process element that worked well]

**What to Change**:
- [Process improvement 1]
- [Process improvement 2]

**New Process Steps**:
```markdown
### [New Step Name]

When: [When to perform this step]
How: [How to perform this step]
Why: [Why this step is important]
```

### Tool Usage Improvements

#### context7
- **Current Usage**: [How used this time]
- **More Effective**: [Better way to use]
- **New Searches**: [Useful queries discovered]

#### WebFetch
- **Best Resources Found**: [URLs that helped]
- **Search Strategies**: [Effective search patterns]
- **Bookmark**: [Resources to save]

#### Sequential
- **Effective For**: [When it helped most]
- **Ineffective For**: [When it didn't help]
- **Improved Prompts**: [Better ways to prompt]

---

## Documentation Updates

### API Reference
**File**: `claudedocs/API_REFERENCE.md`

**Additions**:
```markdown
## [Endpoint Name]

[Complete documentation to add]
```

**Status**: [ ] Complete / [ ] Partial / [ ] Not needed

### Workflow Documentation
**File**: `docs/workflows/[workflow-name].md`

**Updates**:
- [ ] New workflow created
- [ ] Existing workflow updated
- [ ] Example added

**Status**: [ ] Complete / [ ] Partial / [ ] Not needed

### README Updates
**File**: `README.md`

**Changes**:
- [ ] Feature list updated
- [ ] Installation steps updated
- [ ] Usage examples added

**Status**: [ ] Complete / [ ] Partial / [ ] Not needed

---

## Next Endpoint Preparation

### Learnings to Apply
1. **[Learning 1]**: [How to apply in next endpoint]
2. **[Learning 2]**: [How to apply in next endpoint]
3. **[Learning 3]**: [How to apply in next endpoint]

### Patterns to Reuse
- [ ] Pattern 1: [Name] - Apply to [next endpoint]
- [ ] Pattern 2: [Name] - Apply to [next endpoint]

### Mistakes to Avoid
- [ ] Mistake 1: [Name] - Prevention checklist ready
- [ ] Mistake 2: [Name] - Prevention checklist ready

### Template Updates Needed
- [ ] plan.md template: [What to add/change]
- [ ] do.md template: [What to add/change]
- [ ] check.md template: [What to add/change]

---

## Phase-Level Improvements

### If End of Phase

**Phase Retrospective Questions**:
1. Did we meet phase goals?
2. What patterns emerged across all endpoints?
3. What should we do differently in next phase?
4. Are there systematic issues to address?

**Phase Summary**:
- Endpoints Completed: X/Y
- Overall Coverage: Z%
- Major Learnings: [Summary]
- Process Changes Needed: [Summary]

---

## Action Items

### Immediate (Before Next Endpoint)
- [ ] Extract patterns to `docs/patterns/`
- [ ] Document mistakes in `docs/mistakes/`
- [ ] Update CLAUDE.md if applicable
- [ ] Update checklists
- [ ] Update testing requirements
- [ ] Create Serena memories
- [ ] Update project plan if needed

### Short-term (This Phase)
- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

### Long-term (Future Phases)
- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]

---

## Metrics for Project Tracking

### Cumulative Progress
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Endpoints Complete | X | Y | +Z |
| Overall Coverage | X% | Y% | +Z% |
| Patterns Documented | X | Y | +Z |
| Mistakes Recorded | X | Y | +Z |

### Velocity Tracking
- **Estimated Time**: X hours
- **Actual Time**: Y hours
- **Velocity**: Z (actual/estimated)
- **Trend**: Improving/Stable/Declining

---

## Celebration & Motivation

### What We're Proud Of
- 🎉 [Achievement 1]
- 🎉 [Achievement 2]
- 🎉 [Achievement 3]

### Team Appreciation
[Acknowledge good work, learnings, problem-solving]

### Progress Visualization
```
MVP Progress: ████████░░ 80% (12/15 endpoints)
Full D&D:     ████░░░░░░ 40% (10/25 endpoints)
Complete:     ██░░░░░░░░ 20% (7/34 endpoints)
```

---

## Commit to Next Steps

### Ready to Proceed?
**Status**: ✅ Yes / ⚠️ With conditions / ❌ Not yet

**Conditions** (if any): [What needs to happen first]

### Next Endpoint
**Endpoint**: [Name of next endpoint]
**Plan Creation**: [When to create plan.md]
**Estimated Start**: [Date/Time]

---

## Serena Memory Final Update

```python
# Complete the learning cycle
write_memory("learning/patterns/[pattern-name]", """
[Pattern documentation]
""")

write_memory("learning/mistakes/[timestamp]", """
[Mistake documentation]
""")

write_memory("project/progress", """
Phase: X.Y
Endpoints: X/Y complete (Z%)
Coverage: A%
Velocity: B
Status: On track / Behind / Ahead
Next: [Next endpoint name]
""")

write_memory("session/last", """
Completed: [Endpoint name]
Result: Success/Partial/Failed
Key Learnings: [Summary]
Next Actions: [List]
""")
```

---

## Sign-off

**Completed By**: PM Agent
**Date**: YYYY-MM-DD
**Next PDCA Cycle**: [Next endpoint name]
**Continuous Improvement**: ✅ Patterns extracted, mistakes documented, knowledge preserved

---

**End of Act Phase - Ready for Next Implementation**
