# Session Prep Workflow

**Workflow ID**: WF-009  
**Category**: Campaign Management  
**Complexity**: High  
**User Persona**: DM preparing for upcoming session

---

## User Goal

Efficiently prepare for a D&D session by gathering relevant world content, planning encounters, and organizing materials.

---

## Trigger Phrases

- "Help me prep for session [number]"
- "What do I need for next session?"
- "Prepare materials for [location/event]"
- "Session prep for [adventure name]"
- "What's on deck for the party?"
- "Load everything for [session goal]"

---

## Prerequisites

- Active campaign with session history
- Content in World Anvil (NPCs, locations, quests)
- Understanding of where campaign left off

---

## Workflow Steps

### Step 1: Load Campaign Context
**User**: "Help me prep for Session 16"

**Claude Actions**:
1. Load campaign details
2. Get last session report
3. Identify where party is
4. Note active quests and threads
5. Check upcoming scheduled events

**MCP Tools**:
- `get_world` - Campaign context
- `list_articles` (Session Reports) - Recent sessions
- `get_article` - Last session details

---

### Step 2: Generate Session Summary
**Claude Output**:
```
📋 SESSION 16 PREP OVERVIEW

LAST SESSION RECAP (Session 15):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Party defended Goldenfields from hill giant attack
• Met Lifferlas the treant, received quest
• Discovered fire giant involvement
• Decided to head north to investigate

PARTY STATUS:
• Location: Goldenfields (departing)
• Level: 5
• Resources: ~80% (used some spells/potions in combat)
• Motivation: Stop giant attacks

ACTIVE QUEST THREADS:
🔷 Main: Stop the Giant Threat - heading to investigate
🔶 Side: Wave Echo Cave - on hold
◇ Minor: Return Mirna's Heirloom - if passing Thundertree

LIKELY NEXT SESSION:
• Travel north toward giant territory
• Possible random encounters
• May reach Eye of the All-Father or similar

DECISIONS PENDING:
• Route north (via Triboar or direct)
• Whether to recruit help
```

---

### Step 3: Location-Specific Prep
**User**: "They're traveling through the Dessarin Valley"

**Claude Actions**:
1. Load regional information
2. Get relevant location articles
3. Prepare encounter options
4. Identify NPCs they might meet

**MCP Tools**:
- `search_articles` - Regional content
- `get_article` - Location details
- `list_articles` - NPCs in region

**Output**:
```
🗺️ DESSARIN VALLEY TRAVEL PREP

ROUTE OPTIONS:
1. Long Road (safer, 4 days)
   - Passing Westbridge, then north
   - More travelers, less chance of giants
   
2. Cross-country (faster, 3 days)
   - Through foothills
   - Higher giant encounter chance

KEY LOCATIONS EN ROUTE:

📍 Westbridge (if Long Road)
• Small town, nervous about giants
• NPC: Helvur Tarnlar (innkeep) - has info
• Supplies available

📍 Stone Bridge (landmark)
• Ancient dwarven construction
• Rumored entrance to underground realm
• May see giant patrols nearby

📍 Summit Hall (Knights of Samular)
• Potential allies against giants
• NPC: Lady Ushien Stormbanner
• Could provide escort or information

RANDOM ENCOUNTER TABLE (custom for this journey):
| d12 | Encounter | Notes |
|-----|-----------|-------|
| 1-3 | Merchant caravan | Refugees from north |
| 4-5 | Patrol (15 guards) | Questioning travelers |
| 6-7 | Orc raiders (8) | Displaced by giants |
| 8 | Stone giant | Wandering, may parley |
| 9 | Griffon | Territorial |
| 10 | Abandoned camp | Signs of giant attack |
| 11-12 | Harper agent | Has information to share |

WEATHER:
• Season: [Current in-game season]
• Likely: Clear but cold
• Complication: Early snowfall possible
```

---

### Step 4: NPC Quick Sheets
**Claude Actions**:
1. Identify NPCs likely to appear
2. Generate quick reference cards
3. Prep voices/personalities

**Output**:
```
👥 NPCs FOR THIS SESSION

HELVUR TARNLAR (Westbridge Innkeeper)
• Voice: Worried, whispered tones
• Wants: News from south, customers
• Knows: Giant sightings, missing travelers
• Quote: "You heading north? Gods preserve you..."

LADY USHIEN STORMBANNER (Knight Commander)
• Voice: Crisp, military bearing
• Wants: Information about giant coordination
• Knows: Knight patrol reports, regional politics
• Quote: "The giants have never been this organized."
• Potential offer: Letter of introduction

HARSHNAG (Frost Giant) [If introduced]
• Voice: Deep, slow, thoughtful
• Wants: Restore the Ordning properly
• Knows: Giant politics, Eye of All-Father
• Quote: "Not all giants forget honor."
• Ally potential: Guide to sacred site
```

---

### Step 5: Combat Encounter Prep
**User**: "Prep the stone giant encounter"

**Claude Output**:
```
⚔️ ENCOUNTER: STONE GIANT

CREATURE: Stone Giant
CR: 7 | HP: 126 | AC: 17

ATTACKS:
• Greatclub: +9 to hit, 19 (3d8+6) bludgeoning
• Rock (60/240 ft): +9 to hit, 28 (4d10+6) bludgeoning

SPECIAL:
• Stone Camouflage: Advantage on Stealth in rocky terrain

TACTICS:
• Opens with rock throw from distance
• Retreats if badly wounded (intelligent)
• May attempt to parley if party seems strong

ENVIRONMENT:
• Rocky hillside with cover
• Advantage to giant on Stealth initially

TREASURE:
• 2d6 x 100 cp, 2d6 x 10 sp in pouch
• Possible: crude map showing giant movements

NON-COMBAT RESOLUTION:
• Speaks Giant and Dwarvish
• Asking about "the breaking" (Ordning)
• Might share information for food or news
```

---

### Step 6: Session Checklist
**Claude Output**:
```
✅ SESSION 16 CHECKLIST

BEFORE SESSION:
□ Review last session notes
□ Print/load NPC quick sheets
□ Prep encounter stat blocks
□ Random encounter table ready
□ Regional map accessible
□ Background music selected

OPENING:
□ "Previously on..." summary ready
□ Starting location described
□ Initial decision point clear

KEY SCENES TO PREP:
□ Travel montage or detailed
□ Westbridge stopover (if taken)
□ Giant encounter (if random roll)
□ End session hook ready

MATERIALS NEEDED:
□ Dessarin Valley map
□ Stone giant stat block
□ NPC cards: Helvur, Ushien, (Harshnag?)
□ Random encounter table

PLAYER HOOKS THIS SESSION:
• Theren: Brother's trail leads north
• Mira: Lord's Alliance contact at Summit Hall
• [Other PCs]: [Personal hooks]

END OF SESSION GOAL:
• Party reaches destination or
• Major NPC encounter or
• Clear direction for next session
```

---

## MCP Tools Required

| Tool | Operation | Phase | Priority |
|------|-----------|-------|----------|
| `get_world` | Read | 1 | Core |
| `list_articles` | Read | 1 | Core |
| `get_article` | Read | 1 | Core |
| `search_articles` | Read | 2 | High |
| `get_campaign` | Read | 3 | Medium |
| `list_campaign_npcs` | Read | 3 | Medium |

---

## Session Prep Templates

### Dungeon Session
- Map with room numbers
- Encounter by room
- Treasure locations
- Trap details
- Boss prep

### Social/RP Session
- NPC motivations
- Information to reveal
- Relationship dynamics
- Skill check DCs

### Travel Session
- Route with days
- Encounter table
- Weather/terrain
- Destination preview

### Combat Session
- Battle map prep
- Monster stat blocks
- Environmental factors
- Victory conditions

---

## Expected Outcome

- Complete session preparation package
- All relevant content accessible
- Quick reference materials ready
- Contingencies planned
- Smooth session execution

---

## Related Workflows

- [WF-002: Session Note-Taking](session-note-taking.md)
- [WF-005: Quick NPC Lookup](quick-npc-lookup.md)
- [WF-008: Quest/Plot Management](quest-plot-management.md)
