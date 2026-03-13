---
title: CC Remote Control Analysis
source: https://code.claude.com/docs/en/remote-control
purpose: Analysis of Claude Code Remote Control for mobile monitoring of long-running CC sessions and cross-device session continuity.
created: 2026-03-07
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Generally available (all plans)

## What Remote Control Is

A feature that connects `claude.ai/code` or the Claude mobile app (iOS/Android) to a Claude Code session running locally ([source][cc-rc]). The local machine does all execution; the web/mobile interface is a window into that session. Not cloud execution — that's [Claude Code on the web](CC-cloud-sessions-analysis.md).

### Key Mechanics

- **Local execution**: Filesystem, MCP servers, tools, and project configuration stay on your machine ([source][cc-rc])
- **Multi-surface sync**: Conversation stays in sync across terminal, browser, and phone — messages can be sent from any surface interchangeably ([source][cc-rc])
- **Auto-reconnect**: If laptop sleeps or network drops, session reconnects automatically when machine comes back online ([source][cc-rc])
- **Outbound-only**: No inbound ports opened; local session polls Anthropic API over HTTPS. All traffic over TLS ([source][cc-sec])
- **One remote session per CC instance**: Each CC instance supports one remote connection ([source][cc-rc])

### Starting a Session

```bash
# New session
claude remote-control
claude remote-control --name "My Project"
claude remote-control --sandbox  # Enable filesystem/network sandboxing

# From existing session
/remote-control
/rc
```

Press spacebar to show QR code for quick phone access. Session URL is displayed for browser access.

### Connecting from Another Device

1. Open session URL directly in browser
2. Scan QR code with Claude mobile app
3. Find session by name in `claude.ai/code` session list (computer icon + green dot = online)

### Configuration

Enable for all sessions automatically:

```text
/config → "Enable Remote Control for all sessions" → true
```

### Requirements

- **Plans**: Pro, Max, Team, Enterprise (Team/Enterprise: admin must enable CC) ([source][cc-rc])
- **Auth**: Must be logged in via `/login` ([source][cc-rc])
- **Workspace trust**: Must have accepted workspace trust dialog at least once ([source][cc-rc])

### Limitations

1. **One remote session at a time** per CC instance ([source][cc-rc])
2. **Terminal must stay open** — closing terminal or stopping `claude` ends the session ([source][cc-rc])
3. **~10 minute network timeout** — extended outage causes session exit ([source][cc-rc])
4. **No inbound connections** — security model is outbound HTTPS polling only ([source][cc-sec])

### Remote Control vs Claude Code on the Web

<!-- markdownlint-disable MD013 -->

| Aspect | Remote Control | Claude Code on the Web |
| ------ | -------------- | ---------------------- |
| Execution | Your machine | Anthropic-managed cloud VM |
| Local MCP/tools | Available | Not available |
| Project config | Full local config | Needs setup script |
| Use case | Continue local work from another device | Start tasks without local setup |
| Offline survival | Reconnects after sleep | Runs independently of your machine |

<!-- markdownlint-enable MD013 -->

## Applicability to Common Workflows

<!-- markdownlint-disable MD013 -->

| Workflow | Fit | Rationale |
| -------- | --- | --------- |
| Monitor autonomous development loop from phone | Strong | Watch iterations progress without staying at desk; send corrections if stuck |
| Monitor CC teams runs | Strong | Same — observe parallel agent coordination remotely |
| Interactive development (debugging, iteration) | Moderate | Useful for remote coding sessions |
| Batch processes | Weak | No need for interactive monitoring on non-interactive runs |
| Headless `claude -p` invocations | None | Print mode exits on completion; no persistent session to connect to |

<!-- markdownlint-enable MD013 -->

### Decision Rule

**Use Remote Control to monitor long-running interactive sessions (autonomous loops, teams mode) from mobile. Not useful for headless/print-mode invocations.**

### Potential Integration

```makefile
# Example (NOT implemented — YAGNI until measured need)
loop_remote:
    cd $(PROJECT_DIR) && claude remote-control --name "Loop: $(shell date +%Y%m%d-%H%M)"
```

**Recommendation**: No project-level integration needed. Remote Control is a per-developer workflow preference. Developers can run `claude remote-control` manually when they want mobile access. Document the pattern in a usage guide if demand arises.

## References

- [CC Remote Control docs][cc-rc]
- [CC Claude Code on the Web docs][cc-web]
- [CC CLI Reference][cc-cli]
- [CC Security][cc-sec]

[cc-rc]: https://code.claude.com/docs/en/remote-control
[cc-web]: https://code.claude.com/docs/en/claude-code-on-the-web
[cc-cli]: https://code.claude.com/docs/en/cli-reference
[cc-sec]: https://code.claude.com/docs/en/security
