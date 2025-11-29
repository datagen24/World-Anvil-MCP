# Context Engine MCP Specification

**Version**: 1.0  
**Status**: Draft  
**Created**: 2025-11-28  
**Project**: Standalone MCP Server  
**Purpose**: Semantic search over TTRPG reference materials for informed worldbuilding

---

## Executive Summary

The Context Engine provides **semantic search over curated reference materials** that inform worldbuilding decisions. This is NOT campaign content (that's World Anvil) - it's external knowledge that helps CREATE campaign content with accuracy, consistency, and inspiration.

**Core Value Proposition**: Transform "make up a dwarven blacksmith" into "create a culturally-grounded dwarven blacksmith informed by D&D lore, medieval smithing practices, and fantasy genre conventions."

---

## Problem Statement

When creating TTRPG content, GMs face several challenges:

1. **Lore Accuracy**: "What are dwarven cultural norms in D&D 5e?"
2. **Historical Grounding**: "How did medieval blacksmiths actually operate?"
3. **Genre Consistency**: "What tropes fit a gritty low-fantasy setting?"
4. **Naming Authenticity**: "What naming patterns fit this culture?"
5. **Rule Compliance**: "Is this magic item balanced for 5e?"

Currently, this requires manual research across multiple sources, breaking creative flow.

---

## Solution Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Context Engine MCP                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                      Query Interface                        │ │
│  │                                                             │ │
│  │  search_reference()  get_srd_content()  find_similar()     │ │
│  │  generate_inspiration()  list_corpora()  add_to_corpus()   │ │
│  └─────────────────────────┬──────────────────────────────────┘ │
│                            │                                     │
│  ┌─────────────────────────▼──────────────────────────────────┐ │
│  │                    Query Pipeline                           │ │
│  │                                                             │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌─────────┐ │ │
│  │  │  Parse   │──▶│  Embed   │──▶│  Search  │──▶│  Rank   │ │ │
│  │  │  Query   │   │  Query   │   │  Vector  │   │  Results│ │ │
│  │  └──────────┘   └──────────┘   └──────────┘   └─────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Vector Store                             │ │
│  │                                                             │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │  ChromaDB   │  │   Index     │  │  Metadata   │        │ │
│  │  │  (Default)  │  │  Segments   │  │   Store     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   Corpus Registry                           │ │
│  │                                                             │ │
│  │  System Corpora          │  User Corpora                   │ │
│  │  ─────────────────────   │  ────────────────────           │ │
│  │  • dnd5e_srd             │  • user_campaign_notes          │ │
│  │  • pathfinder2e_srd      │  • user_homebrew_rules          │ │
│  │  • fantasy_tropes        │  • user_setting_docs            │ │
│  │  • medieval_history      │                                 │ │
│  │  • mythology_public      │                                 │ │
│  │  • naming_patterns       │                                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## MCP Interface Specification

### Tools

```yaml
tools:
  # ═══════════════════════════════════════════════════════════════
  # SEARCH OPERATIONS
  # ═══════════════════════════════════════════════════════════════
  
  - name: search_reference
    description: |
      Semantic search across reference corpora. Returns passages 
      conceptually related to the query, not just keyword matches.
    parameters:
      query:
        type: string
        description: Natural language search query
        required: true
      corpus:
        type: array
        items: string
        description: |
          Corpora to search. If omitted, searches all available.
          Examples: ["dnd5e_srd", "medieval_history"]
        required: false
      limit:
        type: integer
        description: Maximum results to return
        default: 5
        minimum: 1
        maximum: 20
      similarity_threshold:
        type: number
        description: Minimum relevance score (0.0-1.0)
        default: 0.7
        minimum: 0.0
        maximum: 1.0
      include_metadata:
        type: boolean
        description: Include source metadata in results
        default: true
    returns:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: "#/models/SearchResult"
        query_embedding_time_ms: number
        search_time_ms: number

  - name: find_similar
    description: |
      Find content similar to provided text. Useful for finding 
      inspiration based on existing content.
    parameters:
      text:
        type: string
        description: Source text to find similarities for
        required: true
      corpus:
        type: array
        items: string
        description: Corpora to search
        required: false
      limit:
        type: integer
        default: 5
      exclude_exact:
        type: boolean
        description: Exclude exact matches
        default: true
    returns:
      type: object
      properties:
        results:
          type: array
          items:
            $ref: "#/models/SearchResult"

  # ═══════════════════════════════════════════════════════════════
  # SRD OPERATIONS
  # ═══════════════════════════════════════════════════════════════

  - name: get_srd_content
    description: |
      Retrieve specific SRD content by system, category, and name.
      For direct lookups when you know what you're looking for.
    parameters:
      system:
        type: string
        description: Game system identifier
        enum: ["dnd5e", "pathfinder2e", "osr"]
        required: true
      category:
        type: string
        description: Content category
        enum: 
          - monsters
          - spells
          - classes
          - races
          - items
          - conditions
          - rules
        required: true
      name:
        type: string
        description: |
          Specific item name (optional). If omitted, returns 
          category index.
        required: false
      include_related:
        type: boolean
        description: Include related content links
        default: false
    returns:
      type: object
      properties:
        content: string
        source: string
        related:
          type: array
          items: string

  - name: lookup_rule
    description: |
      Look up a specific game rule or mechanic.
    parameters:
      system:
        type: string
        enum: ["dnd5e", "pathfinder2e"]
        required: true
      topic:
        type: string
        description: Rule topic to look up
        required: true
    returns:
      type: object
      properties:
        rule_text: string
        source: string
        page_reference: string

  # ═══════════════════════════════════════════════════════════════
  # INSPIRATION OPERATIONS
  # ═══════════════════════════════════════════════════════════════

  - name: get_inspiration
    description: |
      Get contextual inspiration for content creation. Combines
      relevant reference material into actionable suggestions.
    parameters:
      content_type:
        type: string
        description: Type of content being created
        enum: ["npc", "location", "item", "organization", "plot", "culture"]
        required: true
      constraints:
        type: object
        description: |
          Type-specific constraints to guide inspiration.
          See examples for each content_type.
        required: true
      tone:
        type: string
        description: Desired tone/style
        enum: ["heroic", "gritty", "comedic", "horror", "mysterious"]
        default: "heroic"
      system:
        type: string
        description: Game system for mechanical context
        enum: ["dnd5e", "pathfinder2e", "system_agnostic"]
        default: "dnd5e"
    returns:
      type: object
      properties:
        inspiration:
          $ref: "#/models/InspirationResult"
        sources_consulted:
          type: array
          items: string

  - name: generate_names
    description: |
      Generate culturally appropriate names based on patterns.
    parameters:
      culture:
        type: string
        description: Cultural basis for names
        required: true
      type:
        type: string
        description: Type of name
        enum: ["person", "place", "organization", "item"]
        default: "person"
      gender:
        type: string
        description: For person names
        enum: ["masculine", "feminine", "neutral"]
        required: false
      count:
        type: integer
        description: Number of names to generate
        default: 5
        maximum: 20
    returns:
      type: object
      properties:
        names:
          type: array
          items:
            type: object
            properties:
              name: string
              meaning: string
              notes: string

  # ═══════════════════════════════════════════════════════════════
  # CORPUS MANAGEMENT
  # ═══════════════════════════════════════════════════════════════

  - name: list_corpora
    description: List all available reference corpora
    parameters: {}
    returns:
      type: object
      properties:
        system_corpora:
          type: array
          items:
            $ref: "#/models/CorpusInfo"
        user_corpora:
          type: array
          items:
            $ref: "#/models/CorpusInfo"

  - name: get_corpus_info
    description: Get detailed information about a corpus
    parameters:
      corpus_id:
        type: string
        required: true
    returns:
      $ref: "#/models/CorpusInfo"

  - name: add_to_user_corpus
    description: |
      Add content to a user corpus. Creates corpus if it doesn't exist.
    parameters:
      corpus_name:
        type: string
        description: User corpus identifier
        required: true
      content:
        type: string
        description: Content to add
        required: true
      title:
        type: string
        description: Title/identifier for this content
        required: true
      metadata:
        type: object
        description: Optional metadata
        required: false
    returns:
      type: object
      properties:
        document_id: string
        corpus_id: string
        chunks_created: integer

  - name: remove_from_user_corpus
    description: Remove content from a user corpus
    parameters:
      corpus_name:
        type: string
        required: true
      document_id:
        type: string
        required: true
    returns:
      type: object
      properties:
        success: boolean

  - name: import_document
    description: |
      Import a document file into a user corpus. Supports PDF, 
      Markdown, and plain text.
    parameters:
      corpus_name:
        type: string
        required: true
      file_path:
        type: string
        description: Path to document file
        required: true
      title:
        type: string
        description: Title for the document
        required: false
    returns:
      type: object
      properties:
        document_id: string
        chunks_created: integer
        warnings: array
```

### Resources

```yaml
resources:
  - uri_template: corpus://{corpus_id}
    description: |
      Access corpus as a context resource. Useful for providing
      full corpus context to LLM.
    
  - uri_template: srd://{system}/{category}
    description: |
      Access SRD category as context. Example: srd://dnd5e/monsters
    
  - uri_template: srd://{system}/{category}/{name}
    description: |
      Access specific SRD entry. Example: srd://dnd5e/monsters/goblin
```

### Models

```yaml
models:
  SearchResult:
    type: object
    properties:
      content:
        type: string
        description: Matched content passage
      relevance:
        type: number
        description: Similarity score (0.0-1.0)
      source:
        type: object
        properties:
          corpus: string
          document: string
          chunk_id: string
      metadata:
        type: object
        description: Source-specific metadata
      highlight:
        type: string
        description: Content with query terms highlighted

  CorpusInfo:
    type: object
    properties:
      id:
        type: string
      name:
        type: string
      description:
        type: string
      document_count:
        type: integer
      chunk_count:
        type: integer
      last_updated:
        type: string
        format: datetime
      license:
        type: string
      is_user_corpus:
        type: boolean

  InspirationResult:
    type: object
    properties:
      summary:
        type: string
        description: Concise inspiration summary
      details:
        type: object
        description: Type-specific detailed suggestions
      reference_excerpts:
        type: array
        items:
          type: object
          properties:
            source: string
            excerpt: string
            relevance: string
      suggested_hooks:
        type: array
        items: string
```

---

## Corpus Specifications

### System Corpora (Pre-loaded)

#### dnd5e_srd
- **Source**: [D&D 5e SRD 5.1](https://dnd.wizards.com/resources/systems-reference-document)
- **License**: Creative Commons Attribution 4.0
- **Content**: Races, classes, spells, monsters, magic items, conditions, combat rules
- **Chunk Strategy**: By entity (one monster = one chunk), rules by section
- **Estimated Size**: ~3,000 chunks

#### pathfinder2e_srd
- **Source**: [Archives of Nethys](https://2e.aonprd.com/) (OGL content)
- **License**: Open Game License
- **Content**: Ancestries, classes, spells, creatures, equipment
- **Chunk Strategy**: By entity
- **Estimated Size**: ~5,000 chunks

#### fantasy_tropes
- **Source**: Curated from public domain worldbuilding guides, TV Tropes (CC content)
- **License**: Mixed (CC, Public Domain)
- **Content**: Character archetypes, plot patterns, setting conventions, genre expectations
- **Chunk Strategy**: By trope/concept
- **Estimated Size**: ~1,500 chunks

#### medieval_history
- **Source**: Wikipedia (CC), Project Gutenberg, academic sources (public domain)
- **License**: CC BY-SA, Public Domain
- **Content**: Feudal society, castle architecture, medieval warfare, daily life, trade, guilds
- **Chunk Strategy**: By topic
- **Estimated Size**: ~2,000 chunks

#### mythology_public
- **Source**: Project Gutenberg, Sacred Texts Archive
- **License**: Public Domain
- **Content**: Greek, Norse, Celtic, Egyptian, Mesopotamian myths and legends
- **Chunk Strategy**: By story/deity/concept
- **Estimated Size**: ~2,500 chunks

#### naming_patterns
- **Source**: Linguistic databases, etymology resources
- **License**: Various (compiled)
- **Content**: Name origins, cultural naming conventions, phonetic patterns
- **Chunk Strategy**: By culture/pattern
- **Estimated Size**: ~1,000 chunks

### User Corpora

Users can create custom corpora for:
- Campaign-specific setting documents
- Homebrew rules and content
- Purchased content they own (user's responsibility for licensing)
- Session notes and established lore

**Storage**: User corpora stored in `~/.context-engine/user_corpora/`

---

## Technical Implementation

### Embedding Model

**Primary**: `sentence-transformers/all-MiniLM-L6-v2`
- 384 dimensions
- Fast inference (~14ms per query)
- Good semantic quality for our use case
- Apache 2.0 license

**Alternative for Quality**: `sentence-transformers/all-mpnet-base-v2`
- 768 dimensions
- Slower but higher quality
- Use if quality issues arise

### Vector Store

**Primary**: ChromaDB
- Embedded mode (no separate server)
- Persistent storage
- Metadata filtering
- Python-native

```python
import chromadb
from chromadb.config import Settings

client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="~/.context-engine/vectordb",
    anonymized_telemetry=False
))
```

**Alternative**: FAISS
- If ChromaDB has issues
- More manual metadata handling

### Chunking Strategy

```python
from dataclasses import dataclass

@dataclass
class ChunkConfig:
    """Chunking configuration by content type."""
    
    chunk_size: int = 512        # Target tokens per chunk
    chunk_overlap: int = 50      # Overlap for context continuity
    respect_boundaries: bool = True  # Don't split mid-sentence
    
# Content-specific configs
CHUNK_CONFIGS = {
    "srd_monster": ChunkConfig(chunk_size=800, chunk_overlap=0),  # Keep monsters whole
    "srd_spell": ChunkConfig(chunk_size=400, chunk_overlap=0),    # Spells are small
    "narrative": ChunkConfig(chunk_size=512, chunk_overlap=100),  # Stories need context
    "rules": ChunkConfig(chunk_size=256, chunk_overlap=50),       # Rules are dense
}
```

### Query Pipeline

```python
async def search_reference(
    query: str,
    corpus: list[str] | None = None,
    limit: int = 5,
    similarity_threshold: float = 0.7,
) -> SearchResults:
    """Execute semantic search across corpora."""
    
    # 1. Embed query
    query_embedding = await embed_text(query)
    
    # 2. Determine target collections
    if corpus:
        collections = [get_collection(c) for c in corpus]
    else:
        collections = get_all_collections()
    
    # 3. Search each collection
    all_results = []
    for collection in collections:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=limit * 2,  # Over-fetch for filtering
            include=["documents", "metadatas", "distances"]
        )
        all_results.extend(normalize_results(results, collection.name))
    
    # 4. Filter by threshold and dedupe
    filtered = [
        r for r in all_results 
        if r.relevance >= similarity_threshold
    ]
    
    # 5. Rank and limit
    ranked = sorted(filtered, key=lambda r: r.relevance, reverse=True)
    return SearchResults(results=ranked[:limit])
```

---

## Integration Patterns

### With World Anvil MCP

```python
# In World Anvil MCP - NPC creation workflow
async def create_informed_npc(
    world_id: str,
    name: str,
    race: str,
    profession: str,
) -> Article:
    """Create NPC with Context Engine research."""
    
    # Check if Context Engine is available
    if not ecosystem.has("Context Engine"):
        # Fall back to basic creation
        return await create_basic_npc(world_id, name, race, profession)
    
    # Get cultural context
    cultural = await context_engine.search_reference(
        query=f"{race} culture society values traditions",
        corpus=["dnd5e_srd", "fantasy_tropes"],
        limit=3
    )
    
    # Get profession context
    prof_context = await context_engine.search_reference(
        query=f"{profession} medieval fantasy role duties",
        corpus=["medieval_history", "fantasy_tropes"],
        limit=2
    )
    
    # Get inspiration
    inspiration = await context_engine.get_inspiration(
        content_type="npc",
        constraints={
            "race": race,
            "profession": profession,
            "cultural_context": cultural.results[0].content if cultural.results else None
        },
        system="dnd5e"
    )
    
    # Generate article with full context
    article_content = generate_npc_content(
        name=name,
        race=race,
        profession=profession,
        cultural_context=cultural,
        profession_context=prof_context,
        inspiration=inspiration
    )
    
    return await world_anvil.create_article(
        world_id=world_id,
        title=name,
        template="character",
        content=article_content
    )
```

### Standalone Usage

```python
# Direct Context Engine queries

# Research for worldbuilding
results = await context_engine.search_reference(
    query="dwarven fortress defensive architecture traps",
    corpus=["dnd5e_srd", "medieval_history", "fantasy_tropes"]
)

# SRD lookup
goblin = await context_engine.get_srd_content(
    system="dnd5e",
    category="monsters", 
    name="goblin"
)

# Name generation
names = await context_engine.generate_names(
    culture="norse",
    type="person",
    gender="masculine",
    count=10
)

# Add custom content
await context_engine.add_to_user_corpus(
    corpus_name="eberron_setting",
    title="Dragonmarked Houses Overview",
    content="The Dragonmarked Houses are...",
    metadata={"source": "Eberron Campaign Setting", "chapter": 3}
)
```

---

## Configuration

### Server Configuration

```yaml
# ~/.context-engine/config.yaml

server:
  host: localhost
  port: 8765  # Default MCP port

embedding:
  model: sentence-transformers/all-MiniLM-L6-v2
  device: cpu  # or cuda
  batch_size: 32

storage:
  vector_db: chromadb
  persist_path: ~/.context-engine/vectordb
  user_corpora_path: ~/.context-engine/user_corpora

corpora:
  # Enable/disable system corpora
  dnd5e_srd: true
  pathfinder2e_srd: true
  fantasy_tropes: true
  medieval_history: true
  mythology_public: true
  naming_patterns: true

search:
  default_limit: 5
  default_threshold: 0.7
  max_limit: 20

logging:
  level: INFO
  file: ~/.context-engine/logs/context-engine.log
```

### Environment Variables

```bash
CONTEXT_ENGINE_CONFIG=~/.context-engine/config.yaml
CONTEXT_ENGINE_CACHE_DIR=~/.context-engine/cache
CONTEXT_ENGINE_LOG_LEVEL=INFO
```

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- ~2GB disk space for corpora
- ~500MB RAM for embedding model

### Installation

```bash
# Install from PyPI (future)
pip install context-engine-mcp

# Or from source
git clone https://github.com/datagen24/context-engine-mcp
cd context-engine-mcp
pip install -e .

# Initialize corpora (downloads and indexes)
context-engine init

# Start server
context-engine serve
```

### First Run

```bash
$ context-engine init

Context Engine Initialization
=============================

Downloading corpora...
  ✓ dnd5e_srd (12.3 MB)
  ✓ pathfinder2e_srd (18.7 MB)
  ✓ fantasy_tropes (3.2 MB)
  ✓ medieval_history (8.1 MB)
  ✓ mythology_public (5.4 MB)
  ✓ naming_patterns (1.1 MB)

Building embeddings...
  ✓ dnd5e_srd (3,042 chunks)
  ✓ pathfinder2e_srd (5,128 chunks)
  ✓ fantasy_tropes (1,487 chunks)
  ✓ medieval_history (2,103 chunks)
  ✓ mythology_public (2,534 chunks)
  ✓ naming_patterns (892 chunks)

Total: 15,186 chunks indexed
Storage: 847 MB

Ready! Run 'context-engine serve' to start the MCP server.
```

---

## Project Structure

```
context-engine-mcp/
├── src/
│   └── context_engine/
│       ├── __init__.py
│       ├── server.py           # MCP server implementation
│       ├── config.py           # Configuration management
│       ├── embedding/
│       │   ├── __init__.py
│       │   ├── models.py       # Embedding model wrapper
│       │   └── chunking.py     # Text chunking strategies
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── chromadb.py     # ChromaDB implementation
│       │   └── corpus.py       # Corpus management
│       ├── search/
│       │   ├── __init__.py
│       │   ├── semantic.py     # Semantic search
│       │   └── srd.py          # SRD-specific lookups
│       ├── inspiration/
│       │   ├── __init__.py
│       │   └── generator.py    # Inspiration generation
│       ├── corpora/
│       │   ├── __init__.py
│       │   ├── loaders/        # Corpus-specific loaders
│       │   └── schemas/        # Corpus metadata schemas
│       └── cli.py              # Command-line interface
├── corpora/
│   ├── dnd5e_srd/              # D&D 5e SRD source files
│   ├── pathfinder2e_srd/
│   ├── fantasy_tropes/
│   ├── medieval_history/
│   ├── mythology_public/
│   └── naming_patterns/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── docs/
│   ├── GETTING_STARTED.md
│   ├── CORPORA.md
│   └── API.md
├── pyproject.toml
├── README.md
└── LICENSE
```

---

## Roadmap

### Phase 1: Core Infrastructure
- [ ] MCP server skeleton
- [ ] ChromaDB integration
- [ ] Embedding pipeline
- [ ] Basic search_reference tool

### Phase 2: System Corpora
- [ ] D&D 5e SRD ingestion
- [ ] Pathfinder 2e SRD ingestion
- [ ] get_srd_content tool
- [ ] lookup_rule tool

### Phase 3: Reference Corpora
- [ ] Fantasy tropes corpus
- [ ] Medieval history corpus
- [ ] Mythology corpus
- [ ] Naming patterns corpus

### Phase 4: Inspiration Engine
- [ ] get_inspiration tool
- [ ] generate_names tool
- [ ] find_similar tool

### Phase 5: User Corpora
- [ ] User corpus management
- [ ] Document import (PDF, MD, TXT)
- [ ] Corpus CRUD operations

### Phase 6: Integration
- [ ] World Anvil MCP integration testing
- [ ] Documentation
- [ ] PyPI release

---

## Open Questions

1. **Hosting Model**: Local-only, or offer cloud option for users without local compute?

2. **Corpus Updates**: How to handle SRD updates? Manual rebuild or automatic?

3. **Copyright Boundaries**: Clear guidance on what users can add to personal corpora?

4. **Caching**: Cache query embeddings? Cache popular searches?

5. **Multi-tenancy**: Single user or support multiple users with separate corpora?

---

## References

- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://www.trychroma.com/)
- [D&D 5e SRD](https://dnd.wizards.com/resources/systems-reference-document)
- [Archives of Nethys](https://2e.aonprd.com/)
- [MCP Specification](https://modelcontextprotocol.io/)
