---
title: Cowork, Skills API & CC Web Programmatic Workflows
source: https://platform.claude.com/docs/en/build-with-claude/skills-guide, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview, https://platform.claude.com/docs/en/build-with-claude/workspaces, https://code.claude.com/docs/en/claude-code-on-the-web, https://code.claude.com/docs/en/github-actions
purpose: API-level analysis of Cowork, Skills API, Chrome extension, and CC Web for programmatic workflow creation, GitHub integration, and multi-repo orchestration.
created: 2026-03-18
updated: 2026-03-18
---

**Status**: Research (API analysis + community tooling survey)

## Scope

Can Claude's product surfaces (Cowork, CC Web, Chrome extension) be populated via API and have their output saved to GitHub? This analysis evaluates each surface's programmatic capabilities.

## Skills API (`/v1/skills`)

### Endpoints

| Operation | Method | Endpoint | Auth |
|---|---|---|---|
| Create | `POST` | `/v1/skills` | API key + beta headers |
| List | `GET` | `/v1/skills` | API key + beta headers |
| Retrieve | `GET` | `/v1/skills/{id}` | API key + beta headers |
| Delete | `DELETE` | `/v1/skills/{id}` | API key + beta headers |
| Create version | `POST` | `/v1/skills/{id}/versions` | API key + beta headers |
| List versions | `GET` | `/v1/skills/{id}/versions` | API key + beta headers |
| Delete version | `DELETE` | `/v1/skills/{id}/versions/{version}` | API key + beta headers |

### Required Beta Headers

```
anthropic-beta: code-execution-2025-08-25,skills-2025-10-02,files-api-2025-04-14
```

### Skill Types

| Aspect | Anthropic Skills | Custom Skills |
|---|---|---|
| Type value | `anthropic` | `custom` |
| IDs | Short names: `pptx`, `xlsx`, `docx`, `pdf` | Generated: `skill_01Abc...` |
| Version format | Date-based: `20251013` or `latest` | Epoch timestamp or `latest` |
| Scope | Available to all users | Private to workspace |

### Usage in Messages API

```python
response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {"type": "anthropic", "skill_id": "xlsx", "version": "latest"},
            {"type": "custom", "skill_id": "skill_01Abc...", "version": "latest"},
        ]
    },
    messages=[{"role": "user", "content": "Analyze data"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}],
)
```

- Max 8 skills per request
- Container reuse via `response.container.id` for multi-turn
- Long-running: handle `pause_turn` stop reason

### Cross-Surface Availability

Skills **do not sync across surfaces**:

| Surface | Skills Source | Sharing |
|---|---|---|
| Claude API | `/v1/skills` upload | Workspace-wide |
| Claude.ai | Settings > Features upload | Individual user only |
| Claude Code | `.claude/skills/` filesystem | Project or personal |
| Cowork | Settings upload | Individual user only |

## Workspaces (Admin API)

### Endpoints

| Operation | Method | Endpoint |
|---|---|---|
| Create | `POST` | `/v1/organizations/workspaces` |
| List | `GET` | `/v1/organizations/workspaces` |
| Archive | `POST` | `/v1/organizations/workspaces/{id}/archive` |
| Add member | `POST` | `/v1/organizations/workspaces/{id}/members` |

- Auth: Admin API key (`sk-ant-admin...`), org admin role
- Max 100 workspaces per organization
- Resources (Files, Batches, Skills) scoped per workspace

## Surface-by-Surface Programmatic Assessment

### 1. Cowork (Desktop)

| Capability | API? | How |
|---|---|---|
| Populate with plugins | CLI only | `claude plugin install sales@knowledge-work-plugins` |
| Populate with skills | Manual upload | Settings UI (no API sync) |
| GitHub as plugin source | Yes | Private GitHub repos for enterprise marketplace |
| Save output to GitHub | No | Manual — Cowork writes to local filesystem |
| Start sessions | No | Desktop app only |
| Schedule tasks | No | Not supported |

**Plugin Structure** (from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins)):

```
plugin-name/
├── .claude-plugin/plugin.json   # Manifest
├── .mcp.json                    # MCP tool connections
├── commands/                    # Slash commands (/plugin:action)
└── skills/                      # Auto-activated domain knowledge
```

**Installation**: `claude plugin marketplace add anthropics/knowledge-work-plugins`

### 2. Claude Code on the Web (`claude.ai/code`)

| Capability | API? | How |
|---|---|---|
| Start sessions | Yes | `claude --remote "prompt"` |
| Parallel execution | Yes | Multiple `--remote` calls |
| GitHub integration | Native | Clones repo, pushes branches, creates PRs |
| Project config | Yes | `CLAUDE.md`, `.claude/`, hooks travel with repo |
| Save output | Automatic | Git branches + PRs |
| Scheduled tasks | GitHub Actions | `anthropics/claude-code-action@v1` with cron |
| Monitor | Yes | `/tasks`, web UI, mobile app |
| Teleport to local | Yes | `claude --teleport` or `/teleport` |

**GitHub Actions Integration**:

```yaml
on:
  schedule:
    - cron: "0 9 * * 1-5"
  issue_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review and fix issues"
```

### 3. Claude for Chrome (Extension)

| Capability | API? | How |
|---|---|---|
| Populate | No | No config API |
| GitHub integration | No | Browser navigation only |
| Save output | No | No export mechanism |
| Schedule | UI only | Saved shortcuts with schedules |
| Programmatic control | No | No API whatsoever |

## Community Orchestration Tools

Projects that wrap Claude Code for multi-repo/parallel execution:

| Project | Architecture | CC Web? | Multi-repo? | Long-running? |
|---|---|---|---|---|
| [claude_code_agent_farm](https://github.com/Dicklesworthstone/claude_code_agent_farm) | Python + tmux, 20-50 agents, file-lock coordination | Local only | Single project | Auto-restart, idle timeout |
| [agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator) | TypeScript, plugin-based (tmux/Docker/K8s), agent-agnostic | Local only | Git worktrees | Session restore, CI retry, escalation |
| [async-code](https://github.com/ObservedObserver/async-code) | Next.js + Flask, Docker isolation, Codex-style UI | Local only | Per-container | Containerized |
| [247-claude-code-remote](https://github.com/QuivrHQ/247-claude-code-remote) | Tailscale + Fly.io VMs, tmux, Cloudflare tunnels | Local (remote access) | Multiple sessions | tmux persistence |
| [Claude-Code-Remote](https://github.com/JessyTsui/Claude-Code-Remote) | Email/Discord/Telegram notifications | Local | Single | Notification on completion |
| [ccswarm](https://github.com/nwiizo/ccswarm) | Rust, git worktrees, MessageBus (93% token savings) | Local only | Worktrees | Crash recovery |
| [overstory](https://github.com/jayminwest/overstory) | SQLite mail, 4-tier conflict resolution, FIFO merge | Local only | Multi-layer | SQLite persistence |

**Gap**: No community tool uses `claude --remote` for cloud execution. All wrap local CLI sessions.

## Multi-Repo Cloud Execution

### Current State

CC Web assumes **1 session = 1 repo = 1 branch = 1 PR**. Cross-repo context sharing is not supported in cloud sessions, unlike local Claude Code with `additionalDirectories`.

- [Feature request #23627](https://github.com/anthropics/claude-code/issues/23627): Multi-repository support for remote/web sessions (open)

### Workaround: Parallel Independent Sessions

```bash
# Each repo gets its own cloud session
claude --remote "Run make validate" --repo github.com/org/repo-a
claude --remote "Run make validate" --repo github.com/org/repo-b
claude --remote "Run make validate" --repo github.com/org/repo-c
```

Results: independent PRs per repo. No cross-repo coordination.

### Durable Scheduling via GitHub Actions

```yaml
jobs:
  validate:
    strategy:
      matrix:
        repo: [repo-a, repo-b, repo-c]
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Run make validate"
```

## Long-Running Tasks Without Keep-Alive

| Method | Session Scope | Persistence | Monitoring |
|---|---|---|---|
| `/loop` (session cron) | Session-scoped, 3-day expiry | Dies with process | In-session only |
| `claude --remote` | Cloud VM | Survives disconnect | `/tasks`, web, mobile |
| GitHub Actions cron | Workflow-scoped | Survives everything | Actions UI |
| Desktop scheduled tasks | Desktop app | Survives restarts | Desktop notifications |

**Recommendation**: `claude --remote` for ad-hoc long tasks; GitHub Actions for durable recurring automation.

## Adoption Decision

| Surface | Populate via API | Save to GitHub | Verdict |
|---|---|---|---|
| **CC Web** | `--remote` + GH Actions | Automatic (PRs) | **Adopt** — full loop |
| **Skills API** | `/v1/skills` CRUD | Store skill source in GitHub | **Adopt** — for API surface |
| **Cowork** | Plugins from GitHub repos (CLI) | Manual | **Defer** — no API control |
| **Chrome** | None | None | **Skip** — no programmatic access |

## Action Items

1. Adapt polyforge `cc-parallel.sh` → `cc-parallel-web.sh` using `claude --remote`
2. Add GitHub Actions workflows for scheduled cross-repo validation
3. Store custom skills in GitHub repo with CI pushing to Skills API
4. Watch [#23627](https://github.com/anthropics/claude-code/issues/23627) for multi-repo cloud support

## References

- [Skills API Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
- [Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Workspaces](https://platform.claude.com/docs/en/build-with-claude/workspaces)
- [CC Web](https://code.claude.com/docs/en/claude-code-on-the-web)
- [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- [Scheduled Tasks](https://code.claude.com/docs/en/scheduled-tasks)
- [Cowork Plugins](https://claude.com/blog/cowork-plugins)
- [Knowledge Work Plugins](https://github.com/anthropics/knowledge-work-plugins)
- [Agent Skills Open Standard](https://agentskills.io)
