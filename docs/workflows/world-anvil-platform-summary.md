# World Anvil Platform Summary

**Research Date**: 2025-11-28  
**Purpose**: Foundation knowledge for MCP Server development  
**API Version**: Boromir (v2)

---

## Platform Overview

World Anvil is a worldbuilding and RPG campaign management platform serving:
- **Worldbuilders** - Creating fictional settings
- **Authors** - Novel/story writing with integrated worldbuilding
- **Game Masters** - D&D and 40+ RPG system support
- **Players** - Character management and campaign participation

### Core Philosophy
- One **World** = One setting/project (can be any scale from a city to a multiverse)
- Everything interconnects via linking system
- Templates provide prompts but are optional/flexible
- System-agnostic core with RPG-specific features

---

## Platform Architecture

### Hierarchy

```
User Account
├── Worlds (settings/projects)
│   ├── Articles (content using templates)
│   │   └── Categories (organization)
│   ├── Maps (interactive, linkable pins)
│   ├── Timelines (historical events)
│   ├── Manuscripts (novel writing)
│   ├── Images (uploaded media)
│   └── Campaigns (RPG management)
│       ├── Sessions
│       ├── Supporting Cast (NPCs)
│       ├── Player Characters (via invitation)
│       └── Plots
└── Characters (player-controlled heroes)
```

### Worlds
- Top-level container for all content
- Can be public or private (Guild feature)
- Each world auto-creates a campaign with the same name
- Genre and RPG System can be configured
- Homepage customizable

### Campaigns
- Always linked to a specific World
- Requires RPG System selection
- Features:
  - Session management
  - NPC management (Supporting Cast)
  - Player invitation system
  - Digital Storyteller Screen (DSTS)
  - Plot tracking

---

## Article Templates (25+)

### Characters & Creatures
| Template | Use Case |
|----------|----------|
| **Character** | Named individuals, NPCs, deities, sentient entities |
| **Species** | Races, creature types, animals, plants |

**Character Template Sections:**
- Generic (basic profile: name, gender, birth/death, location)
- Naming (honorific, given name, family name, etc.)
- Physical (height, weight, features)
- Mental (personality, motivations, fears)
- Social (relationships, family connections)
- Divine/Deity (domain, religious connections)

### Locations
| Template | Use Case |
|----------|----------|
| **Geographic Location** | Continents, regions, landmarks, planes of existence |
| **Settlement** | Cities, towns, villages, space stations |
| **Building/Landmark** | Specific structures, ruins, monuments |

### Organizations & Society
| Template | Use Case |
|----------|----------|
| **Organization** | Governments, guilds, religions, companies, families, countries |
| **Ethnicity/Culture** | Cultural groups, sub-cultures, artistic movements |
| **Tradition** | Celebrations, rituals, customs, beliefs |
| **Title/Rank** | Positions, honors, distinctions |

### Items & Technology
| Template | Use Case |
|----------|----------|
| **Item** | Objects, artifacts, equipment |
| **Material** | Resources, substances, components |
| **Vehicle** | Transportation, ships, mounts |
| **Technology** | Inventions, machines, systems |

### Magic & Conditions
| Template | Use Case |
|----------|----------|
| **Spell** | Magic, psionics, superpowers |
| **Condition** | Diseases, mutations, transformations, status effects |

### Narrative & Documentation
| Template | Use Case |
|----------|----------|
| **Document** | In-world texts, letters, reports |
| **Prose** | Short stories, scenes, chapters, poems |
| **Plot** | Story arcs, quest lines |
| **Session Report** | RPG session summaries |
| **Conflict** | Wars, battles, arguments |
| **Generic Article** | Anything else, meta content |

---

## RPG Campaign Features

### Digital Storyteller Screen (DSTS)
- Quick access to all campaign content during play
- Note-taking during sessions
- Dice rolling
- Music/ambiance playback
- Stat block reference
- PC sheet viewing
- NPC quick creation

### NPCs vs Character Articles
- **Character Articles**: Full worldbuilding articles (templates)
- **Campaign NPCs**: Lightweight entries for session use
- Can be **linked**: NPC → Character Article
- NPCs appear on DSTS, articles are worldbuilding content

### Session Management
- Session scheduling
- Session reports (template)
- Plot tracking
- Session notes

### Player Integration
- Invitation via link
- Players create Heroes (PCs)
- GM can view/edit player sheets
- Subscriber groups for secrets

### Stat Blocks
- D&D 5e SRD included
- Community-created stat blocks
- Homebrew stat block creation (Grandmaster+)
- Supports 40+ RPG systems

---

## Maps & Timelines

### Interactive Maps
- Upload images as map backgrounds
- Drop linkable pins
- Pins can link to:
  - Articles
  - Other maps (drill-down)
- Character location markers (draggable)
- Multiple map layers

### Timelines
- Historical event tracking
- Era divisions
- Parallel timelines (for different perspectives)
- Chronicles feature (map + timeline fusion)

---

## API Details (Boromir v2)

### Authentication
```
Headers:
  x-application-key: YOUR_APPLICATION_KEY
  x-auth-token: USER_AUTH_TOKEN
```

- Application keys: Grandmaster+ rank, requires form submission
- User tokens: Generated at /api/auth/key

### Base URL
```
https://www.worldanvil.com/api/external/boromir/
```

### Granularity Parameter
| Value | Description |
|-------|-------------|
| -1 | Generic reference (default for listings) |
| 0 | Minimal data |
| 1 | Standard detail |
| 2 | Full detail (articles only) |

### Known Endpoints (from pywaclient)
- `GET /identity` - Current user info
- `GET /user` - User details
- `GET /user/{id}/worlds` - List user's worlds
- `GET /world/{id}` - World details
- `GET /world/{id}/articles` - World's articles
- `GET /world/{id}/categories` - World's categories
- `GET /article/{id}` - Article details
- `GET /category/{id}` - Category details
- `GET /category/{id}/articles` - Articles in category

### API Limitations
- **Currently READ-focused**
- Write/edit endpoints in development (Project Oracle)
- Rate limiting applies
- Non-commercial use only without authorization

### Swagger Documentation
```
https://www.worldanvil.com/api/external/boromir/swagger-documentation
```

---

## Guild Membership Tiers

Features vary by tier:
- **Free**: Basic worldbuilding, limited articles
- **Journeyman**: More storage, privacy options
- **Master**: CSS customization, co-authors
- **Grandmaster**: API access, custom templates, stat block creation
- **Sage**: Advanced features, professional tools
- **Inner Sanctum**: All features

---

## Key Concepts for MCP Development

### Read Operations (Available)
1. List worlds
2. Get world details
3. List/get articles
4. List/get categories
5. Get user identity
6. Get maps, timelines (check Swagger)

### Write Operations (Future/Limited)
- Article creation/editing (Project Oracle - in development)
- Campaign management
- NPC creation

### MCP Tool Opportunities
1. **World browsing** - Navigate worlds, articles, categories
2. **Content retrieval** - Get full article details
3. **Search** - Find content across world
4. **Campaign info** - Session details, NPCs, plots
5. **Map/timeline access** - Geographic and historical data

### Workflow Considerations
- DMs need quick NPC lookup
- Session prep involves multiple article types
- Players need character sheet access
- World navigation should be intuitive
- Linking relationships are valuable context

---

## References

- Learn Center: https://www.worldanvil.com/learn
- API Docs: https://www.worldanvil.com/api/external/boromir/documentation
- Swagger: https://www.worldanvil.com/api/external/boromir/swagger-documentation
- Codex (community): https://www.worldanvil.com/w/WorldAnvilCodex
- Python Client: https://gitlab.com/SoulLink/world-anvil-api-client (pywaclient)

---

## Next Steps

1. Access Swagger documentation directly for complete endpoint list
2. Test API with credentials to validate endpoint behavior
3. Map endpoints to D&D campaign workflows
4. Identify gaps where local caching/processing adds value
