# Map Management Workflow

**Workflow ID**: WF-007  
**Category**: World Organization  
**Complexity**: Medium  
**User Persona**: DM managing campaign geography

---

## User Goal

Organize, query, and utilize World Anvil maps for campaign navigation, encounter placement, and player information sharing.

---

## Trigger Phrases

- "Show me the map of [region]"
- "What's near [location]?"
- "Where is [place] on the map?"
- "Add a marker for [location]"
- "Travel from [A] to [B]"
- "What map pins are in [area]?"

---

## Prerequisites

- Maps uploaded to World Anvil
- Map pins/markers configured
- Location articles linked to pins

---

## Workflow Steps

### Step 1: Load Map Context
**User**: "Show me what's around Phandalin"

**Claude Actions**:
1. Identify relevant map
2. Load map metadata
3. Get pins/markers in region
4. Cross-reference with location articles

**MCP Tools**:
- `list_maps` - Get available maps
- `get_map` - Load specific map details
- `get_map_markers` - Get pin locations

---

### Step 2: Present Geographic Information
**Claude Output**:
```
📍 PHANDALIN REGION

Map: Sword Coast - Phandalin Area
Scale: 1 hex = 6 miles

NEARBY LOCATIONS (within 20 miles):
• Tresendar Manor (0.5 mi N) - Ruined keep, Redbrand hideout
• Old Owl Well (12 mi E) - Ancient watchtower, zombie activity
• Wyvern Tor (15 mi NE) - Rocky outcrop, orc raiders
• Cragmaw Hideout (18 mi NE) - Goblin cave complex
• Thundertree (30 mi NW) - Ruined town, dragon sighting

TRAVEL ROUTES:
→ Triboar Trail: West to Triboar (3 days)
→ High Road: South to Leilon (2 days)
→ Neverwinter: North via Triboar Trail (5 days)

TERRAIN: Foothills transitioning to Sword Mountains (N)
         Grasslands and light forest (S/W)
```

---

### Step 3: Travel Calculation (if requested)
**User**: "How long to get to Neverwinter?"

**Claude Actions**:
1. Calculate distance via route
2. Apply terrain modifiers
3. Consider party travel speed
4. Note potential encounters

**Output**:
```
🗺️ TRAVEL: Phandalin → Neverwinter

Distance: ~90 miles
Route: Triboar Trail → High Road

BY FOOT (24 mi/day normal pace):
• 4 days without issues
• Add 1 day if avoiding main roads

BY HORSE (30 mi/day):
• 3 days via roads

ENCOUNTER ZONES:
• Mile 0-20: Redbrand/Cragmaw territory (check clear)
• Mile 20-50: Light traffic, bandit risk
• Mile 50-90: Patrolled, relatively safe

NOTABLE STOPS:
• Day 2: Conyberry (ruined village, avoid at night)
• Day 3: Road intersection (merchant traffic)
```

---

### Step 4: Map Pin Query
**User**: "What pins do I have marked as dangerous?"

**Claude Actions**:
1. Query map markers with filters
2. Return categorized list
3. Provide quick summaries

**Output**:
```
⚠️ DANGEROUS LOCATIONS (marked on maps)

HIGH THREAT:
• Cragmaw Castle - Goblin stronghold, 30+ goblins
• Wave Echo Cave - Undead, unknown threats
• Thundertree - Young green dragon "Venomfang"

MODERATE THREAT:
• Old Owl Well - Necromancer + zombies
• Wyvern Tor - Orc raiding party
• Cragmaw Hideout - Goblins (may be cleared)

UNKNOWN THREAT:
• Ruins north of Triboar - Unexplored
• Mountain cave (unmarked) - Rumors of giants
```

---

## Map Query Types

### Geographic Query
"What's near X" → List locations within radius

### Route Query  
"How to get from A to B" → Travel time, route, encounters

### Threat Query
"What dangers are in region" → Dangerous markers

### Resource Query
"Where can they find X" → Locations with specific tags

### Player-Safe Query
"What do players know about map" → Public information only

---

## Integration with Sessions

### Pre-Session Map Prep
```
User: Party is heading to Thundertree next session

Claude: Loading Thundertree map context...

📍 THUNDERTREE SESSION PREP

Map: Neverwinter Wood Regional
Zoom: Thundertree Town Map (if available)

CONFIRMED THREATS:
• Venomfang (young green dragon) - Tower
• Ash zombies - Throughout town
• Twig blights - Western ruins
• Cultists - Dragon's meeting

ENTRY POINTS:
• South road - Safest approach
• East trail - Closer but through blights
• North - Dragon territory

KEY LOCATIONS TO PREP:
1. Druid's cottage (Reidoth if using)
2. Dragon's tower
3. Cultist camp
4. Herbalist's shop (treasure)

Would you like encounter details for any location?
```

### During-Session Map Reference
```
User: They went into the brown building on the east side

Claude: That's the OLD HERBALIST'S SHOP.

Content:
• Twig blights nest (4-6 creatures)
• Valuable herbs in back room
• Collapsed upper floor

The shop sign is barely readable: "Mirna's..."
(connects to Mirna Dendrar in Phandalin - her family shop)
```

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `list_maps` | Read | 2 | High |
| `get_map` | Read | 2 | High |
| `get_map_markers` | Read | 2 | High |
| `search_articles` | Read | 2 | Core |
| `get_article` | Read | 1 | Core |
| `create_map_marker` | Write | Future | Medium |

---

## Expected Outcome

- Quick geographic reference during play
- Travel planning with encounter awareness
- Map pin information retrieval
- Player-safe information filtering
- Session prep with map context

---

## Related Workflows

- [WF-004: Location Development](location-development.md)
- [WF-009: Session Prep](session-prep.md)
- [WF-002: Session Note-Taking](session-note-taking.md)
