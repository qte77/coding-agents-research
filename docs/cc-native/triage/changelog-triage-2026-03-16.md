## Changelog Monitor Report

Last scanned version: **2.1.71**
New versions detected: **5**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.76 | 35 | 35 | 0 |
| 2.1.75 | 19 | 18 | 1 |
| 2.1.74 | 17 | 17 | 0 |
| 2.1.73 | 26 | 24 | 2 |
| 2.1.72 | 51 | 49 | 2 |

### Feature Coverage Details

#### v2.1.76

- **[covered]** - Added MCP elicitation support — MCP servers can now request structured input mid-task via an interactive dialog (form fields or browser URL)
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Added new `Elicitation` and `ElicitationResult` hooks to intercept and override responses before they're sent back
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Added `-n` / `--name <name>` CLI flag to set a display name for the session at startup
  - Covered by: `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`
- **[covered]** - Added `worktree.sparsePaths` setting for `claude --worktree` in large monorepos to check out only the directories you need via git sparse-checkout
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Added `PostCompact` hook that fires after compaction completes
  - Covered by: `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Added `/effort` slash command to set model effort level
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Added session quality survey — enterprise admins can configure the sample rate via the `feedbackSurveyRate` setting
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed deferred tools (loaded via `ToolSearch`) losing their input schemas after conversation compaction, causing array and number parameters to be rejected with type errors
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed slash commands showing "Unknown skill"
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed plan mode asking for re-approval after the plan was already accepted
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed voice mode swallowing keypresses while a permission dialog or plan editor was open
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed `/voice` not working on Windows when installed via npm
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed spurious "Context limit reached" when invoking a skill with `model:` frontmatter on a 1M-context session
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed "adaptive thinking is not supported on this model" error when using non-standard model strings
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed `Bash(cmd:*)` permission rules not matching when a quoted argument contains `#`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed "don't ask again" in the Bash permission dialog showing the full raw command for pipes and compound commands
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed auto-compaction retrying indefinitely after consecutive failures — a circuit breaker now stops after 3 attempts
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed MCP reconnect spinner persisting after successful reconnection
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed LSP plugins not registering servers when the LSP Manager initialized before marketplaces were reconciled
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed clipboard copying in tmux over SSH — now attempts both direct terminal write and tmux clipboard integration
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed `/export` showing only the filename instead of the full file path in the success message
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed transcript not auto-scrolling to new messages after selecting text
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed Escape key not working to exit the login method selection screen
  - Covered by: `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-model-provider-configuration.md`
- **[covered]** - Fixed several Remote Control issues: sessions silently dying when the server reaps an idle environment, rapid messages being queued one-at-a-time instead of batched, and stale work items causing redelivery after JWT refresh
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed bridge sessions failing to recover after extended WebSocket disconnects
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed slash commands not found when typing the exact name of a soft-hidden command
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Improved `--worktree` startup performance by reading git refs directly and skipping redundant `git fetch` when the remote branch is already available locally
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Improved background agent behavior — killing a background agent now preserves its partial results in the conversation context
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Improved model fallback notifications — now always visible instead of hidden behind verbose mode, with human-friendly model names
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Improved blockquote readability on dark terminal themes — text is now italic with a left bar instead of dim
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/context-memory/CC-extended-context-analysis.md`
- **[covered]** - Improved stale worktree cleanup — worktrees left behind after an interrupted parallel run are now automatically cleaned up
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Improved Remote Control session titles — now derived from your first prompt instead of showing "Interactive session"
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Improved `/voice` to show your dictation language on enable and warn when your `language` setting isn't supported for voice input
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Updated `--plugin-dir` to only accept one path to support subcommands — use repeated `--plugin-dir` for multiple directories
  - Covered by: `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - [VSCode] Fixed gitignore patterns containing commas silently excluding entire filetypes from the @-mention file picker
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`

#### v2.1.75

- **[covered]** - Added 1M context window for Opus 4.6 by default for Max, Team, and Enterprise plans (previously required extra usage)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Added `/color` command for all users to set a prompt-bar color for your session
  - Covered by: `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Added session name display on the prompt bar when using `/rename`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Added last-modified timestamps to memory files, helping Claude reason about which memories are fresh vs. stale
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Added hook source display (settings/plugin/skill) in permission prompts when a hook requires confirmation
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed voice mode not activating correctly on fresh installs without toggling `/voice` twice
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed the Claude Code header not updating the displayed model name after switching models with `/model` or Option+P
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed session crash when an attachment message computation returns undefined values
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed Bash tool mangling `!` in piped commands (e.g., `jq 'select(.x != .y)'` now works correctly)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed managed-disabled plugins showing up in the `/plugin` Installed tab — plugins force-disabled by your organization are now hidden
  - Covered by: `cc-native/configuration/CC-bash-mode-analysis.md`, `cc-native/plugins-ecosystem/CC-cowork-plugins-enterprise-analysis.md`, `cc-native/plugins-ecosystem/CC-official-plugins-landscape.md`
- **[covered]** - Fixed token estimation over-counting for thinking and `tool_use` blocks, preventing premature context compaction
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed corrupted marketplace config path handling
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed `/resume` losing session names after resuming a forked or continued session
  - Covered by: `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed Esc not closing the `/status` dialog after visiting the Config tab
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed input handling when accepting or rejecting a plan
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed footer hint in agent teams showing "↓ to expand" instead of the correct "shift + ↓ to expand"
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Suppressed async hook completion messages by default (visible with `--verbose` or transcript mode)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Breaking change: Removed deprecated Windows managed settings fallback at `C:\ProgramData\ClaudeCode\managed-settings.json` — use `C:\Program Files\ClaudeCode\managed-settings.json`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[UNCOVERED]** - Improved startup performance on macOS non-MDM machines by skipping unnecessary subprocess spawns

#### v2.1.74

- **[covered]** - Added actionable suggestions to `/context` command — identifies context-heavy tools, memory bloat, and capacity warnings with specific optimization tips
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`
- **[covered]** - Added `autoMemoryDirectory` setting to configure a custom directory for auto-memory storage
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed memory leak where streaming API response buffers were not released when the generator was terminated early, causing unbounded RSS growth on the Node.js/npm code path
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed managed policy `ask` rules being bypassed by user `allow` rules or skill `allowed-tools`
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Fixed full model IDs (e.g., `claude-opus-4-5`) being silently ignored in agent frontmatter `model:` field and `--agents` JSON config — agents now accept the same model values as `--model`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed MCP OAuth authentication hanging when the callback port is already in use
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed MCP OAuth refresh never prompting for re-auth after the refresh token expires, for OAuth servers that return errors with HTTP 200 (e.g. Slack)
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/configuration/CC-hooks-system-analysis.md`
- **[covered]** - Fixed voice mode silently failing on the macOS native binary for users whose terminal had never been granted microphone permission — the binary now includes the `audio-input` entitlement so macOS prompts correctly
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `SessionEnd` hooks being killed after 1.5 s on exit regardless of `hook.timeout` — now configurable via `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed `/plugin install` failing inside the REPL for marketplace plugins with local sources
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed marketplace update not syncing git submodules — plugin sources in submodules no longer break after update
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed unknown slash commands with arguments silently dropping input — now shows your input as a warning
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed Hebrew, Arabic, and other RTL text not rendering correctly in Windows Terminal, conhost, and VS Code integrated terminal
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed LSP servers not working on Windows due to malformed file URIs
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`
- **[covered]** - Changed `--plugin-dir` so local dev copies now override installed marketplace plugins with the same name (unless that plugin is force-enabled by managed settings)
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - [VSCode] Fixed delete button not working for Untitled sessions
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - [VSCode] Improved scroll wheel responsiveness in the integrated terminal with terminal-aware acceleration
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`

#### v2.1.73

- **[covered]** - Added `modelOverrides` setting to map model picker entries to custom provider model IDs (e.g. Bedrock inference profile ARNs)
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Added actionable guidance when OAuth login or connectivity checks fail due to SSL certificate errors (corporate proxies, `NODE_EXTRA_CA_CERTS`)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed freezes and 100% CPU loops triggered by permission prompts for complex bash commands
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Fixed a deadlock that could freeze Claude Code when many skill files changed at once (e.g. during `git pull` in a repo with a large `.claude/skills/` directory)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed Bash tool output being lost when running multiple Claude Code sessions in the same project directory
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed subagents with `model: opus`/`sonnet`/`haiku` being silently downgraded to older model versions on Bedrock, Vertex, and Microsoft Foundry
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed background bash processes spawned by subagents not being cleaned up when the agent exits
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed `/resume` showing the current session in the picker
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Fixed `/ide` crashing with `onInstall is not defined` when auto-installing the extension
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed `/loop` not being available on Bedrock/Vertex/Foundry and when telemetry was disabled
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed SessionStart hooks firing twice when resuming a session via `--resume` or `--continue`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed JSON-output hooks injecting no-op system-reminder messages into the model's context on every turn
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed voice mode session corruption when a slow connection overlaps a new recording
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed Linux sandbox failing to start with "ripgrep (rg) not found" on native builds
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed Linux native modules not loading on Amazon Linux 2 and other glibc 2.26 systems
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed "media_type: Field required" API error when receiving images via Remote Control
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `/heapdump` failing on Windows with `EEXIST` error when the Desktop folder already exists
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Improved Up arrow after interrupting Claude — now restores the interrupted prompt and rewinds the conversation in one step
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Improved `/effort` to work while Claude is responding, matching `/model` behavior
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Improved voice mode to automatically retry transient connection failures during rapid push-to-talk re-press
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Improved the Remote Control spawn mode selection prompt with better context
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Changed default Opus model on Bedrock, Vertex, and Microsoft Foundry to Opus 4.6 (was Opus 4.1)
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Deprecated `/output-style` command — use `/config` instead. Output style is now fixed at session start for better prompt caching
  - Covered by: `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - VSCode: Fixed HTTP 400 errors for users behind proxies or on Bedrock/Vertex with Claude 4.5 models
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[UNCOVERED]** - Improved IDE detection speed at startup
- **[UNCOVERED]** - Improved clipboard image pasting performance on macOS

#### v2.1.72

- **[covered]** - Fixed tool search to activate even with `ANTHROPIC_BASE_URL` as long as `ENABLE_TOOL_SEARCH` is set.
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Added `w` key in `/copy` to write the focused selection directly to a file, bypassing the clipboard (useful over SSH)
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Added optional description argument to `/plan` (e.g., `/plan fix the auth bug`) that enters plan mode and immediately starts
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Added `ExitWorktree` tool to leave an `EnterWorktree` session
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Added `CLAUDE_CODE_DISABLE_CRON` environment variable to immediately stop scheduled cron jobs mid-session
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Added `lsof`, `pgrep`, `tput`, `ss`, `fd`, and `fdfind` to the bash auto-approval allowlist, reducing permission prompts for common read-only operations
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Restored the `model` parameter on the Agent tool for per-invocation model overrides
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Simplified effort levels to low/medium/high (removed max) with new symbols (○ ◐ ●) and a brief notification instead of a persistent icon. Use `/effort auto` to reset to default
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Improved `/config` — Escape now cancels changes, Enter saves and closes, Space toggles settings
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Improved up-arrow history to show current session's messages first when running multiple concurrent sessions
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Improved voice input transcription accuracy for repo names and common dev terms (regex, OAuth, JSON)
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Improved bash command parsing by switching to a native module — faster initialization and no memory leak
  - Covered by: `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Changed CLAUDE.md HTML comments (`<!-- ... -->`) to be hidden from Claude when auto-injected. Comments remain visible when read with the Read tool
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed slow exits when background tasks or hooks were slow to respond
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed agent task progress stuck on "Initializing…"
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed skill hooks firing twice per event when a hooks-enabled skill is invoked by the model
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed several voice mode issues: occasional input lag, false "No speech detected" errors after releasing push-to-talk, and stale transcripts re-filling the prompt after submission
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `--continue` not resuming from the most recent point after `--compact`
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed bash security parsing edge cases
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Added support for marketplace git URLs without `.git` suffix (Azure DevOps, AWS CodeCommit)
  - Covered by: `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-model-provider-configuration.md`
- **[covered]** - Improved marketplace clone failure messages to show diagnostic info even when git produces no stderr
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed several plugin issues: installation failing on Windows with `EEXIST` error in OneDrive folders, marketplace blocking user-scope installs when a project-scope install exists, `CLAUDE_CODE_PLUGIN_CACHE_DIR` creating literal `~` directories, and `plugin.json` with marketplace-only fields failing to load
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed feedback survey appearing too frequently in long sessions
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed `--effort` CLI flag being reset by unrelated settings writes on startup
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed backgrounded Ctrl+B queries losing their transcript or corrupting the new conversation after `/clear`
  - Covered by: `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed worktree isolation issues: Task tool resume not restoring cwd, and background task notifications missing `worktreePath` and `worktreeBranch`
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`
- **[covered]** - Fixed `/model` not displaying results when run while Claude is working
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed digit keys selecting menu options instead of typing in plan mode permission prompt's text input
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed sandbox permission issues: certain file write operations incorrectly allowed without prompting, and output redirections to allowlisted directories (like `/tmp/claude/`) prompting unnecessarily
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - Improved CPU utilization in long sessions
  - Covered by: `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed prompt cache invalidation in SDK `query()` calls, reducing input token costs up to 12x
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed Escape key becoming unresponsive after cancelling a query
  - Covered by: `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - Fixed double Ctrl+C not exiting when background agents or tasks are running
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed team agents to inherit the leader's model
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed "Always Allow" saving permission rules that never match again
  - Covered by: `cc-native/configuration/CC-bash-mode-analysis.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`
- **[covered]** - Fixed several hooks issues: `transcript_path` pointing to the wrong directory for resumed/forked sessions, agent `prompt` being silently deleted from settings.json on every settings write, PostToolUse block reason displaying twice, async hooks not receiving stdin with bash `read -r`, and validation error message showing an example that fails validation
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed session crashes in Desktop/SDK when Read returned files containing U+2028/U+2029 characters
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - Fixed terminal title being cleared on exit even when `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` was set
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed several permission rule matching issues: wildcard rules not matching commands with heredocs, embedded newlines, or no arguments; `sandbox.excludedCommands` failing with env var prefixes; "always allow" suggesting overly broad prefixes for nested CLI tools; and deny rules not applying to all command forms
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed oversized and truncated images from Bash data-URL output
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed a crash when resuming sessions that contained Bedrock API errors
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Fixed intermittent "expected boolean, received string" validation errors on Edit, Bash, and Grep tool inputs
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed multi-line session titles when forking from a conversation whose first message contained newlines
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed queued messages not showing attached images, and images being lost when pressing ↑ to edit a queued message
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed parallel tool calls where a failed Read/WebFetch/Glob would cancel its siblings — only Bash errors now cascade
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/configuration/CC-bash-mode-analysis.md`
- **[covered]** - VSCode: Fixed scroll speed in integrated terminals not matching native terminals
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-remote-access-landscape.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - VSCode: Fixed Shift+Enter submitting input instead of inserting a newline for users with older keybindings
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - VSCode: Added effort level indicator on the input border
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/configuration/CC-fast-mode-analysis.md`
- **[covered]** - VSCode: Added `vscode://anthropic.claude-code/open` URI handler to open a new Claude Code tab programmatically, with optional `prompt` and `session` query parameters
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[UNCOVERED]** - Reduced bundle size by ~510 KB
- **[UNCOVERED]** - Fixed `/clear` killing background agent/bash tasks — only foreground tasks are now cleared

---
_Generated by `.github/scripts/changelog-compare.py`_

