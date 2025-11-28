# Location Development Workflow

**Workflow ID**: WF-004  
**Category**: World Building  
**Complexity**: Medium  
**User Persona**: DM building out campaign locations

---

## User Goal

Develop locations with rich detail, strategic information for gameplay, and connections to the broader world, from cities to dungeons.

---

## Trigger Phrases

- "Describe [location]"
- "Build out this town/city/dungeon"
- "What's in [location]?"
- "Create a location for [purpose]"
- "Develop [existing location] further"
- "I need a tavern/shop/temple in [town]"

---

## Prerequisites

- Active world with geographic structure
- Understanding of campaign region
- Template chosen (Settlement, Building, Geographic Location)

---

## Workflow Steps

### Step 1: Determine Location Type & Context
**User**: "Develop the town of Triboar for my players"

**Claude Actions**:
1. Check if location exists in world
2. Identify location type (Settlement, Building, etc.)
3. Load regional context
4. Identify connected content

**MCP Tools**:
- `search_articles` - Find existing location
- `get_article` - Load location if exists
- `list_articles` - Find related locations/NPCs

---

### Step 2: Core Location Framework
**Claude Develops**:
- **Identity**: Name, type, size, population
- **Geography**: Physical placement, terrain, climate
- **Economy**: Primary industries, trade, wealth level
- **Government**: Leadership, laws, factions
- **Defense**: Walls, guards, threats
- **Culture**: Customs, religions, notable features

---

### Step 3: Gameplay-Relevant Details
**For Settlements**:
- Key establishments (tavern, temple, shop, guild)
- Important NPCs with roles
- Current events/tensions
- Rumors and hooks
- Safe/dangerous areas

**For Dungeons/Adventure Sites**:
- Entrance location and concealment
- History and original purpose
- Current inhabitants
- Room-by-room (or zone) breakdown
- Treasure and dangers
- Environmental hazards

**For Wilderness/Regions**:
- Travel routes and times
- Encounter zones
- Resources and hazards
- Landmarks for navigation
- Weather patterns

---

### Step 4: World Integration
**Claude Actions**:
1. Link to governing organizations
2. Connect to nearby locations
3. Assign relevant NPCs
4. Add to regional map (reference)
5. Place in timeline (founding, events)

**MCP Tools**:
- `list_articles` (Organizations, Characters)
- `get_article` - Load related content
- `search_articles` - Find connections

---

### Step 5: Generate Article Content

**Settlement Template Output**:
```markdown
# [Settlement Name]

## Overview
[Vignette capturing the feel]

## Geography
[Location, terrain, notable features]

## Demographics
- **Population**: [Number and trend]
- **Races**: [Composition]
- **Languages**: [Spoken languages]

## Government
- **Type**: [Government structure]
- **Leader**: [Link to NPC article]
- **Laws**: [Notable regulations]

## Economy
- **Primary Industries**: [What they produce]
- **Trade**: [What they import/export]
- **Currency**: [What's accepted]
- **Wealth Level**: [Poor/Modest/Wealthy]

## Defenses
- **Walls**: [Description]
- **Military**: [Guard force, militia]
- **Threats**: [Common dangers]

## Districts/Quarters
### [District 1 Name]
[Description, key locations, atmosphere]

### [District 2 Name]
[Description, key locations, atmosphere]

## Key Locations
| Name | Type | Description |
|------|------|-------------|
| [Tavern name] | Tavern | [Brief description] |
| [Temple name] | Temple | [Brief description] |
| [Shop name] | Shop | [Brief description] |

## Important NPCs
| Name | Role | Notes |
|------|------|-------|
| [NPC 1] | [Role] | [Brief note] |
| [NPC 2] | [Role] | [Brief note] |

## Current Events
- [Event 1 affecting the town]
- [Event 2 creating opportunity]

## Rumors & Hooks
| Rumor | Truth | Hook |
|-------|-------|------|
| [What people say] | [Reality] | [Adventure potential] |

## History
[Brief historical overview]

## Secrets (DM Only)
- [Hidden information]
- [Secret locations]
- [Concealed threats]
```

---

## Example Conversation

```
User: I need to develop Triboar for next session

Claude: Let me check what exists for Triboar in your world.

[Searches for Triboar]

I found a brief mention in your Sword Coast article but no dedicated 
Triboar article yet. Based on Forgotten Realms lore and your campaign:

**Triboar Quick Facts:**
- Trading town at crossroads
- Population ~2,500
- Known for horse breeding
- Recent giant attacks in region (per your Storm King's Thunder campaign)

Would you like me to:
1. **Full Development**: Complete settlement article with all districts, NPCs, shops
2. **Session Focused**: Just the locations your party is likely to visit
3. **Adventure Site**: Focus on encounter locations and plot hooks

User: Session focused - they're passing through looking for information about giants

Claude: Perfect, here's Triboar focused on what your party needs:

---
# Triboar - Session Guide

## First Impressions
A busy crossroads town with dust-covered travelers, horse traders 
haggling loudly, and worried whispers about giant sightings to the 
north. Guard patrols are doubled.

## Where to Find Giant Information

### The Talking Troll (Tavern)
**Owner**: Karroun Vhaelen (human male, ex-caravan guard)
**Atmosphere**: Busy common room, traders sharing news
**Key Info**: Caravan masters have firsthand giant encounter stories
**Price**: Drinks + friendly conversation

### The Lord Protector's Tower
**Contact**: Lord Protector Darathra Shendrel (human female)
**Attitude**: Concerned, looking for capable adventurers
**Key Info**: Official reports, will share if party seems helpful
**Potential Quest**: Investigate specific giant sighting

### Ransor's Open Road (Merchant Company HQ)
**Contact**: Narth Tezrin (human male, merchant lord)
**Attitude**: Business-focused, information costs money
**Key Info**: Trade route disruptions, economic impact
**Price**: 10gp or trade in services

### Uldinath's Arms (Weapon Shop)
**Contact**: Uldinath (half-elf male, veteran)
**Attitude**: Gruff but helpful to fellow warriors
**Key Info**: Practical advice on fighting giants
**Free**: If party buys equipment

## Current Giant Threat Level
- Two caravans attacked in past month
- Fire giant symbol found at attack sites
- Refugees arriving from northern farms

## Random Encounters in Triboar
| d6 | Encounter |
|----|-----------|
| 1 | Frightened refugee begs for food/coin |
| 2 | Merchant tries to hire party as guards |
| 3 | Town guard asks party's business (suspicious) |
| 4 | Drunken farmer claims to know giant lair location |
| 5 | Harper agent (disguised) observes party |
| 6 | Horse trader offers "giant-proof" mounts (scam) |

## Quick Exits
- **North Road**: Toward Longsaddle (giant territory)
- **South Road**: Toward Yartar (safer)
- **East Road**: Toward Everlund (Harper contacts)
---

Need me to expand any of these NPCs or add more locations?
```

---

## Location Type Templates

### Dungeon/Adventure Site
Focus on: Zones, encounters, traps, treasure, boss

### Wilderness Region  
Focus on: Travel times, encounter tables, resources, hazards

### City District
Focus on: Atmosphere, key buildings, NPCs, services, secrets

### Specific Building
Focus on: Purpose, layout, inhabitants, hidden areas

---

## Expected Outcome

- Location ready for immediate use in session
- Gameplay-relevant information prioritized
- Integrated with existing world content
- Appropriate level of detail for need
- Clear DM notes for running encounters

---

## Related Workflows

- [WF-001: Campaign Setup](d-and-d-campaign-setup.md)
- [WF-003: NPC Generation](npc-generation.md)
- [WF-007: Map Management](map-management.md)
