#!/usr/bin/env python3
"""Compare CC CHANGELOG.md against the scanned version range in CC-changelog-feature-scan.md.

Identifies versions newer than the last scanned version and checks whether
existing docs cover those features.

Usage:
    python changelog-compare.py \\
        --changelog PATH \\
        --scan-doc PATH \\
        --docs-dir PATH

Exit codes:
    0 = no new uncovered features
    1 = new features found (workflow should open an issue)
"""

import argparse
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def parse_scanned_version(scan_doc_path: Path) -> str:
    """Extract the last scanned version from the scan doc frontmatter.

    Looks for a ``purpose:`` field containing a version range like
    ``v2.1.0-2.1.71`` or ``v2.1.0–2.1.71`` (en-dash or hyphen).

    Returns the end version string, e.g. ``"2.1.71"``.
    Raises ``SystemExit`` if not found.
    """
    text = scan_doc_path.read_text(encoding="utf-8")
    # Match frontmatter block between --- markers
    fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL | re.MULTILINE)
    if not fm_match:
        sys.exit(f"ERROR: No frontmatter found in {scan_doc_path}")

    frontmatter = fm_match.group(1)
    # purpose: ... (v2.1.0–2.1.71) ...
    # Capture range after 'v' with either hyphen or en-dash separator
    purpose_match = re.search(
        r"purpose:.*?v(\d+\.\d+\.\d+)[–\-](\d+\.\d+\.\d+)", frontmatter
    )
    if not purpose_match:
        sys.exit(
            f"ERROR: Could not find version range in purpose field of {scan_doc_path}"
        )

    return purpose_match.group(2)  # end of range


def version_tuple(v: str) -> tuple[int, ...]:
    """Convert a version string like '2.1.71' to a comparable tuple."""
    return tuple(int(x) for x in v.split("."))


def parse_changelog_versions(changelog_path: Path) -> list[tuple[str, list[str]]]:
    """Parse CHANGELOG.md into a list of (version, feature_lines) pairs.

    Expects section headers like ``## 2.1.72`` or ``## [2.1.72]``.
    Returns list sorted descending (newest first).
    """
    text = changelog_path.read_text(encoding="utf-8")
    # Split on version section headers
    # Format: ## x.y.z  or  ## [x.y.z]
    section_pattern = re.compile(
        r"^##\s+\[?(\d+\.\d+\.\d+)\]?", re.MULTILINE
    )
    matches = list(section_pattern.finditer(text))
    if not matches:
        sys.exit(f"ERROR: No version sections found in {changelog_path}")

    versions: list[tuple[str, list[str]]] = []
    for i, match in enumerate(matches):
        version = match.group(1)
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        section_text = text[start:end]

        # Extract non-empty, non-header lines as feature lines
        feature_lines = [
            line.strip()
            for line in section_text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        versions.append((version, feature_lines))

    # Sort descending
    versions.sort(key=lambda t: version_tuple(t[0]), reverse=True)
    return versions


def collect_doc_index(docs_dir: Path) -> dict[str, list[str]]:
    """Build an index of doc file paths → list of H2/H3 headings.

    Only scans ``*.md`` files under ``docs_dir`` recursively.
    Returns ``{relative_path: [heading_text, ...]}``.
    """
    index: dict[str, list[str]] = {}
    for md_file in sorted(docs_dir.rglob("*.md")):
        rel = str(md_file.relative_to(docs_dir.parent))
        headings: list[str] = []
        for line in md_file.read_text(encoding="utf-8", errors="replace").splitlines():
            h_match = re.match(r"^#{2,3}\s+(.*)", line)
            if h_match:
                headings.append(h_match.group(1).strip())
        index[rel] = headings
    return index


# ---------------------------------------------------------------------------
# Coverage checking
# ---------------------------------------------------------------------------

def extract_keywords(text: str, min_len: int = 4) -> set[str]:
    """Extract lowercase alphanumeric tokens of at least ``min_len`` chars."""
    return {w.lower() for w in re.findall(r"[A-Za-z0-9_/-]{%d,}" % min_len, text)}


def find_covering_docs(
    feature_line: str, doc_index: dict[str, list[str]]
) -> list[str]:
    """Return list of doc paths whose filename or headings share keywords with the feature."""
    feature_kw = extract_keywords(feature_line)
    if not feature_kw:
        return []

    covering: list[str] = []
    for path, headings in doc_index.items():
        # Check filename
        file_kw = extract_keywords(Path(path).name)
        if feature_kw & file_kw:
            covering.append(path)
            continue
        # Check headings
        for heading in headings:
            heading_kw = extract_keywords(heading)
            if feature_kw & heading_kw:
                covering.append(path)
                break

    return covering


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def build_report(
    new_versions: list[tuple[str, list[str]]],
    doc_index: dict[str, list[str]],
    last_scanned: str,
) -> tuple[str, bool]:
    """Build a markdown report and return (report_text, has_uncovered).

    ``has_uncovered`` is True when at least one feature line has no covering doc.
    """
    lines: list[str] = [
        "## Changelog Monitor Report",
        "",
        f"Last scanned version: **{last_scanned}**",
        f"New versions detected: **{len(new_versions)}**",
        "",
    ]

    has_uncovered = False

    if not new_versions:
        lines += [
            "No new versions found beyond the scanned range. Nothing to review.",
            "",
        ]
        return "\n".join(lines), False

    # Summary table
    lines += [
        "### New Versions Summary",
        "",
        "| Version | Features | Covered | Uncovered |",
        "|---------|----------|---------|-----------|",
    ]

    per_version: list[tuple[str, list[tuple[str, list[str]]]]] = []

    for version, feature_lines in new_versions:
        covered: list[tuple[str, list[str]]] = []
        uncovered: list[tuple[str, list[str]]] = []
        for feat in feature_lines:
            docs = find_covering_docs(feat, doc_index)
            if docs:
                covered.append((feat, docs))
            else:
                uncovered.append((feat, []))
        per_version.append((version, covered + uncovered))

        if uncovered:
            has_uncovered = True

        lines.append(
            f"| {version} | {len(feature_lines)} "
            f"| {len(covered)} | {len(uncovered)} |"
        )

    lines.append("")

    # Detailed breakdown
    lines += ["### Feature Coverage Details", ""]

    for version, features in per_version:
        lines += [f"#### v{version}", ""]
        for feat, docs in features:
            if docs:
                doc_links = ", ".join(f"`{d}`" for d in docs[:3])
                lines.append(f"- **[covered]** {feat}")
                lines.append(f"  - Covered by: {doc_links}")
            else:
                lines.append(f"- **[UNCOVERED]** {feat}")
        lines.append("")

    lines += [
        "---",
        "_Generated by `.github/scripts/changelog-compare.py`_",
        "",
    ]

    return "\n".join(lines), has_uncovered


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare CC CHANGELOG.md against scanned version range."
    )
    parser.add_argument(
        "--changelog", required=True, type=Path,
        help="Path to fetched CHANGELOG.md"
    )
    parser.add_argument(
        "--scan-doc", required=True, type=Path,
        help="Path to CC-changelog-feature-scan.md (contains frontmatter with version range)"
    )
    parser.add_argument(
        "--docs-dir", required=True, type=Path,
        help="Path to docs/ directory to search for coverage"
    )
    args = parser.parse_args()

    # Validate inputs
    for p in (args.changelog, args.scan_doc, args.docs_dir):
        if not p.exists():
            sys.exit(f"ERROR: Path does not exist: {p}")

    last_scanned = parse_scanned_version(args.scan_doc)
    print(f"Last scanned version: {last_scanned}", file=sys.stderr)

    all_versions = parse_changelog_versions(args.changelog)
    cutoff = version_tuple(last_scanned)
    new_versions = [
        (v, feats)
        for v, feats in all_versions
        if version_tuple(v) > cutoff
    ]
    print(f"New versions found: {len(new_versions)}", file=sys.stderr)

    doc_index = collect_doc_index(args.docs_dir)
    print(f"Docs indexed: {len(doc_index)}", file=sys.stderr)

    report, has_uncovered = build_report(new_versions, doc_index, last_scanned)

    # Output report to stdout (captured by workflow)
    print(report)

    sys.exit(1 if has_uncovered else 0)


if __name__ == "__main__":
    main()
