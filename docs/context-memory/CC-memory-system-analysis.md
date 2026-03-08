---
title: CC Memory System Analysis
source: https://code.claude.com/docs/en/memory
purpose: Analysis of Claude Code's dual memory system (CLAUDE.md + auto memory) for optimizing agent instructions, cross-session learning, and headless CC workflow context management.
created: 2026-03-07
---

**Status**: Generally available (CLAUDE.md); Auto memory enabled by default

## What the Memory System Is

Two complementary mechanisms that carry knowledge across Claude Code sessions ([source][cc-mem]):

1. **CLAUDE.md files**: Human-written persistent instructions (project standards, workflows, architecture)
2. **Auto memory**: Claude-written notes accumulated from corrections and discoveries

Both load at session start. Neither is enforced configuration — they're context. Specificity and conciseness improve adherence ([source][cc-mem]).

### CLAUDE.md vs Auto Memory

<!-- markdownlint-disable MD013 -->

| Aspect | CLAUDE.md | Auto Memory |
| ------ | --------- | ----------- |
| Author | Human | Claude |
| Content | Instructions and rules | Learnings and patterns |
| Scope | Project, user, or org | Per working tree (git repo) |
| Loaded | Every session (full file) | Every session (first 200 lines of MEMORY.md) |
| Use for | Coding standards, workflows, architecture | Build commands, debugging insights, preferences |

<!-- markdownlint-enable MD013 -->

### CLAUDE.md Scope Hierarchy

<!-- markdownlint-disable MD013 -->

| Scope | Location | Shared with |
| ----- | -------- | ----------- |
| Managed policy | `/etc/claude-code/CLAUDE.md` (Linux) | All users in org (cannot be excluded) |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team via source control |
| User | `~/.claude/CLAUDE.md` | Just you (all projects) |
| Local | `./CLAUDE.local.md` | Just you (current project, gitignored) |

<!-- markdownlint-enable MD013 -->

More specific locations take precedence. Files in parent directories load at launch; files in subdirectories load on demand when Claude reads files there ([source][cc-mem]).

### `.claude/rules/` System

Topic-specific instruction files with optional path scoping:

```text
.claude/
├── CLAUDE.md
└── rules/
    ├── code-style.md      # Always loaded
    ├── testing.md          # Always loaded
    └── api-design.md       # Path-scoped (see below)
```

Path-specific rules use YAML frontmatter:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All endpoints must include input validation
```

Rules without `paths` frontmatter load unconditionally. Path-scoped rules load when Claude reads matching files ([source][cc-mem]).

### Auto Memory Architecture

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index (first 200 lines loaded at session start)
├── debugging.md       # Topic file (loaded on demand)
├── api-conventions.md # Topic file (loaded on demand)
└── ...
```

- `<project>` derived from git repo — all worktrees share one auto memory directory
- Machine-local; not shared across machines or cloud environments
- Claude reads/writes during session; "Writing memory" / "Recalled memory" indicators shown

### Key Behaviors

- **Import syntax**: `@path/to/file` expands imports in CLAUDE.md (max 5 hops recursion) ([source][cc-mem])
- **Size target**: Under 200 lines per CLAUDE.md for best adherence ([source][cc-mem])
- **`/init`**: Auto-generates starting CLAUDE.md from codebase analysis ([source][cc-mem])
- **`/memory`**: Lists all loaded instruction files; toggles auto memory; opens memory folder ([source][cc-mem])
- **Compaction survival**: CLAUDE.md fully survives `/compact` (re-read from disk) ([source][cc-mem])
- **`claudeMdExcludes`**: Skip irrelevant CLAUDE.md files in monorepos ([source][cc-mem])
- **Symlinks**: `.claude/rules/` supports symlinks for cross-project shared rules ([source][cc-mem])
- **Subagent memory**: Subagents can maintain their own auto memory ([source][cc-sub])

### Configuration

```json
{
  "autoMemoryEnabled": false,
  "claudeMdExcludes": ["**/other-team/CLAUDE.md"]
}
```

Or: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var.

## Example Project Usage

A well-structured project might use both systems as follows:

### CLAUDE.md Structure

The filenames below are examples — projects use different names for these concerns:

```text
CLAUDE.md              → @AGENTS.md import (or equivalent entry point)
AGENTS.md              → Behavioral rules, compliance, decision framework
                          (example name; use any name that fits your project)
CONTRIBUTING.md        → Technical workflows, coding standards
ESCALATION.md          → Escalation protocol
                          (example: "AGENT_REQUESTS.md" in some projects)
LEARNINGS.md           → Accumulated pattern knowledge
                          (example: "AGENT_LEARNINGS.md" in some projects)
.claude/rules/
├── context-management.md  → Context window principles
└── core-principles.md     → KISS/DRY/YAGNI mandatory principles
```

### Auto Memory

Active at `~/.claude/projects/<project-path>/memory/`. Contains `MEMORY.md` index and topic files accumulated across sessions.

## Usage Considerations

<!-- markdownlint-disable MD013 -->

| Aspect | Notes | Optimization Opportunity |
| ------ | ----- | ------------------------ |
| CLAUDE.md size | Keep under 200 lines per file for best adherence | Consider splitting large sections into `.claude/rules/` files with path scoping |
| Import chain | CLAUDE.md → supporting docs via `@` imports | Deep chains increase token cost; audit total imported size |
| Path-scoped rules | Rules without `paths` frontmatter load unconditionally | Add path-scoped rules for specific directories (e.g., agent code, tests) to reduce noise |
| Auto memory | Accumulates learnings across sessions | Periodically cross-check with manually maintained learnings docs for duplicates or contradictions |
| Autonomous loop context | Each iteration starts fresh; reads CLAUDE.md + auto memory | Working as designed — see context rot analysis for headless invocation patterns |
| Cloud sessions | Auto memory is machine-local | Cloud sessions rely on committed CLAUDE.md only (see CC-cloud-sessions-analysis.md) |
| Managed policy | `/etc/claude-code/CLAUDE.md` | Use for org-wide CC standards when deploying across a team |

<!-- markdownlint-enable MD013 -->

### Decision Rule

**CLAUDE.md and rules files are a project's primary instruction mechanism. Focus optimization on: (1) path-scoping rules to reduce context noise, (2) keeping the CLAUDE.md import chain under 400 total lines, (3) deduplicating auto memory vs manually maintained learnings files.**

### Potential Optimizations

1. **Path-scope role or subsystem boundaries**:

   ```markdown
   ---
   paths:
     - "src/agents/**/*.py"
   ---
   # Agent Implementation Rules
   - Follow established agent patterns for this codebase
   ```

2. **Deduplicate auto memory vs learnings files**: Run periodic review to ensure auto memory doesn't accumulate stale patterns that contradict updated entries in a manually maintained learnings document.

**Recommendation**: No structural changes needed for a project already using CLAUDE.md + rules + auto memory. Minor wins from path-scoping and deduplication reviews.

## References

- [CC Memory docs][cc-mem]
- [CC Skills docs][cc-skills]
- [CC Settings docs][cc-settings]
- [CC Subagent memory][cc-sub]

[cc-mem]: https://code.claude.com/docs/en/memory
[cc-skills]: https://code.claude.com/docs/en/skills
[cc-settings]: https://code.claude.com/docs/en/settings
[cc-sub]: https://code.claude.com/docs/en/sub-agents#enable-persistent-memory
