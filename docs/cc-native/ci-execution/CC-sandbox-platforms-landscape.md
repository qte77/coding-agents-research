---
title: CC Sandbox Platforms Landscape
source: https://github.com/alibaba/OpenSandbox, https://e2b.dev, https://sprites.dev, https://code.claude.com/docs/en/sandboxing
purpose: Comparison of external sandbox platforms for AI agent code execution — self-hosted and cloud options that complement or replace CC's built-in sandboxing.
category: landscape
created: 2026-03-08
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Landscape research (informational — not implementation requirements)

## Problem Statement

CC's built-in sandboxing (bubblewrap/Seatbelt) enforces filesystem and network
isolation on the local machine. This is sufficient for single-developer, local-first
workflows. But when AI agent workloads need cloud execution, multi-tenant isolation,
persistent state, or stronger security boundaries (gVisor, Firecracker microVMs),
external sandbox platforms fill the gap.

This document compares platforms for running AI-generated code in isolated
environments — from self-hosted open-source to managed cloud services.

## Platform Comparison

<!-- markdownlint-disable MD013 -->

| Aspect | CC Built-in | `sandbox-runtime` | OpenSandbox (Alibaba) | E2B | Sprites.dev (fly.io) | Daytona |
| ------ | ----------- | ------------------ | --------------------- | --- | -------------------- | ------- |
| **Type** | Local (OS-level) | Local (npm package) | Self-hosted (Docker/K8s) | Cloud SaaS | Cloud SaaS | Cloud / self-hosted |
| **Isolation** | bubblewrap (Linux), Seatbelt (macOS) | Same as CC built-in | gVisor, Kata, Firecracker | Firecracker microVM | Firecracker microVM | Container (optional enhanced) |
| **Cold start** | N/A (local process) | N/A | <800ms | ~150ms | 1-2s (cold), <1s (warm) | Fast (container) |
| **State** | N/A | N/A | Ephemeral | Ephemeral (24h max) | Persistent + checkpoint/restore (~300ms) | Stateful |
| **Storage** | Local filesystem | Local filesystem | Container volumes | Ephemeral per session | 100GB persistent NVMe | Persistent |
| **SDKs** | N/A (settings config) | npm CLI | Python, JS/TS, Java/Kotlin, C#/.NET, Go (planned) | Python, JS/TS | REST API | Python, JS/TS |
| **CC integration** | Native | npm package | Documented | Via SDK | Via API | Via SDK |
| **License** | Proprietary (CC) | Open source | Apache 2.0 | Open source (core) | Proprietary | Open source (core) |
| **Pricing** | Free (with CC) | Free | Free (self-hosted) | Per-minute (BYOC available) | $0.07/CPU-hr, $0.04/GB-hr (idle = free) | Usage-based |
| **GPU support** | N/A | N/A | Via K8s | No | No (CPU-only; use Fly Machines for GPU) | Yes |

<!-- markdownlint-enable MD013 -->

## Platform Details

### CC Built-in Sandboxing

Already analyzed in [CC-sandboxing-analysis.md](CC-sandboxing-analysis.md). OS-level
enforcement via bubblewrap (Linux/WSL2) or Seatbelt (macOS). Zero-cost, zero-setup
on macOS; requires `apt install bubblewrap socat` on Linux. Sufficient for
local-first workflows.

The standalone `@anthropic-ai/sandbox-runtime` npm package extends this
outside CC (e.g., for MCP servers). Same isolation primitives, different
entry point.

### OpenSandbox (Alibaba)

Open-sourced March 2026 under Apache 2.0. 6.9k GitHub stars
([source][opensandbox-gh]).

**Architecture** — four-layer modular stack ([source][opensandbox-gh]):

1. **SDKs Layer** — Python, JS/TS, Java/Kotlin, C#/.NET clients
2. **Specs Layer** — Sandbox Protocol defining lifecycle + execution APIs
3. **Runtime Layer** — Docker (local/small) or Kubernetes (distributed)
4. **Sandbox Instances** — FastAPI lifecycle server + Go execution daemon (`execd`)
   with Jupyter kernels for stateful code execution

**Security model** — pluggable container runtimes
([source][opensandbox-marktechpost]):

- **gVisor** — intercepts syscalls at kernel boundary (stronger than containers,
  lighter than VMs)
- **Kata Containers** — lightweight VMs for hardware-level isolation
- **Firecracker** — microVM hypervisor (same as E2B/Sprites)

**Documented integrations**: Claude Code, Gemini CLI, OpenAI Codex, LangGraph,
Google ADK, Playwright, VNC desktop environments ([source][opensandbox-gh]).

**Roadmap**: Connection pooling, persistent volumes, local lightweight variant,
K8s Helm charts ([source][opensandbox-gh]).

**When to use**: Self-hosted sandbox infrastructure with no vendor lock-in. Strong
fit when you need Kubernetes-scale agent execution, multiple SDK languages, or
gVisor-level isolation without paying per-minute cloud fees.

### E2B

Cloud-managed Firecracker microVMs for ephemeral AI code execution
([source][e2b]).

**Key characteristics**:

- ~150ms cold starts — fastest in class
- Session-scoped (ephemeral) — designed for stateless execution per agent run
- 24-hour maximum session duration
- Custom templates define starting environment (packages, config, files)
- BYOC (Bring Your Own Cloud) on AWS for enterprise/VPC requirements
- Python and JS/TS SDKs

**Lifecycle**: `Sandbox.create()` → `sandbox.commands.run()` → sandbox auto-destroys
([source][e2b-docs]).

**Limitation**: Rate limits can constrain high-parallelism workloads. No persistent
state between sessions — every run starts fresh (or from a template).

**When to use**: Quick, disposable code execution where you need fast cold starts
and don't need state persistence. Good for evaluation pipelines where each run is
independent.

### Sprites.dev (fly.io)

Stateful sandbox environments with checkpoint/restore, launched January 2026
([source][sprites], [source][sprites-simon]).

**Key differentiator** — statefulness. Unlike E2B's ephemeral model, Sprites
maintain full filesystem state between executions:

- 100GB persistent NVMe-backed storage (object storage with NVMe read-through cache)
- Checkpoint/restore in ~300ms (incremental, only changed blocks)
- Idle hibernation with automatic wake-up (no charges when idle)
- Pre-installed packages, services, and policies survive checkpoints

**Pricing**: $0.07/CPU-hour, $0.04375/GB-hour memory. A 4-hour Claude Code session
costs ~$0.44. No charges for idle time or allocated-but-unused storage
([source][sprites]).

**AI agent integration**: `/.sprite/llm.txt` teaches Claude how Sprites works
(port opening, checkpoints). Pre-installed skills for self-management
([source][sprites]).

**Limitations**: CPU-only (GPUs require Fly Machines with Docker); single VM
size option; 100GB max storage; fly.io infrastructure only
([source][sprites-medium]).

**When to use**: Long-running agent sessions that need warm environments between
runs (node_modules, databases, tool configs). The checkpoint/restore model avoids
E2B's "rebuild everything each session" overhead.

### Daytona

Pivoted to AI code execution in 2026. Container-based with optional enhanced
isolation. Open-source core with cloud and self-hosted deployment options
([source][daytona]).

Less relevant for CC-specific workflows but included for completeness in the
landscape.

## Ephemeral vs Stateful: The Core Tradeoff

<!-- markdownlint-disable MD013 -->

| Model | Platforms | Pros | Cons |
| ----- | --------- | ---- | ---- |
| **Ephemeral** | E2B, OpenSandbox | Clean slate every run; no state leakage; simple mental model | Rebuild cost (packages, config) per session; no cross-session memory |
| **Stateful** | Sprites, Daytona | Warm environments; fast resume; lower per-session cost | State management complexity; potential for drift; storage costs |
| **Local** | CC built-in, sandbox-runtime | Zero network latency; full local config; no cloud cost | Single machine; no cloud scale; no multi-tenant isolation |

<!-- markdownlint-enable MD013 -->

## Decision Rule

```text
Need cloud execution?
├── No → CC built-in sandboxing (free, sufficient for local-first)
└── Yes
    ├── Need self-hosted / no vendor lock-in?
    │   └── OpenSandbox (Apache 2.0, Docker/K8s, gVisor)
    ├── Need fast ephemeral runs (eval pipelines, one-shot code)?
    │   └── E2B (150ms cold start, session-scoped)
    ├── Need persistent state between sessions (dev environments)?
    │   └── Sprites.dev (checkpoint/restore, idle billing)
    └── Need GPU?
        └── Fly Machines (Docker) or Modal (autoscaling)
```

## Relationship to CC Sandboxing

CC's built-in sandboxing and these platforms solve **different problems**:

- **CC sandboxing** = enforcement layer (what can an agent do on your machine?)
- **External platforms** = execution layer (where does the agent run?)

They compose: you can run CC locally with bubblewrap sandboxing, or run CC
inside an OpenSandbox/E2B/Sprites environment that provides its own
isolation. The external
platform's isolation is additive — it doesn't replace CC's permission model.

## References

- [OpenSandbox GitHub][opensandbox-gh]
- [OpenSandbox announcement (MarkTechPost)][opensandbox-marktechpost]
- [E2B][e2b]
- [E2B docs][e2b-docs]
- [E2B GitHub][e2b-gh]
- [Sprites.dev][sprites]
- [Simon Willison on Sprites][sprites-simon]
- [Sprites deep dive (Medium)][sprites-medium]
- [Daytona][daytona]
- [CC Sandboxing docs][cc-sandbox]
- [Sandbox runtime (open source)][sandbox-runtime]
- [AI sandbox landscape (Northflank)][northflank]
- [AI sandbox landscape (Koyeb)][koyeb]

[opensandbox-gh]: https://github.com/alibaba/OpenSandbox
[opensandbox-marktechpost]: https://www.marktechpost.com/2026/03/03/alibaba-releases-opensandbox-to-provide-software-developers-with-a-unified-secure-and-scalable-api-for-autonomous-ai-agent-execution/
[e2b]: https://e2b.dev
[e2b-docs]: https://e2b.dev/docs
[e2b-gh]: https://github.com/e2b-dev/E2B
[sprites]: https://sprites.dev
[sprites-simon]: https://simonwillison.net/2026/Jan/9/sprites-dev/
[sprites-medium]: https://lewoudar.medium.com/lets-talk-about-fly-io-sprites-aka-stateful-sandboxes-509796942fdd
[daytona]: https://www.daytona.io
[cc-sandbox]: https://code.claude.com/docs/en/sandboxing
[sandbox-runtime]: https://github.com/anthropic-experimental/sandbox-runtime
[northflank]: https://northflank.com/blog/best-sandboxes-for-coding-agents
[koyeb]: https://www.koyeb.com/blog/top-sandbox-code-execution-platforms-for-ai-code-execution-2026
