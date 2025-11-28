# World Anvil API Notes

## API Version
Boromir v2.0.0 (OpenAPI 3.0.3)

## Base URL
```
https://www.worldanvil.com/api/external/boromir
```

## Authentication

### Headers Required
```http
x-application-key: <application_key>
x-auth-token: <user_authentication_token>
```

**Important**: Headers are `x-application-key` and `x-auth-token`, NOT `Authorization: Bearer`

### Getting API Keys
- **Application Key**: Requires Grandmaster guild membership
  - Apply at: https://www.worldanvil.com/api/auth/key
- **User Token**: Generated from user API tokens page
  - Requires guild membership (any tier)

## API Resources

Based on openapi.yml, the API provides access to:

### Core Content
- **Articles** (`/article`, `/world/articles`)
- **Blocks** (`/block`, `/blockfolder`, `/blockfolder/blocks`)
- **Block Templates** (`/blocktemplate`, `/user/blocktemplates`, `/blocktemplatepart`)
- **Categories** (`/category`, `/world/categories`)

### Maps & Geography
- **Maps** (`/map`, `/world/maps`)
- **Layers** (`/layer`, `/map/layers`)
- **Markers** (`/marker`, `/map/markers`)
- **Marker Groups** (`/markergroup`, `/map/markergroups`)
- **Marker Types** (`/markertype`, `/markertypes`)

### Timelines & History
- **Timelines** (`/timeline`, `/world/timelines`)
- **Histories** (`/history`, `/world/histories`)
- **Chronicles** (commented out in spec)

### RPG Systems
- **RPG Systems** (`/rpgsystem`, `/rpgsystems`)

### Manuscripts & Writing
- **Manuscripts** (`/manuscript`, `/world/manuscripts`)
- **Manuscript Beats** (`/manuscript_beat`, `/manuscript_part/manuscript_beats`)
- **Manuscript Bookmarks** (`/manuscript_bookmark`, `/manuscript/manuscript_bookmarks`)
- **Manuscript Parts** (`/manuscript_part`, `/manuscript_version/manuscript_parts`)
- **Manuscript Versions** (`/manuscript_version`, `/manuscript/manuscript_versions`)
- **Manuscript Tags** (`/manuscript_tag`, `/manuscript/manuscript_tags`)
- **Manuscript Stats** (`/manuscript_stat`, `/manuscript_version/manuscript_stats`)
- **Manuscript Labels** (`/manuscript_label`, `/manuscript/manuscript_labels`)
- **Manuscript Plots** (`/manuscript_plot`, `/manuscript_version/manuscript_plots`)

### Notebooks & Notes
- **Notebooks** (`/notebook`, `/world/notebooks`)
- **Note Sections** (`/notesection`, `/notebook/notesections`)
- **Notes** (`/note`, `/notesection/notes`)

### Media
- **Images** (`/image`, `/world/images`)
- **Canvas** (`/canvas`, `/world/canvases`)

### Access Control
- **Secrets** (`/secret`, `/world/secrets`)
- **Subscriber Groups** (`/subscribergroup`, `/world/subscribergroups`)

### Variables
- **Variables** (`/variable`, `/variable_collection/variables`)
- **Variable Collections** (`/variable_collection`, `/world/variablecollections`)

### User & World
- **User** (`/user`, `/identity`)
- **World** (`/world`, `/user/worlds`)

## API Patterns

### Resource Endpoints
Pattern: `/resource` for single resource operations
Example: `/article`, `/map`, `/marker`

### Collection Endpoints
Pattern: `/parent/resources` for listing/filtering
Examples:
- `/world/articles` - List articles in world
- `/map/markers` - List markers on map
- `/notebook/notesections` - List sections in notebook

### Hierarchical Resources
Some resources are nested:
- `/blockfolder/blocks`
- `/blocktemplate/blocktemplateparts`
- `/map/layers`
- `/map/markergroups`
- `/markergroup/markers`

## OpenAPI Spec Structure

The main `openapi.yml` references external files in `parts/` directory:
```yaml
paths:
  /article:
    $ref: 'parts/article/article.yml#/article'
```

**Note**: The `parts/` directory is not included in current repo, only main `openapi.yml`

## Implementation Notes

### Priority Resources for D&D
1. **Articles** - Core content (NPCs, locations, items)
2. **Categories** - Organization
3. **Maps** - Geography and tactical maps
4. **Notebooks** - Session notes and planning
5. **Timelines** - Campaign chronology
6. **Secrets** - Hidden information for DM

### Lower Priority (Future)
- Manuscripts (for published content)
- Canvas (visual design)
- Variables (advanced templating)
- Block Templates (custom templates)

### Rate Limiting
- Implement exponential backoff
- Cache responses aggressively
- Batch requests where possible
- Default rate limit: 60 requests/minute (configurable)

### Caching Strategy
- Cache GET responses for 1 hour (default)
- Invalidate on write operations
- Use granularity parameter for cache keys
- Implement LRU cache with size limits

## Common Granularity Patterns

Many GET endpoints support `?granularity=<level>`:
- **0**: Minimum (preview/choice data)
- **1**: Standard (default display)
- **2**: Detailed (full data with relationships)

Use appropriate granularity:
- List operations: 0 or 1
- Detail views: 1 or 2
- Relationship mapping: 2
