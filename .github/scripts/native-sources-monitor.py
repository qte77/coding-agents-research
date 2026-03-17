#!/usr/bin/env python3
"""Monitor native/Anthropic sources for Claude Code updates.

Polls Anthropic Blog, GitHub Issues (enhancement), and GitHub Discussions
(feature-request) for new entries not yet covered by existing native docs.

Usage:
    python native-sources-monitor.py \\
        --native-docs-dir PATH \\
        [--state-file PATH]

Exit codes:
    0 = no new uncovered content
    1 = new content found (workflow should open a PR)
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lib.monitor_utils import (
    build_doc_keywords,
    entry_fingerprint,
    extract_keywords,
    fetch_text,
    is_covered,
    load_state,
    save_state,
)

# ---------------------------------------------------------------------------
# Source definitions
# ---------------------------------------------------------------------------

CC_REPO_OWNER = "anthropics"
CC_REPO_NAME = "claude-code"

SOURCES: list[dict[str, str]] = [
    {
        "name": "anthropic-blog",
        "url": "https://www.anthropic.com/news",
        "type": "html",
        "auth": "none",
        "description": "Anthropic Blog — announcements and product updates",
    },
    {
        "name": "cc-issues-enhancement",
        "url": (
            f"https://api.github.com/repos/{CC_REPO_OWNER}/{CC_REPO_NAME}"
            "/issues?labels=enhancement&state=open&per_page=100"
        ),
        "type": "github_rest",
        "auth": "github_token",
        "description": "CC GitHub Issues labeled 'enhancement'",
    },
    {
        "name": "cc-discussions-feature-request",
        "type": "github_graphql",
        "auth": "github_token",
        "description": "CC GitHub Discussions in feature-request category",
    },
]

MAX_PAGES = 3


# ---------------------------------------------------------------------------
# Extractors
# ---------------------------------------------------------------------------

def extract_blog_entries(html: str) -> list[dict[str, str]]:
    """Extract blog post entries from Anthropic /news HTML.

    Looks for link+text patterns that mention Claude Code or related features.
    """
    entries: list[dict[str, str]] = []

    # Strip script/style
    clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    clean = re.sub(r"<style[^>]*>.*?</style>", "", clean, flags=re.DOTALL)

    # Extract links with text: <a href="...">Title</a>
    for match in re.finditer(r'<a[^>]+href="(/news/[^"]+)"[^>]*>(.*?)</a>', clean, re.DOTALL):
        href = match.group(1)
        title = re.sub(r"<[^>]+>", "", match.group(2)).strip()
        if not title or len(title) < 5:
            continue
        entries.append({
            "name": title,
            "url": f"https://www.anthropic.com{href}",
            "description": title,
            "heading": "Anthropic Blog",
        })

    # Deduplicate by URL
    seen_urls: set[str] = set()
    deduped: list[dict[str, str]] = []
    for entry in entries:
        if entry["url"] not in seen_urls:
            seen_urls.add(entry["url"])
            deduped.append(entry)

    return deduped


def extract_issues(json_pages: list[list[dict]]) -> list[dict[str, str]]:
    """Extract entries from GitHub REST Issues API response pages."""
    entries: list[dict[str, str]] = []
    for page in json_pages:
        for issue in page:
            # Skip pull requests (they have a pull_request key)
            if "pull_request" in issue:
                continue
            entries.append({
                "name": issue.get("title", ""),
                "url": issue.get("html_url", ""),
                "description": (issue.get("body") or "")[:200],
                "heading": "GitHub Issues (enhancement)",
            })
    return entries


def extract_discussions(nodes: list[dict]) -> list[dict[str, str]]:
    """Extract entries from GitHub GraphQL Discussions response nodes."""
    entries: list[dict[str, str]] = []
    for node in nodes:
        entries.append({
            "name": node.get("title", ""),
            "url": node.get("url", ""),
            "description": (node.get("body") or "")[:200],
            "heading": f"GitHub Discussions ({node.get('category', {}).get('name', 'feature-request')})",
        })
    return entries


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def github_headers(token: str) -> dict[str, str]:
    """Build GitHub API request headers."""
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def fetch_github_rest_pages(url: str, token: str) -> list[list[dict]]:
    """Fetch paginated GitHub REST API results (up to MAX_PAGES)."""
    pages: list[list[dict]] = []
    current_url: str | None = url

    for _ in range(MAX_PAGES):
        if current_url is None:
            break
        headers = github_headers(token)
        req = urllib.request.Request(current_url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            pages.append(json.loads(resp.read().decode("utf-8")))

            # Parse Link header for next page
            link_header = resp.headers.get("Link", "")
            next_match = re.search(r'<([^>]+)>;\s*rel="next"', link_header)
            current_url = next_match.group(1) if next_match else None

    return pages


def resolve_discussion_category_id(token: str) -> str | None:
    """Resolve the 'Feature Requests' discussion category ID via GraphQL."""
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        discussionCategories(first: 25) {
          nodes { id name }
        }
      }
    }
    """
    variables = {"owner": CC_REPO_OWNER, "name": CC_REPO_NAME}
    data = graphql_request(query, variables, token)
    if data is None:
        return None

    categories = (
        data.get("data", {})
        .get("repository", {})
        .get("discussionCategories", {})
        .get("nodes", [])
    )
    for cat in categories:
        if "feature" in cat.get("name", "").lower():
            return cat["id"]
    return None


def fetch_discussions_graphql(token: str, category_id: str | None) -> list[dict]:
    """Fetch discussions via GraphQL with cursor pagination (up to MAX_PAGES)."""
    all_nodes: list[dict] = []
    cursor: str | None = None

    query = """
    query($owner: String!, $name: String!, $categoryId: ID, $after: String) {
      repository(owner: $owner, name: $name) {
        discussions(first: 100, categoryId: $categoryId, after: $after) {
          pageInfo { hasNextPage endCursor }
          nodes { title url body createdAt category { name } }
        }
      }
    }
    """

    for _ in range(MAX_PAGES):
        variables: dict = {
            "owner": CC_REPO_OWNER,
            "name": CC_REPO_NAME,
            "after": cursor,
        }
        if category_id:
            variables["categoryId"] = category_id

        data = graphql_request(query, variables, token)
        if data is None:
            break

        discussions = (
            data.get("data", {})
            .get("repository", {})
            .get("discussions", {})
        )
        nodes = discussions.get("nodes", [])
        all_nodes.extend(nodes)

        page_info = discussions.get("pageInfo", {})
        if not page_info.get("hasNextPage"):
            break
        cursor = page_info.get("endCursor")

    return all_nodes


def graphql_request(
    query: str, variables: dict, token: str
) -> dict | None:
    """Execute a GitHub GraphQL request."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    headers = github_headers(token)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"WARNING: GraphQL request failed: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Source dispatching
# ---------------------------------------------------------------------------

def fetch_and_extract(source: dict[str, str]) -> list[dict[str, str]]:
    """Fetch a source and extract entries based on its type and auth.

    Returns extracted entries. Skips with WARNING on auth/network failures.
    """
    source_type = source["type"]
    auth = source["auth"]

    # Check auth requirements
    if auth == "github_token":
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            print(
                f"WARNING: Skipping {source['name']} — GITHUB_TOKEN not set",
                file=sys.stderr,
            )
            return []

    if source_type == "html":
        html = fetch_text(source["url"])
        return extract_blog_entries(html)

    if source_type == "github_rest":
        token = os.environ["GITHUB_TOKEN"]
        pages = fetch_github_rest_pages(source["url"], token)
        return extract_issues(pages)

    if source_type == "github_graphql":
        token = os.environ["GITHUB_TOKEN"]
        category_id = resolve_discussion_category_id(token)
        nodes = fetch_discussions_graphql(token, category_id)
        return extract_discussions(nodes)

    print(f"WARNING: Unknown source type '{source_type}'", file=sys.stderr)
    return []


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(source_results: list[dict]) -> tuple[str, bool]:
    """Build a markdown report of uncovered native source content.

    Returns (report_text, has_new_content).
    """
    lines: list[str] = [
        "## Native Sources Monitor Report",
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
            for entry in new_entries[:30]:
                name_col = entry.get("name", "")[:60].replace("|", "\\|")
                heading = entry.get("heading", "")[:40].replace("|", "\\|")
                desc = entry.get("description", "")[:80].replace("|", "\\|")
                lines.append(f"| {name_col} | {heading} | {desc} |")
            lines.append("")

            if len(new_entries) > 30:
                lines.append(f"_... and {len(new_entries) - 30} more entries._")
                lines.append("")

    lines += [
        "---",
        f"Total new uncovered entries: **{total_new}**",
        "",
        "_Generated by `.github/scripts/native-sources-monitor.py`_",
        "",
    ]

    return "\n".join(lines), total_new > 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the native sources monitor script."""
    parser = argparse.ArgumentParser(
        description="Monitor native/Anthropic sources for CC updates."
    )
    parser.add_argument(
        "--native-docs-dir", required=True, type=Path,
        help="Path to docs/cc-native/ directory",
    )
    parser.add_argument(
        "--state-file", type=Path,
        default=Path(".github/state/native-monitor-state.json"),
        help="Path to state file tracking previously seen entries",
    )
    args = parser.parse_args()

    if not args.native_docs_dir.exists():
        sys.exit(f"ERROR: Native docs dir does not exist: {args.native_docs_dir}")

    # Build keyword index from existing native docs
    doc_keywords = build_doc_keywords(args.native_docs_dir)
    print(f"Doc keywords indexed: {len(doc_keywords)}", file=sys.stderr)

    # Load previous state
    state = load_state(args.state_file)

    source_results: list[dict] = []

    for source in SOURCES:
        name = source["name"]
        print(f"Fetching {name}...", file=sys.stderr)

        try:
            entries = fetch_and_extract(source)
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
