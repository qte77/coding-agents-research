#!/usr/bin/env python3
"""Collect Claude platform incidents from Statuspage API into a JSONL archive.

Fetches all incidents (resolved + unresolved) from the Anthropic Statuspage
and upserts them into a local JSONL archive. Can also process webhook payloads
from repository_dispatch events.

Usage:
    # Fetch from API (daily cron)
    python status-collector.py --archive triage/status-monitor/outages.jsonl

    # Process webhook payload (repository_dispatch)
    python status-collector.py --archive triage/status-monitor/outages.jsonl --webhook-payload /tmp/payload.json

Exit codes:
    0 = no new or updated incidents
    1 = archive was updated (workflow should commit)
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

STATUSPAGE_BASE = "https://status.anthropic.com"


def fetch_incidents(base_url: str) -> list[dict]:
    """Fetch all incidents from the Statuspage JSON API."""
    url = f"{base_url}/api/v2/incidents.json"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"ERROR: Failed to fetch incidents: {e}", file=sys.stderr)
        sys.exit(2)
    return data.get("incidents", [])


def normalize_incident(raw: dict) -> dict:
    """Normalize a Statuspage incident into an archive record."""
    started_at = raw.get("started_at") or raw.get("created_at", "")
    resolved_at = raw.get("resolved_at")
    duration = compute_duration(started_at, resolved_at)

    components = []
    for comp in raw.get("components", []):
        name = comp.get("name", "")
        if name:
            components.append(name)

    updates = raw.get("incident_updates", [])

    return {
        "id": raw["id"],
        "name": raw.get("name", ""),
        "status": raw.get("status", ""),
        "impact": raw.get("impact", ""),
        "started_at": started_at,
        "resolved_at": resolved_at or "",
        "duration_minutes": duration,
        "affected_components": components,
        "updates_count": len(updates),
        "url": raw.get("shortlink", f"{STATUSPAGE_BASE}/incidents/{raw['id']}"),
        "collected_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def compute_duration(started_at: str, resolved_at: str | None) -> int | None:
    """Compute incident duration in minutes. Returns None if unresolved."""
    if not resolved_at or not started_at:
        return None
    try:
        start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        end = datetime.fromisoformat(resolved_at.replace("Z", "+00:00"))
        return max(0, int((end - start).total_seconds() / 60))
    except (ValueError, TypeError):
        return None


def normalize_webhook_incident(payload: dict) -> dict | None:
    """Extract and normalize incident from a webhook payload."""
    incident = payload.get("incident")
    if not incident:
        return None
    return normalize_incident(incident)


def load_archive(path: Path) -> dict[str, dict]:
    """Load existing archive as a dict keyed by incident ID."""
    archive: dict[str, dict] = {}
    if not path.exists():
        return archive
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            archive[record["id"]] = record
    return archive


def save_archive(path: Path, archive: dict[str, dict]) -> None:
    """Write archive to JSONL, sorted by started_at."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sorted_records = sorted(archive.values(), key=lambda r: r.get("started_at", ""))
    with open(path, "w") as f:
        for record in sorted_records:
            f.write(json.dumps(record, separators=(",", ":")) + "\n")


def record_changed(old: dict, new: dict) -> bool:
    """Check if a record has meaningfully changed (ignoring collected_at)."""
    for key in ("status", "resolved_at", "duration_minutes", "updates_count",
                "affected_components", "impact", "name"):
        if old.get(key) != new.get(key):
            return True
    return False


def main() -> None:
    """Entry point for the status collector."""
    parser = argparse.ArgumentParser(
        description="Collect Claude platform incidents into JSONL archive."
    )
    parser.add_argument(
        "--archive", type=Path, default=Path("triage/status-monitor/outages.jsonl"),
        help="Path to the JSONL archive file (default: triage/status-monitor/outages.jsonl)",
    )
    parser.add_argument(
        "--statuspage-base", default=STATUSPAGE_BASE,
        help=f"Statuspage base URL (default: {STATUSPAGE_BASE})",
    )
    parser.add_argument(
        "--webhook-payload", type=Path, default=None,
        help="Path to webhook payload JSON file (for repository_dispatch)",
    )
    args = parser.parse_args()

    archive = load_archive(args.archive)
    changed = False

    if args.webhook_payload:
        # Process webhook payload
        with open(args.webhook_payload) as f:
            payload = json.load(f)
        record = normalize_webhook_incident(payload)
        if record:
            existing = archive.get(record["id"])
            if not existing or record_changed(existing, record):
                archive[record["id"]] = record
                changed = True
                print(f"Webhook: {'updated' if existing else 'new'} incident {record['id']}: {record['name']}")
            else:
                print(f"Webhook: no changes for incident {record['id']}")
    else:
        # Fetch all incidents from API
        incidents = fetch_incidents(args.statuspage_base)
        print(f"Fetched {len(incidents)} incidents from API")

        for raw in incidents:
            record = normalize_incident(raw)
            existing = archive.get(record["id"])
            if not existing:
                archive[record["id"]] = record
                changed = True
                print(f"  NEW: {record['id']} — {record['name']}")
            elif record_changed(existing, record):
                archive[record["id"]] = record
                changed = True
                print(f"  UPDATED: {record['id']} — {record['name']}")

    if changed:
        save_archive(args.archive, archive)
        print(f"Archive updated: {len(archive)} total incidents in {args.archive}")
        sys.exit(1)
    else:
        print(f"No changes. Archive has {len(archive)} incidents.")
        sys.exit(0)


if __name__ == "__main__":
    main()
