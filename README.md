# claude-code-research

> Field research and feature analysis for Claude Code — from sandboxing internals to agent orchestration.

## Overview

A collection of independent, deep-dive analyses of Claude Code (CC) features,
capabilities, and integration patterns. Each document evaluates a specific CC
feature through the lens of practical adoption: what it does, how it works,
when to use it, and when to skip it.

## Contents

| Directory | Analyses |
|---|---|
| [`docs/agent-orchestration/`](docs/agent-orchestration/) | Agent Teams, Skills adoption, Ralph loop enhancements |
| [`docs/execution-infrastructure/`](docs/execution-infrastructure/) | Sandboxing, cloud sessions, remote control, remote access landscape |
| [`docs/context-memory/`](docs/context-memory/) | Extended context (1M tokens), memory system, llms.txt |
| [`docs/configuration/`](docs/configuration/) | Model/provider configuration, fast mode, hooks system |
| [`docs/packaging-enterprise/`](docs/packaging-enterprise/) | Plugin packaging, cowork/enterprise plugins, Chrome extension |
| [`docs/CC-changelog-feature-scan.md`](docs/CC-changelog-feature-scan.md) | Changelog triage of new CC features (v2.1.0–2.1.71) |

| [`examples/`](examples/) | Settings, statusline, rules, and user preferences |

## Structure

Each file is a standalone analysis following a consistent format:

- **What it is** — feature description and mechanics
- **How it works** — technical details, configuration, limitations
- **Adoption decision** — adopt / defer / skip, with rationale
- **Action items** — concrete next steps if adopting

## Origin

These analyses were originally produced as part of
[Agents-eval](https://github.com/qte77/Agents-eval) to inform adoption
decisions for a multi-agent evaluation framework built on Claude Code.

## License

[MIT](LICENSE)
