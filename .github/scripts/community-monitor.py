#!/usr/bin/env python3
"""Monitor community sources for Claude Code features, tips, and tricks.

Fetches content from community sources (claudelog.com, awesome-claude-code,
awesome-claude-code-plugins) and identifies entries not yet covered by
existing community docs.

Usage:
    python community-monitor.py \\
        --community-docs-dir PATH \\
        --sources-dir PATH \\
        [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
"""

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Source definitions
# ---------------------------------------------------------------------------

SOURCES: list[dict[str, str]] = [
    {
        "name": "claudelog",
        "url": "https://claudelog.com/claude-code-changelog/",
        "type": "html",
        "description": "Third-party CC changelog aggregator with community annotations",
    },
    {
        "name": "awesome-claude-code",
        "url": "https://raw.githubusercontent.com/hesreallyhim/awesome-claude-code/main/README.md",
        "type": "markdown",
        "description": "Curated resource list (skills, workflows, tooling, hooks, commands)",
    },
    {
        "name": "awesome-claude-code-plugins",
        "url": "https://raw.githubusercontent.com/ccplugins/awesome-claude-code-plugins/main/README.md",
        "type": "markdown",
        "description": "Installable plugin registry with marketplace format",
    },
]


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

def fetch_source(url: str, timeout: int = 30) -> str:
    """Fetch text content from a URL."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "cc-community-monitor/1.0"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_markdown_entries(text: str) -> list[dict[str, str]]:
    """Extract list entries and headings from markdown content.

    Returns list of {heading, entry} dicts representing notable items.
    """
    entries: list[dict[str, str]] = []
    current_heading = ""

    for line in text.splitlines():
        h_match = re.match(r"^(#{1,4})\s+(.*)", line)
        if h_match:
            current_heading = h_match.group(2).strip()
            continue

        # Match markdown list items with links: - [Name](url) - description
        # or plain list items: - **Name** - description
        link_match = re.match(
            r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*[-–—:]?\s*(.*)", line
        )
        if link_match:
            entries.append({
                "heading": current_heading,
                "name": link_match.group(1).strip(),
                "url": link_match.group(2).strip(),
                "description": link_match.group(3).strip(),
            })
            continue

        bold_match = re.match(
            r"^\s*[-*]\s+\*\*([^*]+)\*\*\s*[-–—:]?\s*(.*)", line
        )
        if bold_match:
            entries.append({
                "heading": current_heading,
                "name": bold_match.group(1).strip(),
                "url": "",
                "description": bold_match.group(2).strip(),
            })

    return entries


def extract_html_entries(text: str) -> list[dict[str, str]]:
    """Extract notable entries from HTML content (claudelog).

    Looks for headings and list-like content patterns.
    """
    entries: list[dict[str, str]] = []

    # Extract text from HTML by stripping tags (simple approach)
    clean = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<[^>]+>", "\n", clean)
    clean = re.sub(r"\n{3,}", "\n\n", clean)

    # Extract lines that look like feature descriptions
    current_heading = ""
    for line in clean.splitlines():
        line = line.strip()
        if not line or len(line) < 10:
            continue

        # Lines that look like version headers or feature titles
        version_match = re.match(r"^v?(\d+\.\d+\.\d+)", line)
        if version_match:
            current_heading = line
            continue

        # Lines with feature-like keywords
        feature_keywords = {
            "added", "new", "feature", "support", "improved", "fix",
            "hook", "plugin", "skill", "agent", "team", "command",
            "tool", "mode", "config", "memory", "context", "remote",
        }
        line_words = set(line.lower().split())
        if line_words & feature_keywords and len(line) > 20:
            entries.append({
                "heading": current_heading,
                "name": line[:80],
                "url": "",
                "description": line,
            })

    return entries


# ---------------------------------------------------------------------------
# Coverage checking
# ---------------------------------------------------------------------------

def build_doc_keywords(community_docs_dir: Path) -> set[str]:
    """Build a keyword set from existing community docs."""
    keywords: set[str] = set()
    for md_file in sorted(community_docs_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        words = re.findall(r"[A-Za-z0-9_/-]{4,}", text)
        keywords.update(w.lower() for w in words)
    return keywords


def entry_fingerprint(entry: dict[str, str]) -> str:
    """Generate a stable fingerprint for an entry."""
    key = f"{entry.get('name', '')}|{entry.get('url', '')}".lower()
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def is_covered(entry: dict[str, str], doc_keywords: set[str]) -> bool:
    """Check if an entry's key terms appear in existing docs."""
    entry_text = f"{entry.get('name', '')} {entry.get('description', '')}"
    entry_words = {
        w.lower()
        for w in re.findall(r"[A-Za-z0-9_/-]{4,}", entry_text)
    }
    # Remove common words that match too broadly
    noise = {
        "claude", "code", "with", "that", "this", "from", "have",
        "been", "will", "your", "more", "tool", "tools", "https",
        "github", "added", "fixed", "support", "feature",
    }
    entry_words -= noise

    if not entry_words:
        return True  # No meaningful keywords to match

    overlap = entry_words & doc_keywords
    # Consider covered if >40% of entry keywords appear in docs
    return len(overlap) / len(entry_words) > 0.4


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state(state_file: Path) -> dict[str, list[str]]:
    """Load previously seen entry fingerprints per source."""
    if state_file.exists():
        return json.loads(state_file.read_text(encoding="utf-8"))
    return {}


def save_state(
    state_file: Path, state: dict[str, list[str]]
) -> None:
    """Save seen entry fingerprints."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(
        json.dumps(state, indent=2) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(
    source_results: list[dict],
) -> tuple[str, bool]:
    """Build a markdown report of uncovered community content.

    Returns (report_text, has_new_content).
    """
    lines: list[str] = [
        "## Community Monitor Report",
        "",
        f"Sources checked: **{len(source_results)}**",
        "",
    ]

    total_new = 0

    for result in source_results:
        name = result["name"]
        new_entries = result["new_entries"]
        total_new += len(new_entries)

        lines += [
            f"### {name}",
            "",
            f"- Source: {result['description']}",
            f"- Entries fetched: {result['total']}",
            f"- New uncovered: {len(new_entries)}",
            "",
        ]

        if new_entries:
            lines.append("| Entry | Section | Description |")
            lines.append("|-------|---------|-------------|")
            for entry in new_entries[:30]:  # Cap at 30 per source
                name_col = entry.get("name", "")[:60]
                heading = entry.get("heading", "")[:40]
                desc = entry.get("description", "")[:80]
                # Escape pipe chars in table cells
                name_col = name_col.replace("|", "\\|")
                heading = heading.replace("|", "\\|")
                desc = desc.replace("|", "\\|")
                lines.append(f"| {name_col} | {heading} | {desc} |")
            lines.append("")

            if len(new_entries) > 30:
                lines.append(
                    f"_... and {len(new_entries) - 30} more entries._"
                )
                lines.append("")

    lines += [
        "---",
        f"Total new uncovered entries: **{total_new}**",
        "",
        "_Generated by `.github/scripts/community-monitor.py`_",
        "",
    ]

    return "\n".join(lines), total_new > 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the community monitor script."""
    parser = argparse.ArgumentParser(
        description="Monitor community sources for CC features and tips."
    )
    parser.add_argument(
        "--community-docs-dir", required=True, type=Path,
        help="Path to docs/community/ directory",
    )
    parser.add_argument(
        "--state-file", type=Path,
        default=Path(".github/state/community-monitor-state.json"),
        help="Path to state file tracking previously seen entries",
    )
    args = parser.parse_args()

    if not args.community_docs_dir.exists():
        sys.exit(
            f"ERROR: Community docs dir does not exist: {args.community_docs_dir}"
        )

    # Build keyword index from existing community docs
    doc_keywords = build_doc_keywords(args.community_docs_dir)
    print(f"Doc keywords indexed: {len(doc_keywords)}", file=sys.stderr)

    # Load previous state
    state = load_state(args.state_file)

    source_results: list[dict] = []

    for source in SOURCES:
        name = source["name"]
        print(f"Fetching {name}: {source['url']}", file=sys.stderr)

        try:
            content = fetch_source(source["url"])
        except Exception as e:
            print(f"WARNING: Failed to fetch {name}: {e}", file=sys.stderr)
            source_results.append({
                "name": name,
                "description": source["description"],
                "total": 0,
                "new_entries": [],
            })
            continue

        # Extract entries based on content type
        if source["type"] == "markdown":
            entries = extract_markdown_entries(content)
        else:
            entries = extract_html_entries(content)

        print(f"  Extracted {len(entries)} entries", file=sys.stderr)

        # Filter to entries not previously seen and not covered by docs
        seen = set(state.get(name, []))
        new_entries: list[dict[str, str]] = []

        for entry in entries:
            fp = entry_fingerprint(entry)
            if fp in seen:
                continue
            if not is_covered(entry, doc_keywords):
                new_entries.append(entry)

        print(f"  New uncovered: {len(new_entries)}", file=sys.stderr)

        # Update state with all current fingerprints
        state[name] = [entry_fingerprint(e) for e in entries]

        source_results.append({
            "name": name,
            "description": source["description"],
            "total": len(entries),
            "new_entries": new_entries,
        })

    # Save updated state
    save_state(args.state_file, state)
    print(f"State saved to {args.state_file}", file=sys.stderr)

    # Build and output report
    report, has_new = build_report(source_results)
    print(report)

    sys.exit(1 if has_new else 0)


if __name__ == "__main__":
    main()
