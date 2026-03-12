---
title: CC GitHub Actions — claude-code-action & Claude GitHub App
source: https://code.claude.com/docs/en/github-actions, https://github.com/apps/claude, https://github.com/anthropics/claude-code-action/discussions/578, https://dev.to/myougatheaxo/automate-your-entire-pr-workflow-with-claude-code-description-review-tests-1i41
purpose: Evaluate Claude Code GitHub Actions for PR automation, code review, issue triage, and scheduled workflows — setup, capabilities, limitations, and cost.
created: 2026-03-12
updated: 2026-03-12
validated_links: false
---

**Status**: Research (informational — not implementation requirements)

## What It Is

Claude Code GitHub Actions (`anthropics/claude-code-action@v1`) brings AI-powered automation to GitHub workflows. Mention `@claude` in any PR or issue, and Claude analyzes code, creates PRs, implements features, and fixes bugs — following the repo's `CLAUDE.md` standards ([source][cc-gha-docs]).

Built on the [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview). Defaults to Sonnet; Opus 4.6 available via `--model claude-opus-4-6` ([source][cc-gha-docs]).

The **Claude GitHub App** ([github.com/apps/claude][claude-app]) is the companion app that provides the GitHub integration layer — handling permissions, webhooks, and token management. It requires read & write access to Contents, Issues, and Pull Requests ([source][cc-gha-docs]).

## Setup

### Quick Setup

```bash
# Inside Claude Code terminal
/install-github-app
```

Requires repository admin. Only available for direct Anthropic API users (not Bedrock/Vertex) ([source][cc-gha-docs]).

### Manual Setup

1. Install the [Claude GitHub App][claude-app] to your repository
2. Add `ANTHROPIC_API_KEY` to repository secrets
3. Copy the [example workflow](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) into `.github/workflows/`

Test by tagging `@claude` in an issue or PR comment ([source][cc-gha-docs]).

## Capabilities

### Interactive Mode — `@claude` Mentions

Responds to `@claude` in issue comments, PR comments, and PR review comments:

```text
@claude implement this feature based on the issue description
@claude fix the TypeError in the user dashboard component
@claude how should I implement user authentication for this endpoint?
```

### Automation Mode — Prompt-Driven

Runs immediately with a configured prompt, no mention required:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Review this pull request for code quality, correctness, and security."
    claude_args: "--max-turns 5"
```

### Scheduled Workflows

Cron-triggered automation for reports, audits, or maintenance:

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model opus"
```

([source][cc-gha-docs])

## Workflow Patterns from Community

### PR Description Generation

Pipe `git diff` to Claude for structured descriptions ([source][dev-to-pr]):

```bash
git diff main...HEAD | claude -p "Write a PR description for these changes..."
```

### Pre-PR Self-Review

Request senior-level analysis before opening a PR — focuses on correctness, security, performance, missing tests, and style violations ([source][dev-to-pr]).

### GHA Auto-Review on PR Open

Trigger review on `pull_request: [opened, synchronize]`, generate diff, run review via Claude, post results as PR comment ([source][dev-to-pr]).

### Merge Conflict Resolution

Provide Claude with both conflict sides plus context about intent, and it resolves the conflict ([source][dev-to-pr]).

### Release Notes Generation

Aggregate merged PR titles/descriptions, filter for user-facing changes, group by Features / Bug Fixes / Breaking Changes ([source][dev-to-pr]).

## Configuration Reference

### Action Parameters (v1)

| Parameter | Description | Required |
|---|---|---|
| `prompt` | Instructions for Claude (text or skill name) | No* |
| `claude_args` | CLI arguments passed through | No |
| `anthropic_api_key` | Claude API key | Yes** |
| `github_token` | GitHub token for API access | No |
| `trigger_phrase` | Custom trigger (default: `@claude`) | No |
| `use_bedrock` | Use AWS Bedrock | No |
| `use_vertex` | Use Google Vertex AI | No |

\*Optional — when omitted for comments, responds to trigger phrase
\*\*Required for direct API, not for Bedrock/Vertex

([source][cc-gha-docs])

### Common `claude_args`

```yaml
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

- `--max-turns`: Maximum conversation turns (default: 10)
- `--model`: Model selection (e.g., `claude-sonnet-4-6`, `claude-opus-4-6`)
- `--mcp-config`: Path to MCP server configuration
- `--allowed-tools`: Comma-separated tool allowlist
- `--append-system-prompt`: Additional system instructions

### Migration from Beta to v1

| Beta Input | v1 Input |
|---|---|
| `mode` | *(Removed — auto-detected)* |
| `direct_prompt` | `prompt` |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns` | `claude_args: --max-turns` |
| `model` | `claude_args: --model` |
| `allowed_tools` | `claude_args: --allowedTools` |
| `claude_env` | `settings` JSON format |

([source][cc-gha-docs])

## Enterprise: AWS Bedrock & Google Vertex AI

Both providers use OIDC authentication (no static credentials). Requires a custom GitHub App for token generation ([source][cc-gha-docs]).

### AWS Bedrock

- Enable Bedrock + request Claude model access
- Configure GitHub OIDC Identity Provider in AWS
- Create IAM role with `AmazonBedrockFullAccess`
- Model ID format includes region prefix: `us.anthropic.claude-sonnet-4-6`

### Google Vertex AI

- Enable Vertex AI API + IAM Credentials API + STS API
- Create Workload Identity Federation pool with GitHub OIDC provider
- Create service account with `Vertex AI User` role
- Project ID auto-retrieved from auth step

## Known Limitations

### PR Creation Not Fully Automatic

Claude Code Action does not call GitHub's PR creation API directly. It generates a "Create PR" button/link in the comment that users must click manually. The codebase has no `octokit.rest.pulls.create` calls ([source][gh-discussion-578]). This is a significant gap for fully autonomous issue-to-PR workflows.

### CLAUDE.md Is the Primary Control Surface

All project-specific behavior (review criteria, coding standards, patterns) is driven by `CLAUDE.md` at repo root. There's no per-workflow instruction file — `CLAUDE.md` + `prompt` parameter is the full configuration surface ([source][cc-gha-docs]).

### Cost Considerations

**GitHub Actions costs**: Runs on GitHub-hosted runners, consuming Actions minutes ([source][cc-gha-docs]).

**API costs**: Token usage varies by task complexity and codebase size. Cost optimization tips ([source][cc-gha-docs]):

- Use specific `@claude` commands to reduce unnecessary API calls
- Configure `--max-turns` to prevent excessive iterations
- Set workflow-level timeouts to avoid runaway jobs
- Use GitHub concurrency controls to limit parallel runs

### Runner Sizing & Pricing

Standard runners (`ubuntu-latest`) are 2-core/7 GB RAM. For large repos or complex Claude tasks, **larger runners** provide up to 96 cores and proportionally more RAM/disk. Requires GitHub Team or Enterprise Cloud plan ([source][gh-larger-runners]).

<!-- markdownlint-disable MD013 -->

| Runner | Cores | Per-min (Linux x64) | Notes |
|---|---|---|---|
| Standard | 2 | $0.006 | Included minutes on private repos |
| Larger 4-core | 4 | $0.012 | No included minutes; per-minute only |
| Larger 16-core | 16 | $0.048 | Good balance for CC agent workloads |
| Larger 64-core | 64 | $0.168 | Heavy parallel / large codebase |
| GPU (4-core + T4) | 4 | $0.052 | ML workloads only |
| arm64 2-core | 2 | $0.005 | Cheapest option |

<!-- markdownlint-enable MD013 -->

([source][gh-runner-pricing])

**Key billing facts**: Minutes rounded up to nearest whole minute. Larger runners are *not* free for public repos and *cannot* use included plan minutes. No extra cost for static IPs on larger runners ([source][gh-runner-pricing]).

**Selecting a larger runner** — use the runner label directly in `runs-on` ([source][gh-larger-runner-jobs]):

```yaml
jobs:
  claude:
    runs-on: ubuntu-24.04-16core  # larger runner label
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

Or target a runner group:

```yaml
runs-on:
  group: my-runner-group
  labels: ubuntu-24.04-16core
```

**CC-specific guidance**: Claude Code is primarily I/O-bound (API calls to Anthropic), not CPU-bound. Standard 2-core runners are sufficient for most `@claude` workflows. Consider larger runners only when: (1) the repo checkout + dependency install is slow, (2) Claude invokes heavy build/test commands via Bash, or (3) you need static IPs for network-restricted environments.

## Fit Assessment

**Adopt for `@claude` interactive use.** The mention-based workflow is low-friction — install app, add secret, copy workflow, start mentioning. Ideal for PR feedback, issue triage, and ad-hoc code questions.

**Evaluate for automated PR review.** The prompt-driven mode on `pull_request: [opened, synchronize]` enables auto-review, but results post as comments, not GitHub review annotations. Compare with the [Code Review plugin](../plugins-ecosystem/CC-official-plugins-landscape.md#code-review) for structured multi-agent scoring.

**Defer for fully autonomous issue-to-PR.** PR creation is manual (button click). Until the action calls the PR creation API directly, fully unattended issue→branch→PR pipelines require wrapper scripts.

**Monitor scheduled workflows.** Cron-triggered prompts (daily reports, audits) are powerful but cost-unconstrained — set `--max-turns` and workflow `timeout-minutes` aggressively.

## Cross-References

- Version pinning and self-hosted runners for GHA — [CC-version-pinning-resilience.md](CC-version-pinning-resilience.md#github-actions)
- Official plugins (Code Review, Security Guidance) — [CC-official-plugins-landscape.md](../plugins-ecosystem/CC-official-plugins-landscape.md)
- Bash tool behavior inside GHA — [CC-bash-mode-analysis.md](../configuration/CC-bash-mode-analysis.md)
- Cloud sessions as alternative execution — [CC-cloud-sessions-analysis.md](CC-cloud-sessions-analysis.md)

## References

[cc-gha-docs]: https://code.claude.com/docs/en/github-actions
[claude-app]: https://github.com/apps/claude
[gh-discussion-578]: https://github.com/anthropics/claude-code-action/discussions/578
[dev-to-pr]: https://dev.to/myougatheaxo/automate-your-entire-pr-workflow-with-claude-code-description-review-tests-1i41
[gh-larger-runners]: https://docs.github.com/en/actions/concepts/runners/larger-runners
[gh-runner-pricing]: https://docs.github.com/en/billing/reference/actions-runner-pricing
[gh-larger-runner-jobs]: https://docs.github.com/en/actions/using-github-hosted-runners/using-larger-runners/running-jobs-on-larger-runners
