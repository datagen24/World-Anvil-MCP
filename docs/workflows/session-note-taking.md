# Session Note-Taking Workflow

**Workflow ID**: WF-002  
**Category**: Campaign Management  
**Complexity**: High (real-time during play)  
**User Persona**: DM during active game session

---

## User Goal

Efficiently capture session notes, NPC interactions, plot developments, and player decisions during live D&D play without disrupting game flow.

---

## Trigger Phrases

- "Start session notes for tonight"
- "Log this encounter"
- "Note that the party met [NPC name]"
- "Record this plot development"
- "Add to session log"
- "The party just [action]"

---

## Prerequisites

- Active campaign in World Anvil
- Session Logs category exists
- DM has world context loaded

---

## Workflow Steps

### Step 1: Initialize Session Context
**User**: "Start session notes for Session 15 of Storm King's Thunder"

**Claude Actions**:
1. Load world context
2. Get recent session reports for continuity
3. Load active NPCs and locations
4. Prepare note-taking mode

**MCP Tools**:
- `get_world` - Load world context
- `list_articles` (filter: Session Report) - Get recent sessions
- `list_categories` - Verify structure

---

### Step 2: Quick Reference Loading
**Claude Actions**:
1. Cache frequently-accessed NPCs
2. Load current location details
3. Prepare quick-lookup for monsters/items

**MCP Tools**:
- `get_article` (multiple) - Preload key NPCs
- `search_articles` - Enable quick lookup

---

### Step 3: During-Session Note Capture
**User Examples**:
- "The party arrived at Goldenfields"
- "They met Naxene Drathkala, the wizard"
- "Combat with 3 Hill Giants"
- "Lifferlas the treant gave them a quest"

**Claude Actions**:
1. Parse key information (who, what, where)
2. Cross-reference with existing articles
3. Structure notes for later report
4. Flag new NPCs/locations for creation

**MCP Tools**:
- `search_articles` - Quick NPC/location lookup
- `get_article` - Retrieve details on mention

---

### Step 4: Session Summary Generation
**User**: "Wrap up session notes"

**Claude Actions**:
1. Compile all captured notes
2. Structure into session report format
3. List new entities encountered
4. Summarize key events and decisions
5. Note plot threads advanced

**Output Format**:
```markdown
# Session 15: Attack on Goldenfields

## Date
[Real date]

## In-Game Timeline
[Game calendar if tracked]

## Summary
[2-3 paragraph overview]

## Key Events
- Event 1
- Event 2

## NPCs Encountered
- Naxene Drathkala (existing article)
- Lifferlas (NEW - needs article)

## Locations Visited
- Goldenfields

## Combat Encounters
- 3 Hill Giants at the east gate

## Loot/Rewards
- [Items gained]

## Plot Threads
- Advanced: Giant attacks investigation
- New: Treant's request

## Player Decisions
- [Key choices made]

## Next Session Hooks
- [Setup for next session]
```

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `get_world` | Read | 1 | Core |
| `list_articles` | Read | 1 | Core |
| `get_article` | Read | 1 | Core |
| `search_articles` | Read | 2 | High |
| `create_article` | Write | Future | Critical |

---

## Real-Time Interaction Pattern

```
[Session in progress]

User: The party just met an elf named Silvanus at the Goldenfields temple

Claude: [Quick search for "Silvanus" and "Goldenfields"]

📝 Noted: Party met Silvanus (elf) at Goldenfields temple

I found an existing article for Goldenfields. Silvanus doesn't appear 
in your world yet - want me to flag them for article creation later?

Quick stats I can see for Goldenfields:
- Population: ~5,000
- Type: Farming settlement  
- Key NPCs: Naxene Drathkala, Lifferlas

User: Yes flag Silvanus. He's a priest of Chauntea

Claude: ✓ Flagged: Silvanus (elf priest of Chauntea, met at Goldenfields temple)

Continuing session...

User: Combat! 2 ogres attacking the north gate

Claude: 📝 Combat logged: 2 Ogres at Goldenfields north gate
       Need the outcome when combat ends.

[Later]

User: Party killed them both. Took 15 damage total, used 2 healing potions

Claude: ✓ Combat resolved: 2 Ogres defeated
  - Party damage: 15 HP total
  - Resources used: 2 healing potions
```

---

## Post-Session Processing

After the session, Claude can:
1. Generate formatted Session Report article content
2. List new NPCs/locations that need articles
3. Update plot thread tracking
4. Prepare "Previously on..." summary for next session

---

## Expected Outcome

- Comprehensive session notes without disrupting play
- Cross-referenced with existing world content
- Structured for easy session report creation
- New content flagged for later development

---

## Error Scenarios

| Error | Cause | Resolution |
|-------|-------|------------|
| NPC not found | New character | Flag for creation, note details |
| Slow response | API latency | Pre-cache common lookups |
| Name ambiguity | Multiple matches | Ask for clarification |

---

## Optimization Tips

1. **Pre-load** expected NPCs/locations before session
2. **Use abbreviations** for speed (DM can say "NG" for north gate)
3. **Batch lookups** when possible
4. **Cache** frequently referenced articles
5. **Async processing** - don't block game flow

---

## Related Workflows

- [WF-001: D&D Campaign Setup](d-and-d-campaign-setup.md)
- [WF-003: NPC Generation](npc-generation.md)
- [WF-004: Location Development](location-development.md)
