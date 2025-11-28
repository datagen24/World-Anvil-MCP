# World Anvil Platform Research

**Research Date**: 2025-11-28  
**Purpose**: Foundation knowledge for MCP Server development  
**API Version**: Boromir (v2)

---

## Platform Overview

World Anvil is a worldbuilding and RPG campaign management platform serving:
- **Worldbuilders**: Creating fictional settings
- **Authors**: Novel/story writing with integrated worldbuilding
- **Game Masters**: D&D and 40+ RPG system support
- **Players**: Character management and campaign participation

### Key Metrics
- 2+ million users
- 40+ supported RPG systems
- 25+ article templates

---

## API Details (Boromir v2)

### Authentication
```
Headers:
  x-application-key: YOUR_APPLICATION_KEY
  x-auth-token: USER_AUTH_TOKEN
```

- **Application keys**: Grandmaster+ rank, requires form submission
- **User tokens**: Generated at `/api/auth/key`

### Base URL
```
https://www.worldanvil.com/api/external/boromir/
```

### Granularity Parameter
All GET endpoints support a `granularity` parameter:

| Value | Description | Use Case |
|-------|-------------|----------|
| -1 | Generic reference | Listings, minimal data |
| 0 | Minimal data | IDs and basic fields |
| 1 | Standard detail | Most operations |
| 2 | Full detail | Articles with all content |

### Known Endpoints (from openapi.yml + pywaclient)

**User/Identity**:
- `GET /identity` - Current authenticated user
- `GET /user` - User details (id via query param)
- `GET /user/worlds` - List user's worlds

**Worlds**:
- `GET /world` - World details (id via query param)
- `POST /world/articles` - World's articles (pagination via body)
- `GET /world/categories` - World's categories (id via query param)

**Articles**:
- `GET /article` - Article details (id via query param, granularity "2" for full content)
- `PUT /article` - Create
- `PATCH /article` - Update (id via query param)
- `DELETE /article` - Delete (id via query param)
- Article includes `content` and `content_parsed` fields

**Categories**:
- `GET /category` - Category details (id via query param)
- `GET /world/categories` - List categories (id via query param)

### API Notes

1. Core base endpoints expose CRUD via header-authenticated PUT/PATCH/DELETE (identifier via query params)
2. World-scoped listings commonly use POST with body for pagination (`limit`, `offset`)
3. Rate limiting applies; implement backoff and caching
4. Grandmaster+ required for application keys; user tokens required for user-level access

### Documentation Sources
- API Docs: `https://www.worldanvil.com/api/external/boromir/documentation`
- Swagger: `https://www.worldanvil.com/api/external/boromir/swagger-documentation`
- Python Client: `https://gitlab.com/SoulLink/world-anvil-api-client` (pywaclient)

---

## Platform Architecture

### Content Hierarchy
```
User Account
├── Worlds (settings/projects)
│   ├── Articles (25+ templates)
│   │   └── Categories (organization)
│   ├── Maps (interactive, linkable pins)
│   ├── Timelines (historical events)
│   ├── Manuscripts (novel writing)
│   ├── Images (uploaded media)
│   └── Campaigns (RPG management)
│       ├── Sessions
│       ├── Supporting Cast (NPCs)
│       ├── Player Characters
│       └── Plots
└── Characters (player-controlled heroes)
```

### World Concept
- One **World** = One setting/project
- Can be any scale (city to multiverse)
- Auto-creates a Campaign with same name
- Configurable: Genre, RPG System, Privacy

---

## Article Templates (25+)

### Characters & Creatures
| Template | Use Case |
|----------|----------|
| **Character** | Named individuals, NPCs, deities |
| **Species** | Races, creature types, animals |

### Locations
| Template | Use Case |
|----------|----------|
| **Geographic Location** | Continents, regions, planes |
| **Settlement** | Cities, towns, stations |
| **Building/Landmark** | Specific structures, ruins |

### Organizations & Society
| Template | Use Case |
|----------|----------|
| **Organization** | Governments, guilds, companies, countries |
| **Ethnicity/Culture** | Cultural groups, movements |
| **Tradition** | Celebrations, rituals, customs |
| **Title/Rank** | Positions, honors |

### Items & Technology
| Template | Use Case |
|----------|----------|
| **Item** | Objects, artifacts, equipment |
| **Material** | Resources, substances |
| **Vehicle** | Transportation |
| **Technology** | Inventions, machines |

### Magic & Conditions
| Template | Use Case |
|----------|----------|
| **Spell** | Magic, psionics, powers |
| **Condition** | Diseases, mutations, statuses |

### Narrative
| Template | Use Case |
|----------|----------|
| **Document** | In-world texts |
| **Prose** | Stories, chapters, poems |
| **Plot** | Story arcs, quest lines |
| **Session Report** | RPG session summaries |
| **Conflict** | Wars, battles |
| **Generic** | Anything else |

---

## Campaign Manager Features

### Digital Storyteller Screen (DSTS)
- Quick access to campaign content
- Note-taking during sessions
- Dice rolling
- Music/ambiance playback
- Stat block reference
- PC sheet viewing

### NPCs vs Character Articles
- **Character Articles**: Full worldbuilding content
- **Campaign NPCs**: Lightweight session entries
- Can be **linked**: NPC → Character Article
- NPCs on DSTS, articles are lore

### Player Integration
- Invitation via link
- Players create Heroes (PCs)
- GM can view/edit player sheets
- Subscriber groups for secrets

### Stat Blocks
- D&D 5e SRD included
- Community-created blocks
- Homebrew creation (Grandmaster+)

---

## Maps & Timelines

### Interactive Maps
- Upload images as backgrounds
- Linkable pins to articles or other maps
- Character location markers (draggable)
- Multiple layers

### Timelines
- Historical event tracking
- Era divisions
- Parallel timelines
- Chronicles: Map + Timeline fusion

---

## Guild Membership Tiers

| Tier | Key Features |
|------|--------------|
| Free | Basic worldbuilding, limited articles |
| Journeyman | More storage, privacy |
| Master | CSS, co-authors |
| **Grandmaster** | API access, custom templates |
| Sage | Advanced features |
| Inner Sanctum | All features |

**Note**: API application keys require Grandmaster or above.

---

## BBCode System

World Anvil uses BBCode for formatting and embedding:
- Text formatting (bold, italic, headers)
- Article linking via `@` mentions
- Embedding maps, timelines, images
- Spoiler tags and secrets
- Dice roll buttons

---

## Key Integrations

### Slash Menu (`/` command)
- Headers, tables, breaks
- Embed World Anvil content
- Markdown-like shortcuts

### Mentions System
- `@` + 3 letters to search/link articles
- Auto-links even unwritten articles
- Creates interconnected world graph

### Secrets
- Content hidden from specific users
- Subscriber groups control visibility
- Separate player/DM views

---

## MCP Development Implications

### Read Operations (Available Now)
1. List user's worlds
2. Get world details and settings
3. List/get articles by category or template
4. Get full article content
5. Navigate categories
6. Access maps and timelines

### Write Operations (Future)
When Project Oracle completes:
- Article creation/editing
- Category management
- Campaign NPC creation
- Map marker placement

### Caching Opportunities
- User's world list (rarely changes)
- Category structure
- Frequently accessed NPCs/locations
- Session-relevant content pre-load

### Search Considerations
- API may have search endpoint (check Swagger)
- Client-side filtering as fallback
- Cache enables local search

---

## Reference Links

| Resource | URL |
|----------|-----|
| Learn Center | https://www.worldanvil.com/learn |
| API Docs | https://www.worldanvil.com/api/external/boromir/documentation |
| Swagger | https://www.worldanvil.com/api/external/boromir/swagger-documentation |
| Codex (Community) | https://www.worldanvil.com/w/WorldAnvilCodex |
| Python Client | https://gitlab.com/SoulLink/world-anvil-api-client |
| Discord | World Anvil Official Discord (#api-development) |
