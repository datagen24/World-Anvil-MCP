# Quest / Plot Management Workflow

**Workflow ID**: WF-008  
**Category**: Campaign Management  
**Complexity**: Medium  
**User Persona**: DM tracking campaign storylines

---

## User Goal

Track active quests, plot threads, story arcs, and their interconnections to maintain narrative coherence across sessions.

---

## Trigger Phrases

- "What quests are active?"
- "Track this plot thread"
- "Update quest [name]"
- "What plots connect to [element]?"
- "The party completed [quest]"
- "Create a quest for [objective]"
- "What's the main storyline status?"

---

## Prerequisites

- Campaign with plot/quest tracking setup
- Understanding of World Anvil Plot template

---

## Workflow Steps

### Step 1: Load Quest/Plot Context
**User**: "What active quests does the party have?"

**Claude Actions**:
1. Load campaign context
2. Get articles with Plot template
3. Filter by status (active/complete/abandoned)
4. Organize by type (main/side/personal)

**MCP Tools**:
- `list_articles` (filter: Plot template)
- `get_article` - Load quest details
- `search_articles` - Find connected content

---

### Step 2: Present Quest Overview
**Claude Output**:
```
📜 ACTIVE QUESTS - Storm King's Thunder Campaign

MAIN QUESTLINE:
━━━━━━━━━━━━━━━
🔷 Stop the Giant Threat [In Progress]
   Status: Investigating giant attacks
   Current Lead: Fire giant symbol found at attack sites
   Next Step: Travel to investigate giant activity
   Sessions Active: 12-present

MAJOR SIDE QUESTS:
━━━━━━━━━━━━━━━━━━
🔶 Find Wave Echo Cave [On Hold]
   Status: Location discovered, not explored
   Blocker: Party chose to pursue giant threat first
   Reward: 10% of mine profits

🔶 Rescue Gundren Rockseeker [Completed ✓]
   Completed: Session 8
   Outcome: Gundren alive, revealed cave location

MINOR QUESTS:
━━━━━━━━━━━━━
◇ Return Mirna's Heirloom [Active]
  Location: Thundertree herbalist shop
  Reward: Emerald necklace location

◇ Investigate Hamun Kost [Abandoned]
  Reason: Necromancer fled before confrontation

PERSONAL QUESTS:
━━━━━━━━━━━━━━━
👤 Theren (PC): Find missing brother
   Last Progress: Session 10 - clue in Triboar
   
👤 Mira (PC): Clear family name  
   Last Progress: Session 7 - evidence found
```

---

### Step 3: Quest Detail View
**User**: "Tell me about the giant threat quest"

**Claude Output**:
```
🔷 QUEST: Stop the Giant Threat

STATUS: In Progress (Main Questline)
STARTED: Session 12
PATRON: Lords' Alliance / Sildar Hallwinter

OBJECTIVE:
Investigate and stop the coordinated giant attacks 
threatening the North.

PROGRESS LOG:
━━━━━━━━━━━━━
Session 12: Learned of giant attacks from Triboar
Session 13: Found fire giant symbol at attack site
Session 14: Spoke with refugees, heading north
Session 15: [Current] Investigating Goldenfields attack

KNOWN INFORMATION:
• Giants attacking settlements (unusual coordination)
• Fire giant symbols found (war markings?)
• Refugees report multiple giant types working together
• Something has disrupted the "Ordning" (giant hierarchy)

CONNECTED ELEMENTS:
• NPCs: Sildar Hallwinter, Harshnag (rumored)
• Locations: Triboar, Goldenfields, Eye of the All-Father
• Factions: Lords' Alliance, Zhentarim (also investigating)

POTENTIAL COMPLICATIONS:
• Zhentarim may try to profit from crisis
• Giants have internal conflicts
• Ancient dragon involvement rumored

REWARD: Fame, Alliance favor, payment negotiable
```

---

### Step 4: Update Quest Status
**User**: "The party found the entrance to Wave Echo Cave"

**Claude Actions**:
1. Load quest details
2. Update progress
3. Note session and details
4. Identify newly unlocked content

**Output**:
```
✓ QUEST UPDATED: Find Wave Echo Cave

Previous Status: Location discovered, not explored
New Status: Entrance located

Added to Progress Log:
"Session 15: Party located cave entrance via [method]"

UNLOCKED:
• Wave Echo Cave can now be explored
• Connects to: Gundren's gratitude, Forge of Spells mystery

Note: This is a significant dungeon. Shall I prep encounter 
information for next session?
```

---

### Step 5: Quest Creation
**User**: "Create a quest to recover a stolen artifact"

**Claude Actions**:
1. Gather quest parameters
2. Generate quest framework
3. Connect to existing world elements
4. Create article content

**Output Format**:
```markdown
# The Stolen Relic of [Name]

## Type
Side Quest / Dungeon Delve

## Synopsis
[Brief hook description]

## Quest Giver
[NPC link]

## Objective
[Clear goal]

## Background
[Why this matters]

## Stages
1. **Discovery**: [How party learns of quest]
2. **Investigation**: [Finding the thief/location]
3. **Confrontation**: [Main challenge]
4. **Resolution**: [Returning item/reward]

## Key Locations
- [Location 1]: [Purpose]
- [Location 2]: [Purpose]

## Key NPCs
- [NPC 1]: [Role]
- [NPC 2]: [Role]

## Encounters
- [Encounter type and difficulty]

## Rewards
- [XP, gold, items, reputation]

## Complications
- [Twist 1]
- [Twist 2]

## Connections
Links to: [Other plots, NPCs, locations]

## DM Notes
[Additional guidance]
```

---

## Quest Status Types

| Status | Meaning | Display |
|--------|---------|---------|
| Available | Quest can be discovered | 🔘 |
| Active | Party is pursuing | 🔷 |
| On Hold | Temporarily set aside | 🔶 |
| Completed | Successfully finished | ✅ |
| Failed | Objective no longer possible | ❌ |
| Abandoned | Party chose not to pursue | ⬜ |

---

## Plot Thread Tracking

For ongoing narratives (not discrete quests):

```
📊 PLOT THREADS

THREAD: The Shattered Ordning
Type: Campaign Background
Status: Developing
Visibility: Partially revealed to players

Events:
• Giant hierarchy disrupted (cause unknown)
• Each giant type pursuing own agenda
• Ancient conflict resurging

Foreshadowing Placed:
✓ Giants not cooperating (Session 12)
✓ Fire giants seeking weapons (Session 14)
◇ Storm giant king missing (not yet revealed)
◇ Dragon involvement (not yet revealed)

Party Understanding: 40%
(They know giants are disorganized but not why)
```

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `list_articles` | Read | 1 | Core |
| `get_article` | Read | 1 | Core |
| `search_articles` | Read | 2 | High |
| `create_article` | Write | Future | High |
| `update_article` | Write | Future | High |

---

## Expected Outcome

- Clear view of campaign quest status
- Easy progress tracking
- Connected story elements visible
- Historical log of developments
- New quest creation support

---

## Related Workflows

- [WF-002: Session Note-Taking](session-note-taking.md)
- [WF-009: Session Prep](session-prep.md)
- [WF-003: NPC Generation](npc-generation.md)
