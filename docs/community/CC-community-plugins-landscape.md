---
title: CC Community Plugins Landscape
description: Survey of community plugin catalogs — awesome-claude-code (curated resource list) and awesome-claude-code-plugins (installable plugin registry with marketplace format).
category: landscape
status: research
sources:
  - https://github.com/hesreallyhim/awesome-claude-code
  - https://github.com/ccplugins/awesome-claude-code-plugins
created: 2026-03-13
updated: 2026-03-13
---

**Status**: Research (informational)

## Summary

Two community-maintained catalogs serve complementary roles: awesome-claude-code is a broad curated resource list (~100-200+ entries across 9 categories), while awesome-claude-code-plugins is a structured plugin registry (~136 installable plugins across 13 categories with marketplace format). Together they represent the community ecosystem around Claude Code extensions.

## awesome-claude-code (hesreallyhim)

**Repo**: [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | **License**: CC BY-NC-ND 4.0

A curated "awesome list" of Claude Code resources — links, tools, configurations, and methodologies. Not a plugin registry; catalogs anything useful for CC users.

### Categories (9)

| Category | Description | Notable Entries |
|----------|-------------|-----------------|
| Agent Skills | Model-controlled specialized task configs | 16+ entries; Claude Scientific Skills, DevOps/security skills |
| Workflows & Knowledge Guides | Development methodologies and project guidance | 22+ entries; Ralph Wiggum Pattern (5+ implementations), Auto-Claude (multi-agent SDLC with kanban) |
| Tooling | Applications built on CC | IDE integrations, usage monitors (ccflare), orchestrators, config managers |
| Status Lines | Terminal customizations | CC usage metrics display |
| Hooks | Lifecycle hook configurations | Pre/post tool call, session, stop events |
| Slash Commands | Custom prompt/action definitions | ~40+ entries (largest section) |
| CLAUDE.md Files | Language/domain-specific instruction files | Project templates and examples |
| Alternative Clients | Non-default UIs and front-ends | Community-built interfaces |
| Official Documentation | Anthropic reference materials | Canonical docs links |

### Contribution Model

- Submissions via automated GitHub issue template ("Recommend a new resource here")
- **Unique constraint**: *"The only person who is allowed to submit PRs to this repo is Claude"* — humans open issues, Claude Code handles PRs
- Multiple display formats: Awesome, Extra, Classic, Flat views + CSV table

### Key Patterns

- **Ralph Wiggum Pattern** has a dedicated subcategory with 5+ implementations cataloged
- Strong representation of DevOps, infrastructure automation, and security tooling
- Multiple session management and context continuity solutions
- Serves as community health indicator — entry velocity tracks ecosystem adoption

## awesome-claude-code-plugins (ccplugins)

**Repo**: [ccplugins/awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) | **License**: Apache-2.0

A structured plugin registry organized around Claude Code's installable plugin format (`/plugin` command, `.claude-plugin/marketplace.json`).

### Categories (13)

| Category | Plugins | Notable Focus |
|----------|---------|---------------|
| Official Claude Code Plugins | 5 | Anthropic-maintained |
| Code Quality Testing | 16 | Linting, testing, review automation |
| Development Engineering | 15 | Language-specific tooling, frameworks |
| Git Workflow | 14 | Review, branching, commit messaging |
| Project & Product Management | 10 | Agile, roadmapping, stakeholder tools |
| Business Sales | 8 | CRM, outreach, pipeline management |
| Workflow Orchestration | 8 | Multi-step automation, pipelines |
| Design UX | 8 | UI patterns, accessibility, prototyping |
| Documentation | 8 | Doc generation, API docs, changelogs |
| Marketing Growth | 7 | SEO, content, analytics |
| Security, Compliance & Legal | 7 | Vulnerability scanning, policy generation |
| Automation DevOps | 5 | CI/CD, infrastructure, deployment |
| Data Analytics | 5 | Dashboards, data processing, visualization |
| **Total** | **~136** | |

### Plugin System

- **Install**: `claude plugin install [plugin-name]` or `/plugin marketplace add user-or-org/repo-name`
- **Package format**: `.claude-plugin/marketplace.json` in a Git repo
- **Composability**: each plugin bundles slash commands + subagents + MCP servers + hooks as a single unit
- **Role-specific subagents**: plugins target named roles (data-scientist, frontend-developer, legal-advisor)
- **100% Python** implementation

### Contribution Model

- Open contributions: anyone can create and share a marketplace by publishing `.claude-plugin/marketplace.json`
- Decentralized: submit a link to your marketplace repo for inclusion

## Comparison

| Dimension | awesome-claude-code | awesome-claude-code-plugins |
|-----------|--------------------|-----------------------------|
| **Type** | Curated resource list (links, repos) | Installable plugin registry |
| **Scope** | Anything useful for CC users | Installable plugins only |
| **Entry format** | Free-form links to external repos | Plugin packages with manifest |
| **Installability** | Manual setup per resource | One-command via `/plugin` |
| **Business coverage** | Technical/developer focus | Includes Sales, Marketing, Legal |
| **Contribution** | Issue-only; Claude submits PRs | Open PRs; decentralized marketplaces |
| **License** | CC BY-NC-ND 4.0 (restrictive) | Apache-2.0 (permissive) |
| **Size** | ~100-200+ resources | ~136 plugins |
| **Unique content** | Workflow methodologies, CLAUDE.md examples, alternative clients | Business-function plugins, formal marketplace format |

## Ecosystem Observations

1. **Business-function plugins** (Sales, Marketing, Legal) exist only in the ccplugins registry — the awesome-claude-code list is developer-focused
2. **Ralph Wiggum Pattern** appears in both catalogs, confirming community convergence on autonomous loop workflows
3. **5 official plugins** are tracked by ccplugins, establishing a baseline for the official-to-community plugin ratio (~1:27)
4. **Git workflow** is disproportionately represented (14 plugins in ccplugins + numerous entries in awesome-cc), suggesting this is the primary CC extension use case

## Cross-References

- [CC-official-plugins-landscape.md](../cc-native/plugins-ecosystem/CC-official-plugins-landscape.md) — official Anthropic plugins (the 5 tracked by ccplugins)
- [CC-plugin-packaging-research.md](../cc-native/plugins-ecosystem/CC-plugin-packaging-research.md) — plugin packaging format and distribution
- [CC-community-skills-landscape.md](CC-community-skills-landscape.md) — skill libraries (gstack, pm-skills)
- [CC-cowork-plugins-enterprise-analysis.md](../cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md) — Cowork/enterprise plugin distribution
