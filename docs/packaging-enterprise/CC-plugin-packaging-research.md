---
title: CC Plugin Packaging Research
source: https://platform.claude.com/docs/en/agent-sdk/plugins, https://code.claude.com/docs/en/plugins
purpose: Evaluate packaging project skills, agents, and rules as a CC Plugin — including migration from repo-local configuration to a plugin-based integration.
created: 2026-03-07
---

**Status**: Research (informational — not implementation requirements)

## Context

This research evaluates whether a project's CC configuration — skills, agents, hooks, and behavioral rules — would benefit from being packaged as a CC Plugin instead of remaining as repo-local files. The tradeoff is portability and versioned distribution vs simplicity of direct repo-local management.

## What CC Plugins Are

Plugins are portable directory bundles that extend Claude Code with commands, agents, skills, hooks, and MCP servers ([source][sdk-plugins]). They work across Cowork and the Claude Agent SDK.

### Plugin Structure

```text
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # Required: manifest
├── commands/                 # Custom slash commands
│   └── custom-cmd.md
├── agents/                   # Custom subagents
│   └── specialist.md
├── skills/                   # Agent Skills (SKILL.md)
│   └── my-skill/
│       └── SKILL.md
├── hooks/                    # Event handlers
│   └── hooks.json
└── .mcp.json                # MCP server definitions
```

([source][sdk-plugins])

### Loading Plugins

```python
# Agent SDK (Python)
async for message in query(
    prompt="Hello",
    options={
        "plugins": [
            {"type": "local", "path": "./my-plugin"},
        ]
    },
):
    pass
```

```bash
# CLI — install from marketplace or local
/plugin install my-plugin@marketplace
# Or reference by path in settings
```

([source][sdk-plugins])

### Key Mechanics

- Commands namespaced: `plugin-name:command-name` ([source][sdk-plugins])
- Plugins discovered via `.claude-plugin/plugin.json` manifest ([source][sdk-plugins])
- CLI-installed plugins stored in `~/.claude/plugins/` ([source][sdk-plugins])
- Plugins loaded at session init; appear in system init message ([source][sdk-plugins])
- Skills within plugins follow standard SKILL.md format with progressive disclosure ([source][skill-dev])

## Typical Project Structure vs Plugin Structure

<!-- markdownlint-disable MD013 -->

| Project Component | Typical Location | Plugin Equivalent | Notes |
| ----------------- | ---------------- | ----------------- | ----- |
| Skills | `.claude/skills/` | `plugin/skills/` | Direct mapping — SKILL.md format identical |
| Agents | `.claude/agents/` | `plugin/agents/` | Direct mapping — .md format identical |
| Rules | `.claude/rules/` | No plugin equivalent | Rules are repo-local only; not portable via plugins |
| CLAUDE.md / project instructions | `./CLAUDE.md` | No plugin equivalent | Project instructions are repo-local |
| Hooks | `.claude/settings.json` hooks | `plugin/hooks/hooks.json` | Can be ported to plugin hooks format |
| MCP servers | `.claude/settings.json` mcpServers | `plugin/.mcp.json` | Can be ported to plugin MCP config |
| Automation scripts | `scripts/` or similar | `plugin/commands/` | Could expose as slash commands |

<!-- markdownlint-enable MD013 -->

## Direct Edit vs Plugin Packaging

When a project's CC configuration grows beyond a single repo, there are three options:

### Option A: Direct Edit (Repo-Local)

- **Effort**: Minimal — edit files in `.claude/` directly
- **Scope**: Project-local only
- **Maintenance**: Update `.claude/` files directly when adding new skills/agents
- **Portability**: None — tied to this repo

### Option B: Plugin Packaging

Package project skills, agents, and automation commands as a plugin:

```text
example-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── loop-init.md         # /example-plugin:loop-init
│   ├── loop-run.md          # /example-plugin:loop-run
│   └── loop-status.md       # /example-plugin:loop-status
├── agents/
│   ├── backend-architect.md
│   ├── python-developer.md
│   ├── code-reviewer.md
│   └── ...
├── skills/
│   ├── designing-backend/SKILL.md
│   ├── implementing-python/SKILL.md
│   ├── reviewing-code/SKILL.md
│   └── generating-prd/SKILL.md
└── hooks/
    └── hooks.json           # quality gates
```

- **Effort**: 2-4 hours to create plugin manifest + restructure
- **Scope**: Portable across projects and teams
- **Maintenance**: Plugin version management; separate from repo
- **Portability**: High — reusable across projects

### Option C: Hybrid (Recommended)

Keep project instructions and rules as repo-local (they're project-specific). Separately evaluate plugin packaging only for components that would benefit from cross-project reuse.

<!-- markdownlint-disable MD013 -->

| Component | Keep Repo-Local | Package as Plugin | Rationale |
| --------- | --------------- | ----------------- | --------- |
| Project instructions / behavioral rules | Yes | No | Project-specific behavioral rules |
| `.claude/rules/` | Yes | No | Project-specific context rules |
| `.claude/skills/` | Yes | Future | Skills are project-tailored; plugin only if reusing across projects |
| `.claude/agents/` | Yes | Future | Agent definitions reference project-specific patterns |
| Automation loop commands | Yes | Future | Loop scripts are project infrastructure; plugin if standardizing across repos |
| MCP config | Yes | No | Project-specific server endpoints |

<!-- markdownlint-enable MD013 -->

## Plugin Packaging: When It Makes Sense

Based on external research on plugin adoption patterns:

**Package as plugin when** ([source][skill-dev], [source][plugin-structure]):

- Skills/agents are **domain-generic** (e.g., "code-reviewer" applicable to any Python project)
- Multiple repos need the **same configuration** (e.g., org-wide security review agent)
- You want **versioned distribution** via marketplace or private GitHub repo
- The Agent SDK is used for **programmatic agent orchestration** beyond CLI

**Keep repo-local when** ([source][cc-mem]):

- Configuration references **project-specific paths, patterns, or conventions**
- CLAUDE.md / rules contain **behavioral rules tied to this codebase**
- Skills reference **project-specific files** (e.g., source modules unique to your project)
- No cross-project reuse demand exists

## Actionable Recommendation

### Immediate (Tier 1)

**Start with repo-local configuration.** This is the minimal, KISS approach:

- Keep skills, agents, and rules in `.claude/` within the project repo
- Update project instructions directly when adding new skills or agents
- No plugin manifest or restructuring needed until cross-project reuse is required

### Future (Tier 3 — triggered by cross-project reuse)

**If your project spawns sibling repos** that need the same skills, extract domain-generic skills into a plugin:

```json
{
  "name": "shared-dev-skills",
  "version": "1.0.0",
  "description": "Shared development skills for reuse across projects",
  "skills": ["reviewing-code", "testing-python", "designing-backend"]
}
```

This is YAGNI until a second project needs these skills.

## References

- [Agent SDK Plugins docs][sdk-plugins] — plugin loading and structure
- [CC Plugins docs][cc-plugins] — full plugin development guide
- [CC Plugins reference][cc-plugins-ref] — technical specs and schemas
- [Plugin Structure skill][plugin-structure] — community plugin scaffolding guide
- [Skill Development skill][skill-dev] — SKILL.md authoring best practices
- [CC Memory docs][cc-mem] — CLAUDE.md and rules (repo-local patterns)


[sdk-plugins]: https://platform.claude.com/docs/en/agent-sdk/plugins
[cc-plugins]: https://code.claude.com/docs/en/plugins
[cc-plugins-ref]: https://code.claude.com/docs/en/plugins-reference
[plugin-structure]: https://claude-plugins.dev/skills/@anthropics/claude-plugins-official/plugin-structure
[skill-dev]: https://lobehub.com/skills/sjnims-plugin-dev-skill-development
[cc-mem]: https://code.claude.com/docs/en/memory
