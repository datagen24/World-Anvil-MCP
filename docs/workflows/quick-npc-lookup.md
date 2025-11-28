# Quick NPC Lookup Workflow

**Workflow ID**: WF-005  
**Category**: Session Support  
**Complexity**: Low  
**User Persona**: DM during active session needing quick reference

---

## User Goal

Instantly retrieve NPC information during live play without disrupting game flow.

---

## Trigger Phrases

- "Who is [NPC name]?"
- "What do I know about [NPC]?"
- "Quick info on [character]"
- "Remind me about [NPC]"
- "Pull up [NPC name]"
- "[NPC name] stats"

---

## Prerequisites

- NPCs exist in World Anvil as articles or campaign NPCs
- World context loaded

---

## Workflow Steps

### Step 1: Parse NPC Query
**User**: "Who is Sildar Hallwinter?"

**Claude Actions**:
1. Extract NPC name
2. Search articles for match
3. Search campaign NPCs if no article match
4. Handle ambiguous names

**MCP Tools**:
- `search_articles` (quick, name-based)
- `get_article` (if found)

---

### Step 2: Return Quick Reference
**Claude Output Format** (optimized for speed):

```
📋 SILDAR HALLWINTER

Race: Human | Age: 50s | Role: Lords' Alliance Agent

APPEARANCE: Weathered soldier, gray streaked hair, practical armor

PERSONALITY: Honorable, determined, believes in civilization

VOICE: Firm, military cadence, addresses people formally

CURRENT STATUS: [From session notes/last known]

QUICK FACTS:
• Looking for Iarno Albrek (missing ally)
• Will pay 50gp to escort to Phandalin
• Knows about Wave Echo Cave rumors

SECRETS (DM): [If any recorded]
```

---

### Step 3: Offer Expansion
If time permits, offer:
- Full article details
- Related NPCs
- Recent interactions logged

---

## Response Time Target

- **Ideal**: < 2 seconds
- **Acceptable**: < 5 seconds
- **Strategy**: Pre-cache session-relevant NPCs

---

## Quick Reference Templates

### For Combat-Ready NPC
```
⚔️ [NAME] - [CR/Level]
HP: [X] | AC: [Y] | Speed: [Z]
Attacks: [Primary attack +X, damage]
Special: [Key ability]
Location: [Where they are]
```

### For Social NPC
```
🗣️ [NAME] - [Role]
Attitude: [Friendly/Neutral/Hostile]
Wants: [Current goal]
Knows: [Key information]
Voice: [Speech pattern hint]
```

### For Mystery/Investigation
```
🔍 [NAME]
Alibi: [Where they claim to be]
Motive: [Potential reasons]
Evidence: [Clues pointing to/away]
Truth: [DM knowledge]
```

---

## Handling Not Found

```
User: Who is Bartok the Magnificent?

Claude: No "Bartok the Magnificent" in your world yet.

Options:
1. Quick create: Tell me about them and I'll note for later
2. Search broader: Should I check for similar names?
3. Improvise: Need me to generate a quick NPC?
```

---

## Example Conversation

```
[Mid-session]

User: Who is Halia Thornton again?

Claude: 
📋 HALIA THORNTON

Race: Human | Role: Phandalin Miner's Exchange Guildmaster

PERSONALITY: Ambitious, calculating, charming facade

VOICE: Smooth, always measuring value of conversation

⚠️ SECRET: Zhentarim agent seeking to control Phandalin

LAST SESSION: Party sold gems to her, she offered 
"special work" (Zhentarim recruitment attempt)

---

User: What was the special work?

Claude: She offered 100gp to "deal with" the Redbrands 
leadership - eliminating competition while looking helpful.
Party hasn't responded yet.
```

---

## Optimization Strategies

1. **Session Pre-load**
   - Before session, cache NPCs likely to appear
   - Load all NPCs in current location

2. **Smart Search**
   - Partial name matching
   - Alias/nickname support
   - Role-based fallback ("the blacksmith")

3. **Context Awareness**
   - Prioritize NPCs in current location
   - Recent session NPCs ranked higher
   - Campaign NPCs over world articles

4. **Progressive Detail**
   - Quick summary first
   - Offer expansion on request
   - Don't overload DM mid-scene

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `search_articles` | Read | 2 | Critical |
| `get_article` | Read | 1 | Core |
| `list_campaign_npcs` | Read | 3 | High |
| `get_campaign_npc` | Read | 3 | High |

---

## Expected Outcome

- Instant NPC recall during play
- Just enough info to roleplay effectively
- No game disruption
- Easy expansion if needed

---

## Related Workflows

- [WF-002: Session Note-Taking](session-note-taking.md)
- [WF-003: NPC Generation](npc-generation.md)
- [WF-010: Content Search](content-search.md)
