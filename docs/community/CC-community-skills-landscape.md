---
title: CC Community Skills Landscape
description: Survey of community-built Claude Code skill libraries — gstack (founder/engineering workflows), pm-skills (product management framework), and claude-code-best-practice (knowledge base).
category: landscape
status: research
sources:
  - https://github.com/garrytan/gstack
  - https://github.com/phuryn/pm-skills
  - https://github.com/shanraisshan/claude-code-best-practice
created: 2026-03-13
updated: 2026-03-13
---

**Status**: Research (informational)

## Summary

Three community skill libraries demonstrate distinct models for packaging CC capabilities: gstack enforces cognitive mode-switching through role-locked skills, pm-skills delivers professional frameworks as installable plugins, and claude-code-best-practice curates a knowledge index of CC patterns and open questions.

## gstack (Garry Tan)

**Repo**: [garrytan/gstack](https://github.com/garrytan/gstack) | **Stars**: 4,000+ | **License**: MIT

8 skills targeting founder/engineering workflows with browser automation:

| Skill | Role | What It Does |
|-------|------|-------------|
| `/plan-ceo-review` | Founder | 11-phase plan review in EXPANSION / HOLD SCOPE / REDUCTION mode. Mandatory ASCII diagrams, error registries, TODOS.md entries. 9 "Prime Directives" govern every review. |
| `/plan-eng-review` | Engineering manager | Step 0 Scope Challenge gates BIG vs SMALL change review. Per-issue `AskUserQuestion` with lettered options. Produces reuse analysis and "NOT in scope" section. |
| `/review` | Security auditor | Two-pass PR audit: CRITICAL (SQL injection, TOCTOU, unvalidated LLM output) then INFORMATIONAL. Terse `file:line` output. Reads versioned `checklist.md`. |
| `/ship` | Release engineer | Automated: fetch/merge main, parallel test suites, review checklist, 4-digit VERSION bump, CHANGELOG, coherent commits, PR creation. Stops only on merge conflicts, test failures, or critical review issues. |
| `/browse` | QA inspector | Persistent headless Chromium daemon (~100ms round trips after first 3s startup). 50+ commands across navigate/read/snapshot/interact/inspect. Ref-based element selection via accessibility tree (`@e`, `@c`). |
| `/qa` | QA lead | Full/Quick/Regression modes. Weighted health score across 8 categories. 7-category issue taxonomy. Framework-specific guidance (Next.js, Rails, WordPress, SPAs). JSON snapshots for trend tracking. |
| `/setup-browser-cookies` | Session manager | Imports cookies from installed Chromium browsers (Chrome, Arc, Brave, Edge, Comet) via dark-themed web UI. Domain names only — no values exposed. |
| `/retro` | Engineering manager | Git history analysis with configurable time windows. Work session detection (45-min gaps), hourly commit distribution, contributor leaderboard, hotspot files, test/production ratio. |

### Cognitive Mode-Switching

The central design principle: *"Planning is not review. Review is not shipping. Founder taste is not engineering rigor."*

- **Hard role assignment**: each skill installs a specific persona that cannot drift
- **Mode-lock**: once a user selects EXPANSION/HOLD SCOPE/REDUCTION in `/plan-ceo-review`, the agent commits fully
- **Per-issue interruption**: both plan skills enforce one `AskUserQuestion` per issue — no batching
- **Mechanical handoffs**: `/ship` invokes the `/review` checklist and stops at critical findings

### Browser Automation Architecture

- **Daemon model**: Bun-compiled binary (~58MB) + persistent Chromium process. State file at `/tmp/browse-server.json`
- **Cookie persistence**: cookies and storage survive context recreation events
- **Multi-workspace isolation**: port derived from `CONDUCTOR_PORT` env var for parallel sessions
- **Token efficiency**: accessibility tree snapshots instead of full DOM. "In a 20-command session, MCP tools burn 30,000-40,000 tokens on protocol framing alone. gstack burns zero."
- **Security**: bearer token auth (random UUID), state file chmod 600

### Conductor Integration

[conductor.build](https://conductor.build) runs multiple CC sessions in parallel. Integration is via `CONDUCTOR_PORT` environment variable — each session gets isolated workspace and browser instance. No SDK dependency; pure env var convention.

## pm-skills (Pawel Huryn)

**Repo**: [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | **Stars**: 6,800+ | **License**: MIT

65 skills and 36 chained workflow commands across 8 plugins:

| Plugin | Skills | Commands | Domain |
|--------|--------|----------|--------|
| `pm-execution` | 15 | 10 | PRDs, OKRs, roadmaps, sprints, retrospectives, stakeholder maps |
| `pm-product-discovery` | 13 | 5 | Ideation, OSTs, assumption testing, interviews |
| `pm-product-strategy` | 12 | 5 | Vision, canvases, pricing, competitive frameworks |
| `pm-market-research` | 7 | 3 | Personas, segmentation, journey maps, market sizing |
| `pm-go-to-market` | 6 | 3 | GTM strategy, ICPs, growth loops, battlecards |
| `pm-marketing-growth` | 5 | 2 | Positioning, North Star, naming |
| `pm-data-analytics` | 3 | 3 | SQL generation, cohort analysis, A/B testing |
| `pm-toolkit` | 4 | 5 | Resume review, NDA drafting, privacy policy, grammar |

### Key Insight: Plugins as Framework Delivery

pm-skills is the clearest public example of CC plugins as a **domain expertise distribution platform**:

- **Framework encoding**: each skill embeds a complete named methodology (Teresa Torres' OST, Strategyzer's BMC, SMART/OKR metrics) — not generic prompts
- **Dual installation surface**: same skills install via `claude plugin install` (CLI) and Claude Cowork (GUI), reaching both developers and non-technical PMs
- **Cross-AI portability**: README notes compatibility with Gemini CLI, OpenCode, Cursor, Codex CLI, Kiro via folder copying
- **Commands as orchestrators**: `/discover` chains 7 sequential steps across multiple skills — workflow orchestration on top of atomic capabilities
- **Intellectual attribution**: credits 12 named PM thought leaders; skills cite specific book titles
- **Brand integration**: `plugin.json` points to productcompass.pm — plugins as lead-generation vehicle

### Skill Authoring Patterns

- **Single-file simplicity**: each skill is one `SKILL.md` — no YAML, no imports, no external refs
- **Noun/verb naming discipline**: skills = nouns (`stakeholder-map`), commands = verbs (`write-prd`)
- **No cross-plugin dependencies**: CONTRIBUTING.md forbids cross-plugin references; inter-plugin discovery via natural language suggestions
- **Validation**: `validate_plugins.py` enforces naming and metadata compliance at contribution time
- **Marketplace manifest**: root `.claude-plugin/marketplace.json` registers all 8 plugins (`"$schema": "https://anthropic.com/claude-code/marketplace.schema.json"`)

## claude-code-best-practice (shanraisshan)

**Repo**: [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | **Author**: Claude Community Ambassador

A **living community knowledge base** — not a skill library or plugin, but a curated reference index.

### Content Structure

| Section | Entries | Coverage |
|---------|---------|----------|
| Concepts Table | 12 | Core CC features with docs links and example repos |
| Hot Features | 8 | Emerging/beta capabilities (/btw, voice mode, agent teams, remote control) |
| Orchestration Workflow | 1 | Visual diagram: Command -> Agent -> Skill architecture |
| Development Workflows | 7+ | External patterns with star counts (Ralph, RPI, cross-model, Agent Teams) |
| Tips and Tricks | 38+ | Across 7 categories (prompting, planning, workflows, debugging, utilities, daily) |
| Startup Comparison | 5 | CC features vs commercial tool equivalents |
| Open Research Questions | 13 | Across 4 domains |
| Technical Reports | 9 | Deep-dives on specific CC features |

### Notable Workflow Patterns Referenced

- **Ralph Wiggum Loop**: autonomous development loop (listed as hot feature)
- **RPI (Research -> Plan -> Implement)**: from Human Layer, systematic structured development
- **Cross-Model (Claude Code + Codex)**: multi-model collaboration
- **Agent Teams**: parallel development using tmux and git worktrees

### Open Research Questions (13)

Organized across 4 domains — memory/instructions (4), agents/skills/workflows (6), specs/documentation (3). Key questions include:

- Selection criteria: command vs. agent vs. skill vs. vanilla CC
- Optimal CLAUDE.md content scope and staleness detection
- Built-in plan mode vs. custom planning enforcement
- Conflict resolution between personal and community skills
- Why Claude ignores explicit MUST directives

### Relevance

Valuable as a **community health indicator** and discovery entry point. The open research questions surface gaps in CC documentation and community understanding. The workflow pattern catalog (with star counts) tracks ecosystem adoption velocity.

## Cross-References

- [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — native skills format and adoption
- [CC-plans-as-skill-rule-templates.md](../cc-native/agents-skills/CC-plans-as-skill-rule-templates.md) — plan-to-skill extraction (gstack's `/plan-*` skills are concrete examples)
- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — official plugin ecosystem
- [CC-community-plugins-landscape.md](CC-community-plugins-landscape.md) — plugin catalogs
