# PDCA Documentation System

**Purpose**: Systematic learning and improvement through Plan-Do-Check-Act cycles

This directory contains PDCA (Plan-Do-Check-Act) documentation for the World Anvil MCP Server project. The PDCA methodology ensures continuous learning, quality improvement, and knowledge capture throughout development.

---

## What is PDCA?

**PDCA** (Plan-Do-Check-Act) is a four-step iterative cycle for continuous improvement:

1. **Plan (仮説)**: Define hypothesis, goals, and approach
2. **Do (実験)**: Execute the plan, document trial-and-error
3. **Check (評価)**: Evaluate results against expectations
4. **Act (改善)**: Formalize successes, prevent mistakes

### Why PDCA for Software Development?

- **Learning Capture**: Document what works and what doesn't
- **Mistake Prevention**: Root cause analysis prevents recurring errors
- **Knowledge Transfer**: Future team members benefit from documented learnings
- **Continuous Improvement**: Systematic refinement of processes and patterns

---

## Directory Structure

```
docs/pdca/
├── README.md                    # This file
├── _template/                   # PDCA templates
│   ├── plan.md                 # Plan phase template
│   ├── do.md                   # Do phase template
│   ├── check.md                # Check phase template
│   └── act.md                  # Act phase template
│
├── phase-0-retrospective/       # Phase 0 retrospective
│   └── check.md                # Completed retrospective
│
├── phase-1.1-foundation/        # Example: Phase 1.1 PDCA
│   ├── plan.md                 # Implementation plan
│   ├── do.md                   # Execution log
│   ├── check.md                # Evaluation
│   └── act.md                  # Improvement actions
│
└── [feature-name]/              # Feature-specific PDCA
    ├── plan.md
    ├── do.md
    ├── check.md
    └── act.md
```

---

## PDCA Workflow

### Phase 1: Plan (仮説)

**Purpose**: Define hypothesis and implementation approach

**Create**: `docs/pdca/[feature-name]/plan.md`

**Contents**:
- **Hypothesis**: What to implement and why this approach
- **Expected Outcomes**: Quantitative targets (coverage, performance, etc.)
- **Implementation Approach**: Step-by-step plan
- **Risks & Mitigation**: Potential issues and prevention strategies
- **Acceptance Criteria**: Definition of done

**Serena Memory**:
```python
write_memory("plan/[feature]/hypothesis", """
Feature: [Name]
Approach: [Strategy]
Expected: [Metrics]
""")
```

**Example**: See `docs/pdca/phase-1.1-foundation/plan.md`

---

### Phase 2: Do (実験)

**Purpose**: Execute plan and document trial-and-error

**Create**: `docs/pdca/[feature-name]/do.md`

**Contents**:
- **Implementation Log**: Chronological execution diary
- **Errors Encountered**: All errors with timestamps
- **Root Cause Analysis**: Why errors occurred
- **Solutions Applied**: How errors were resolved
- **Learnings During Work**: Insights gained

**Critical Rule**: **Never retry without understanding WHY it failed**

**Investigation Pattern**:
1. Error occurs → STOP
2. Investigate root cause (context7, WebFetch, Grep, Read)
3. Form hypothesis about cause
4. Design solution (must be different from failed approach)
5. Execute solution
6. Document learning

**Serena Memory**:
```python
# Continuous updates
write_memory("execution/[feature]/do", execution_log)
write_memory("execution/[feature]/errors", error_log)
write_memory("execution/[feature]/solutions", solution_log)

# Checkpoints every 30 minutes
write_memory("session/checkpoint", current_state)
```

**Example Template**: See `docs/pdca/_template/do.md`

---

### Phase 3: Check (評価)

**Purpose**: Evaluate results against expectations

**Create**: `docs/pdca/[feature-name]/check.md`

**Contents**:
- **Results vs Expectations**: Metric comparison table
- **What Worked Well**: Successes to replicate
- **What Failed / Challenges**: Issues encountered
- **Unexpected Discoveries**: Surprises (positive and negative)
- **Key Learnings**: Technical and process insights

**Evaluation Triggers**:
- Feature implementation complete
- All tests passing
- Quality gates met
- Ready for production

**Serena Memory**:
```python
write_memory("evaluation/[feature]/check", """
Results: [Metrics achieved]
Successes: [What worked]
Failures: [What didn't]
Learnings: [Key insights]
""")
```

**Example**: See `docs/pdca/phase-0-retrospective/check.md`

---

### Phase 4: Act (改善)

**Purpose**: Formalize successes and prevent mistakes

**Create**: `docs/pdca/[feature-name]/act.md`

**Contents**:
- **Success Pattern Formalization**: Create reusable patterns
- **Learnings → Global Rules**: Update CLAUDE.md
- **Checklist Updates**: Add validation steps
- **Next Actions**: Follow-up work needed

**Success Path**:
```
Feature succeeded →
  1. Create docs/patterns/[feature].md (清書)
  2. Update CLAUDE.md with best practices
  3. Add to quality checklists
  4. Write memory for reuse
```

**Failure Path**:
```
Feature failed →
  1. Create docs/mistakes/[feature]-YYYY-MM-DD.md
  2. Document root cause and prevention
  3. Update anti-patterns documentation
  4. Add validation to checklists
```

**Serena Memory**:
```python
# Success
write_memory("learning/patterns/[name]", reusable_pattern)

# Failure
write_memory("learning/mistakes/[timestamp]", failure_analysis)
```

**Example Template**: See `docs/pdca/_template/act.md`

---

## Serena Memory Schema

PDCA documentation integrates with Serena MCP for persistent memory.

### Memory Key Structure

**Pattern**: `[category]/[subcategory]/[identifier]`

```yaml
session/:
  session/context        # Complete PM state snapshot
  session/last           # Previous session summary
  session/checkpoint     # Progress snapshots (30-min intervals)

plan/:
  plan/[feature]/hypothesis     # Plan phase: 仮説・設計
  plan/[feature]/architecture   # Architecture decisions
  plan/[feature]/rationale      # Why this approach

execution/:
  execution/[feature]/do        # Do phase: 実験・試行錯誤
  execution/[feature]/errors    # Error log with timestamps
  execution/[feature]/solutions # Solution attempts log

evaluation/:
  evaluation/[feature]/check    # Check phase: 評価・分析
  evaluation/[feature]/metrics  # Quality metrics
  evaluation/[feature]/lessons  # What worked, what failed

learning/:
  learning/patterns/[name]      # Reusable success patterns
  learning/solutions/[error]    # Error solution database
  learning/mistakes/[timestamp] # Failure analysis

project/:
  project/context               # Project understanding
  project/architecture          # System architecture
  project/conventions           # Code style, naming patterns
```

### Session Lifecycle

**Session Start**:
```python
# Restore context
list_memories()
read_memory("session/context")
read_memory("plan/[current-feature]/hypothesis")
read_memory("execution/[current-feature]/do")
```

**During Work**:
```python
# Update continuously
write_memory("execution/[feature]/do", execution_log)

# Checkpoint every 30 minutes
write_memory("session/checkpoint", current_state)
```

**Session End**:
```python
# Save final state
write_memory("session/last", summary)
write_memory("session/context", complete_state)
```

---

## Integration with PM Agent

The PDCA system is deeply integrated with the PM Agent self-improvement workflow.

### Automatic Triggers

**PM Agent Auto-Activates PDCA for**:
1. Session start (restore context)
2. Feature implementation (create plan)
3. Error detection (root cause analysis)
4. Task completion (check evaluation)
5. Session end (save state)

### Self-Correcting Execution

**Core Principle**: Never retry without understanding WHY it failed

**Error Response Pattern**:
```yaml
1. Error Occurs:
   → STOP: Never re-execute same command
   → Question: "なぜこのエラーが出たのか？"

2. Root Cause Investigation (MANDATORY):
   - context7: Official documentation research
   - WebFetch: Community solutions (Stack Overflow, GitHub)
   - Grep: Codebase pattern analysis
   - Read: Related files inspection
   → Document: "原因は[X]。根拠: [Y]"

3. Hypothesis Formation:
   - State: "原因は[X]。解決策: [Z]"
   - Rationale: "なぜこの方法なら解決するか"

4. Solution Design (MUST BE DIFFERENT):
   - Previous Approach A failed → Design Approach B
   - NOT: Retry Approach A

5. Execute New Approach:
   - Implement based on root cause understanding
   - Measure: Did it fix the actual problem?

6. Learning Capture:
   - Success → write_memory("learning/solutions/[error_type]", solution)
   - Failure → Return to Step 2 with new hypothesis
```

### Warning Investigation Culture

**Rule**: All warnings and errors require investigation

```yaml
Warning Detected:
  1. NEVER dismiss as "probably not important"
  2. ALWAYS investigate:
     - context7: Official documentation
     - WebFetch: "What does this warning mean?"
     - Understanding: "Why is this being warned?"
  3. Categorize Impact:
     - Critical: Must fix immediately
     - Important: Fix before completion
     - Informational: Document why safe to ignore (with evidence)
  4. Document Decision:
     - If fixed: Why important + what learned
     - If ignored: Why safe + evidence + future implications
```

---

## Best Practices

### 1. Plan Early and Thoroughly

- Define hypothesis before coding
- Set quantitative targets
- Document risks upfront
- Estimate timeline realistically

### 2. Document During Work, Not After

- Update `do.md` continuously
- Log errors immediately
- Capture solutions as discovered
- Checkpoint every 30 minutes

### 3. Root Cause Analysis is Mandatory

- Never skip investigation
- Use multiple information sources
- Form evidence-based hypotheses
- Document reasoning clearly

### 4. Formalize Learnings

- Success → `docs/patterns/[name].md`
- Failure → `docs/mistakes/[name].md`
- Update `CLAUDE.md` with global patterns
- Write Serena memory for reuse

### 5. Quality Over Speed

- Better to understand than to rush
- Root cause prevents future errors
- Documentation saves time long-term
- Quality foundation enables speed

---

## Examples

### Phase 0 Retrospective

See `docs/pdca/phase-0-retrospective/check.md` for complete retrospective example:
- Timeline analysis
- Success factors
- Improvement areas
- Key learnings
- Metrics summary

### Phase 1.1 Implementation Plan

See `docs/pdca/phase-1.1-foundation/plan.md` for implementation planning example:
- Hypothesis and approach
- Expected outcomes
- Step-by-step plan
- Risk mitigation
- Acceptance criteria

---

## Quality Metrics

### PDCA Documentation Quality Indicators

**Completeness**:
- [ ] All four phases documented (Plan, Do, Check, Act)
- [ ] Quantitative metrics defined and measured
- [ ] Root cause analysis for all errors
- [ ] Learnings formalized (patterns or mistakes)

**Usefulness**:
- [ ] Reusable patterns identified
- [ ] Prevention checklists created
- [ ] Global rules updated in CLAUDE.md
- [ ] Serena memory updated

**Timeliness**:
- [ ] Plan created before implementation
- [ ] Do updated during execution (not after)
- [ ] Check completed immediately after feature
- [ ] Act executed within same phase

---

## Tools Integration

### Serena MCP

- **Memory Management**: Persistent storage across sessions
- **Context Restoration**: Resume work from previous session
- **Learning Database**: Searchable pattern and solution library

### Sequential MCP

- **Root Cause Analysis**: Structured problem investigation
- **Hypothesis Testing**: Systematic solution validation
- **Complex Reasoning**: Multi-step analysis for difficult issues

### Context7 MCP

- **Official Documentation**: Research for root cause analysis
- **Best Practices**: Industry-standard patterns and solutions
- **Version-Specific**: Correct information for dependencies

---

## Templates

All PDCA templates are located in `docs/pdca/_template/`:

- **plan.md**: Implementation planning template
- **do.md**: Execution log template
- **check.md**: Evaluation template
- **act.md**: Improvement actions template

**Usage**:
```bash
# Create new feature PDCA directory
mkdir -p docs/pdca/[feature-name]

# Copy templates
cp docs/pdca/_template/*.md docs/pdca/[feature-name]/

# Edit plan.md and begin implementation
```

---

## References

- **PDCA Methodology**: [Deming's PDCA Cycle](https://en.wikipedia.org/wiki/PDCA)
- **Root Cause Analysis**: [5 Whys Technique](https://en.wikipedia.org/wiki/Five_whys)
- **Learning Organizations**: Peter Senge's "The Fifth Discipline"
- **Continuous Improvement**: Kaizen philosophy

---

## Next Steps

1. **Review Templates**: Familiarize yourself with PDCA templates
2. **Start Phase 1.1**: Create `docs/pdca/phase-1.1-foundation/plan.md`
3. **Follow Workflow**: Execute full PDCA cycle for first implementation
4. **Build Habit**: Use PDCA for all significant features

---

**Document Status**: ✅ Complete
**Last Updated**: 2025-11-28
**Next Review**: Phase 1.1 completion
