# ADR-002: License Compatibility Analysis

**Status**: Analysis
**Date**: 2025-11-28
**Context**: Phase 0 - Legal/Licensing Decision

---

## Context

We need to determine license compatibility between:
- **pywaclient**: Apache 2.0 License
- **Our Project**: BSD 4-Clause License (user specified)

This affects whether we can:
1. Use pywaclient as a dependency
2. Reference pywaclient code
3. Need to change our license

---

## License Overview

### Apache 2.0 License (pywaclient)

**Key Characteristics**:
- ✅ Permissive (allows commercial use, modification, distribution)
- ✅ Requires preservation of copyright notices
- ✅ Requires statement of changes made
- ✅ **Grants explicit patent rights**
- ✅ Compatible with most other licenses
- ✅ Can be combined with proprietary code

**Requirements**:
- Include copy of Apache 2.0 license
- Preserve copyright notices
- State significant changes
- Include NOTICE file (if present)

### BSD 4-Clause License (Original BSD)

**Key Characteristics**:
- ✅ Permissive (allows commercial use, modification, distribution)
- ✅ Requires preservation of copyright notice
- ⚠️ **Contains "advertising clause" (problematic)**
- ❌ No explicit patent grant
- ⚠️ Less commonly used today (most projects use BSD 3-Clause)

**The 4 Clauses**:
1. Source distribution must retain copyright notice
2. Binary distribution must retain copyright notice
3. **Advertising clause**: All advertising must acknowledge use
4. No endorsement without permission

**The Problem with BSD 4-Clause**:
- Clause 3 (advertising) is considered onerous
- Creates compliance burden for downstream users
- **Incompatible with GPL** due to advertising clause
- Most projects have moved to BSD 3-Clause or BSD 2-Clause

---

## Compatibility Analysis

### Scenario 1: Use pywaclient as Dependency

**Approach**: Install pywaclient via pip, use as library

**Compatibility**: ✅ **COMPATIBLE**

**Legal Analysis**:
- Apache 2.0 → BSD 4-Clause: **Compatible**
- We can use Apache 2.0 licensed dependencies in BSD 4-Clause projects
- pywaclient remains Apache 2.0 (their license)
- Our code remains BSD 4-Clause (our license)

**Requirements**:
```
world-anvil-mcp/
├── LICENSE (BSD 4-Clause - our code)
├── THIRD_PARTY_LICENSES/
│   └── pywaclient-LICENSE (Apache 2.0 - their code)
└── NOTICE (acknowledgments)
```

**NOTICE file example**:
```
This software includes the following third-party components:

pywaclient (https://gitlab.com/SoulLink/world-anvil-api-client)
Copyright (c) [Year] [Author]
Licensed under Apache License 2.0
See THIRD_PARTY_LICENSES/pywaclient-LICENSE for full license text
```

**Verdict**: ✅ **Legally sound, no issues**

---

### Scenario 2: Build Custom Client (Reference Only)

**Approach**: Study pywaclient code, write our own implementation

**Compatibility**: ✅ **NO LICENSE CONCERNS**

**Legal Analysis**:
- Not using their code directly
- Learning from public API implementation
- Clean room implementation
- 100% our own code
- No license obligations to pywaclient

**Requirements**:
- None (not using their code)
- Can optionally acknowledge in README: "Inspired by pywaclient"
- Our code: 100% BSD 4-Clause

**Verdict**: ✅ **Cleanest approach, no license concerns**

---

### Scenario 3: Copy/Modify pywaclient Code

**Approach**: Fork or copy portions of pywaclient code

**Compatibility**: ⚠️ **COMPATIBLE WITH CONDITIONS**

**Legal Analysis**:
- Apache 2.0 allows modification and redistribution
- **MUST preserve Apache 2.0 license for their code**
- **MUST state changes made**
- **MUST include NOTICE file if present**
- Can't relicense their code as BSD 4-Clause

**Requirements**:
```python
# src/world_anvil_mcp/api/client.py
"""
Portions of this code derived from pywaclient:
https://gitlab.com/SoulLink/world-anvil-api-client

Copyright (c) [Year] [Author]
Licensed under Apache License 2.0

Modifications made:
- Added MCP Context integration
- Implemented granularity-aware caching
- Custom retry logic
"""
```

**File Structure**:
```
world-anvil-mcp/
├── LICENSE (BSD 4-Clause - our new code)
├── src/world_anvil_mcp/
│   └── api/
│       ├── client.py (Apache 2.0 - derived from pywaclient)
│       └── models.py (BSD 4-Clause - our code)
└── LICENSES/
    ├── BSD-4-Clause.txt (our license)
    └── Apache-2.0.txt (for derived code)
```

**Verdict**: ⚠️ **More complex, dual licensing required**

---

## BSD 4-Clause Concerns

### The Advertising Clause Problem

**BSD 4-Clause Clause 3**:
> "All advertising materials mentioning features or use of this software must display the following acknowledgement: This product includes software developed by [organization]."

**Issues**:
1. **Compliance Burden**: Downstream users must track and acknowledge in all advertising
2. **GPL Incompatibility**: Cannot combine with GPL code
3. **Scalability**: If 100 dependencies have this clause, need 100 acknowledgments
4. **Modern Practice**: Most projects abandoned this clause

**Historical Note**:
- UC Berkeley (original BSD license creator) **rescinded this clause in 1999**
- Recommended projects move to BSD 3-Clause
- BSD 4-Clause is now considered deprecated

### Recommendation: Use BSD 3-Clause Instead

**BSD 3-Clause License** (Modified BSD):
- ✅ All benefits of BSD 4-Clause
- ✅ **No advertising clause**
- ✅ More compatible with other licenses
- ✅ **GPL compatible**
- ✅ Industry standard for permissive licensing

**Changes from BSD 4-Clause**:
- Remove Clause 3 (advertising clause)
- Keep Clauses 1, 2, 4 (same protections)

**Benefits**:
- Broader ecosystem compatibility
- Easier for downstream users
- No compliance burden
- GPL compatibility if ever needed

---

## Decision Matrix

| Approach | License Compatibility | Complexity | Recommendation |
|----------|----------------------|------------|----------------|
| **Dependency (pywaclient)** | ✅ Compatible | Low | ✅ **OK if using pywaclient** |
| **Custom Client (reference)** | ✅ No concerns | Low | ✅ **Best - cleanest** |
| **Copy/Modify code** | ⚠️ Dual licensing | High | ⚠️ Avoid unless necessary |

| Our License | Apache 2.0 Compat | GPL Compat | Modern Practice | Recommendation |
|-------------|-------------------|------------|-----------------|----------------|
| **BSD 4-Clause** | ✅ Yes | ❌ No | ❌ Deprecated | ⚠️ Consider changing |
| **BSD 3-Clause** | ✅ Yes | ✅ Yes | ✅ Standard | ✅ **Recommended** |
| **BSD 2-Clause** | ✅ Yes | ✅ Yes | ✅ Standard | ✅ Also good |
| **MIT** | ✅ Yes | ✅ Yes | ✅ Standard | ✅ Also good |

---

## Recommendations

### Immediate Recommendations

#### 1. License Choice (Critical)

**Recommendation**: **Switch to BSD 3-Clause License**

**Rationale**:
- BSD 4-Clause advertising clause is problematic
- UC Berkeley rescinded it in 1999
- Modern standard is BSD 3-Clause
- Better ecosystem compatibility
- GPL compatible if ever needed

**Action**:
```bash
# Update LICENSE file to BSD 3-Clause
# Remove advertising clause (Clause 3)
# Maintain same permissive spirit
```

**BSD 3-Clause Template**:
```
Copyright (c) [Year], [Your Name]
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES...
```

#### 2. pywaclient Usage Strategy

**If Using as Dependency** (Option 1):
- ✅ Apache 2.0 compatible with BSD 3-Clause
- Create `THIRD_PARTY_LICENSES/` directory
- Include Apache 2.0 license text
- Add NOTICE file with acknowledgments

**If Building Custom Client** (Option 2 - Recommended):
- ✅ No license concerns
- Clean room implementation
- 100% BSD 3-Clause
- Optional: Acknowledge in README

**If Copying Code** (Option 3 - Not Recommended):
- Complex dual licensing
- Must preserve Apache 2.0 for derived code
- Must state changes
- Avoid unless absolutely necessary

---

## Implementation Guidance

### If Using pywaclient as Dependency

**File Structure**:
```
world-anvil-mcp/
├── LICENSE                           # BSD 3-Clause (our code)
├── THIRD_PARTY_LICENSES/
│   └── pywaclient.txt               # Apache 2.0 (their license)
├── NOTICE                           # Acknowledgments
└── pyproject.toml                   # Dependency declaration
```

**pyproject.toml**:
```toml
[project]
name = "world-anvil-mcp"
license = {text = "BSD-3-Clause"}
dependencies = [
    "pywaclient>=0.1.0",  # Apache 2.0
    # ... other deps
]
```

**NOTICE file**:
```
World Anvil MCP Server
Copyright (c) 2025, [Your Name]

This software includes the following third-party components:

1. pywaclient
   Copyright (c) [Year] [Author]
   Licensed under Apache License 2.0
   https://gitlab.com/SoulLink/world-anvil-api-client
   See THIRD_PARTY_LICENSES/pywaclient.txt for full license text
```

### If Building Custom Client

**File Structure**:
```
world-anvil-mcp/
├── LICENSE                           # BSD 3-Clause (all our code)
├── README.md                         # Optional acknowledgment
└── src/world_anvil_mcp/
    └── api/
        └── client.py                 # 100% our code, BSD 3-Clause
```

**README.md acknowledgment** (optional):
```markdown
## Acknowledgments

This project was inspired by [pywaclient](https://gitlab.com/SoulLink/world-anvil-api-client),
a World Anvil API client for Python. While we implemented our own client optimized for
MCP integration, we acknowledge their pioneering work on the World Anvil API.
```

---

## Legal Compliance Checklist

### If Using pywaclient Dependency

- [ ] Create `THIRD_PARTY_LICENSES/` directory
- [ ] Copy Apache 2.0 license text to `THIRD_PARTY_LICENSES/pywaclient.txt`
- [ ] Create NOTICE file with acknowledgment
- [ ] Verify pywaclient has no NOTICE file (if it does, include it)
- [ ] Document in README that we use Apache 2.0 licensed dependencies
- [ ] Update pyproject.toml with correct license metadata

### If Building Custom Client

- [ ] Confirm we're not copying any pywaclient code directly
- [ ] Document that implementation is original
- [ ] Optional: Add acknowledgment in README
- [ ] Single LICENSE file (BSD 3-Clause) is sufficient

### General

- [ ] **Switch to BSD 3-Clause** (remove advertising clause)
- [ ] Update LICENSE file
- [ ] Update pyproject.toml license metadata
- [ ] Add copyright headers to source files
- [ ] Document license choice in README

---

## Conclusion

### Answer to Your Question

**Q: Is there incompatibility between Apache 2.0 (pywaclient) and BSD 4-Clause (our project)?**

**A**: ✅ **No incompatibility for dependency use**

- Apache 2.0 dependency in BSD 4-Clause project: **Compatible**
- Just need to include their license and acknowledgments
- Our code stays BSD 4-Clause, theirs stays Apache 2.0

**However**:
- ⚠️ **BSD 4-Clause itself is problematic** (advertising clause)
- 🎯 **Recommend switching to BSD 3-Clause**
- ✅ **Apache 2.0 also compatible with BSD 3-Clause**

### Final Recommendation

**Option A: Custom Client (Best)**
1. ✅ Build custom client using pywaclient as reference only
2. ✅ No license concerns
3. ✅ Switch to BSD 3-Clause license
4. ✅ Single clean license for all our code

**Option B: Use pywaclient Dependency**
1. ✅ Use pywaclient as dependency
2. ✅ Include Apache 2.0 license in THIRD_PARTY_LICENSES/
3. ✅ Create NOTICE file
4. ✅ Switch to BSD 3-Clause for our code
5. ✅ Dual licensing (BSD 3-Clause + Apache 2.0 dependency)

**Both options are legally sound. Option A is cleaner.**

---

## Next Steps

1. **User Decision**:
   - Confirm: Switch to BSD 3-Clause? (Recommended)
   - Or: Keep BSD 4-Clause? (Not recommended but legal)

2. **pywaclient Strategy**:
   - Custom client (no license concerns)
   - Or dependency (need license files)

3. **Implementation**:
   - Update LICENSE file
   - Create necessary compliance files
   - Proceed with Phase 0

---

**Status**: ✅ **APPROVED**
**Date**: 2025-11-28

**Decisions Made**:
1. **License**: BSD 3-Clause (modern standard, no advertising clause)
2. **pywaclient**: Custom client with pywaclient as reference only
3. **Result**: Single clean BSD 3-Clause license, no dependency compliance needed
