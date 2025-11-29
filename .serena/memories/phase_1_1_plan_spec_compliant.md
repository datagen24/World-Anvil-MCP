# Phase 1.1 Plan - Spec-Compliant Integration

**Status**: Spec-compliant with MCP-ECOSYSTEM-SPEC.md
**Date**: 2025-11-29
**Revision**: Updated ecosystem detection to match formal specifications

## Integration Summary

Combined three sources:
1. Structural improvements from user feedback
2. Detailed code implementations and examples
3. **Spec-compliant MCP ecosystem detection**

## Latest Revision Highlights

### Ecosystem Detection (Spec-Compliant)

**Updated to match** `docs/specs/MCP-ECOSYSTEM-SPEC.md`:

1. **IntegrationTier Enum**:
   - CRITICAL (Tier 1): Foundry VTT, Context Engine
   - RECOMMENDED (Tier 2): Dropbox, Notion
   - OPTIONAL (Tier 3): Discord, Calendar

2. **Enhanced CompanionMCP Dataclass**:
   - `tier: IntegrationTier` (priority level)
   - `can_read`, `can_write`, `bidirectional` (capabilities)
   - `workflow_suggestions: dict[str, str]` (context-aware hints)
   - `documentation_url` (installation links)

3. **EcosystemDetector Enhancements**:
   - `critical_companions` property (Tier 1 only)
   - `get_ecosystem_status()` method (markdown report)
   - `suggest_for_workflow()` returns tuple with companion object
   - Tier-based sorting (critical first)

4. **Context Engine Clarification**:
   - **SEPARATE MCP server project** (NOT part of World Anvil MCP)
   - Provides semantic search over TTRPG reference materials
   - Phase 1.1 implements DETECTION ONLY
   - Full specification: `docs/specs/CONTEXT-ENGINE-SPEC.md`
   - Implementation: Future phase (TBD)

## Timeline

**7-8 days** (realistic for foundation work)

- **Day 1**: CI/CD + client foundation + cache (MANDATORY)
- **Day 2**: Exceptions + **spec-compliant ecosystem detection** + models
- **Days 3-4**: User & World endpoints + live validation
- **Days 5-6**: Testing + write API validation
- **Days 7-8**: Documentation + retrospective

## Quality Gates

- CI/CD operational from Day 1
- ≥90% test coverage
- 100% type coverage (mypy strict)
- Ecosystem detection for 6 companions (3 tiers)
- Write API capabilities documented
- Zero technical debt

## Key Risk Mitigations

- Day 1: CI catches issues immediately
- Day 3: Auth connectivity test before heavy implementation
- Day 6: Write API spike before Phase 2 commitment
- Spec alignment: Prevents future ecosystem refactoring

## References

- **MCP Ecosystem Spec**: `docs/specs/MCP-ECOSYSTEM-SPEC.md`
- **Context Engine Spec**: `docs/specs/CONTEXT-ENGINE-SPEC.md` (separate project)
- **Phase 1.1 Plan**: `docs/pdca/phase-1.1-foundation/plan.md`

## Next Steps

1. User approval of spec-compliant plan
2. Create execution log: `docs/pdca/phase-1.1-foundation/do.md`
3. Begin Day 1 implementation
4. Continuous PDCA documentation during execution

**CRITICAL**: Context Engine is separate project - Phase 1.1 detects it, doesn't implement it.
