---
title: CC Official Plugins Landscape
source: https://www.firecrawl.dev/blog/best-claude-code-plugins, https://code.claude.com/docs/en/plugins
purpose: Catalog the official CC plugin ecosystem, assess coverage gaps in this research repo, and provide adoption guidance per plugin.
created: 2026-03-12
---

**Status**: Reference (living catalog — update as ecosystem evolves)

## Overview

The CC plugin ecosystem has grown to 9,000+ plugins across the marketplace, ClaudePluginHub, and Claude-Plugins.dev ([source][firecrawl-blog]). This document catalogs the top official plugins, maps coverage in this research repo, and provides adoption guidance.

## Plugin Coverage Matrix

<!-- markdownlint-disable MD013 -->

| # | Plugin | Installs | This Repo Coverage | Action |
|---|---|---|---|---|
| 1 | [Frontend Design](#frontend-design) | 96.4k | None | Brief section (UI-focused, skip unless frontend) |
| 2 | [Context7](#context7) | 71.8k | None | Full section (actively used via MCP) |
| 3 | [Code Review](#code-review) | 50k | Name-only mention | Moderate section (multi-agent scoring) |
| 4 | [Firecrawl](#firecrawl) | — | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 5 | [Playwright](#playwright) | 28.1k | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 6 | [Security Guidance](#security-guidance) | 25.5k | Name-only mention | Moderate section (9 security patterns) |
| 7 | [Chrome DevTools MCP](#chrome-devtools-mcp) | 20k | Full ([web-scraping analysis](CC-web-scraping-plugins-analysis.md)) | Cross-ref only |
| 8 | [Figma MCP](#figma-mcp) | 18.1k | None | Brief section (design-focused, skip unless UI) |
| 9 | [Linear](#linear) | 9.5k | None | Brief section (adopt if using Linear PM) |
| 10 | [Ralph Loop](#ralph-loop) | — | Full ([ralph enhancement research](../agent-orchestration/CC-ralph-enhancement-research.md)) | Cross-ref only |
| — | [CLI-Anything](#cli-anything) | — | Full ([CLI-Anything analysis](../agent-orchestration/CC-cli-anything-analysis.md)) | Cross-ref only |

<!-- markdownlint-enable MD013 -->

**Coverage summary**: 3 fully covered, 3 now documented below, 5 cross-referenced to existing analysis (including CLI-Anything as a notable community plugin).

## Plugin Details

### Context7

**What it does**: Injects real, up-to-date library documentation into Claude's context via MCP, reducing hallucinations from stale training data ([source][firecrawl-blog]).

**Installation**: `/plugin install context7@claude-plugins-official`

**How it works**:

1. `resolve-library-id` — search for a library by name, get a Context7-compatible ID
2. `get-library-docs` — fetch documentation by library ID, with optional `topic` filter and `tokens` budget

**Setup in this project**: Configured as an MCP server in `.claude/settings.json`. Available libraries include PydanticAI, Pydantic, pytest, Streamlit, loguru, scikit-learn, and others (see [CONTRIBUTING.md context7 section][contributing-c7]).

**Fit assessment**: **Strong adopt.** Already in daily use. Context7 solves the stale-docs problem for rapidly evolving libraries (PydanticAI, Streamlit). The MCP integration means it works in both interactive and headless CC sessions.

**Example usage**:

```bash
# Search for a library
mcp__context7__resolve-library-id --libraryName "pydantic-ai"

# Get focused documentation
mcp__context7__get-library-docs \
  --context7CompatibleLibraryID "/pydantic/pydantic-ai" \
  --topic "agents" --tokens 5000
```

### Code Review

**What it does**: Runs multiple specialized review agents in parallel to analyze code quality, tests, error handling, and type design. Produces structured summaries with confidence scores ([source][firecrawl-blog]).

**Installation**: `/plugin install code-review@claude-plugins-official`

**Usage**: Run `/code-review` on a PR branch.

**How it works**:

- Spawns parallel review agents, each focused on a specific concern (quality, security, tests, types)
- Each agent scores findings with confidence levels
- Results aggregated into a structured review summary
- Flags potential bugs, edge cases, and missing test coverage

**Fit assessment**: **Moderate adopt.** Complements the existing `/review` skill pattern. The multi-agent scoring approach aligns with the parallel review pattern documented in [CC-agent-teams-orchestration.md](../agent-orchestration/CC-agent-teams-orchestration.md). Consider using alongside project-specific review skills for defense-in-depth.

**Interaction with CC's bash layer**: The plugin's review agents use CC's Bash tool ([source][sdk-bash]) to run linters, type checkers, and test suites as part of their analysis. The persistent bash session (245 input tokens per tool use) means agents can chain `git diff`, `ruff check`, and `pyright` in sequence while maintaining working directory state.

### Security Guidance

**What it does**: Scans Claude Code's file edits for security vulnerabilities and blocks risky changes before they happen ([source][firecrawl-blog]).

**Installation**: `/plugin install security-guidance@claude-plugins-official`

**How it works**:

- Uses `PreToolUse` hook to scan edits before they're applied
- Monitors 9 security patterns:
  1. Command injection
  2. XSS (cross-site scripting)
  3. SQL injection
  4. Unsafe input handling
  5. Dangerous HTML generation
  6. Hardcoded secrets
  7. Path traversal
  8. Insecure deserialization
  9. SSRF (server-side request forgery)
- Provides warnings with fix suggestions
- Non-repetitive: warns once per pattern per session

**Fit assessment**: **Moderate adopt.** Relevant to all projects. Complements existing security tests (`tests/security/`) by catching issues at edit time rather than test time. The `PreToolUse` hook pattern is lightweight — no performance impact on non-edit operations.

**Interaction with CC's bash layer**: Security Guidance hooks into the edit pipeline, not the bash layer. It intercepts `Write` and `Edit` tool calls, not `Bash` tool calls. For bash-level security (blocking dangerous commands), use CC's built-in permission model (`Bash(pattern:*)` syntax, see [CC-bash-mode-analysis.md](../configuration/CC-bash-mode-analysis.md)).

### Figma MCP

**What it does**: Reads Figma design files directly and generates functional front-end code from design data — frames, components, and layout ([source][firecrawl-blog]).

**Installation**: `/plugin install figma@claude-plugins-official`

**Fit assessment**: **Skip unless UI work.** Targets design-to-code workflows for front-end projects. Not relevant for CLI/API/backend projects. Adopt if the project adds a web UI with Figma-designed components.

### Frontend Design

**What it does**: Applies stronger design judgment to Claude's UI generation — intentional typography, distinctive palettes, professional spacing. Avoids generic AI-generated defaults ([source][firecrawl-blog]).

**Installation**: `/plugin install frontend-design@claude-plugins-official`

**Fit assessment**: **Skip unless frontend project.** A skills-based plugin that adjusts Claude's design sensibility. No backend or API relevance. Adopt if building user-facing web interfaces where visual quality matters.

### Linear

**What it does**: Connects Claude to Linear issue tracker — pull issues, summarize tickets, mark in-progress, break into subtasks ([source][firecrawl-blog]).

**Installation**: `/plugin install linear@claude-plugins-official`

**Fit assessment**: **Adopt if using Linear for project management.** Enables issue-driven development without leaving CC. The auto-status-update (mark in-progress when starting work) reduces context switching. Not relevant if using GitHub Issues, Jira, or other PM tools.

## Applicability Decision Framework

<!-- markdownlint-disable MD013 -->

| Project Type | Recommended Plugins | Skip |
|---|---|---|
| **Backend/API** | Context7, Code Review, Security Guidance | Figma, Frontend Design |
| **Full-stack web** | Context7, Code Review, Security Guidance, Figma, Frontend Design | — |
| **Data science/ML** | Context7, Code Review | Figma, Frontend Design, Linear |
| **Open-source library** | Context7, Code Review, Security Guidance | Figma, Frontend Design |
| **Enterprise team** | All above + Linear (if using Linear) | Per project type |

<!-- markdownlint-enable MD013 -->

### Decision Rule

**Install Context7 and Code Review for all projects. Add Security Guidance for projects with security-sensitive code. Everything else is conditional on project type and tooling choices.**

## Already Covered Plugins

These plugins have full analysis elsewhere in this repo:

- **Firecrawl** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Playwright** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Chrome DevTools MCP** — [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- **Ralph Loop** — [CC Ralph Enhancement Research](../agent-orchestration/CC-ralph-enhancement-research.md)
- **CLI-Anything** (community) — [CC CLI-Anything Analysis](../agent-orchestration/CC-cli-anything-analysis.md)

## Community Resources

### Official Documentation

- [CC Best Practices][cc-best-practices]
- [CC Plugins docs][cc-plugins]
- [CC Skills docs][cc-skills]

### Community Guides and Catalogs

- [awesome-claude-code][awesome-cc] — skills, hooks, commands, and plugins catalog
- [CC Ultimate Guide][cc-ultimate] — beginner to power user guide with templates and quizzes
- [45 CC Tips (ykdojo)][cc-tips] — custom statusline, system prompt reduction, dx plugin
- [CC Best Practice][cc-best-practice-gh] — curated best practices collection
- [Everything Claude Code (Context7)][everything-cc] — battle-tested configs and patterns
- [Cuttlesoft Advanced Tips][cuttlesoft] — expert workflows for advanced users

## References

- [Firecrawl blog — Best CC Plugins][firecrawl-blog]
- [CC Plugins docs][cc-plugins]
- [Agent SDK Bash tool][sdk-bash]
- [CC Bash Mode Analysis](../configuration/CC-bash-mode-analysis.md)
- [CC Web Scraping Plugins Analysis](CC-web-scraping-plugins-analysis.md)
- [CC Plugin Packaging Research](CC-plugin-packaging-research.md)

[firecrawl-blog]: https://www.firecrawl.dev/blog/best-claude-code-plugins
[cc-plugins]: https://code.claude.com/docs/en/plugins
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-best-practices]: https://code.claude.com/docs/en/best-practices
[sdk-bash]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool
[contributing-c7]: https://github.com/qte77/Agents-eval/blob/main/CONTRIBUTING.md#context7-mcp-documentation-access
[awesome-cc]: https://github.com/hesreallyhim/awesome-claude-code
[cc-ultimate]: https://github.com/FlorianBruniaux/claude-code-ultimate-guide
[cc-tips]: https://github.com/ykdojo/claude-code-tips
[cc-best-practice-gh]: https://github.com/shanraisshan/claude-code-best-practice
[everything-cc]: https://github.com/affaan-m/everything-claude-code
[cuttlesoft]: https://cuttlesoft.com/blog/2026/02/03/claude-code-for-advanced-users/
