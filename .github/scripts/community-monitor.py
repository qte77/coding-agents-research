#!/usr/bin/env python3
"""Monitor community sources for Claude Code features, tips, and tricks.

Fetches content from community sources (claudelog.com, awesome-claude-code,
awesome-claude-code-plugins, Reddit, X) and identifies entries not yet
covered by existing community docs.

Usage:
    python community-monitor.py \\
        --community-docs-dir PATH \\
        [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import (
    build_doc_keywords,
    entry_fingerprint,
    fetch_text,
    is_covered,
    load_state,
    save_state,
)

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
    {
        "name": "reddit-claudeai",
        "url": "https://oauth.reddit.com/r/ClaudeAI/search.json?q=claude+code&sort=new&limit=100&restrict_sr=1",
        "type": "reddit",
        "auth": "reddit",
        "description": "r/ClaudeAI posts mentioning Claude Code",
    },
    {
        "name": "x-claudecode",
        "url": "https://api.x.com/2/tweets/search/recent?query=%23ClaudeCode&max_results=100&tweet.fields=text,created_at",
        "type": "x",
        "auth": "x_bearer",
        "description": "X/Twitter posts with #ClaudeCode hashtag",
    },
]


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
# Reddit / X fetching and extraction
# ---------------------------------------------------------------------------

def fetch_reddit(url: str, client_id: str, client_secret: str) -> list[dict[str, str]]:
    """Fetch Reddit search results using OAuth2 client_credentials grant.

    Args:
        url: Reddit OAuth API search URL.
        client_id: Reddit app client ID.
        client_secret: Reddit app client secret.

    Returns:
        List of entry dicts extracted from search results.
    """
    # Obtain access token
    token_url = "https://www.reddit.com/api/v1/access_token"
    credentials = base64.b64encode(
        f"{client_id}:{client_secret}".encode()
    ).decode()
    token_data = urllib.parse.urlencode(
        {"grant_type": "client_credentials"}
    ).encode()
    token_req = urllib.request.Request(
        token_url,
        data=token_data,
        headers={
            "Authorization": f"Basic {credentials}",
            "User-Agent": "cc-community-monitor/1.0",
        },
    )
    with urllib.request.urlopen(token_req, timeout=15) as resp:
        token_resp = json.loads(resp.read().decode("utf-8"))
    access_token = token_resp["access_token"]

    # Fetch search results
    search_req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "cc-community-monitor/1.0",
        },
    )
    with urllib.request.urlopen(search_req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    entries: list[dict[str, str]] = []
    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        entries.append({
            "name": post.get("title", ""),
            "url": f"https://reddit.com{post.get('permalink', '')}",
            "description": (post.get("selftext") or "")[:200],
            "heading": "r/ClaudeAI",
        })
    return entries


def fetch_x_tweets(url: str, bearer_token: str) -> list[dict[str, str]]:
    """Fetch recent tweets from X API v2.

    Args:
        url: X API search/recent endpoint URL with query params.
        bearer_token: X API bearer token.

    Returns:
        List of entry dicts extracted from tweet results.
    """
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "cc-community-monitor/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    entries: list[dict[str, str]] = []
    for tweet in data.get("data", []):
        text = tweet.get("text", "")
        tweet_id = tweet.get("id", "")
        entries.append({
            "name": text[:80],
            "url": f"https://x.com/i/status/{tweet_id}" if tweet_id else "",
            "description": text[:200],
            "heading": "#ClaudeCode",
        })
    return entries


# ---------------------------------------------------------------------------
# Auth-aware fetch dispatcher
# ---------------------------------------------------------------------------

def fetch_and_extract_source(source: dict[str, str]) -> list[dict[str, str]]:
    """Fetch and extract entries from a source, handling auth requirements.

    Returns extracted entries. Skips with WARNING on missing auth or errors.
    """
    source_type = source["type"]
    auth = source.get("auth", "none")

    if auth == "reddit":
        client_id = os.environ.get("REDDIT_CLIENT_ID", "")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
        if not client_id or not client_secret:
            print(
                f"WARNING: Skipping {source['name']} — REDDIT_CLIENT_ID/SECRET not set",
                file=sys.stderr,
            )
            return []
        return fetch_reddit(source["url"], client_id, client_secret)

    if auth == "x_bearer":
        bearer = os.environ.get("X_BEARER_TOKEN", "")
        if not bearer:
            print(
                f"WARNING: Skipping {source['name']} — X_BEARER_TOKEN not set",
                file=sys.stderr,
            )
            return []
        return fetch_x_tweets(source["url"], bearer)

    # No auth required — fetch as text and extract by type
    content = fetch_text(source["url"])
    if source_type == "markdown":
        return extract_markdown_entries(content)
    return extract_html_entries(content)


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
        print(f"Fetching {name}...", file=sys.stderr)

        try:
            entries = fetch_and_extract_source(source)
        except Exception as e:
            print(f"WARNING: Failed to fetch {name}: {e}", file=sys.stderr)
            source_results.append({
                "name": name,
                "description": source["description"],
                "total": 0,
                "new_entries": [],
            })
            continue

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
