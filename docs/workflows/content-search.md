# Content Search Workflow

**Workflow ID**: WF-010  
**Category**: Information Retrieval  
**Complexity**: Low  
**User Persona**: DM or worldbuilder finding specific content

---

## User Goal

Quickly find specific content within a World Anvil world using various search strategies.

---

## Trigger Phrases

- "Find [content]"
- "Search for [term]"
- "Where did I put [article]?"
- "What articles mention [topic]?"
- "List all [category/type]"
- "Show me everything about [subject]"

---

## Prerequisites

- Content exists in World Anvil
- World context loaded

---

## Workflow Steps

### Step 1: Parse Search Intent
**User**: "Find all articles about dragons"

**Claude Actions**:
1. Identify search type (name, topic, category, tag)
2. Determine scope (current world, all worlds)
3. Choose search strategy

**Search Types**:
- **Name Search**: Specific article by title
- **Topic Search**: Keyword across all content
- **Category Search**: All articles in category
- **Template Search**: All articles using specific template
- **Tag Search**: Articles with specific tags
- **Connected Search**: Articles linked to specific article

---

### Step 2: Execute Search
**MCP Tools**:
- `search_articles` - Keyword/name search
- `list_articles` - By category or template
- `get_article` - Load specific article for connections

---

### Step 3: Present Results
**Claude Output Format**:
```
🔍 SEARCH RESULTS: "dragons"

FOUND 7 ARTICLES:

BY RELEVANCE:
━━━━━━━━━━━━━
1. 📄 Venomfang (Character)
   Young green dragon in Thundertree
   Last updated: 2 weeks ago
   
2. 📄 Dragons of the Sword Coast (Generic)
   Overview of dragon activity in region
   Last updated: 1 month ago

3. 📄 Cult of the Dragon (Organization)
   Dragon-worshipping faction
   Last updated: 3 weeks ago

BY CATEGORY:
━━━━━━━━━━━━
• Characters: 2 (Venomfang, Claugiyliamatar)
• Organizations: 1 (Cult of the Dragon)
• Locations: 1 (Dragon's Barrow)
• Generic: 2 (Dragon lore articles)
• Species: 1 (Chromatic Dragons)

QUICK ACTIONS:
• View [number] for full article
• "More about [name]" for details
• "Related to [name]" for connections
```

---

### Step 4: Drill-Down Options
**User**: "More about Venomfang"

**Claude Output**:
```
📄 VENOMFANG

Template: Character
Category: Antagonists
Tags: dragon, villain, thundertree

QUICK SUMMARY:
Young green dragon who has claimed the ruined tower 
in Thundertree as a lair. Cunning and manipulative,
seeks to build power through cultist minions.

CONNECTIONS:
→ Location: Thundertree (lair)
→ Organization: Cult of the Dragon (potential allies)
→ NPCs: Favric (cultist contact)
→ Quests: None active

MENTIONED IN:
• Thundertree location article
• Session 8 report (party heard rumors)
• Cult of the Dragon article

STATS REFERENCE:
• Young Green Dragon (MM p.94)
• CR 8, HP 136, AC 18

View full article? [Y/N]
```

---

## Search Strategies

### By Name (Exact)
```
User: Find "Sildar Hallwinter"

Claude: [Searches exact name match]

📄 SILDAR HALLWINTER
Found in: Characters category
Type: Character article
```

### By Topic (Broad)
```
User: Everything about the Zhentarim

Claude: [Searches "Zhentarim" across all articles]

Found 12 mentions:
• Zhentarim (Organization) - Main article
• Halia Thornton (Character) - Member
• Triboar (Location) - Zhentarim presence
• Session 5 (Report) - First contact
...
```

### By Category
```
User: List all my NPCs

Claude: [Lists articles in Characters category]

📁 CHARACTERS (47 articles)

ANTAGONISTS (8):
• Glasstaff, Venomfang, King Grol...

ALLIES (12):
• Sildar Hallwinter, Gundren Rockseeker...

NEUTRAL (15):
• Shopkeepers, tavern owners...

PLAYER CHARACTERS (4):
• [PC names]

OTHER (8):
• Deities, historical figures...
```

### By Template
```
User: Show me all locations

Claude: [Filters by Settlement, Building, Geographic Location templates]

📍 LOCATIONS BY TYPE

SETTLEMENTS (12):
• Phandalin, Triboar, Waterdeep...

BUILDINGS (8):
• Tresendar Manor, Stonehill Inn...

GEOGRAPHIC (15):
• Sword Mountains, Dessarin Valley...

DUNGEONS (4):
• Cragmaw Hideout, Wave Echo Cave...
```

### By Tag
```
User: Find everything tagged "haunted"

Claude: [Searches by tag]

🏷️ TAG: "haunted" (5 articles)

• Old Owl Well - Ruined watchtower
• Manor House - Tresendar Manor
• Thundertree - Ruined town  
• The Warrens - Abandoned mine
• Agatha's Lair - Banshee dwelling
```

### Connected Content
```
User: What's connected to Phandalin?

Claude: [Gets article, extracts links]

🔗 PHANDALIN CONNECTIONS

LOCATED HERE:
• Stonehill Inn, Barthen's Provisions, Shrine of Luck...

NPCS:
• Toblen Stonehill, Elmar Barthen, Sister Garaele...

ORGANIZATIONS:
• Redbrands, Miner's Exchange, Townmaster's Hall

NEARBY LOCATIONS:
• Tresendar Manor, Cragmaw Hideout, Old Owl Well...

MENTIONED IN QUESTS:
• Find Wave Echo Cave, Clear the Redbrands...

SESSIONS:
• Sessions 3-11 (party based here)
```

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `search_articles` | Read | 2 | Critical |
| `list_articles` | Read | 1 | Core |
| `get_article` | Read | 1 | Core |
| `list_categories` | Read | 1 | Core |

---

## Search Tips for Users

1. **Be specific**: "Zhentarim agent in Phandalin" > "bad guy"
2. **Use names**: Article names are fastest
3. **Try categories**: When browsing, not searching
4. **Check tags**: If you've tagged content consistently
5. **Follow connections**: One article leads to related ones

---

## Error Handling

```
SEARCH: "the blue wizard"
RESULT: No exact matches

SUGGESTIONS:
• Did you mean: "Glasstaff" (wizard character)?
• Search broader: "wizard" (found 3 results)
• Check spelling variations
• This might be new content - create article?
```

---

## Expected Outcome

- Quick content discovery
- Multiple search strategies available
- Easy navigation through results
- Connected content visible
- Efficient information retrieval

---

## Related Workflows

- [WF-005: Quick NPC Lookup](quick-npc-lookup.md)
- [WF-007: Map Management](map-management.md)
- [WF-009: Session Prep](session-prep.md)
