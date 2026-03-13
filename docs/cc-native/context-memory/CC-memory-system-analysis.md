---
title: CC Memory System Analysis
source: https://code.claude.com/docs/en/memory
purpose: Analysis of Claude Code's dual memory system (CLAUDE.md + auto memory) for optimizing agent instructions, cross-session learning, and headless CC workflow context management.
created: 2026-03-07
updated: 2026-03-12
validated_links: 2026-03-12
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
    ├── code-style.md      # Always loaded (no paths frontmatter)
    ├── testing.md          # Always loaded
    └── api-design.md       # Path-scoped (see below)
```

Rules without `paths` frontmatter load unconditionally at launch with the same priority as `.claude/CLAUDE.md`. Path-scoped rules load when Claude reads matching files ([source][cc-mem]).

### Path-Scoped Rules Deep Dive

Path-specific rules use YAML frontmatter with the `paths` field:

```markdown
---
paths:
  - "src/api/**/*.ts"
---
# API Development Rules
- All endpoints must include input validation
- Use the standard error response format
```

#### Glob Syntax

| Pattern | Matches |
|---|---|
| `**/*.ts` | All TypeScript files in any directory |
| `src/**/*` | All files under `src/` directory |
| `*.md` | Markdown files in the project root only |
| `src/components/*.tsx` | React components in a specific directory |
| `src/**/*.{ts,tsx}` | Brace expansion for multiple extensions |
| `tests/**/*.test.ts` | Test files in a specific naming convention |

Multiple patterns and brace expansion are supported in a single rule ([source][cc-mem]):

```markdown
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Behavioral Rules

- **Trigger**: Path-scoped rules trigger when Claude **reads** files matching the pattern, not on every tool use ([source][cc-mem])
- **Multiple patterns**: A single rule file can specify multiple glob patterns
- **No paths field**: Rules without `paths` load unconditionally at launch
- **Subdirectory CLAUDE.md**: Files in subdirectories load on-demand when Claude reads files there — not at launch ([source][cc-mem])
- **User-level rules**: Personal rules in `~/.claude/rules/` apply to every project; loaded before project rules (lower priority) ([source][cc-mem])

#### Symlinks for Cross-Project Sharing

`.claude/rules/` supports symlinks for sharing rules across projects ([source][cc-mem]):

```bash
# Link a shared rules directory
ln -s ~/shared-claude-rules .claude/rules/shared

# Link an individual file
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Circular symlinks are detected and handled gracefully ([source][cc-mem]).

### Monorepo Management

#### `claudeMdExcludes`

Skip irrelevant CLAUDE.md files in monorepos via `.claude/settings.local.json` ([source][cc-mem]):

```json
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

- Patterns matched against **absolute file paths** using glob syntax
- Configurable at any settings layer (user, project, local, managed policy)
- Arrays merge across layers
- **Managed policy CLAUDE.md cannot be excluded** — ensures org-wide instructions always apply ([source][cc-mem])

#### Organization-Wide Managed CLAUDE.md

Centrally managed file that applies to all users on a machine ([source][cc-mem]):

| OS | Path |
|---|---|
| macOS | `/Library/Application Support/ClaudeCode/CLAUDE.md` |
| Linux / WSL | `/etc/claude-code/CLAUDE.md` |
| Windows | `C:\Program Files\ClaudeCode\CLAUDE.md` |

Deploy via MDM, Group Policy, Ansible, or similar. Cannot be excluded by individual `claudeMdExcludes` settings.

#### Additional Directories

Load CLAUDE.md from directories outside the main working directory ([source][cc-mem]):

```bash
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Overly broad globs (e.g., `**/*`) | Fires on every file read, defeating scoping purpose | Scope to specific directories or extensions |
| CLAUDE.md > 200 lines | Reduced adherence; more tokens consumed | Split into `.claude/rules/` files or use `@` imports |
| Conflicting instructions across files | Claude picks one arbitrarily | Periodic review; use `/memory` to audit loaded files |
| Deep `@` import chains | Increases token cost | Audit total imported size; keep chain under 400 total lines |
| Duplicate auto memory vs manual learnings | Stale or contradicting patterns | Periodic deduplication review |

### Auto Memory Architecture

```text
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index (first 200 lines loaded at session start)
├── debugging.md       # Topic file (loaded on demand)
├── api-conventions.md # Topic file (loaded on demand)
└── ...
```

- `<project>` derived from git repo — all worktrees and subdirectories within the same repo share one auto memory directory. Outside a git repo, the project root is used instead ([source][cc-mem])
- **MEMORY.md**: First 200 lines loaded at session start. Content beyond line 200 is not loaded. Claude keeps it concise by moving detailed notes into topic files ([source][cc-mem])
- **Topic files** (e.g., `debugging.md`, `patterns.md`): Not loaded at startup. Claude reads them on demand using file tools when needed ([source][cc-mem])
- Machine-local; not shared across machines or cloud environments
- Claude reads/writes during session; "Writing memory" / "Recalled memory" indicators shown
- **Subagent support**: Subagents can maintain their own auto memory ([source][cc-sub])
- **Agent memory frontmatter**: Agent definitions in `.claude/agents/` support persistent memory via frontmatter configuration (v2.1.33) — scoped to that agent's execution, distinct from subagent auto-memory

#### Configuration

```json
{
  "autoMemoryEnabled": false
}
```

Or: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` env var. Toggle via `/memory` command in session ([source][cc-mem]).

#### Auditing

Auto memory files are plain markdown — edit or delete at any time. Run `/memory` to browse loaded files, toggle auto memory, and open the memory folder ([source][cc-mem]).

### Key Behaviors

- **Import syntax**: `@path/to/file` expands imports in CLAUDE.md. Both relative and absolute paths supported; relative paths resolve relative to the containing file. Max 5 hops recursion ([source][cc-mem])
- **Size target**: Under 200 lines per CLAUDE.md for best adherence ([source][cc-mem])
- **`/init`**: Auto-generates starting CLAUDE.md from codebase analysis. If CLAUDE.md exists, suggests improvements rather than overwriting ([source][cc-mem])
- **`/memory`**: Lists all loaded instruction files; toggles auto memory; opens memory folder ([source][cc-mem])
- **Compaction survival**: CLAUDE.md fully survives `/compact` (re-read from disk). Instructions given only in conversation are lost after compaction ([source][cc-mem])
- **`InstructionsLoaded` hook**: Log exactly which instruction files load, when, and why — useful for debugging path-specific rules ([source][cc-mem])
- **First-time trust**: CC shows approval dialog for external `@` imports on first encounter in a project ([source][cc-mem])

## Usage Considerations

<!-- markdownlint-disable MD013 -->

| Aspect | Notes | Optimization Opportunity |
| ------ | ----- | ------------------------ |
| Autonomous loop context | Each iteration starts fresh; reads CLAUDE.md + auto memory | Working as designed — see context rot analysis for headless invocation patterns |
| Cloud sessions | Auto memory is machine-local | Cloud sessions rely on committed CLAUDE.md only (see CC-cloud-sessions-analysis.md) |
| `includeGitInstructions` | `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS=1` removes built-in git workflow instructions from context (v2.1.69) | Saves context tokens in headless/autonomous loops that don't need commit/PR guidance |

<!-- markdownlint-enable MD013 -->

For CLAUDE.md size, import chains, path-scoped rules, auto memory deduplication, `claudeMdExcludes`, and managed policy details, see the expanded sections above.

### Decision Rule

**CLAUDE.md and rules files are a project's primary instruction mechanism. Focus optimization on: (1) path-scoping rules to reduce context noise, (2) keeping the CLAUDE.md import chain under 400 total lines, (3) deduplicating auto memory vs manually maintained learnings files.**

### Potential Optimizations

1. **Path-scope role or subsystem boundaries** (see [glob syntax table](#glob-syntax) above):

   ```markdown
   ---
   paths:
     - "src/agents/**/*.py"
   ---
   # Agent Implementation Rules
   - Follow established agent patterns for this codebase
   ```

2. **Deduplicate auto memory vs learnings files**: Run periodic review to ensure auto memory doesn't accumulate stale patterns that contradict updated entries in a manually maintained learnings document.

3. **Use `InstructionsLoaded` hook** to audit which rules actually fire during typical workflows — prune rules that never trigger.

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
