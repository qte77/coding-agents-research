---
title: Claude Code Sandboxing and Security Analysis
description: Analysis of CC sandboxing mechanics, configuration options, security model, and sandbox configuration options.
source: https://code.claude.com/docs/en/sandboxing, https://code.claude.com/docs/en/settings#sandbox-settings, https://code.claude.com/docs/en/security
category: analysis
created: 2026-03-07
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Research (informational)

## Summary

Claude Code sandboxing uses OS-level primitives to enforce filesystem and network
isolation on bash commands ([source][cc-sandboxing]). This replaces approval
fatigue with automated enforcement — commands that stay within sandbox boundaries
run without prompts.

**Both layers required**: Without network isolation, a compromised agent could
exfiltrate files (e.g., SSH keys). Without filesystem isolation, it could
backdoor system resources to gain network access ([source][cc-security]).

## Platform Support

| Platform | Mechanism | Setup |
| -------- | --------- | ----- |
| macOS | Seatbelt (built-in) | Works out of the box |
| Linux/WSL2 | bubblewrap + socat | `make setup_sandbox` or `sudo apt-get install bubblewrap socat` |
| WSL1 | Not supported | bubblewrap requires WSL2 kernel features |
| Windows | Not supported | Planned |

([source][cc-sandboxing])

## Example Configuration

From `.claude/settings.json` ([source][cc-sandbox-settings]):

```json
"sandbox": {
  "enabled": true,
  "autoAllowBashIfSandboxed": true,
  "allowUnsandboxedCommands": false,
  "enableWeakerNestedSandbox": false,
  "network": {
    "allowLocalBinding": true,
    "allowedHosts": ["api.github.com"]
  },
  "filesystem": {
    "write": {
      "allowOnly": ["/tmp/claude-1000", ".git"]
    }
  }
}
```

**Key choices:**

- [x] Sandbox enabled with auto-allow
- [x] Unsandboxed escape hatch disabled (`allowUnsandboxedCommands: false`)
- [x] Weaker nested sandbox disabled
- [x] Network restricted to `api.github.com` only
- [x] Filesystem writes restricted to `/tmp/claude-1000` and `.git`
- [ ] `raw.githubusercontent.com` not in `allowedHosts` — needed if fetching
  raw GitHub content
- [ ] No `allowedDomains` for PyPI/npm — package install commands must run
  outside sandbox or with `excludedCommands`

Setup on Linux/WSL2 ([source][cc-sandboxing]):

```bash
sudo apt-get install bubblewrap socat
```

Or via a Makefile recipe if your project defines one. Not typically bundled with
the default dev setup — must be run separately.

## Configuration Reference

### Core Settings

| Key | Description | Default |
| --- | ----------- | ------- |
| `sandbox.enabled` | Enable bash sandboxing | `false` |
| `sandbox.autoAllowBashIfSandboxed` | Auto-approve sandboxed bash commands | `true` |
| `sandbox.excludedCommands` | Commands that bypass sandbox entirely | — |
| `sandbox.allowUnsandboxedCommands` | Allow `dangerouslyDisableSandbox` escape hatch | `true` |

([source][cc-sandbox-settings])

### Filesystem

| Key | Description |
| --- | ----------- |
| `sandbox.filesystem.allowWrite` | Additional writable paths |
| `sandbox.filesystem.denyWrite` | Paths blocked from writing |
| `sandbox.filesystem.denyRead` | Paths blocked from reading |

**Defaults**: Write to CWD and subdirectories only. Read entire filesystem
except explicitly denied paths ([source][cc-sandbox-settings]).

### Network

| Key | Description |
| --- | ----------- |
| `sandbox.network.allowedDomains` | Domains allowed for outbound traffic (supports wildcards) |
| `sandbox.network.allowManagedDomainsOnly` | Only allow managed domains; block others silently |
| `sandbox.network.allowUnixSockets` | Specific Unix socket paths to allow |
| `sandbox.network.allowAllUnixSockets` | Allow all Unix socket connections |
| `sandbox.network.allowLocalBinding` | Allow binding to localhost ports (macOS only) |
| `sandbox.network.httpProxyPort` | HTTP proxy port |
| `sandbox.network.socksProxyPort` | SOCKS5 proxy port |

([source][cc-sandbox-settings])

### Security-Reducing Options

| Key | Description | Default |
| --- | ----------- | ------- |
| `enableWeakerNestedSandbox` | Weaker sandbox for unprivileged Docker (Linux/WSL2) | `false` |
| `enableWeakerNetworkIsolation` | Allow system TLS trust service (macOS) for `gh`, `gcloud`, `terraform` | `false` |

([source][cc-sandbox-settings])

### Path Prefix Conventions

| Prefix | Meaning | Example |
| ------ | ------- | ------- |
| `//` | Absolute from filesystem root | `//tmp/build` → `/tmp/build` |
| `~/` | Relative to home directory | `~/.kube` → `$HOME/.kube` |
| `/` | Relative to settings file directory | `/build` → `$SETTINGS_DIR/build` |

([source][cc-sandbox-settings])

### Array Merging Across Scopes

When `allowWrite`, `denyWrite`, or `denyRead` are defined in multiple settings
scopes (managed, user, project, local), arrays **merge** (concatenate +
deduplicate) rather than replace. No scope can accidentally remove another
scope's entries ([source][cc-sandbox-settings]).

## How It Works

### Filesystem Isolation

Enforced at OS level (Seatbelt on macOS, bubblewrap on Linux/WSL2). Restrictions
apply to **all subprocess commands** — `kubectl`, `terraform`, `npm`, not just
Claude's own file tools ([source][cc-sandboxing]).

### Network Isolation

Controlled through a **proxy server running outside the sandbox**. Only approved
domains pass through. Unapproved domain requests trigger permission prompts
(unless `allowManagedDomainsOnly` auto-blocks them) ([source][cc-sandboxing]).

### Escape Hatch

When a command fails due to sandbox restrictions, Claude may retry with
`dangerouslyDisableSandbox`. These go through the normal permission flow. Disable
with `allowUnsandboxedCommands: false` ([source][cc-sandboxing]).

### Two Sandbox Modes

**Auto-allow** (`/sandbox`): Sandboxed bash commands run without prompts.
Unsandboxable commands fall back to regular permission flow
([source][cc-sandboxing]).

**Regular permissions**: All bash commands go through standard permission flow
even when sandboxed. More control, more approvals.

## Relationship to Skills

Skills (`.claude/skills/`) are not explicitly addressed in sandbox docs.
Based on architecture:

- Skill instructions are processed by the model — not subject to sandbox
- Bash commands **executed by** a skill go through the sandboxed bash tool
- File read/edit operations by skills follow permission rules
- The `allowed-tools` frontmatter restricts which tools a skill can invoke,
  complementing sandbox restrictions

## Security Model

### What Sandbox Protects Against

- Modification of critical config files (`~/.bashrc`, `/bin/`)
- Data exfiltration to attacker-controlled servers
- Malicious dependency scripts (npm postinstall, etc.)
- Prompt injection via compromised build tools
- Unauthorized API calls

([source][cc-security])

### Known Limitations

| Limitation | Risk | Mitigation |
| ---------- | ---- | ---------- |
| No traffic inspection | Allowed domains can carry any payload | Only allow trusted domains |
| Domain fronting | Broad domains (e.g., `github.com`) may enable exfiltration | Use specific subdomains |
| Unix socket escalation | Docker socket grants host access | Avoid `allowAllUnixSockets` |
| Broad `allowWrite` | Write to `$PATH` dirs enables privilege escalation | Restrict to project dirs |
| Weaker nested sandbox | Considerably weakens security in unprivileged Docker | Keep disabled unless externally isolated |

([source][cc-sandboxing], [source][cc-security])

### Incompatible Commands

- `watchman` (used by `jest`) — use `jest --no-watchman`
- `docker` — add to `excludedCommands`

([source][cc-sandboxing])

## Additional Security Features (Non-Sandbox)

| Feature | Description |
| ------- | ----------- |
| Command blocklist | `curl` and `wget` blocked by default |
| Isolated WebFetch | Separate context window prevents prompt injection via web |
| Trust verification | First-time codebase runs require trust confirmation |
| Command injection detection | Suspicious bash commands require manual approval |
| Fail-closed matching | Unmatched commands default to requiring approval |
| Secure credential storage | API keys encrypted at rest |

([source][cc-security])

## Open Source Sandbox Runtime

The sandbox runtime is available as a standalone npm package
([source][sandbox-runtime]):

```bash
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Enables sandboxing outside Claude Code, including MCP servers.

## Cross-Repo Write Access Pattern

When a Claude Code session needs to operate on repos outside its CWD (e.g.,
sibling repos under `/workspaces/`), the Bash sandbox blocks writes by default.

**Symptom**: Write/Edit tools work on cross-repo files, but `git add`,
`git commit`, and other Bash commands fail with "Read-only file system."

**Root cause**: Write/Edit tools have their own permission model and bypass the
Bash sandbox entirely. Only Bash tool commands are subject to
`sandbox.filesystem` restrictions.

**Solution**: Add the parent workspace path to `write.allowOnly`:

```json
"sandbox": {
  "filesystem": {
    "write": {
      "allowOnly": ["/tmp/claude-1000", ".git", "/workspaces/qte77"]
    }
  }
}
```

**Alternatives**:

- Use `sandbox.filesystem.allowWrite` (additive, merges across scopes) instead
  of modifying `allowOnly`
- Set in `~/.claude/settings.json` (user-level) for global cross-repo access
- Use `permissions.additionalDirectories` to expand the overall permission scope

**Security note**: Adding broad paths like `/workspaces/` to `allowWrite`
expands the blast radius. Prefer specific repo paths over parent directories.

## See Also

For external sandbox platforms (OpenSandbox, E2B, Sprites.dev) that provide cloud
execution and stronger isolation (gVisor, Firecracker microVMs) beyond CC's local
bubblewrap/Seatbelt enforcement, see
[CC-sandbox-platforms-landscape.md](CC-sandbox-platforms-landscape.md).

## References

- [CC Sandboxing docs][cc-sandboxing]
- [CC Sandbox settings][cc-sandbox-settings]
- [CC Security docs][cc-security]
- [Sandbox runtime (open source)][sandbox-runtime]

[cc-sandboxing]: https://code.claude.com/docs/en/sandboxing
[cc-sandbox-settings]: https://code.claude.com/docs/en/settings#sandbox-settings
[cc-security]: https://code.claude.com/docs/en/security
[sandbox-runtime]: https://github.com/anthropic-experimental/sandbox-runtime
