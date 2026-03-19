---
title: Claude Connectors — MCP-Based Integrations
purpose: Analysis of Claude's connector ecosystem, capabilities, limitations, and platform availability.
created: 2026-03-19
sources:
  - https://claude.com/docs/connectors/overview
  - https://claude.com/docs/connectors/google/gmail
  - https://claude.com/docs/connectors/google/drive
  - https://claude.com/docs/connectors/google/calendar
  - https://code.claude.com/docs/en/mcp
  - https://code.claude.com/docs/en/changelog
---

# Claude Connectors Overview

Connectors extend Claude via [MCP (Model Context Protocol)][mcp] — an open standard by Anthropic for AI-to-external-service interaction. They provide tool access (search, read, act) and UI rendering (charts, maps, forms via MCP Apps).

## Prebuilt Connectors

| Connector | Read | Write | Plan | Status |
|-----------|------|-------|------|--------|
| Google Drive | Docs only (up to 10 MB) | No | Pro+ | Beta |
| Gmail | Search & read threads | No (can't send/draft) | Pro+ | Beta |
| Google Calendar | Schedule, attendees, conflicts | No (can't create/modify/delete) | Pro+ | Beta |
| GitHub | Issues, PRs, code | Yes (via Claude Code) | Pro+ | GA |
| Slack | Messages, channels | Yes (send messages) | Pro+ | Beta |
| Microsoft 365 | Excel, PowerPoint | Yes (cross-app orchestration) | Paid | Research preview |

**Key pattern**: Google connectors are **read-only** — Claude can search and answer questions but cannot create, modify, or delete any content.

## Custom Connector Types

| Type | Hosting | Distribution | Use case |
|------|---------|-------------|----------|
| Remote MCP servers | Cloud | URL | Custom APIs, cloud tools |
| MCP Apps | Cloud | URL | Interactive UI (charts, maps, forms) |
| MCP Bundles (MCPB) | Local | Desktop package | Desktop tools with dependencies |
| Self-serve local MCP | Local | npm/PyPI (plugins) | Developer tools, CLI integrations |

## Platform Availability

| Platform | Remote MCP | Local MCP | MCP Apps | Plugins | claude.ai Connectors |
|----------|-----------|-----------|----------|---------|---------------------|
| Claude.ai | Yes | No | Yes | No | Native |
| Claude Desktop | Yes | Yes | Yes | Yes | Yes |
| Claude Mobile | Yes | No | No | No | Yes |
| Claude Code | Yes | Yes (plugins) | No | Yes | Yes (since v2.1.46) |
| Claude Cowork | Yes | Yes | Yes | Yes | Yes |

### Claude Code MCP Bridge (v2.1.46+)

Since [v2.1.46 (Feb 18, 2026)][cc-changelog], Claude Code automatically surfaces MCP servers configured in claude.ai — including Gmail, Google Drive, and Google Calendar connectors.

**Setup** ([source][cc-mcp-docs]):

1. Configure connectors at [claude.ai/settings/connectors](https://claude.ai/settings/connectors) (Team/Enterprise: admin-only)
2. Complete authentication in claude.ai
3. In Claude Code, run `/mcp` — claude.ai servers appear with indicators showing their origin

**Opt out**: `ENABLE_CLAUDEAI_MCP_SERVERS=false claude` (added in [v2.1.63, Feb 28, 2026][cc-changelog])

**v2.1.71 fixes** (March 7, 2026):

- Fixed startup UI freeze when many connectors refresh OAuth tokens simultaneously
- Fixed connectors failing to reconnect after OAuth token refresh
- Fixed startup notification noise for unauthenticated org connectors
- Removed notification spam for every org-configured connector

## Google Connectors Detail

### Google Drive

- **Supported**: Google Docs only (text extraction, live sync with latest version)
- **Not supported**: Google Sheets, Google Slides, images/comments within docs
- **Access**: Permission-mirrored — only docs the user can view
- **Setup**: Plus (+) button in chat or "Add Content" in projects → Google auth
- **Workaround**: Convert `.docx` to Google Docs via File → Save as Google Docs
- **Reconnect**: Settings → Integrations → disconnect and re-authenticate

### Gmail

- **Can do**: Search emails, analyze threads, provide citations linking to source
- **Cannot do**: Create, send, or modify emails; view embedded images
- **Access**: Mirrors existing Gmail permissions (specific OAuth scopes undocumented)

### Google Calendar

- **Can do**: Query schedule, meeting details, attendees, conflict detection, pattern analysis; citations link to original events
- **Cannot do**: Create, modify, or delete events; send invitations
- **Access**: Only calendars accessible to the authenticated user

### Common Google Connector Properties

- **Auth**: Direct Google account authentication (no API keys)
- **Admin**: Team/Enterprise requires Owner or Primary Owner to enable integrations
- **Data handling**: Retrieved data stored on Anthropic servers with security protections; retention tied to chat (delete chat = delete data); models not trained on integration data
- **Access pattern**: Data retrieved only on explicit user request, minimal information fetched

## Applicability to Coding Agent Workflows

| Aspect | Fit | Rationale |
|--------|-----|-----------|
| Code execution | No | Connectors are for data access, not compute |
| Research input | Yes | Drive/Gmail feed docs and threads into CC context via MCP bridge |
| Task automation | Low | Google connectors are read-only; no write actions |
| CI/CD integration | No | Use GitHub Actions or Claude Code directly |
| Multi-repo orchestration | No | Connectors don't provide repo-level operations |
| Enterprise admin | Yes | Connectors + plugins provisioning via admin controls |

**Bottom line**: Since v2.1.46, all claude.ai connectors work in Claude Code via the MCP bridge. Google connectors are read-only but useful for ingesting docs, emails, and calendar context into coding workflows. GitHub and Slack connectors support both read and write.

## Discovery

- Full docs index: `https://claude.com/docs/llms.txt`
- Connectors Directory: vetted third-party integrations across all Claude products

## References

- [Connectors overview][overview]
- [Google Drive connector][drive]
- [Gmail connector][gmail]
- [Google Calendar connector][calendar]
- [CC MCP docs][cc-mcp-docs]
- [MCP specification][mcp]
- [Cowork plugins & enterprise analysis](CC-cowork-plugins-enterprise-analysis.md)

[overview]: https://claude.com/docs/connectors/overview
[drive]: https://claude.com/docs/connectors/google/drive
[gmail]: https://claude.com/docs/connectors/google/gmail
[calendar]: https://claude.com/docs/connectors/google/calendar
[mcp]: https://modelcontextprotocol.io
[cc-changelog]: https://code.claude.com/docs/en/changelog
[cc-mcp-docs]: https://code.claude.com/docs/en/mcp
