---
title: CC Bash Mode — CLI `!` Prefix and Dynamic Context Injection in Skills/Rules
source: https://code.claude.com/docs/en/interactive-mode, https://code.claude.com/docs/en/slash-commands
purpose: Document bash mode usage in CLI interactive sessions and dynamic shell execution within skills and rules files.
created: 2026-03-12
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Adopted (both features are stable and production-ready)

## Overview

Claude Code provides two distinct bash execution mechanisms:

1. **CLI Bash Mode (`!` prefix)** — run shell commands directly from the interactive prompt
2. **Dynamic Context Injection (`` !`command` ``)** — run shell commands within skill/command `.md` files to inject live output before Claude processes the prompt

These are complementary features serving different purposes.

## CLI Bash Mode (`!` Prefix)

### What It Is

Prefixing any input with `!` in the interactive Claude Code prompt runs the command directly in your shell, bypassing Claude entirely. The command output is added to the conversation context so Claude can reference it ([source][cc-interactive-mode]).

### How It Works

```bash
# In the Claude Code interactive prompt:
! git status
! npm test
! ls -la src/
! docker ps
```

- The command executes immediately — Claude does not interpret, approve, or explain it
- Output streams in real-time and is added to conversation context
- Claude can then reference the output in subsequent responses
- Supports `Ctrl+B` to background long-running commands ([source][cc-interactive-mode])

### Key Behaviors

| Behavior | Description |
|---|---|
| **No approval needed** | Runs directly, no permission prompt |
| **Context injection** | Command + output added to conversation |
| **Tab autocomplete** | Type partial command + Tab to complete from previous `!` commands |
| **Backgrounding** | `Ctrl+B` sends running command to background |
| **Exit** | `Escape`, `Backspace`, or `Ctrl+U` on empty prompt |
| **History** | Up/Down arrows navigate `!` command history |

([source][cc-interactive-mode])

### Why Use It Over Claude's Bash Tool

| Scenario | `! command` (direct) | Claude runs bash |
|---|---|---|
| **Steps** | 1 (execute) | 3 (interpret, execute, explain) |
| **Token cost** | Output only | Prompt + reasoning + output + explanation |
| **Approval** | None | May require permission approval |
| **Speed** | Instant | Waits for Claude's reasoning |
| **Best for** | Quick checks, test runs, git ops | Complex commands needing explanation |

([source][devto-bash-mode])

### Practical Workflow

Rapid iteration combining bash mode with fast mode ([source][cc-interactive-mode]):

1. Give Claude a task
2. `! make test` — run tests directly
3. Review failures in context
4. Ask Claude to fix based on the test output
5. `! make test` — verify fix
6. Repeat

### Permission Behavior

Bash mode commands respect the configured permission rules. They may still trigger approval prompts based on allow/deny classifications in your permission settings ([source][cc-interactive-mode]).

## Dynamic Context Injection (`` !`command` ``)

### What It Is

Within skill files (`SKILL.md`) and custom command files (`.claude/commands/*.md`), the `` !`command` `` syntax runs shell commands as a preprocessing step before the content is sent to Claude. The command output replaces the placeholder in the rendered prompt ([source][cc-skills-docs]).

### How It Works

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

When this skill runs ([source][cc-skills-docs]):

1. Each `` !`command` `` executes immediately (before Claude sees anything)
2. The command output replaces the placeholder in the skill content
3. Claude receives the fully-rendered prompt with actual data

**This is preprocessing, not something Claude executes.** Claude only sees the final output.

### Available String Substitutions

Skills support these built-in variables alongside bash injection ([source][cc-skills-docs]):

| Variable | Description |
|---|---|
| `$ARGUMENTS` | All arguments passed when invoking the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's `SKILL.md` |

### Use Cases for Dynamic Injection

#### Git Context in Skills

```yaml
---
name: commit
description: Create a well-formatted commit
disable-model-invocation: true
---

## Current state
- Status: !`git status --short`
- Staged diff: !`git diff --cached --stat`
- Recent commits: !`git log --oneline -5`

Create a commit message following conventional commits format.
```

#### Environment-Aware Skills

```yaml
---
name: deploy-check
description: Pre-deployment validation
disable-model-invocation: true
---

## Environment
- Branch: !`git branch --show-current`
- Node version: !`node --version`
- Python version: !`python --version 2>&1`
- Disk usage: !`df -h . | tail -1`

Validate this environment is ready for deployment.
```

#### Codebase-Aware Skills

```yaml
---
name: review-changes
description: Review recent code changes
---

## Changes since last tag
!`git diff $(git describe --tags --abbrev=0)..HEAD --stat`

## Modified source files
!`git diff --name-only $(git describe --tags --abbrev=0)..HEAD -- src/`

Review these changes for quality and consistency.
```

### Dynamic Rules Context

While `.claude/rules/*.md` files are static markdown (no bash injection support), dynamic behavior can be achieved through:

1. **Skills that inject context** — a skill with `` !`command` `` can inject environment-specific rules at invocation time
2. **CLAUDE.md with static references** — reference files that are updated externally (e.g., by CI or hooks)
3. **Hooks** — `hooks.json` can run shell commands on specific tool events, injecting context via `stopMessage` or `exitCode`

### Limitations

| Limitation | Detail |
|---|---|
| **Skills/commands only** | `` !`command` `` works in `SKILL.md` and `.claude/commands/*.md`, not in `CLAUDE.md` or `.claude/rules/*.md` |
| **Preprocessing only** | Commands run before Claude sees the prompt — no interactive or conditional execution |
| **No `$()` syntax** | Uses `` !`command` `` (backtick), not `$(command)` shell substitution |
| **Timeout** | Long-running commands may timeout; keep injection commands fast |
| **Error handling** | If a command fails, the error output (or empty string) replaces the placeholder — no retry logic |

## Comparison: CLI `!` vs Skill `` !`cmd` ``

| Aspect | CLI `! command` | Skill `` !`command` `` |
|---|---|---|
| **Where** | Interactive prompt | `SKILL.md` / `.claude/commands/*.md` files |
| **When** | On demand, during conversation | At skill invocation time (preprocessing) |
| **Who runs it** | User types it directly | Automated when skill loads |
| **Output destination** | Added to conversation context | Injected into skill prompt text |
| **Claude involvement** | None (direct execution) | None (preprocessing) |
| **Use case** | Quick checks, test runs | Live data in skill templates |

## Security Considerations

### CLI Bash Mode

- Commands run with the user's full shell permissions
- Permission rules (allow/deny) still apply based on settings
- No sandboxing beyond CC's configured permission model

### Dynamic Context Injection

- Commands in skill files execute automatically when the skill is invoked
- **Supply chain risk**: Third-party skills (plugins, marketplace) can contain arbitrary `` !`command` `` injections ([source][snyk-toxicskills])
- **Mitigation**: Review skill files before installing; prefer project-local skills over marketplace for sensitive environments
- Claude Code's trust verification prompts on first-time codebase runs help catch unexpected injection ([source][cc-security])

## Adoption Recommendation

**Both features are stable and recommended for adoption.**

### CLI Bash Mode (`!`)

Adopt immediately. Zero setup, zero risk beyond normal shell usage. Significantly reduces token cost and latency for routine operations (git, tests, builds) during interactive sessions.

### Dynamic Context Injection (`` !`command` ``)

Adopt for any skill that benefits from live data. The preprocessing model is clean and predictable. Essential for:

- Git-aware skills (commit, review, deploy)
- Environment-aware skills (validation, diagnostics)
- Any skill that needs runtime context without Claude running commands itself

## Related: Agent SDK Bash Tool

The Agent SDK provides a server-side Bash tool (`bash_20250124`) that is distinct from CC's client-side `!` prefix ([source][sdk-bash]):

| Aspect | CC `!` prefix | SDK Bash tool |
|---|---|---|
| **Side** | Client-side (user's terminal) | Server-side (Claude requests execution, host implements) |
| **Session** | User's shell | Persistent bash session maintained by host |
| **Pricing** | No API cost (direct execution) | 245 input tokens per tool use + output tokens |
| **Approval** | None (direct) | Host controls execution policy |
| **State** | User's env | Persistent across tool calls (env vars, cwd) |

### SDK Bash Tool Key Patterns

- **Git-based checkpointing**: Commit baseline before agent work, commit per feature, revert on failure via `git checkout` ([source][sdk-bash])
- **Persistent session**: Environment variables and working directory persist between commands within a conversation
- **Security**: Run in isolated environments (Docker/VM), implement command filtering/allowlists, set resource limits with `ulimit` ([source][sdk-bash])
- **No interactive commands**: Cannot handle `vim`, `less`, or password prompts

### Community: Bash Permission Patterns

The `Bash(pattern:*)` syntax in `~/.claude.json` controls which commands Claude can execute per project ([source][claudelog-bash]):

```json
{
  "projects": {
    "/path/to/project": {
      "allowedTools": [
        "Bash(git *:*)",
        "Bash(npm run:*)",
        "Bash(make *:*)"
      ]
    }
  }
}
```

The `/permissions` command provides interactive visual management. Tab completion (v2.0.10+) mirrors standard terminal behavior ([source][claudelog-bash]).

**Security principle**: Use specific patterns (`Bash(git *:*)`) rather than blanket `Bash(*)`. Configure per-project for isolation ([source][claudelog-bash]).

## References

- [CC Interactive Mode docs][cc-interactive-mode]
- [CC Skills docs][cc-skills-docs]
- [CC Security docs][cc-security]
- [Agent SDK Bash tool][sdk-bash]
- [Claudelog — What is Bash Mode?][claudelog-bash]
- [DEV.to — The `!` prefix every Claude Code user needs][devto-bash-mode]
- [Snyk — ToxicSkills supply chain research][snyk-toxicskills]

[cc-interactive-mode]: https://code.claude.com/docs/en/interactive-mode
[cc-skills-docs]: https://code.claude.com/docs/en/slash-commands
[cc-security]: https://code.claude.com/docs/en/security
[sdk-bash]: https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool
[claudelog-bash]: https://claudelog.com/faqs/what-is-bash-mode/
[devto-bash-mode]: https://dev.to/rajeshroyal/stop-wasting-tokens-the-prefix-that-every-claude-code-user-needs-to-know-2c6i
[snyk-toxicskills]: https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/
