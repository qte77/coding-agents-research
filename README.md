# coding-agents-research

> Field research and feature analysis for AI coding agents — from sandboxing internals to agent orchestration.

## Why

Understand how Claude Code works under the hood so you can make informed adopt/defer/skip decisions before building production systems with it.

## What

Standalone deep-dive analyses of CC features, each following a consistent format:
**What it is** → **How it works** → **Adoption decision** → **Action items**

## Contents

| Directory | What's there |
|---|---|
| [`docs/cc-native/`](docs/cc-native/) | Anthropic-native features: agents/skills, CI/sandboxing, context/memory, configuration, plugins/ecosystem |
| [`docs/non-cc/`](docs/non-cc/) | Non-CC agents and orchestrators: JetBrains Air, agent-era/devteam |
| [`docs/community/`](docs/community/) | Community skills, plugins, tooling, and domain-specific CLAUDE.md patterns |
| [`triage/`](triage/) | Auto-generated monitor outputs: outage archive, changelog triage, community triage |
| [`.github/`](.github/README.md) | CI automation: monitors, scripts, templates — see [.github/README.md](.github/README.md) |

## How it stays current

Three automated monitors poll external sources on cron and open triage PRs when new content is found. See [`.github/README.md`](.github/README.md) for details.

## Origin

These analyses were originally produced as part of [Agents-eval](https://github.com/qte77/Agents-eval) to inform adoption decisions for a multi-agent evaluation framework built on Claude Code.

## License

[MIT](LICENSE)
