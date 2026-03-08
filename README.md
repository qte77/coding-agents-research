# claude-code-research

> Field research and feature analysis for Claude Code — from sandboxing internals to agent orchestration.

## Overview

A collection of independent, deep-dive analyses of Claude Code (CC) features,
capabilities, and integration patterns. Each document evaluates a specific CC
feature through the lens of practical adoption: what it does, how it works,
when to use it, and when to skip it.

Topics span the full CC surface area:

| Category | Analyses |
|---|---|
| **Agent & Orchestration** | Agent Teams, Skills adoption, Ralph loop enhancements |
| **Execution & Infrastructure** | Sandboxing, cloud sessions, remote control, remote access landscape |
| **Context & Memory** | Extended context (1M tokens), memory system, llms.txt |
| **Configuration & Providers** | Model/provider configuration, fast mode, hooks system |
| **Packaging & Enterprise** | Plugin packaging, cowork/enterprise plugins, Chrome extension |
| **Planning & Tracking** | Adoption plan, changelog feature scan |

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
