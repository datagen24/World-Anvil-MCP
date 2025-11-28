# World Building Workflow

**Workflow ID**: WF-006  
**Category**: Content Creation  
**Complexity**: High  
**User Persona**: Worldbuilder developing campaign setting

---

## User Goal

Systematically develop world lore, cultures, history, and interconnected elements that create a rich, consistent setting.

---

## Trigger Phrases

- "Help me worldbuild"
- "Develop the lore for [topic]"
- "Create a culture/religion/faction"
- "Build out the history of [region]"
- "How should [element] work in my world?"
- "Connect [thing A] to [thing B]"

---

## Prerequisites

- World created in World Anvil
- Basic premise/genre established
- Understanding of intended use (novel, RPG, both)

---

## Workflow Steps

### Step 1: Assess Current World State
**User**: "Help me develop the pantheon for my world"

**Claude Actions**:
1. Load world meta information
2. Check existing religious content
3. Identify connected elements (cultures, organizations)
4. Understand tone/genre

**MCP Tools**:
- `get_world` - Load world details
- `list_categories` - See what exists
- `list_articles` - Find related content
- `search_articles` - Check for existing religious content

---

### Step 2: Worldbuilding Consultation
**Claude Approach**:
1. Ask clarifying questions about vision
2. Identify key decisions needed
3. Suggest frameworks and options
4. Consider implications for other world elements

**Key Questions by Topic**:

**Pantheon/Religion**:
- Polytheistic, monotheistic, animistic?
- Do gods directly interact with mortals?
- How does magic relate to divine power?
- Are there clergy organizations?

**Culture/Society**:
- What real-world inspiration?
- Technology level?
- Social structure?
- Values and taboos?

**History/Timeline**:
- How old is civilization?
- Major cataclysms or golden ages?
- Recent conflicts affecting present?
- What's "ancient" vs "modern"?

**Geography/Cosmology**:
- Natural or magical landscape?
- Other planes of existence?
- Climate and biomes?
- Resources and scarcity?

---

### Step 3: Generate Content Framework
**Claude Creates**:
- Overview document
- Key entities list
- Relationship map (conceptual)
- Article templates for each element
- Questions for further development

---

### Step 4: Integration Check
**Claude Actions**:
1. Cross-reference new content with existing
2. Identify potential conflicts
3. Suggest connections
4. Note gaps to fill later

**MCP Tools**:
- `search_articles` - Find related content
- `get_article` - Load connected elements

---

### Step 5: Output Article Content
**Example: Pantheon Overview Article**:

```markdown
# The Celestial Court

## Overview
[Summary of religious structure]

## Cosmology
[How divine realm relates to mortal world]

## The Major Deities

### [Deity 1 Name] - [Domain]
**Portfolio**: [What they govern]
**Alignment**: [If applicable]
**Symbol**: [Holy symbol]
**Worshippers**: [Who follows them]
**Clergy**: [Religious organization]

### [Deity 2 Name] - [Domain]
...

## Religious Practices
[Common worship across the pantheon]

## Holy Days
| Festival | Date | Deity | Practices |
|----------|------|-------|-----------|
| [Name] | [When] | [Who] | [What] |

## Conflicts & Relationships
[Inter-deity politics]

## Impact on Mortal World
[How religion affects daily life]

## Secret Truths (DM/Author Only)
[Hidden cosmological facts]
```

---

## Worldbuilding Topic Templates

### Culture Article
- Name & identity
- Geography & territory
- Social structure
- Economy & trade
- Military tradition
- Art & expression
- Religion & spirituality
- Coming of age & death
- Attitudes toward outsiders
- Historical moments

### Faction/Organization Article
- Purpose & goals
- Structure & hierarchy
- Membership & recruitment
- Resources & assets
- Allies & enemies
- Public face vs reality
- History & founding
- Current leadership
- Secret agenda

### Historical Era Article
- Name & dates
- Defining characteristics
- Major events
- Key figures
- Beginning & end
- Legacy & artifacts
- What people remember vs truth

### Magic System Article
- Source of power
- Limitations & costs
- Who can use it
- Schools or types
- Relationship to religion
- Social status of practitioners
- Dangers & corruption
- Historical development

---

## Example Conversation

```
User: Help me develop the dwarven culture in my world

Claude: I'll help you develop your dwarves! Let me check what you 
have established.

[Checks existing dwarf content]

I found mentions of dwarves in your Mountain Kingdoms region article 
and a draft article called "Clan Ironforge." 

To create a cohesive dwarven culture, let's establish some foundations:

**Core Identity Questions:**

1. **Origin Story**: Were dwarves created by gods, born from stone, 
   evolved naturally, or something else?

2. **Relationship to Stone/Earth**: 
   - Practical miners and craftsmen?
   - Spiritual connection to the earth?
   - Literally made of stone elements?

3. **Clan Structure**:
   - How important are clans vs individual identity?
   - What determines clan membership - blood, craft, geography?
   - How do clans interact?

4. **Cultural Values** (pick 3-5 core values):
   - Honor / Oath-keeping
   - Craftsmanship / Excellence
   - Tradition / Ancestors
   - Wealth / Prosperity  
   - Warfare / Strength
   - Knowledge / Secrets
   - Community / Kinship

What feels right for the tone of your world?

User: They're deeply spiritual, connected to stone, and honor-bound. 
Clans are based on craft traditions.

Claude: Excellent choices! That creates interesting dynamics. Here's 
a framework:

---
# Dwarven Culture: The Stoneheart Traditions

## Core Belief: The Living Stone
Dwarves believe the mountain itself is alive—a slumbering god whose 
dreams manifest as veins of ore. To mine is to interpret these dreams. 
To craft is to give them form.

## The Craft-Clans
Dwarven society organizes around ancestral crafts:

| Clan Type | Specialty | Status | Symbol |
|-----------|-----------|--------|--------|
| Forgekin | Metalwork | Highest | Hammer & Anvil |
| Stonesingers | Architecture | High | Arch & Column |
| Deepdelvers | Mining | Respected | Pick & Lantern |
| Runebinders | Enchantment | Mysterious | Open Book & Gem |
| Alebrewers | Provisions | Beloved | Barrel & Grain |

## The Oathstone Tradition
Every major oath is sworn upon a clan's Oathstone—a piece of the 
original mountain from their founding. Breaking a sworn oath causes 
physical pain through this spiritual connection.

**Implications:**
- Dwarves are extremely careful about exact wording
- Oathbreakers are physically marked (gray skin, brittle bones)
- Trade deals are sacred contracts
- Marriage is a craft-partnership oath

## Coming of Age: The First Shaping
Young dwarves spend a decade learning their clan craft, culminating 
in the First Shaping—creating a masterwork that proves their skill 
and defines their adult name.

**Adventure Hook:** A young dwarf's First Shaping was stolen; they 
cannot take their adult name until they recover it.

---

Would you like me to develop any of these elements further? We should 
also consider:
- How dwarves interact with other races
- Their relationship to your pantheon
- Current political situation
```

---

## Expected Outcome

- Coherent worldbuilding that integrates with existing content
- Multiple interconnected articles
- Clear foundations for future development
- Adventure/story hooks embedded in lore
- Consistent tone and themes

---

## Related Workflows

- [WF-004: Location Development](location-development.md)
- [WF-003: NPC Generation](npc-generation.md)
- [WF-008: Quest/Plot Management](quest-plot-management.md)
