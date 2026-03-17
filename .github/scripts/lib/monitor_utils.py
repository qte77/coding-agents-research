"""Shared utilities for CC monitor scripts.

Provides keyword extraction, doc scanning, coverage checking,
state management, and HTTP fetching used by changelog-compare,
community-monitor, and native-sources-monitor.
"""

import hashlib
import json
import re
import urllib.request
from pathlib import Path

# Noise words that match too broadly across docs
DEFAULT_NOISE: set[str] = {
    "claude", "code", "with", "that", "this", "from", "have",
    "been", "will", "your", "more", "tool", "tools", "https",
    "github", "added", "fixed", "support", "feature",
}


def extract_keywords(text: str, min_len: int = 4) -> set[str]:
    """Extract lowercase alphanumeric tokens of at least ``min_len`` chars."""
    return {w.lower() for w in re.findall(r"[A-Za-z0-9_/-]{%d,}" % min_len, text)}


def build_doc_keywords(docs_dir: Path) -> set[str]:
    """Build a keyword set from all markdown files under ``docs_dir``."""
    keywords: set[str] = set()
    for md_file in sorted(docs_dir.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8", errors="replace")
        keywords.update(extract_keywords(text))
    return keywords


def is_covered(
    entry: dict[str, str],
    doc_keywords: set[str],
    threshold: float = 0.4,
    noise: set[str] | None = None,
) -> bool:
    """Check if an entry's key terms appear in existing docs.

    Returns True when overlap exceeds ``threshold`` fraction of entry keywords
    (after removing noise words).
    """
    if noise is None:
        noise = DEFAULT_NOISE

    entry_text = f"{entry.get('name', '')} {entry.get('description', '')}"
    entry_words = extract_keywords(entry_text) - noise

    if not entry_words:
        return True  # No meaningful keywords to match

    overlap = entry_words & doc_keywords
    return len(overlap) / len(entry_words) > threshold


def entry_fingerprint(entry: dict[str, str]) -> str:
    """Generate a stable 16-char hex fingerprint for an entry."""
    key = f"{entry.get('name', '')}|{entry.get('url', '')}".lower()
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def load_state(state_file: Path) -> dict[str, list[str]]:
    """Load previously seen entry fingerprints per source."""
    if state_file.exists():
        text = state_file.read_text(encoding="utf-8")
        if text.strip():
            return json.loads(text)
    return {}


def save_state(state_file: Path, state: dict[str, list[str]]) -> None:
    """Save seen entry fingerprints."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def fetch_text(
    url: str,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> str:
    """Fetch text content from a URL.

    Args:
        url: Target URL.
        headers: Optional HTTP headers (merged with default User-Agent).
        timeout: Request timeout in seconds.

    Returns:
        Response body as string.
    """
    default_headers = {"User-Agent": "cc-monitor/1.0"}
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")
