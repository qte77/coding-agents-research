---
title: CC Platform Status Monitoring & Outage Archive
source: https://status.anthropic.com
purpose: Real-time and archival monitoring of Claude platform incidents via Statuspage API, webhook integration, and statistical analysis.
created: 2026-03-17
updated: 2026-03-17
validated_links: 2026-03-17
---

**Status**: Adopt

## What It Is

Automated monitoring of the Claude platform status page (`status.anthropic.com`) to build a structured outage archive and generate statistical analysis. Two collection modes: daily cron poll (reliable baseline) and webhook-driven capture (near-real-time, future enhancement).

## Statuspage API Endpoints

### JSON API (Public, No Auth)

All endpoints are under `https://status.anthropic.com/api/v2/`.

| Endpoint | Returns |
|----------|---------|
| `incidents.json` | All incidents (resolved + unresolved) with full update history |
| `summary.json` | Current status + components + active incidents |
| `status.json` | Page-level status indicator only |
| `components.json` | All components with current status |

### Incident Object Structure

```json
{
  "id": "abc123def456",
  "name": "Elevated errors on Claude API",
  "status": "resolved",
  "impact": "major",
  "created_at": "2026-03-17T14:07:00.000Z",
  "started_at": "2026-03-17T14:07:00.000Z",
  "resolved_at": "2026-03-17T15:45:00.000Z",
  "shortlink": "https://stspg.io/abc123",
  "incident_updates": [
    {
      "id": "upd001",
      "status": "investigating",
      "body": "We are investigating elevated error rates...",
      "created_at": "2026-03-17T14:07:00.000Z"
    }
  ],
  "components": [
    { "id": "comp1", "name": "Claude API", "status": "operational" }
  ]
}
```

**Impact levels**: `none`, `minor`, `major`, `critical`

**Incident statuses**: `investigating`, `identified`, `monitoring`, `resolved`, `postmortem`

### RSS Feed

`https://status.anthropic.com/history.rss` — chronological incident feed with RFC 2822 dates. Useful for simple feed readers but lacks structured data compared to JSON API.

## Webhook Integration

### Statuspage Native Webhook

Statuspage supports webhook subscriptions that POST on every incident update and component status change.

**Payload format** (POST body):
- `page.status_indicator`, `page.status_description`
- `incident.*` — full incident object (same structure as JSON API)
- `component_update.old_status`, `.new_status`, `component.name`

### GitHub repository_dispatch Integration

To connect Statuspage webhooks to GitHub Actions:

1. **Direct connection won't work** — Statuspage sends its own payload format, not GitHub's required `{"event_type": "...", "client_payload": {...}}`

2. **Proxy required** — A lightweight intermediary (Cloudflare Worker, AWS Lambda, or GitHub App) that:
   - Receives Statuspage webhook POST
   - Wraps the payload: `{"event_type": "status-change", "client_payload": <original>}`
   - POSTs to `https://api.github.com/repos/qte77/coding-agents-research/dispatches`
   - Authenticates with a PAT (stored as proxy secret)

3. **PAT requirements** — Fine-grained token with `contents: write` on the target repo, stored as a secret in the proxy service

**Decision**: Use 4-hour cron polling instead of webhook. The JSON API returns full incident history, so nothing is missed. A webhook proxy adds infrastructure complexity for marginal latency gain. See [Statuspage webhook docs](https://support.atlassian.com/statuspage/docs/enable-webhook-notifications/) and [GitHub repository_dispatch docs](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch) for the format incompatibility.

## API Error Correlation

Claude API error documentation at `platform.claude.com/docs/en/api/errors` defines error codes (429, 500, 529) that correlate with incidents:

| Error | Correlation |
|-------|-------------|
| 429 (rate_limit) | Often precedes "degraded performance" incidents |
| 500 (api_error) | Correlates with "partial outage" incidents |
| 529 (overloaded) | Correlates with "major outage" incidents |

The outage archive enables retrospective correlation: match incident timestamps against application error logs to distinguish platform issues from application bugs.

## Implementation

### Archive Format

JSONL file (`triage/status-monitor/outages.jsonl`) with one normalized record per line, sorted by `started_at`:

```json
{"id":"abc123","name":"Elevated errors","status":"resolved","impact":"major","started_at":"2026-03-17T14:07:00Z","resolved_at":"2026-03-17T15:45:00Z","duration_minutes":98,"affected_components":["Claude API"],"updates_count":4,"url":"https://stspg.io/abc123","collected_at":"2026-03-17T16:00:00Z"}
```

**Upsert logic**: Records are merged by incident ID. Existing records are updated if `status`, `resolved_at`, `duration_minutes`, `updates_count`, `affected_components`, `impact`, or `name` changed. This handles both new incidents and resolution updates.

### Statistical Analysis

Generated from the archive as `triage/status-monitor/outage-stats.md`, covering:

- **Frequency**: incidents per week/month, trend over time
- **Duration**: min/max/median/mean resolution time (MTTR)
- **Severity**: count by impact level (minor/major/critical)
- **Components**: which components fail most, per-component downtime
- **Time patterns**: hour-of-day and day-of-week incident distributions
- **Uptime**: estimated uptime percentage per component

### Workflow

`cc-status-monitor.yaml` runs on:
- **4-hour cron** — primary collection mechanism, catches everything
- **`repository_dispatch`** (`status-change` event) — retained for future webhook proxy
- **`workflow_dispatch`** — manual trigger for testing

Changes are submitted via PR (branch protection requires PRs on `main`). Unlike other monitors, no timestamped report copies are created — `outages.jsonl` is the sole database and `outage-stats.md` the derived view.

## Design Decisions

| Decision | Rationale |
|----------|-----------|
| JSONL, not database | Git-native, diffable, appendable, zero dependencies |
| Stdlib-only scripts | Consistent with existing monitors (no pandas/numpy) |
| PR without timestamped report | Branch protection requires PRs; no redundant report copies needed |
| Upsert by incident ID | Handles new incidents and resolution updates idempotently |
| 4-hour cron, no webhook | Webhook needs proxy; cron catches everything with zero infra |
| `triage/` directory | Consolidates all monitor outputs under a single root |

## Adoption Decision

**Adopt** — Platform status monitoring provides direct value for:

1. Understanding Claude reliability patterns before building production systems
2. Correlating observed errors with platform incidents
3. Informing SLA expectations and retry/fallback strategies
4. Tracking platform maturity over time

### Action Items

- [x] Implement collector script (`status-collector.py`)
- [x] Implement stats script (`status-stats.py`)
- [x] Create GHA workflow (`cc-status-monitor.yaml`)
- [x] Create archive and stats data files
- [ ] Seed archive with historical data (first workflow run or manual execution)
- [ ] Consider webhook proxy if near-real-time capture needed

## References

- [Statuspage API docs](https://developer.statuspage.io/)
- [GitHub repository_dispatch](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch)
- [Claude API errors](https://docs.anthropic.com/en/api/errors)
