---
title: CC Version Pinning & Provider Resilience
source: https://code.claude.com/docs/en/setup, https://www.npmjs.com/package/@anthropic-ai/claude-code, https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners, https://www.vcluster.com/blog/comparing-coder-vs-codespaces-vs-gitpod-vs-devpod
purpose: Document how to pin Claude Code versions for reproducible CI/CD and container environments, self-hosted runners, cloud dev environments, and resilience against Anthropic API outages or discontinuation.
created: 2026-03-12
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Reference (actionable configuration guide)

## Context

Claude Code auto-updates by default, which is fine for interactive development but problematic for containers, CI/CD pipelines, and reproducible builds. Additionally, relying solely on Anthropic's API creates a single point of failure. This document covers version pinning for stability and provider diversification for resilience.

## Version Pinning

### Native Installer (Recommended)

The native installer accepts a specific version number or release channel ([source][cc-setup]).

```bash
# Pin to exact version
curl -fsSL https://claude.ai/install.sh | bash -s 2.1.42

# Pin to stable channel (~1 week behind latest, skips regressions)
curl -fsSL https://claude.ai/install.sh | bash -s stable

# Latest (default)
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell:**

```powershell
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.42
```

### npm (Deprecated but Useful for Pinning)

npm installation is deprecated but still works. It provides the most familiar version pinning for Node.js ecosystems ([source][cc-setup]).

```bash
npm install -g @anthropic-ai/claude-code@2.1.42
```

Check latest version: `npm view @anthropic-ai/claude-code dist-tags.latest`

**Warning**: Anthropic may drop the npm package in the future. Track [this issue](https://github.com/anthropics/claude-code/issues/24568) for deprecation timeline.

### Disable Auto-Updates

Pinning a version is pointless if CC auto-updates over it. Disable the updater ([source][cc-setup]):

```json
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

Or pass as env var: `DISABLE_AUTOUPDATER=1 claude`

### Release Channels

| Channel | Behavior | Use Case |
|---|---|---|
| `latest` (default) | Newest features immediately | Interactive dev |
| `stable` | ~1 week behind, skips regressions | CI/CD, containers |

Configure via `/config` or settings.json: `"autoUpdatesChannel": "stable"` ([source][cc-setup]).

## Docker / Container Setup

### Dockerfile with Version Pinning (Native Installer)

```dockerfile
FROM node:20-slim

ARG CLAUDE_CODE_VERSION=2.1.42

# Native installer with pinned version
RUN curl -fsSL https://claude.ai/install.sh | bash -s ${CLAUDE_CODE_VERSION}

# Disable auto-updates inside container
ENV DISABLE_AUTOUPDATER=1

# API key injected at runtime, never baked into image
# docker run -e ANTHROPIC_API_KEY="$KEY" ...
```

### Dockerfile with npm Pinning (Legacy)

```dockerfile
FROM node:20-slim

ARG CLAUDE_CODE_VERSION=2.1.42

RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}
ENV DISABLE_AUTOUPDATER=1
```

**Use `node:20-slim` not `node:20-alpine`** — Alpine's musl libc causes occasional compatibility issues with native npm packages ([source][datacamp-docker]).

### Runtime

```bash
# Pass API key at runtime (never in Dockerfile)
docker run --rm \
  -e ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
  -v "$(pwd):/workspace" \
  -w /workspace \
  my-claude-image claude -p "your prompt"

# Or with alternative provider
docker run --rm \
  -e ANTHROPIC_BASE_URL="http://host.docker.internal:11434" \
  -e ANTHROPIC_AUTH_TOKEN="ollama" \
  -e ANTHROPIC_API_KEY="" \
  my-claude-image claude --model qwen3-coder -p "your prompt"
```

## GitHub Actions

### Using claude-code-action

Anthropic provides an official GHA action ([source][cc-action]):

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

This handles version management internally. Pin with a commit SHA for reproducibility:

```yaml
- uses: anthropics/claude-code-action@abc1234  # pin to commit
```

### Self-Managed in GHA

For full control over the CC version:

```yaml
jobs:
  ai-task:
    runs-on: ubuntu-latest
    env:
      CLAUDE_CODE_VERSION: "2.1.42"
      DISABLE_AUTOUPDATER: "1"
    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code (pinned)
        run: curl -fsSL https://claude.ai/install.sh | bash -s ${{ env.CLAUDE_CODE_VERSION }}

      - name: Run task
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: claude -p "your prompt" --output-format json
```

**Note**: `-p` mode now supports structured output schemas (v2.1.22), not just the `json` format flag — enables enforcing result schemas (e.g., pass/fail/error + identifiers) directly in CLI calls, reducing parsing brittleness in shell wrapper scripts.

### With Alternative Provider in GHA

```yaml
      - name: Run with OpenRouter fallback
        env:
          ANTHROPIC_BASE_URL: "https://openrouter.ai/api"
          ANTHROPIC_AUTH_TOKEN: ${{ secrets.OPENROUTER_API_KEY }}
          ANTHROPIC_API_KEY: ""
        run: claude -p "your prompt" --output-format json
```

## Self-Hosted Runners

### When to Use Self-Hosted Runners

GitHub-hosted runners (`ubuntu-latest`) work for most CC workloads but have limitations:

| Concern | GitHub-Hosted | Self-Hosted |
|---|---|---|
| **Custom hardware** | Fixed specs (2-4 vCPU) | Any spec (GPU, high-memory) |
| **Compliance** | Shared infrastructure | On-premises, air-gapped capable |
| **Cost at scale** | Per-minute billing | Free with GHA (you pay infrastructure) |
| **Pre-installed tools** | Fresh VM each run | Persistent or pre-baked images |
| **Network access** | Public internet only | Private network, VPN, internal APIs |

Self-hosted runners can be physical, virtual, in a container, on-premises, or in a cloud. They're free to use with GitHub Actions — you pay only for your own infrastructure ([source][gh-runners]).

### Supported Platforms

Self-hosted runners support a wide range of OS and architecture combinations ([source][gh-runners-req]):

| OS | Architectures |
|---|---|
| Linux | x64, ARM64 |
| macOS | x64, ARM64 (Apple Silicon) |
| Windows | x64, ARM64 |

### Deployment Levels

| Level | Scope | Use Case |
|---|---|---|
| Repository | Single repo | Project-specific CC workflows |
| Organization | Multiple repos | Shared CC runner pool across team |
| Enterprise | Multiple orgs | Centralized CC infrastructure |

### Ephemeral Runners

Use `--ephemeral` for clean CC execution per job — the runner picks up one job and then un-registers itself ([source][gh-runners]):

```bash
./config.sh --url https://github.com/ORG/REPO --token TOKEN --ephemeral
```

**CC-specific benefit**: Each job starts with a clean filesystem. No risk of CC state leakage (auto memory, cached plugins, session artifacts) between jobs.

**Trade-off**: Longer startup time (re-register + re-install CC per job). Mitigate by pre-baking CC into the runner image.

### Network Requirements

Self-hosted runners need outbound HTTPS (443) to these domains ([source][gh-runners-net]):

| Domain | Purpose |
|---|---|
| `github.com` | Repository access |
| `api.github.com` | API calls |
| `*.actions.githubusercontent.com` | Action downloads, artifacts |
| `ghcr.io`, `*.ghcr.io` | Container registry |
| `objects.githubusercontent.com` | Release asset downloads |

**CC-specific additions**:

| Domain | Purpose |
|---|---|
| `api.anthropic.com` | Anthropic API (primary) |
| `claude.ai` | CC installer + auto-updates |
| `storage.googleapis.com` | CC binary distribution |
| OpenRouter / Bedrock / Vertex endpoints | If using fallback providers |

### Autoscaling Options

| Method | Infrastructure | Complexity | Best For |
|---|---|---|---|
| **ARC (Actions Runner Controller)** | Kubernetes | High | Large-scale K8s environments |
| **Runner Scale Sets** | Kubernetes (ARC v2) | Medium | Modern K8s with event-driven scaling |
| **Webhook-based** | Any (Lambda, Cloud Functions) | Medium | Serverless / cloud-native |
| **Scheduled** | Any (cron, systemd) | Low | Predictable workloads |

### Security Considerations

- Runners receive **automatic updates** for the runner application only (within 30 days). OS and other software is your responsibility ([source][gh-runners])
- **Don't need a clean instance** for every job — but for CC, ephemeral mode is recommended to prevent state leakage
- **Log forwarding**: Configure centralized logging for audit trails of CC command execution
- **Minimal permissions**: Run the runner process as a dedicated non-root user
- Runners don't have access to other runners' data at the GitHub level, but shared infrastructure must be hardened

### CC-Specific Runner Configuration

```dockerfile
FROM ubuntu:22.04

ARG CLAUDE_CODE_VERSION=2.1.42
ARG RUNNER_VERSION=2.321.0

# Install runner
RUN mkdir /actions-runner && cd /actions-runner \
    && curl -o runner.tar.gz -L \
       https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz \
    && tar xzf runner.tar.gz && rm runner.tar.gz

# Install CC (pinned version)
RUN curl -fsSL https://claude.ai/install.sh | bash -s ${CLAUDE_CODE_VERSION}

# Disable auto-updates — version is baked into the image
ENV DISABLE_AUTOUPDATER=1

# API key injected at runtime
# docker run -e ANTHROPIC_API_KEY="$KEY" ...
```

**Checklist for self-hosted CC runners**:

- [ ] Pin CC version in runner image (native installer or npm)
- [ ] Set `DISABLE_AUTOUPDATER=1`
- [ ] Inject `ANTHROPIC_API_KEY` at runtime, never bake into image
- [ ] Use `--ephemeral` for clean state per job
- [ ] Allow outbound HTTPS to `api.anthropic.com` and `claude.ai`
- [ ] Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` if minimizing outbound calls
- [ ] Configure log forwarding for CC command audit trails
- [ ] Set resource limits (memory, CPU) appropriate for CC workloads

## Binary Integrity Verification

SHA256 checksums are published for each release ([source][cc-setup]):

```text
https://storage.googleapis.com/claude-code-dist-.../claude-code-releases/{VERSION}/manifest.json
```

Signed binaries: macOS (signed by "Anthropic PBC", Apple notarized), Windows (signed by "Anthropic, PBC").

## Provider Resilience Strategy

### Risk: Anthropic API Outage or Discontinuation

CC communicates via the Anthropic Messages API (`/v1/messages`). If Anthropic's API is unavailable, CC stops working — unless configured with an alternative endpoint.

### Mitigation Layers

| Layer | Mechanism | Effort | Coverage |
|---|---|---|---|
| **1. OpenRouter** | `ANTHROPIC_BASE_URL=https://openrouter.ai/api` | Low (env vars) | API outage failover to same models via different route |
| **2. Cloud providers** | Bedrock / Vertex / Foundry | Medium | Same Anthropic models via cloud infrastructure |
| **3. Local models** | Ollama + open-weight models | Medium | Full independence from any API provider |
| **4. LLM gateway** | LiteLLM / Bifrost proxy | Medium | Route to any provider; switch at proxy level |

### Recommended Resilience Configuration

For CI/CD pipelines that must not fail due to API outages:

```yaml
# Primary: Anthropic direct
ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# Fallback: OpenRouter (same models, different route)
# ANTHROPIC_BASE_URL: "https://openrouter.ai/api"
# ANTHROPIC_AUTH_TOKEN: ${{ secrets.OPENROUTER_API_KEY }}

# Emergency: Local model (no external dependency)
# ANTHROPIC_BASE_URL: "http://localhost:11434"
# ANTHROPIC_AUTH_TOKEN: "ollama"
```

Implement failover in a wrapper script:

```bash
#!/usr/bin/env bash
# cc-resilient.sh — try Anthropic, fall back to OpenRouter
if claude -p "$@" 2>/dev/null; then
  exit 0
fi

echo "Anthropic API unavailable, falling back to OpenRouter"
ANTHROPIC_BASE_URL="https://openrouter.ai/api" \
ANTHROPIC_AUTH_TOKEN="$OPENROUTER_API_KEY" \
ANTHROPIC_API_KEY="" \
claude -p "$@"
```

### Full Independence from Anthropic

For scenarios where Anthropic may be entirely unavailable (business discontinuation, regional blocking, air-gapped environments):

1. **Pin a known-good CC version** — store the binary or npm package in your own artifact registry
2. **Use Ollama or llama.cpp** — run open-weight models locally, zero external API dependency
3. **Disable all Anthropic traffic** — `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` + `DISABLE_AUTOUPDATER=1`
4. **Cache the installer** — download `https://claude.ai/install.sh` to your artifact registry for offline install

**Important limitation**: CC still phones home for license validation on startup. Fully air-gapped operation is not officially supported. For true offline use, the local model + proxy approach with login bypass (`"hasCompletedOnboarding": true` in `~/.claude.json`) is the closest workaround ([source][local-setup]).

## Version Pinning Checklist

- [ ] Pin CC version in Dockerfile / GHA workflow
- [ ] Set `DISABLE_AUTOUPDATER=1`
- [ ] Choose release channel: `stable` for CI, `latest` for dev
- [ ] Never bake API keys into images — inject at runtime
- [ ] Configure at least one fallback provider (OpenRouter recommended)
- [ ] Verify binary integrity via SHA256 manifest for production images
- [ ] Test fallback provider path in CI before relying on it

## References

- [CC Advanced Setup — Version Pinning][cc-setup]
- [CC GitHub Action][cc-action]
- [@anthropic-ai/claude-code npm package][npm-cc]
- [CC Docker Tutorial (DataCamp)][datacamp-docker]
- [CC Model & Provider Configuration](../configuration/CC-model-provider-configuration.md)
- [Local setup guide][local-setup]
- [GitHub Self-Hosted Runners][gh-runners]

[cc-setup]: https://code.claude.com/docs/en/setup
[cc-action]: https://github.com/anthropics/claude-code-action
[npm-cc]: https://www.npmjs.com/package/@anthropic-ai/claude-code
[datacamp-docker]: https://www.datacamp.com/tutorial/claude-code-docker
[local-setup]: https://medium.com/@luongnv89/run-claude-code-on-local-cloud-models-in-5-minutes-ollama-openrouter-llama-cpp-6dfeaee03cda
[gh-runners]: https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners
[gh-runners-req]: https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#requirements-for-self-hosted-runner-machines
[gh-runners-net]: https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#communication-requirements
