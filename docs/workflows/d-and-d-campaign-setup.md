# D&D Campaign Setup Workflow

**Workflow ID**: WF-001  
**Category**: Campaign Management  
**Complexity**: Medium  
**User Persona**: Dungeon Master starting a new campaign

---

## User Goal

Set up a new D&D campaign in World Anvil with proper structure, categories, and initial organization ready for content creation and session play.

---

## Trigger Phrases

- "Set up a new D&D campaign"
- "Create a campaign for [campaign name]"
- "Initialize my World Anvil for D&D"
- "Prepare a new campaign world"
- "Start a fresh D&D 5e campaign"

---

## Prerequisites

- User has World Anvil account with API access
- User has at least one World created
- Valid API credentials configured

---

## Workflow Steps

### Step 1: Identify or Create World
**User**: "Set up a new D&D 5e campaign called 'Storm King's Thunder' in my Forgotten Realms world"

**Claude Actions**:
1. Call `list_worlds()` to get available worlds
2. Match world by name or prompt user to select
3. If no world exists, inform user (world creation may require manual step)

**MCP Tool**: `list_worlds`  
**Expected Output**: List of worlds with IDs

---

### Step 2: Configure RPG System
**Claude Actions**:
1. Verify/link RPG system to the campaign
2. Note: Campaign is auto-created with world

**MCP Tool**: `get_world` (to verify RPG system setting)  
**Note**: RPG system linking may require manual configuration or future write API

---

### Step 3: Create Category Structure
**Claude Actions**:
1. Create "Characters" category for NPCs and PCs
2. Create "Locations" category for places
3. Create "Organizations" category for factions
4. Create "Session Logs" category for session reports
5. Create "Items" category for magic items/equipment
6. Create "Lore" category for world background

**MCP Tools**: 
- `create_category` (×6) - *Requires write API*
- OR `list_categories` to verify existing structure

**Alternative (Read-Only)**:
- `list_categories` to show existing categories
- Recommend manual creation with specific names

---

### Step 4: Verify Campaign Setup
**Claude Actions**:
1. Get world details to confirm configuration
2. List existing categories
3. Summarize setup status

**MCP Tools**:
- `get_world`
- `list_categories`

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `list_worlds` | Read | 1 | Core |
| `get_world` | Read | 1 | Core |
| `list_categories` | Read | 1 | Core |
| `create_category` | Write | Future | High |
| `link_rpg_system` | Write | Future | Medium |

---

## Example Conversation

```
User: Set up a new D&D 5e campaign called "Storm King's Thunder"

Claude: I'll help you set up your D&D campaign. Let me check your available worlds.

[Calls list_worlds]

I found 3 worlds in your account:
1. Forgotten Realms (ID: abc123)
2. Homebrew Setting (ID: def456)  
3. Test World (ID: ghi789)

Which world should "Storm King's Thunder" be in?

User: Forgotten Realms

Claude: Great! Let me check the current setup of your Forgotten Realms world.

[Calls get_world, list_categories]

Your Forgotten Realms world is configured for D&D 5e and has the following categories:
- Characters (12 articles)
- Locations (8 articles)

For a well-organized campaign, I recommend creating these additional categories:
- Session Logs (for session reports)
- Items (for magic items and equipment)
- Organizations (for factions like the Zhentarim, Lords' Alliance)
- Quests (for plot threads)

Would you like me to guide you through creating these categories in World Anvil?
```

---

## Expected Outcome

- User has clear understanding of their world structure
- Campaign organization is optimized for D&D play
- Categories are set up for efficient content creation
- User knows next steps for adding content

---

## Error Scenarios

| Error | Cause | Resolution |
|-------|-------|------------|
| No worlds found | New account | Guide user to create world in UI first |
| Authentication failed | Invalid credentials | Prompt to check API settings |
| World not D&D system | Wrong RPG config | Note for manual system change |

---

## Related Workflows

- [WF-002: Session Note-Taking](session-note-taking.md)
- [WF-003: NPC Generation](npc-generation.md)
- [WF-005: Quick NPC Lookup](quick-npc-lookup.md)
