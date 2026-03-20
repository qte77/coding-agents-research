---
title: JetBrains Air Analysis
source: https://air.dev, https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/
purpose: Analysis of JetBrains Air as an agentic development environment for multi-agent orchestration.
created: 2026-03-20
updated: 2026-03-20
---

**Status**: Public Preview (macOS only, Windows/Linux planned 2026)

## What It Is

JetBrains Air is an **agentic development environment** (not an IDE or coding
agent itself) that orchestrates multiple coding agents in parallel. Built by
JetBrains, it wraps existing agents -- Codex, Claude Agent, Gemini CLI, and
Junie -- into a unified task management interface.

**Key distinction**: Air is an orchestrator, not an agent. It delegates to
agents rather than writing code itself.

## Core Capabilities

- **Multi-agent parallel execution**: Run Codex, Claude Agent, Gemini CLI,
  Junie concurrently on different tasks
- **Task isolation**: Git worktrees, Docker containers, or cloud environments
  (coming soon) per task
- **Codebase-aware context**: Reference files, commits, classes, methods,
  symbols, images when defining tasks
- **Built-in diff viewer** with commenting for agent feedback
- **Interactive plan mode**: Refine tasks step-by-step before execution
- **Agent Client Protocol (ACP)** support: Will add agents from ACP Agent
  Registry

## Agent Support

| Agent | Status |
|---|---|
| Claude Agent (Anthropic) | Supported |
| OpenAI Codex | Supported |
| Gemini CLI | Supported |
| Junie (JetBrains) | Supported |
| ACP-compatible agents | Planned |

## Execution Environments

- **Local** (default)
- **Git Worktree** -- isolated branch per task
- **Docker** -- containerized sandboxing
- **Cloud** -- coming soon

## Key Differentiators

- **JetBrains ecosystem**: 26 years of IDE tooling; built-in terminal, Git
  client, preview
- **Not a replacement for IDEs**: Designed to complement JetBrains IDEs, not
  replace them
- **Agent-agnostic**: Switch agents freely across projects
- **BYOK + JetBrains AI subscription**: Dual auth model

## Limitations

- macOS only (preview)
- No CLI / headless mode (GUI-only)
- No SDK
- Not open source
- Requires JetBrains AI subscription or provider API keys
- No Anthropic subscription support for BYOK (API key required)

## Relevance to coding-agent-eval

**Tier 2** (AI IDE / orchestrator, no headless). Air cannot be included in
the automated harness comparison since it has no CLI or headless mode. However,
it is relevant as a **competing orchestration pattern** -- Air's multi-agent
parallel task model with git worktree isolation mirrors what the
coding-agent-eval harness builds programmatically.

## Sources

| Source | Content |
|---|---|
| [air.dev](https://air.dev) | Product page |
| [JetBrains blog](https://blog.jetbrains.com/air/2026/03/air-launches-as-public-preview-a-new-wave-of-dev-tooling-built-on-26-years-of-experience/) | Launch announcement |
| [Quick start docs](https://www.jetbrains.com/help/air/quick-start-with-air.html) | Setup and usage |
