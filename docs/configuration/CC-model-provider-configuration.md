---
title: CC Model & Provider Configuration
source: https://code.claude.com/docs/en/settings#environment-variables, https://openrouter.ai/docs/guides/guides/coding-agents/claude-code-integration, https://ollama.com/blog/claude, https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models
purpose: Reference for configuring CC with alternative models, endpoints, API keys, third-party providers (OpenRouter, Bedrock, Vertex, Foundry), local models (Ollama, llama.cpp, LM Studio), and LLM gateway proxies.
created: 2026-03-07
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Reference (actionable configuration guide)

## Model Selection

<!-- markdownlint-disable MD013 -->

| Variable | Purpose | Example |
| -------- | ------- | ------- |
| `ANTHROPIC_MODEL` | Primary model override | `claude-sonnet-4-6` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Override Haiku-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Override Sonnet-class model | Custom model ID |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Override Opus-class model | Custom model ID |
| `CLAUDE_CODE_SUBAGENT_MODEL` | Model for subagents/teammates | Custom model ID |
| `CLAUDE_CODE_EFFORT_LEVEL` | Reasoning effort (Opus 4.6, Sonnet 4.6) | `low`, `medium`, `high` |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` | Disable adaptive reasoning | `1` |

All variables can also be set in `settings.json` under the `env` key. ([source][cc-settings])

<!-- markdownlint-enable MD013 -->

## API Key & Endpoint

<!-- markdownlint-disable MD013 -->

| Variable | Purpose | Example |
| -------- | ------- | ------- |
| `ANTHROPIC_API_KEY` | API key (sent as `X-Api-Key` header) | `sk-ant-...` |
| `ANTHROPIC_AUTH_TOKEN` | Custom `Authorization` header value (auto-prefixed with `Bearer`) | OpenRouter key |
| `ANTHROPIC_BASE_URL` | Override API endpoint | `https://openrouter.ai/api` |
| `ANTHROPIC_CUSTOM_HEADERS` | Extra headers (newline-separated `Name: Value`) | Custom routing headers |

<!-- markdownlint-enable MD013 -->

## Provider Configuration

### Anthropic API (default)

No extra config needed. Set `ANTHROPIC_API_KEY` or use `/login`. ([source][cc-settings])

### OpenRouter

Routes requests through OpenRouter for provider failover, budget controls, and usage analytics. OpenRouter implements an "Anthropic Skin" compatible with the Messages API — no local proxy needed. ([source][openrouter])

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api"
export ANTHROPIC_AUTH_TOKEN="<openrouter-api-key>"
export ANTHROPIC_API_KEY=""  # must be explicitly empty
```

Or in `.claude/settings.local.json` (project-level, git-ignored):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
    "ANTHROPIC_AUTH_TOKEN": "<openrouter-api-key>",
    "ANTHROPIC_API_KEY": ""
  }
}
```

**Key caveats** ([source][openrouter]):

- CC compatibility guaranteed only with Anthropic first-party provider on OpenRouter
- Run `/logout` first to clear existing Anthropic credentials
- Standard `.env` files are NOT read by CC — use shell profile or `settings.local.json`
- Prompts not logged unless explicitly enabled in OpenRouter account settings

**Benefits**: Provider failover during Anthropic outages, centralized team budget controls, real-time cost monitoring via Activity Dashboard. ([source][openrouter])

### AWS Bedrock

```bash
export CLAUDE_CODE_USE_BEDROCK=true
# Optional: export AWS_BEARER_TOKEN_BEDROCK="<api-key>"
# For LLM gateways: export CLAUDE_CODE_SKIP_BEDROCK_AUTH=true
```

([source][cc-settings])

### Google Vertex AI

```bash
export CLAUDE_CODE_USE_VERTEX=true
# For LLM gateways: export CLAUDE_CODE_SKIP_VERTEX_AUTH=true
```

([source][cc-settings])

### Microsoft Azure Foundry

```bash
export CLAUDE_CODE_USE_FOUNDRY=true
export ANTHROPIC_FOUNDRY_BASE_URL="https://my-resource.services.ai.azure.com/anthropic"
# Or: export ANTHROPIC_FOUNDRY_RESOURCE="my-resource"
# Optional: export ANTHROPIC_FOUNDRY_API_KEY="<api-key>"
# For LLM gateways: export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=true
```

([source][cc-settings])

### Local Models

Claude Code works with any backend that speaks the Anthropic Messages API format. Several local inference engines now support this natively.

#### Ollama (Recommended for Local)

Ollama v0.14+ implements the Anthropic Messages API natively — no proxy needed ([source][ollama-claude]).

```bash
# Pull a model
ollama pull qwen3-coder

# Run Claude Code against Ollama
ANTHROPIC_AUTH_TOKEN=ollama \
ANTHROPIC_BASE_URL=http://localhost:11434 \
ANTHROPIC_API_KEY="" \
claude --model qwen3-coder
```

**Supported features**: Messages, streaming, system prompts, tool calling, extended thinking, vision ([source][ollama-claude]).

**Requirements** ([source][ollama-claude]):

- Ollama v0.14.0+
- Model with at least 32K context window (64K+ recommended for agentic use)
- 32GB+ RAM recommended for usable coding experience (Apple Silicon unified memory or PC RAM)

**Recommended models** (as of March 2026): `qwen3-coder`, `gpt-oss:20b`, `glm-4.7:cloud`, `minimax-m2.1:cloud` ([source][ollama-claude])

#### llama.cpp

llama.cpp server supports the Anthropic Messages API directly. It converts Anthropic format to OpenAI internally, reusing the existing inference pipeline ([source][llamacpp-anthropic]).

```bash
# Start llama.cpp server with a model
llama-server -hf unsloth/Qwen3-Next-80B-A3B-Instruct-GGUF:Q4_K_M

# Run Claude Code
ANTHROPIC_BASE_URL=http://127.0.0.1:8080 \
ANTHROPIC_API_KEY="" \
claude
```

#### LM Studio & Other OpenAI-Compatible Servers

Servers that only speak OpenAI's Chat Completions format (not Anthropic's Messages API) need a translation proxy. Options:

- **claude-code-proxy** ([source][cc-proxy]) — lightweight Node.js proxy converting Anthropic → OpenAI format
- **Olla** ([source][olla]) — multi-backend proxy with load balancing across Ollama, LM Studio, and vLLM
- **LiteLLM** ([source][litellm]) — full-featured proxy with auth, rate limiting, audit logging

```bash
# Example with claude-code-proxy
ANTHROPIC_BASE_URL=http://localhost:8082 \
ANTHROPIC_API_KEY="any-value" \
claude
```

#### Tips for Local Models

<!-- markdownlint-disable MD013 -->

| Tip | Detail |
|---|---|
| **KV cache invalidation** | CC prepends an attribution header that invalidates KV cache. Set `CLAUDE_CODE_ATTRIBUTION_HEADER=0` to prevent this ([source][local-setup]) |
| **Login bypass** | If CC prompts for login, add `"hasCompletedOnboarding": true` and `"primaryApiKey": "sk-dummy-key"` to `~/.claude.json` ([source][local-setup]) |
| **Non-essential traffic** | Set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` to reduce calls to Anthropic servers ([source][cc-settings]) |
| **Cost savings** | Local models are free; third-party cloud options like DeepSeek V3.2 are ~$0.28/$0.42 per million tokens vs Opus ~$15/$75 ([source][local-setup]) |

<!-- markdownlint-enable MD013 -->

### LLM Gateway / Proxy Configuration

For enterprise or multi-provider setups, an LLM gateway sits between CC and the provider, translating API formats and adding features like auth, rate limiting, and audit logging.

#### LiteLLM

Full-featured proxy supporting 100+ providers. Recommended for team environments ([source][litellm]).

```bash
# Start LiteLLM proxy
litellm --model gpt-4o

# Point Claude Code at it
export ANTHROPIC_BASE_URL="http://0.0.0.0:4000"
export ANTHROPIC_AUTH_TOKEN="$LITELLM_MASTER_KEY"
claude --model gpt-4o
```

Supports: `claude --model gpt-4o`, `claude --model gemini-3.0-flash-exp`, `claude --model azure-gpt-4`, etc.

#### Bifrost (Maxim AI)

Open-source Go-based gateway supporting 1000+ models. Intercepts Anthropic-format requests, converts to target provider format, and translates responses back transparently ([source][bifrost]).

#### Direct CC-Compatible Endpoints

Some providers expose Anthropic-compatible endpoints natively (no proxy needed):

```bash
# Example: Z.AI
export ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
export ANTHROPIC_AUTH_TOKEN=YOUR_API_KEY
claude
```

#### Gateway Requirements

For a gateway to work with CC, it must ([source][cc-settings]):

- Expose at least one of: Anthropic Messages (`/v1/messages`), Bedrock InvokeModel (`/invoke`), or Vertex rawPredict (`:rawPredict`)
- Forward required headers: `anthropic-beta`, `anthropic-version`

When routing through gateways, additionally set ([source][cc-settings]):

- `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` — disable Anthropic-specific `anthropic-beta` headers
- `CLAUDE_CODE_SKIP_*_AUTH=true` — skip native provider auth (Bedrock/Vertex/Foundry)

## Output & Context Tuning

<!-- markdownlint-disable MD013 -->

| Variable | Purpose | Default |
| -------- | ------- | ------- |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max output tokens | 32,000 (max 64,000) |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` | Token limit for file reads | Default |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` | Disable 1M context window (see [extended context analysis](../context-memory/CC-extended-context-analysis.md)) | `1` to disable |

([source][cc-settings])

<!-- markdownlint-enable MD013 -->

## Applicability

<!-- markdownlint-disable MD013 -->

| Aspect | Fit | Rationale |
| ------ | --- | --------- |
| Model override (`ANTHROPIC_MODEL`) | Strong | Direct env var control per run; useful in any project to select model per task |
| Subagent model (`CLAUDE_CODE_SUBAGENT_MODEL`) | Strong | Control cost by routing teammates/subagents to cheaper models |
| OpenRouter for failover | Strong | Provider failover during Anthropic outages + centralized budget controls |
| Ollama / local models | Moderate | Free, private, no API dependency; limited by local hardware and model quality |
| LLM gateway (LiteLLM/Bifrost) | Moderate | Team auth, rate limiting, multi-provider routing; adds infrastructure |
| Bedrock/Vertex/Foundry | Conditional | Relevant when a project runs on cloud infrastructure |
| Effort level tuning | Strong | `CLAUDE_CODE_EFFORT_LEVEL=medium` for routine tasks saves tokens |

<!-- markdownlint-enable MD013 -->

### Decision Rule

**Model and effort variables are immediately useful** for optimizing autonomous CC runs (cost vs quality trade-offs). OpenRouter is recommended for provider failover and team budget controls. Local models (Ollama) are useful for privacy-sensitive work, offline development, or eliminating API costs — but quality and context window are limited by hardware. LLM gateways (LiteLLM) add value for team environments needing auth and audit logging. Cloud providers (Bedrock/Vertex/Foundry) are relevant once a project runs on cloud infrastructure.

### Provider Decision Matrix

<!-- markdownlint-disable MD013 -->

| Need | Best Option | Setup Effort |
|---|---|---|
| **Default (best quality)** | Anthropic API direct | None |
| **Failover / budget** | OpenRouter | Low (env vars) |
| **Free / private / offline** | Ollama + local model | Medium (install + model download) |
| **Multi-provider / team** | LiteLLM proxy | Medium (proxy setup) |
| **Enterprise cloud** | Bedrock / Vertex / Foundry | High (cloud config) |
| **Non-Anthropic models in CC** | LiteLLM or claude-code-proxy | Medium (proxy) |

<!-- markdownlint-enable MD013 -->

## References

- [CC Settings — Environment Variables][cc-settings]
- [OpenRouter — Claude Code Integration][openrouter]
- [Ollama — Claude Code with Anthropic API Compatibility][ollama-claude]
- [llama.cpp — Anthropic Messages API][llamacpp-anthropic]
- [LiteLLM — Claude Code with Non-Anthropic Models][litellm]
- [claude-code-proxy (GitHub)][cc-proxy]
- [Olla — Multi-Backend Proxy][olla]
- [Bifrost — Open-Source AI Gateway][bifrost]
- [Local setup guide][local-setup]

[cc-settings]: https://code.claude.com/docs/en/settings#environment-variables
[openrouter]: https://openrouter.ai/docs/guides/guides/coding-agents/claude-code-integration
[ollama-claude]: https://ollama.com/blog/claude
[llamacpp-anthropic]: https://huggingface.co/blog/ggml-org/anthropic-messages-api-in-llamacpp
[litellm]: https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models
[cc-proxy]: https://github.com/fuergaosi233/claude-code-proxy
[olla]: https://thushan.github.io/olla/integrations/frontend/claude-code/
[bifrost]: https://www.getmaxim.ai/articles/running-non-anthropic-models-in-claude-code-via-an-enterprise-ai-gateway/
[local-setup]: https://medium.com/@luongnv89/run-claude-code-on-local-cloud-models-in-5-minutes-ollama-openrouter-llama-cpp-6dfeaee03cda
