Documentation Workflow
======================

This document describes the markdown-to-RST workflow for keeping documentation in sync.

Overview
--------

The World Anvil MCP Server uses a **hybrid documentation approach**:

- **Source**: Markdown files in ``docs/workflows/``, ``docs/quality/``, ``docs/research/``, ``docs/specs/``
- **Build**: Automatically transpiled to reStructuredText for Sphinx
- **Output**: Professional documentation on Read the Docs

This approach provides:

- ✅ Easy editing in Markdown
- ✅ Professional Sphinx/RTD output
- ✅ Automatic synchronization
- ✅ Single source of truth

Workflow
--------

Editing Documentation
~~~~~~~~~~~~~~~~~~~~~

1. **Edit markdown files** in their original locations:

   .. code-block:: bash

       # Workflow documentation
       vim docs/workflows/session-note-taking.md

       # Quality standards
       vim docs/quality/code-quality-rules.md

       # Research
       vim docs/research/pywaclient-analysis.md

       # Specifications
       vim docs/specs/tool-specifications.md

2. **Build documentation** - conversion happens automatically:

   .. code-block:: bash

       make docs

   This will:

   a. Run ``python scripts/md_to_rst.py`` to convert markdown to RST
   b. Build Sphinx documentation with converted files
   c. Output to ``docs/build/html/``

3. **Preview locally**:

   .. code-block:: bash

       make docs-serve

   Opens browser with live-reload enabled.

Automatic Conversion
~~~~~~~~~~~~~~~~~~~~

The ``scripts/md_to_rst.py`` script automatically:

- Converts all ``.md`` files to ``.rst`` format using pandoc
- Places converted files in appropriate Sphinx directories
- Maintains file structure and organization
- Reports conversion status for each file

**Conversion Mappings**:

.. code-block:: text

    docs/workflows/*.md         → docs/source/workflows/*.rst
    docs/quality/*.md           → docs/source/development/quality/*.rst
    docs/research/*.md          → docs/source/research/*.rst
    docs/specs/*.md             → docs/source/specs/*.rst

Manual Documentation
~~~~~~~~~~~~~~~~~~~~

Some documentation is written directly in RST for Sphinx:

- ``docs/source/index.rst`` - Main entry point
- ``docs/source/overview.rst`` - Project overview
- ``docs/source/installation.rst`` - Installation guide
- ``docs/source/quickstart.rst`` - Quick start guide
- ``docs/source/api/index.rst`` - API reference
- ``docs/source/development/index.rst`` - Development guide
- ``docs/source/architecture/index.rst`` - Architecture docs

Commands Reference
------------------

Documentation Build Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Install documentation dependencies
    make install-docs

    # Convert markdown to RST (runs automatically with make docs)
    make docs-sync

    # Build HTML documentation
    make docs

    # Serve with live reload
    make docs-serve

    # Check for broken links
    make docs-linkcheck

    # Clean all generated files
    make docs-clean

Requirements
------------

Pandoc Installation
~~~~~~~~~~~~~~~~~~~

The markdown-to-RST conversion requires pandoc:

**macOS**:

.. code-block:: bash

    brew install pandoc

**Ubuntu/Debian**:

.. code-block:: bash

    sudo apt-get install pandoc

**Windows**:

.. code-block:: bash

    choco install pandoc

Or download from: https://pandoc.org/installing.html

Python Dependencies
~~~~~~~~~~~~~~~~~~~

Install documentation dependencies:

.. code-block:: bash

    pip install -e ".[docs]"

This installs:

- sphinx>=7.2.0
- sphinx-rtd-theme>=2.0.0
- sphinx-autodoc-typehints>=1.25.0
- sphinx-autobuild>=2021.3.14
- myst-parser>=2.0.0

Directory Structure
-------------------

Source Files (Markdown)
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    docs/
    ├── workflows/          # 10 workflow markdown files
    │   ├── session-note-taking.md
    │   ├── npc-generation.md
    │   └── ...
    ├── quality/            # 4 quality standard files
    │   ├── code-quality-rules.md
    │   ├── testing-requirements.md
    │   └── ...
    ├── research/           # Research documents
    │   ├── pywaclient-analysis.md
    │   └── world-anvil-platform-summary.md
    └── specs/              # Technical specifications
        ├── tool-specifications.md
        └── client-architecture.md

Sphinx Structure (RST)
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    docs/source/
    ├── index.rst                   # Main entry point
    ├── overview.rst                # Manual RST
    ├── installation.rst            # Manual RST
    ├── quickstart.rst              # Manual RST
    ├── workflows/                  # Converted from markdown
    │   ├── index.rst               # Manual RST
    │   ├── session-note-taking.rst # AUTO-GENERATED
    │   └── ...                     # AUTO-GENERATED
    ├── development/
    │   ├── index.rst               # Manual RST
    │   └── quality/
    │       ├── index.rst           # Manual RST
    │       ├── code-quality-rules.rst  # AUTO-GENERATED
    │       └── ...                     # AUTO-GENERATED
    ├── research/
    │   ├── index.rst               # Manual RST
    │   └── pywaclient-analysis.rst # AUTO-GENERATED
    ├── specs/
    │   ├── index.rst               # Manual RST
    │   ├── tool-specifications.rst # AUTO-GENERATED
    │   └── client-architecture.rst # AUTO-GENERATED
    ├── api/
    │   └── index.rst               # Manual RST (auto-docs when code exists)
    └── architecture/
        └── index.rst               # Manual RST

Gitignore Configuration
-----------------------

Generated RST files are ignored by git:

.. code-block:: text

    # .gitignore

    # Generated RST files from markdown (auto-synced by scripts/md_to_rst.py)
    docs/source/workflows/*.rst
    docs/source/development/quality/
    docs/source/research/
    docs/source/specs/

This ensures:

- Only source markdown files are committed
- Generated RST files are created during build
- No duplication in version control
- Clean repository structure

Best Practices
--------------

Editing Guidelines
~~~~~~~~~~~~~~~~~~

1. **Edit markdown files only** - Never manually edit generated ``.rst`` files
2. **Run make docs** after editing to verify conversion
3. **Check broken links** with ``make docs-linkcheck`` before committing
4. **Preview changes** with ``make docs-serve`` for visual verification

Documentation Standards
~~~~~~~~~~~~~~~~~~~~~~~

Follow these standards for markdown files:

- Use ATX-style headers (``#``, ``##``, ``###``)
- Include code blocks with language specifiers
- Use relative links for cross-references
- Add frontmatter for metadata (workflow ID, category, etc.)
- Keep line length reasonable (<100 chars when practical)

Version Control
~~~~~~~~~~~~~~~

.. code-block:: bash

    # Commit source markdown files
    git add docs/workflows/new-workflow.md
    git commit -m "docs: add new workflow documentation"

    # Generated RST files are auto-created during build
    # Do NOT commit generated .rst files

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Pandoc not found**:

.. code-block:: text

    ❌ Error: pandoc is not installed

Solution: Install pandoc (see Requirements section)

**Conversion failures**:

.. code-block:: text

    ✗ Failed to convert workflow.md

Solution: Check markdown syntax, ensure file exists, verify pandoc works

**Broken links after conversion**:

.. code-block:: text

    WARNING: unknown document: 'workflows/session-note-taking'

Solution: Run ``make docs-linkcheck`` to identify issues, update references

**Sphinx build errors**:

.. code-block:: text

    Error: Unknown directive type "autosummary"

Solution: Ensure all sphinx extensions are installed (``make install-docs``)

Verification
~~~~~~~~~~~~

After making documentation changes:

.. code-block:: bash

    # 1. Clean previous build
    make docs-clean

    # 2. Convert and build
    make docs

    # 3. Check for broken links
    make docs-linkcheck

    # 4. Verify locally
    make docs-serve

CI/CD Integration
-----------------

Read the Docs Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``.readthedocs.yaml`` file configures automatic builds:

.. code-block:: yaml

    version: 2

    build:
      os: ubuntu-22.04
      tools:
        python: "3.11"
      jobs:
        post_checkout:
          # Install pandoc for markdown conversion
          - sudo apt-get update
          - sudo apt-get install -y pandoc

    python:
      install:
        - method: pip
          path: .
          extra_requirements:
            - docs

    formats:
      - pdf
      - epub

**Note**: Remember to install pandoc in the RTD build environment!

Development Workflow
--------------------

Typical Development Session
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # 1. Edit markdown documentation
    vim docs/workflows/my-workflow.md

    # 2. Build and preview
    make docs-serve

    # 3. Edit, save, auto-reload happens

    # 4. Check links
    make docs-linkcheck

    # 5. Commit source files only
    git add docs/workflows/my-workflow.md
    git commit -m "docs: add my-workflow documentation"

Adding New Documentation
~~~~~~~~~~~~~~~~~~~~~~~~

**New Workflow**:

1. Create ``docs/workflows/my-workflow.md``
2. Add entry to ``docs/source/workflows/index.rst`` toctree
3. Run ``make docs`` to convert and build
4. Verify with ``make docs-serve``

**New Quality Standard**:

1. Create ``docs/quality/my-standard.md``
2. Add entry to ``docs/source/development/quality/index.rst`` toctree
3. Run ``make docs`` to convert and build
4. Verify with ``make docs-serve``

See Also
--------

- :doc:`installation` - Installation guide
- :doc:`development/index` - Development guide
- :doc:`development/quality/documentation-standards` - Documentation standards
