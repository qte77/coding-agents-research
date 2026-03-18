## Changelog Monitor Report

Last scanned version: **2.1.76**
New versions detected: **2**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.78 | 26 | 23 | 3 |
| 2.1.77 | 44 | 41 | 3 |

### Feature Coverage Details

#### v2.1.78

- **[covered]** - Added `StopFailure` hook event that fires when the turn ends due to an API error (rate limit, auth failure, etc.)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-status-monitoring-analysis.md`
- **[covered]** - Added `${CLAUDE_PLUGIN_DATA}` variable for plugin persistent state that survives plugin updates; `/plugin uninstall` prompts before deleting it
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Added `effort`, `maxTurns`, and `disallowedTools` frontmatter support for plugin-shipped agents
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-fast-mode-analysis.md`
- **[covered]** - Terminal notifications (iTerm2/Kitty/Ghostty popups, progress bar) now reach the outer terminal when running inside tmux with `set -g allow-passthrough on`
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed `git log HEAD` failing with "ambiguous argument" inside sandboxed Bash on Linux, and stub files polluting `git status` in the working directory
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed `cc log` and `--resume` silently truncating conversation history on large sessions (>5 MB) that used subagents
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed infinite loop when API errors triggered stop hooks that re-fed blocking errors to the model
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed `deny: ["mcp__servername"]` permission rules not removing MCP server tools before sending to the model, allowing it to see and attempt blocked tools
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-permissions-bypass-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Fixed `sandbox.filesystem.allowWrite` not working with absolute paths (previously required `//` prefix)
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - **Security:** Fixed silent sandbox disable when `sandbox.enabled: true` is set but dependencies are missing — now shows a visible startup warning
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed `.git`, `.claude`, and other protected directories being writable without a prompt in `bypassPermissions` mode
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed ctrl+u in normal mode scrolling instead of readline kill-line (ctrl+u/ctrl+d half-page scroll moved to transcript mode only)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed voice mode modifier-combo push-to-talk keybindings (e.g. ctrl+k) requiring a hold instead of activating immediately
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed voice mode not working on WSL2 with WSLg (Windows 11); WSL1/Win10 users now get a clear error
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed `--worktree` flag not loading skills and hooks from the worktree directory
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` and `includeGitInstructions` setting not suppressing the git status section in the system prompt
  - Covered by: `cc-native/context-memory/CC-llms-txt-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`
- **[covered]** - Fixed Bash tool not finding Homebrew and other PATH-dependent binaries when VS Code is launched from Dock/Spotlight
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed washed-out Claude orange color in VS Code/Cursor/code-server terminals that don't advertise truecolor support
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Added `ANTHROPIC_CUSTOM_MODEL_OPTION` env var to add a custom entry to the `/model` picker, with optional `_NAME` and `_DESCRIPTION` suffixed vars for display
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed `ANTHROPIC_BETAS` environment variable being silently ignored when using Haiku models
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Improved memory usage and startup time when resuming large sessions
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - [VSCode] Fixed a brief flash of the login screen when opening the sidebar while already authenticated
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - [VSCode] Fixed "API Error: Rate limit reached" when selecting Opus — model dropdown no longer offers 1M context variant to subscribers whose plan tier is unknown
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[UNCOVERED]** - Response text now streams line-by-line as it's generated
- **[UNCOVERED]** - Fixed `/sandbox` Dependencies tab showing Linux prerequisites on macOS instead of macOS-specific info
- **[UNCOVERED]** - Fixed queued prompts being concatenated without a newline separator

#### v2.1.77

- **[covered]** - Increased default maximum output token limits for Claude Opus 4.6 to 64k tokens, and the upper bound for Opus 4.6 and Sonnet 4.6 models to 128k tokens
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Added `allowRead` sandbox filesystem setting to re-allow read access within `denyRead` regions
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - `/copy` now accepts an optional index: `/copy N` copies the Nth-latest assistant response
  - Covered by: `cc-native/context-memory/CC-llms-txt-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed "Always Allow" on compound bash commands (e.g. `cd src && npm test`) saving a single rule for the full string instead of per-subcommand, leading to dead rules and repeated permission prompts
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed auto-updater starting overlapping binary downloads when the slash-command overlay repeatedly opened and closed, accumulating tens of gigabytes of memory
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed PreToolUse hooks returning `"allow"` bypassing `deny` permission rules, including enterprise managed settings
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed Write tool silently converting line endings when overwriting CRLF files or creating files in CRLF directories
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed memory growth in long-running sessions from progress messages surviving compaction
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed cost and token usage not being tracked when the API falls back to non-streaming mode
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` not stripping beta tool-schema fields, causing proxy gateways to reject requests
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/configuration/CC-hooks-system-analysis.md`
- **[covered]** - Fixed Bash tool reporting errors for successful commands when the system temp directory path contains spaces
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed paste being lost when typing immediately after pasting
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed Ctrl+D in `/feedback` text input deleting forward instead of the second press exiting the session
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed API error when dragging a 0-byte image file into the prompt
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-status-monitoring-analysis.md`
- **[covered]** - Fixed Claude Desktop sessions incorrectly using the terminal CLI's configured API key instead of OAuth
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `git-subdir` plugins at different subdirectories of the same monorepo commit colliding in the plugin cache
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed a race condition where stale-worktree cleanup could delete an agent worktree just resumed from a previous crash
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed input deadlock when opening `/mcp` or similar dialogs while the agent is running
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed Backspace and Delete keys not working in vim NORMAL mode
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed status line not updating when vim mode is toggled on or off
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed hyperlinks opening twice on Cmd+click in VS Code, Cursor, and other xterm.js-based terminals
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed background colors rendering as terminal-default inside tmux with default configuration
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed iTerm2 session crash when selecting text inside tmux over SSH
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed clipboard copy silently failing in tmux sessions; copy toast now indicates whether to paste with `⌘V` or tmux `prefix+]`
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed `←`/`→` accidentally switching tabs in settings, permissions, and sandbox dialogs while navigating lists
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-permissions-bypass-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed IDE integration not auto-connecting when Claude Code is launched inside tmux or screen
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed CJK characters visually bleeding into adjacent UI elements when clipped at the right edge
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed teammate panes not closing when the leader exits
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed iTerm2 auto mode not detecting iTerm2 for native split-pane teammates
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Faster startup on macOS (~60ms) by reading keychain credentials in parallel with module loading
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Faster `--resume` on fork-heavy and very large sessions — up to 45% faster loading and ~100-150MB less peak memory
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`
- **[covered]** - Improved `claude plugin validate` to check skill, agent, and command frontmatter plus `hooks/hooks.json`, catching YAML parse errors and schema violations
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Background bash tasks are now killed if output exceeds 5GB, preventing runaway processes from filling disk
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Sessions are now auto-named from plan content when you accept a plan
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Improved headless mode plugin installation to compose correctly with `CLAUDE_CODE_PLUGIN_SEED_DIR`
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Show a notice when `apiKeyHelper` takes longer than 10s, preventing it from blocking the main loop
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - The Agent tool no longer accepts a `resume` parameter — use `SendMessage({to: agentId})` to continue a previously spawned agent
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - `SendMessage` now auto-resumes stopped agents in the background instead of returning an error
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-status-monitoring-analysis.md`
- **[covered]** - Renamed `/fork` to `/branch` (`/fork` still works as an alias)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - [VSCode] Improved plan preview tab titles to use the plan's heading instead of "Claude's Plan"
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - [VSCode] When option+click doesn't trigger native selection on macOS, the footer now points to the `macOptionClickForcesSelection` setting
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[UNCOVERED]** - Fixed `--resume` silently truncating recent conversation history due to a race between memory-extraction writes and the main transcript
- **[UNCOVERED]** - Fixed ordered list numbers not rendering in terminal UI
- **[UNCOVERED]** - Improved Esc to abort in-flight non-streaming API requests

---
_Generated by `.github/scripts/changelog-compare.py`_

## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 12
- New uncovered: 0

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 1

| Entry | Section | Description |
|-------|---------|-------------|
| [FEATURE] Add Traditional Chinese (繁體中文 / zh-TW) localizatio | GitHub Issues (enhancement) | ## Feature Request

### Summary

Please add **Traditional Chinese (繁體中文, zh-TW)* |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **1**

_Generated by `.github/scripts/native-sources-monitor.py`_

