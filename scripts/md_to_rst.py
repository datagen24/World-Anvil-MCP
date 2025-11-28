#!/usr/bin/env python3
"""Convert markdown documentation files to reStructuredText for Sphinx.

This script automatically transpiles .md files from various docs folders
into .rst files in the appropriate Sphinx documentation structure.

Usage:
    python scripts/md_to_rst.py
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def check_pandoc() -> bool:
    """Check if pandoc is installed and available.

    Returns:
        True if pandoc is available, False otherwise.
    """
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"✓ Found {result.stdout.splitlines()[0]}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def convert_md_to_rst(md_file: Path, rst_file: Path) -> bool:
    """Convert a markdown file to reStructuredText using pandoc.

    Args:
        md_file: Path to source .md file
        rst_file: Path to destination .rst file

    Returns:
        True if conversion successful, False otherwise.
    """
    try:
        # Ensure output directory exists
        rst_file.parent.mkdir(parents=True, exist_ok=True)

        # Convert using pandoc with Sphinx-friendly options
        subprocess.run(
            [
                "pandoc",
                str(md_file),
                "-f", "markdown",
                "-t", "rst",
                "--wrap=none",  # Don't wrap lines
                "-o", str(rst_file),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"  ✓ {md_file.name} → {rst_file.relative_to(rst_file.parents[2])}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ Failed to convert {md_file.name}: {e.stderr}")
        return False


def get_conversion_mappings() -> Dict[str, List[tuple[Path, Path]]]:
    """Define which markdown files should be converted to which RST locations.

    Returns:
        Dictionary mapping category names to list of (source, destination) tuples.
    """
    project_root = Path(__file__).parent.parent
    docs_root = project_root / "docs"
    sphinx_source = docs_root / "source"

    mappings = {
        "workflows": [],
        "quality": [],
        "research": [],
        "specs": [],
    }

    # Workflow documents (10 workflow .md files)
    workflows_dir = docs_root / "workflows"
    workflow_files = [
        "d-and-d-campaign-setup.md",
        "session-note-taking.md",
        "npc-generation.md",
        "location-development.md",
        "quick-npc-lookup.md",
        "world-building.md",
        "map-management.md",
        "quest-plot-management.md",
        "session-prep.md",
        "content-search.md",
    ]

    for workflow_file in workflow_files:
        src = workflows_dir / workflow_file
        if src.exists():
            # Convert to .rst with same name
            rst_name = workflow_file.replace(".md", ".rst")
            dst = sphinx_source / "workflows" / rst_name
            mappings["workflows"].append((src, dst))

    # Quality standards documents
    quality_dir = docs_root / "quality"
    quality_files = [
        "code-quality-rules.md",
        "testing-requirements.md",
        "documentation-standards.md",
        "api-client-patterns.md",
    ]

    for quality_file in quality_files:
        src = quality_dir / quality_file
        if src.exists():
            rst_name = quality_file.replace(".md", ".rst")
            dst = sphinx_source / "development" / "quality" / rst_name
            mappings["quality"].append((src, dst))

    # Research documents
    research_dir = docs_root / "research"
    research_files = [
        "world-anvil-platform-summary.md",
        "pywaclient-analysis.md",
    ]

    for research_file in research_files:
        src = research_dir / research_file
        if src.exists():
            rst_name = research_file.replace(".md", ".rst")
            dst = sphinx_source / "research" / rst_name
            mappings["research"].append((src, dst))

    # Specification documents
    specs_dir = docs_root / "specs"
    specs_files = [
        "tool-specifications.md",
        "client-architecture.md",
    ]

    for specs_file in specs_files:
        src = specs_dir / specs_file
        if src.exists():
            rst_name = specs_file.replace(".md", ".rst")
            dst = sphinx_source / "specs" / rst_name
            mappings["specs"].append((src, dst))

    return mappings


def main() -> int:
    """Main entry point for markdown to RST conversion.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    print("📝 Converting Markdown to reStructuredText for Sphinx...\n")

    # Check for pandoc
    if not check_pandoc():
        print("\n❌ Error: pandoc is not installed")
        print("\nInstall pandoc:")
        print("  macOS:   brew install pandoc")
        print("  Ubuntu:  sudo apt-get install pandoc")
        print("  Windows: choco install pandoc")
        print("\nOr visit: https://pandoc.org/installing.html")
        return 1

    print()

    # Get conversion mappings
    mappings = get_conversion_mappings()

    # Convert files by category
    total_converted = 0
    total_failed = 0

    for category, files in mappings.items():
        if not files:
            continue

        print(f"🔄 Converting {category} documentation:")

        for src, dst in files:
            if convert_md_to_rst(src, dst):
                total_converted += 1
            else:
                total_failed += 1

        print()

    # Summary
    print("─" * 60)
    print(f"✅ Successfully converted: {total_converted} files")
    if total_failed > 0:
        print(f"❌ Failed: {total_failed} files")
        return 1

    print("\n💡 Run 'make docs' to build the updated documentation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
