# claude-code-research

> Field research and feature analysis for Claude Code — from sandboxing internals to agent orchestration.

## Overview

A collection of independent, deep-dive analyses of Claude Code (CC) features,
capabilities, and integration patterns. Each document evaluates a specific CC
feature through the lens of practical adoption: what it does, how it works,
when to use it, and when to skip it.

## Contents

### Anthropic Native (`docs/cc-native/`)

| Directory | Analyses |
|---|---|
| [`agents-skills/`](docs/cc-native/agents-skills/) | Agent Teams, Skills adoption, Ralph loop enhancements, CLI-Anything analysis, plans as skill/rule templates |
| [`ci-execution/`](docs/cc-native/ci-execution/) | Sandboxing, cloud sessions, remote control, remote access landscape, version pinning & self-hosted runners, GitHub Actions & Claude App |
| [`context-memory/`](docs/cc-native/context-memory/) | Extended context (1M tokens), memory system (with path-scoped rules deep dive), llms.txt |
| [`configuration/`](docs/cc-native/configuration/) | Model/provider configuration, fast mode, hooks system, bash mode (with SDK & community refs) |
| [`plugins-ecosystem/`](docs/cc-native/plugins-ecosystem/) | Plugin packaging, cowork/enterprise plugins, Chrome extension, web scraping plugins, official plugins landscape |
| [`CC-changelog-feature-scan.md`](docs/cc-native/CC-changelog-feature-scan.md) | Changelog triage of new CC features (v2.1.0–2.1.71) |

### Community & Third-Party (`docs/community/`)

| Document | Coverage |
|---|---|
| [`CC-community-skills-landscape.md`](docs/community/CC-community-skills-landscape.md) | Community skill libraries: gstack, pm-skills, claude-code-best-practice |
| [`CC-community-plugins-landscape.md`](docs/community/CC-community-plugins-landscape.md) | Plugin catalogs: awesome-claude-code, awesome-claude-code-plugins |
| [`CC-community-tooling-landscape.md`](docs/community/CC-community-tooling-landscape.md) | Developer tooling: RTK (Rust Token Killer) context compression |
| [`CC-domain-claudemd-showcase.md`](docs/community/CC-domain-claudemd-showcase.md) | Domain-specific CLAUDE.md patterns: genome analysis pipeline |

### Other

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
