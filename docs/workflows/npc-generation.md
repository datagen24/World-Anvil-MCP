# NPC Generation Workflow

**Workflow ID**: WF-003  
**Category**: Content Creation  
**Complexity**: Medium  
**User Persona**: DM preparing NPCs for campaign

---

## User Goal

Create well-developed NPCs with consistent details, motivations, and connections to the world, stored in World Anvil for easy reference during play.

---

## Trigger Phrases

- "Create an NPC"
- "I need a [role] NPC"
- "Generate a character for [purpose]"
- "Make a shopkeeper/guard/noble/etc"
- "Create [Name] as an NPC"
- "Build out this NPC: [description]"

---

## Prerequisites

- Active world in World Anvil
- Characters category exists
- Understanding of campaign context

---

## Workflow Steps

### Step 1: Gather NPC Requirements
**User**: "I need a blacksmith NPC for Waterdeep"

**Claude Actions**:
1. Identify role/profession
2. Identify location context
3. Check for existing related content
4. Ask clarifying questions if needed

**MCP Tools**:
- `search_articles` - Check for existing Waterdeep content
- `get_article` - Load location details for context

---

### Step 2: Generate NPC Concept
**Claude Actions**:
1. Generate name appropriate to setting/culture
2. Determine species/ancestry
3. Create core personality traits
4. Establish motivation/goals
5. Define relationship to location

**Information Gathered**:
- Name
- Species/Race
- Gender
- Age
- Appearance (brief)
- Personality (2-3 traits)
- Motivation
- Role in community
- Potential plot hooks

---

### Step 3: World Integration
**Claude Actions**:
1. Link to existing organizations
2. Connect to known NPCs (relationships)
3. Tie to campaign themes
4. Add local knowledge/secrets

**MCP Tools**:
- `list_articles` (Organizations) - Find faction connections
- `search_articles` - Find related characters
- `get_article` - Load connected content

---

### Step 4: Generate Character Article Content
**Claude Output Format**:
```markdown
# [NPC Name]

## Overview
[Vignette - 2-3 sentences capturing essence]

## Appearance
[Physical description]

## Personality
[Key traits, mannerisms, speech patterns]

## Background
[Brief history relevant to current role]

## Motivations
[Goals, fears, desires]

## Connections
- **Organization**: [Faction membership]
- **Location**: [Where found]
- **Relationships**: [Key NPCs they know]

## Role in Story
[Potential uses for DM]

## Secrets
[Hidden information - DM only]

## Stat Block
[If combat-relevant, D&D 5e stats or reference]
```

---

### Step 5: Campaign Integration (Optional)
**User**: "Also add them to my campaign as an NPC"

**Claude Actions**:
1. Create campaign NPC entry
2. Link to character article
3. Add to Digital Storyteller Screen

**MCP Tools**:
- `create_campaign_npc` - Add to campaign (future write API)
- `link_npc_to_article` - Connect to article (future)

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `search_articles` | Read | 2 | High |
| `get_article` | Read | 1 | Core |
| `list_articles` | Read | 1 | Core |
| `get_world` | Read | 1 | Core |
| `create_article` | Write | Future | Critical |
| `create_campaign_npc` | Write | Future | High |

---

## Example Conversation

```
User: I need a blacksmith NPC for the town of Phandalin

Claude: I'll help you create a blacksmith for Phandalin! Let me check 
what exists in your world for context.

[Searches for Phandalin, existing blacksmiths]

I found your Phandalin article. It mentions the town was recently 
reclaimed from bandits and is growing. No blacksmith exists yet.

For a frontier town blacksmith, here's what I'm thinking:

**Name**: Tharden Rockseeker (dwarf, ties to local Rockseeker clan?)
         OR Elara Stonehammer (human woman, came seeking opportunity)

**Personality Options**:
- Gruff but fair craftsman
- Eager entrepreneur in growing town
- Retired adventurer seeking quiet life

Which direction interests you, or would you like me to develop 
one of these further?

User: I like Elara as a retired adventurer

Claude: Great choice! Here's Elara Stonehammer:

---
# Elara Stonehammer

## Overview
A muscular human woman in her late 40s, Elara runs Phandalin's 
only smithy with the efficiency of someone who's seen too many 
cheap blades fail at critical moments. She came to town six 
months ago and quickly became essential to the growing community.

## Appearance
- Tall and broad-shouldered with arms like oak branches
- Silver-streaked black hair kept in a practical braid
- Burn scars on her forearms; a thin scar across her left cheek
- Usually wears a leather apron over simple clothes

## Personality
- **Pragmatic**: Values function over form
- **Protective**: Watches over Phandalin like her own family
- **Haunted**: Rarely speaks of her adventuring days

## Background
Elara spent 20 years as a mercenary and dungeon delver. After 
her party was killed by [DM choice], she retired to craft tools 
instead of use them. She chose Phandalin because it reminded her 
of her home village—and because it needed protection.

## Motivations
- **Goal**: Build a peaceful life, protect her adopted town
- **Fear**: Being forced to fight again, losing more people
- **Secret Desire**: Teach a worthy apprentice everything she knows

## Connections
- **Location**: Stonehammer Smithy, west end of Phandalin
- **Organizations**: Former member of [adventuring company]
- **Relationships**: 
  - Sildar Hallwinter (mutual respect between veterans)
  - Toblen Stonehill (regular customer, friend)

## Role in Story
- Quest hook: Knows about dungeon locations from her past
- Resource: Can repair/upgrade equipment
- Information: Veteran's insight on monsters and tactics
- Protection: Will fight to defend Phandalin if pushed

## Secrets (DM Only)
- Keeps her old adventuring gear in a locked chest under the forge
- Recognized one of the Redbrands as someone from her past
- Knows the location of a cache of magic weapons she never retrieved

## RPG Notes
**NPC Type**: Commoner/Veteran (fight only if necessary)
**Attitude**: Friendly to party if they help Phandalin
**Voice**: Low, measured, chooses words carefully
---

Would you like me to add connections to other NPCs or expand 
any section?
```

---

## Quick NPC Templates

### Shopkeeper
- Focus: What they sell, prices, personality quirk
- Quick hook: "Special item in back"

### Guard/Soldier  
- Focus: Duty, allegiance, corruption level
- Quick hook: "Seen something strange"

### Noble/Authority
- Focus: Power, ambition, secrets
- Quick hook: "Needs discreet help"

### Tavern Staff
- Focus: Rumors heard, regulars, establishment character
- Quick hook: "Overheard conversation"

### Random Encounter
- Focus: Immediate purpose, reaction to party
- Quick hook: "Traveling to [destination]"

---

## Expected Outcome

- Fully developed NPC ready for play
- World-integrated with existing content
- Multiple potential plot hooks
- Consistent with campaign tone
- Formatted for World Anvil article

---

## Related Workflows

- [WF-001: Campaign Setup](d-and-d-campaign-setup.md)
- [WF-005: Quick NPC Lookup](quick-npc-lookup.md)
- [WF-004: Location Development](location-development.md)
