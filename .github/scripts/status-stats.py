#!/usr/bin/env python3
"""Generate statistical analysis of Claude platform outages from JSONL archive.

Reads the outage archive and produces a markdown report with frequency,
duration, severity, component, and time-of-day analysis.

Usage:
    python status-stats.py --archive triage/status-monitor/outages.jsonl > triage/status-monitor/outage-stats.md

All calculations use stdlib only (no pandas/numpy).
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


def load_archive(path: Path) -> list[dict]:
    """Load all records from the JSONL archive."""
    records: list[dict] = []
    if not path.exists():
        print(f"ERROR: Archive not found: {path}", file=sys.stderr)
        sys.exit(2)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def parse_dt(s: str) -> datetime | None:
    """Parse an ISO 8601 datetime string."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def median(values: list[int | float]) -> float:
    """Compute median of a sorted list."""
    if not values:
        return 0.0
    s = sorted(values)
    n = len(s)
    if n % 2 == 1:
        return float(s[n // 2])
    return (s[n // 2 - 1] + s[n // 2]) / 2.0


def mean(values: list[int | float]) -> float:
    """Compute mean of a list."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def format_duration(minutes: float) -> str:
    """Format minutes as human-readable duration."""
    if minutes < 60:
        return f"{minutes:.0f}m"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f}h"
    days = hours / 24
    return f"{days:.1f}d"


def _extract_timing(records: list[dict]) -> tuple[list[dict], list[datetime], list[int]]:
    """Extract resolved records, start times, and durations from records."""
    resolved = []
    all_starts: list[datetime] = []
    durations: list[int] = []
    for r in records:
        start = parse_dt(r.get("started_at", ""))
        if start:
            all_starts.append(start)
        dur = r.get("duration_minutes")
        if dur is not None and isinstance(dur, (int, float)):
            durations.append(int(dur))
            resolved.append(r)
    return resolved, all_starts, durations


def _section_summary(
    records: list[dict], resolved: list[dict], all_starts: list[datetime],
) -> list[str]:
    """Build the Summary section."""
    lines = ["## Summary", ""]
    unresolved = sum(1 for r in records if r.get("status") != "resolved")
    lines.append(f"- **Total incidents**: {len(records)}")
    lines.append(f"- **Resolved**: {len(resolved)}")
    lines.append(f"- **Unresolved/ongoing**: {unresolved}")
    if all_starts:
        earliest, latest = min(all_starts), max(all_starts)
        span_days = max(1, (latest - earliest).days)
        lines.append(f"- **Date range**: {earliest.strftime('%Y-%m-%d')} to {latest.strftime('%Y-%m-%d')}")
        lines.append(f"- **Span**: {span_days} days")
        lines.append(f"- **Rate**: {len(records) / (span_days / 7):.1f} incidents/week")
    lines.append("")
    return lines


def _section_resolution_time(durations: list[int]) -> list[str]:
    """Build the Resolution Time section."""
    if not durations:
        return []
    return [
        "## Resolution Time", "",
        "| Metric | Value |", "|--------|-------|",
        f"| Min | {format_duration(min(durations))} |",
        f"| Max | {format_duration(max(durations))} |",
        f"| Median | {format_duration(median(durations))} |",
        f"| Mean | {format_duration(mean(durations))} |",
        f"| Total downtime | {format_duration(sum(durations))} |",
        "",
    ]


def _section_severity(records: list[dict]) -> list[str]:
    """Build the Severity Distribution section."""
    impact_counts = Counter(r.get("impact", "unknown") for r in records)
    lines = ["## Severity Distribution", "", "| Impact | Count | % |", "|--------|-------|---|"]
    for impact, count in impact_counts.most_common():
        pct = count / len(records) * 100
        lines.append(f"| {impact} | {count} | {pct:.0f}% |")
    lines.append("")
    return lines


def _section_mttr(resolved: list[dict]) -> list[str]:
    """Build the MTTR by Severity section."""
    severity_durations: dict[str, list[int]] = defaultdict(list)
    for r in resolved:
        dur = r.get("duration_minutes")
        if dur is not None:
            severity_durations[r.get("impact", "unknown")].append(int(dur))
    if not severity_durations:
        return []
    lines = ["## MTTR by Severity", "",
             "| Impact | MTTR (mean) | MTTR (median) | Count |",
             "|--------|-------------|---------------|-------|"]
    for impact in sorted(severity_durations.keys()):
        durs = severity_durations[impact]
        lines.append(
            f"| {impact} | {format_duration(mean(durs))} "
            f"| {format_duration(median(durs))} | {len(durs)} |"
        )
    lines.append("")
    return lines


def _build_component_data(
    records: list[dict],
) -> tuple[Counter[str], dict[str, list[int]]]:
    """Aggregate component incident counts and durations."""
    comp_counts: Counter[str] = Counter()
    comp_durations: dict[str, list[int]] = defaultdict(list)
    for r in records:
        dur = r.get("duration_minutes")
        for comp in r.get("affected_components", []):
            comp_counts[comp] += 1
            if dur is not None:
                comp_durations[comp].append(int(dur))
    return comp_counts, comp_durations


def _section_components(
    comp_counts: Counter[str], comp_durations: dict[str, list[int]],
) -> list[str]:
    """Build the Component Frequency section."""
    if not comp_counts:
        return []
    lines = ["## Component Frequency", "",
             "| Component | Incidents | Total Downtime | Avg Duration |",
             "|-----------|-----------|----------------|--------------|"]
    for comp, count in comp_counts.most_common():
        durs = comp_durations.get(comp, [])
        total = format_duration(sum(durs)) if durs else "—"
        avg = format_duration(mean(durs)) if durs else "—"
        lines.append(f"| {comp} | {count} | {total} | {avg} |")
    lines.append("")
    return lines


def _section_time_distributions(all_starts: list[datetime]) -> list[str]:
    """Build Time-of-Day, Day-of-Week, and Monthly Trend sections."""
    if not all_starts:
        return []
    lines: list[str] = []

    # Time-of-Day
    hour_counts = Counter(dt.hour for dt in all_starts)
    max_hour = max(hour_counts.values())
    lines += ["## Time-of-Day Distribution (UTC)", "",
              "| Hour | Incidents | Bar |", "|------|-----------|-----|"]
    for hour in range(24):
        count = hour_counts.get(hour, 0)
        bar = "#" * int(count / max_hour * 20) if count > 0 else ""
        lines.append(f"| {hour:02d}:00 | {count} | {bar} |")
    lines.append("")

    # Day-of-Week
    dow_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    dow_counts = Counter(dt.weekday() for dt in all_starts)
    max_dow = max(dow_counts.values())
    lines += ["## Day-of-Week Distribution", "",
              "| Day | Incidents | Bar |", "|-----|-----------|-----|"]
    for day_idx, day_name in enumerate(dow_names):
        count = dow_counts.get(day_idx, 0)
        bar = "#" * int(count / max_dow * 20) if count > 0 else ""
        lines.append(f"| {day_name} | {count} | {bar} |")
    lines.append("")

    # Monthly Trend
    month_counts: Counter[str] = Counter(dt.strftime("%Y-%m") for dt in all_starts)
    max_month = max(month_counts.values())
    lines += ["## Monthly Trend", "",
              "| Month | Incidents | Bar |", "|-------|-----------|-----|"]
    for month in sorted(month_counts.keys()):
        count = month_counts[month]
        bar = "#" * int(count / max_month * 20) if count > 0 else ""
        lines.append(f"| {month} | {count} | {bar} |")
    lines.append("")

    return lines


def _section_uptime(
    all_starts: list[datetime], durations: list[int],
    comp_durations: dict[str, list[int]],
) -> list[str]:
    """Build the Uptime Estimate section."""
    if not all_starts or not durations:
        return []
    span_minutes = max(1, (max(all_starts) - min(all_starts)).total_seconds() / 60)
    total_down = sum(durations)
    uptime_pct = (1 - total_down / span_minutes) * 100
    lines = [
        "## Uptime Estimate", "",
        f"- **Overall uptime**: {uptime_pct:.3f}%",
        f"- **Total downtime**: {format_duration(total_down)}",
        f"- **Measurement period**: {format_duration(span_minutes)}",
        "",
    ]
    if comp_durations:
        lines += ["| Component | Uptime % | Downtime |",
                   "|-----------|----------|----------|"]
        for comp, durs in sorted(comp_durations.items(), key=lambda x: -sum(x[1])):
            comp_down = sum(durs)
            comp_up = (1 - comp_down / span_minutes) * 100
            lines.append(f"| {comp} | {comp_up:.3f}% | {format_duration(comp_down)} |")
        lines.append("")
    return lines


def generate_report(records: list[dict]) -> str:
    """Generate a markdown statistical report from outage records."""
    lines: list[str] = [
        "# Claude Platform Outage Statistics", "",
        f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} "
        f"| {len(records)} incidents in archive*", "",
    ]

    if not records:
        lines.append("No incidents recorded yet.")
        return "\n".join(lines)

    resolved, all_starts, durations = _extract_timing(records)
    comp_counts, comp_durations = _build_component_data(records)

    lines += _section_summary(records, resolved, all_starts)
    lines += _section_resolution_time(durations)
    lines += _section_severity(records)
    lines += _section_mttr(resolved)
    lines += _section_components(comp_counts, comp_durations)
    lines += _section_time_distributions(all_starts)
    lines += _section_uptime(all_starts, durations, comp_durations)

    return "\n".join(lines)


def main() -> None:
    """Entry point for the status stats generator."""
    parser = argparse.ArgumentParser(
        description="Generate outage statistics from JSONL archive."
    )
    parser.add_argument(
        "--archive", type=Path, default=Path("triage/status-monitor/outages.jsonl"),
        help="Path to the JSONL archive file (default: triage/status-monitor/outages.jsonl)",
    )
    args = parser.parse_args()

    records = load_archive(args.archive)
    report = generate_report(records)
    print(report)


if __name__ == "__main__":
    main()
