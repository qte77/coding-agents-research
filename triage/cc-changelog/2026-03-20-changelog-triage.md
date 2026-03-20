## Changelog Monitor Report

Last scanned version: **2.1.78**
New versions detected: **2**

### New Versions Summary

| Version | Features | Covered | Uncovered |
|---------|----------|---------|-----------|
| 2.1.80 | 17 | 16 | 1 |
| 2.1.79 | 18 | 16 | 2 |

### Feature Coverage Details

#### v2.1.80

- **[covered]** - Added `rate_limits` field to statusline scripts for displaying Claude.ai rate limit usage (5-hour and 7-day windows with `used_percentage` and `resets_at`)
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Added `source: 'settings'` plugin marketplace source — declare plugin entries inline in settings.json
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Added CLI tool usage detection to plugin tips, in addition to file pattern matching
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Added `effort` frontmatter support for skills and slash commands to override the model effort level when invoked
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Added `--channels` (research preview) — allow MCP servers to push messages into your session
  - Covered by: `cc-native/CC-changelog-feature-scan.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`
- **[covered]** - Fixed `--resume` dropping parallel tool results — sessions with parallel tool calls now restore all tool_use/tool_result pairs instead of showing `[Tool result missing]` placeholders
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Fixed voice mode WebSocket failures caused by Cloudflare bot detection on non-browser TLS fingerprints
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed 400 errors when using fine-grained tool streaming through API proxies, Bedrock, or Vertex
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`
- **[covered]** - Fixed `/remote-control` appearing for gateway and third-party provider deployments where it cannot function
  - Covered by: `cc-native/ci-execution/CC-version-pinning-resilience.md`, `cc-native/configuration/CC-model-provider-configuration.md`
- **[covered]** - Improved responsiveness of `@` file autocomplete in large git repositories
  - Covered by: `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`
- **[covered]** - Improved `/effort` to show what auto currently resolves to, matching the status bar indicator
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - Improved `/permissions` — Tab and arrow keys now switch tabs from within a list
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Improved background tasks panel — left arrow now closes from the list view
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Simplified plugin install tips to use a single `/plugin install` command instead of a two-step flow
  - Covered by: `cc-native/agents-skills/CC-cli-anything-analysis.md`, `cc-native/agents-skills/CC-ralph-enhancement-research.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Reduced memory usage on startup in large repositories (~80 MB saved on 250k-file repos)
  - Covered by: `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`, `cc-native/examples/rules/context-management.md`
- **[covered]** - Fixed managed settings (`enabledPlugins`, `permissions.defaultMode`, policy-set env vars) not being applied at startup when `remote-settings.json` was cached from a prior session
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[UNCOVERED]** - Fixed `/sandbox` tab switching not responding to Tab or arrow keys

#### v2.1.79

- **[covered]** - Added `--console` flag to `claude auth login` for Anthropic Console (API billing) authentication
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `claude -p` hanging when spawned as a subprocess without explicit stdin (e.g. Python `subprocess.run`)
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`
- **[covered]** - Fixed Ctrl+C not working in `-p` (print) mode
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `/btw` returning the main agent's output instead of answering the side question when triggered during streaming
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[covered]** - Fixed voice mode not activating correctly on startup when `voiceEnabled: true` is set
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `CLAUDE_CODE_DISABLE_TERMINAL_TITLE` not preventing terminal title from being set on startup
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed custom status line showing nothing when workspace trust is blocking it
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-version-pinning-resilience.md`
- **[covered]** - Fixed enterprise users being unable to retry on rate limit (429) errors
  - Covered by: `cc-native/ci-execution/CC-github-actions-analysis.md`
- **[covered]** - Fixed `SessionEnd` hooks not firing when using interactive `/resume` to switch sessions
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - Improved startup memory usage by ~18MB across all scenarios
  - Covered by: `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/configuration/CC-hooks-system-analysis.md`, `cc-native/context-memory/CC-memory-system-analysis.md`
- **[covered]** - Improved non-streaming API fallback with a 2-minute per-attempt timeout, preventing sessions from hanging indefinitely
  - Covered by: `cc-native/CC-inline-visuals-analysis.md`, `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-cli-anything-analysis.md`
- **[covered]** - `CLAUDE_CODE_PLUGIN_SEED_DIR` now supports multiple seed directories separated by the platform path delimiter (`:` on Unix, `;` on Windows)
  - Covered by: `cc-native/ci-execution/CC-sandbox-platforms-landscape.md`, `cc-native/ci-execution/CC-sandboxing-analysis.md`, `cc-native/context-memory/CC-llms-txt-analysis.md`
- **[covered]** - [VSCode] Added `/remote-control` — bridge your session to claude.ai/code to continue from a browser or phone
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-cloud-sessions-analysis.md`
- **[covered]** - [VSCode] Session tabs now get AI-generated titles based on your first message
  - Covered by: `cc-native/agents-skills/CC-recursive-spawning-patterns.md`, `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/ci-execution/CC-remote-control-analysis.md`
- **[covered]** - [VSCode] Fixed the thinking pill showing "Thinking" instead of "Thought for Ns" after a response completes
  - Covered by: `cc-native/agents-skills/CC-skills-adoption-analysis.md`, `cc-native/plugins-ecosystem/CC-plugin-packaging-research.md`
- **[covered]** - [VSCode] Fixed missing session diff button when opening sessions from the left sidebar
  - Covered by: `cc-native/agents-skills/CC-agent-teams-orchestration.md`, `cc-native/agents-skills/CC-plans-as-skill-rule-templates.md`, `cc-native/agents-skills/CC-recursive-spawning-patterns.md`
- **[UNCOVERED]** - Added "Show turn duration" toggle to the `/config` menu
- **[UNCOVERED]** - Fixed left/right arrow tab navigation in `/permissions`

---
_Generated by `.github/scripts/changelog-compare.py`_

## Native Sources Monitor Report

Sources checked: **3**

### anthropic-blog

- Source: Anthropic Blog — announcements and product updates
- Entries fetched: 13
- New uncovered: 3

| Entry | Section | Description |
|-------|---------|-------------|
| Mar 5, 2026AnnouncementsWhere things stand with the Departme | Anthropic Blog | Mar 5, 2026AnnouncementsWhere things stand with the Department of War |
| Feb 27, 2026AnnouncementsStatement on the comments from Secr | Anthropic Blog | Feb 27, 2026AnnouncementsStatement on the comments from Secretary of War Pete He |
| Feb 26, 2026AnnouncementsStatement from Dario Amodei on our  | Anthropic Blog | Feb 26, 2026AnnouncementsStatement from Dario Amodei on our discussions with the |

### cc-issues-enhancement

- Source: CC GitHub Issues labeled 'enhancement'
- Entries fetched: 300
- New uncovered: 5

| Entry | Section | Description |
|-------|---------|-------------|
| Add solarized-light theme | GitHub Issues (enhancement) | ## Feature request

Please add a `solarized-light` theme to complement the exist |
| [FEATURE] Use ''git rev-parse --git-common-dir'' for groupin | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |
| [FEATURE] Allow customizing the past tense thinking verb ("C | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |
| [FEATURE]  Dispatch for Claude CLI | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |
| [FEATURE] Incognito mode in Claude Code #9044 | GitHub Issues (enhancement) | ### Preflight Checklist

- [x] I have searched [existing requests](https://githu |

### cc-discussions-feature-request

- Source: CC GitHub Discussions in feature-request category
- Entries fetched: 0
- New uncovered: 0

---
Total new uncovered entries: **8**

_Generated by `.github/scripts/native-sources-monitor.py`_

