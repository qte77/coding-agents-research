---
title: agent-era/devteam Analysis
source: https://github.com/agent-era/devteam
purpose: Analysis of devteam as a terminal-based multi-agent orchestration tool for parallel coding agent workflows.
created: 2026-03-20
updated: 2026-03-20
---

**Status**: Active development (MIT licensed, open source)

## What It Is

A **terminal UI** for orchestrating multiple AI coding agents (Claude Code,
Codex, Gemini CLI) working in parallel on development tasks. Users launch
agents, switch between them, review changes, and manage pull requests from a
single interface.

```bash
npm i -g @agent-era/devteam
devteam
```

## Core Capabilities

- **Parallel agent execution**: Launch multiple agents simultaneously
- **Git worktree isolation**: Each agent runs in its own worktree
- **Built-in diff viewer**: Review agent changes with commenting
- **PR management**: Create and track PRs from the TUI
- **Real-time progress**: Diff line counts, PR status, GitHub checks
- **Local server support**: Run servers/programs per worktree for testing

## Agent Support

| Agent | Status |
|---|---|
| Claude Code | Supported |
| OpenAI Codex | Supported |
| Gemini CLI | Supported |

## Technical Details

- **Language**: TypeScript (95.4%)
- **License**: MIT
- **Install**: `npm i -g @agent-era/devteam`
- **Interface**: Terminal UI (not headless)
- **Isolation**: Git worktrees

## Key Differentiators

- **Open source** (MIT) -- unlike JetBrains Air
- **Terminal-native** -- no GUI/Electron dependency
- **Lightweight** -- single npm package, no IDE required
- **Experiment-driven**: Built to measure "how fast development can happen
  with multiple parallel agents"

## Limitations

- No headless / scriptable mode documented
- No SDK or programmatic API
- Terminal UI only (interactive)
- Limited to 3 agents (CC, Codex, Gemini CLI)
- No Cline, opencode, Codebuff, or Junie support

## Comparison with JetBrains Air

<!-- markdownlint-disable MD013 -->

| Aspect | devteam | JetBrains Air |
|---|---|---|
| Interface | Terminal UI | Desktop GUI |
| Open source | Yes (MIT) | No |
| Agents | CC, Codex, Gemini CLI | CC, Codex, Gemini CLI, Junie |
| Isolation | Git worktrees | Git worktrees, Docker, cloud (planned) |
| Codebase awareness | Basic | Symbol-level (files, commits, classes, methods) |
| Platform | Cross-platform (Node.js) | macOS only (preview) |
| Cost | Free | JetBrains AI subscription or BYOK |

<!-- markdownlint-enable MD013 -->

## Relevance to coding-agent-eval

**Tier 2** (orchestrator, no headless). Cannot be automated in the harness.
However, devteam's git worktree pattern directly informs the harness design --
both use worktrees for agent isolation. The key difference: the eval harness
drives agents programmatically via `claude -p` / CLI subprocess, while devteam
requires interactive TUI operation.

## Sources

| Source | Content |
|---|---|
| [GitHub repo](https://github.com/agent-era/devteam) | Source, README, license |
