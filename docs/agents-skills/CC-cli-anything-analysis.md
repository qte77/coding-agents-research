---
title: CC CLI-Anything Analysis
source: https://github.com/HKUDS/CLI-Anything
purpose: Evaluate CLI-Anything as a framework for generating agent-native CLIs from existing software, and its fit relative to .gitmodules, bun scripts, and Makefile recipes.
created: 2026-03-12
updated: 2026-03-12
validated_links: 2026-03-12
---

**Status**: Research (informational — monitor as ecosystem matures)

## What CLI-Anything Is

CLI-Anything is a framework that transforms any software into an agent-native CLI through automated code analysis and generation ([source][cli-anything]). It bridges the gap between AI agents and professional software that lacks agent-friendly interfaces.

Available as a CC plugin: `/plugin install cli-anything` ([source][cli-anything]).

## The 7-Phase Pipeline

CLI-Anything automates a complete development workflow ([source][cli-anything]):

| Phase | Action | Output |
|---|---|---|
| 1. **Analyze** | Scan source code, map GUI actions to underlying APIs | API surface map |
| 2. **Design** | Architect command groups, state models, output formats | CLI specification |
| 3. **Implement** | Build Click-based CLI with REPL, JSON output, undo/redo | Working CLI |
| 4. **Plan Tests** | Create comprehensive test strategies (unit + E2E) | Test plan |
| 5. **Write Tests** | Implement full test suite | Passing tests |
| 6. **Document** | Update documentation with results | Docs |
| 7. **Publish** | Generate `setup.py`, install to system PATH | Installable CLI |

### Key Design Decisions

- **Click framework** for structured command definitions with `--help` auto-discovery
- **Structured JSON output** for agent consumption + human-readable fallback
- **Persistent state management** with undo/redo across sessions
- **Namespace isolation**: commands under `cli_anything.*` to prevent conflicts (e.g., `cli-anything-gimp`, `cli-anything-blender`)

## Test Results

1,508 passing tests across 11 production applications ([source][cli-anything]):

- **1,073 unit tests** (synthetic data validation)
- **435 end-to-end tests** (real file/software integration)
- **100% pass rate**

Tested applications: GIMP (107), Blender (208), Inkscape (202), Audacity (161), LibreOffice (158), OBS Studio (153), Kdenlive (155), Shotcut (154), Zoom (22), Draw.io (138), AnyGen (50).

### Backend Integration Methods

Applications use authentic backends, not UI automation ([source][cli-anything]):

| Application | Backend |
|---|---|
| GIMP | Pillow + GEGL/Script-Fu |
| Blender | bpy (native Python scripting) |
| Inkscape | Direct SVG/XML manipulation |
| LibreOffice | Headless ODF generation |
| OBS Studio | WebSocket + JSON scenes |
| Video editors | MLT XML + melt renderer |

## CC Plugin Integration

```bash
# Install from marketplace
/plugin marketplace add HKUDS/CLI-Anything
/plugin install cli-anything

# Generate CLI for a codebase
/cli-anything:cli-anything <software-path>

# Iterative refinement
/cli-anything:refine <software-path> [optional-focus]
```

Also available for OpenCode (experimental, `.opencode/commands/`) and Codex (`codex-skill/` directory) ([source][cli-anything]).

## Comparison with Existing Tooling

<!-- markdownlint-disable MD013 -->

| Aspect | CLI-Anything | `.gitmodules` | `bun` scripts | Makefile recipes |
|---|---|---|---|---|
| **Purpose** | Generate agent-native CLIs from any codebase | Distribute source code as submodules | Run JS/TS scripts | Hand-written shell recipes |
| **Language** | Python (Click) | Any | JavaScript/TypeScript | Shell |
| **Auto-discovery** | Yes (`--help`, `--json`) | No | No | Partial (`make help`) |
| **Agent-native output** | Structured JSON | No | No | No |
| **Undo/redo** | Built-in | No (git revert) | No | No |
| **Effort** | Automated generation | Manual setup | Manual writing | Manual writing |
| **Distribution** | pip install / CC plugin | git submodule add | npm/bun install | Copy Makefile |

<!-- markdownlint-enable MD013 -->

### Relationship to Each Tool

- **vs `.gitmodules`**: Different layers. Submodules distribute *source code*; CLI-Anything generates *agent-native CLIs* from that code. Complementary, not competing.
- **vs `bun` scripts**: Bun is a JS runtime for running scripts; CLI-Anything generates Python Click CLIs from any codebase. Complementary: bun for JS tooling, CLI-Anything for wrapping non-JS software.
- **vs Makefile recipes**: CLI-Anything auto-generates the CLI with `--help` and JSON output; Makefile recipes are hand-written. CLI-Anything adds auto-discovery and structured output that Makefiles lack.

## Fit Assessment

### Relevant If

- Project needs to wrap external tools (e.g., pandoc, lychee, jscpd) as agent-native CLIs with JSON output and auto-discovery
- Non-developer stakeholders need to interact with complex software through agent-mediated CLIs
- Multiple applications need unified CLI interfaces for agent orchestration

### Not Relevant If

- Tools already have adequate CLI interfaces (most dev tools do)
- Makefiles or shell scripts are sufficient for the project's automation needs
- No need for structured JSON output or undo/redo state management

### Decision

**Monitor, do not adopt.** CLI-Anything solves a real problem (wrapping GUI-first software for agent use) but targets a different use case than typical developer tooling. Most developer tools (git, pytest, ruff, pandoc) already have CLIs. The framework is most valuable for creative/enterprise software (GIMP, Blender, LibreOffice) that lacks agent-friendly interfaces.

Worth revisiting if:

1. A project workflow requires wrapping GUI-only software
2. The CC plugin ecosystem standardizes on CLI-Anything-generated interfaces
3. The framework adds support for wrapping existing CLIs with enhanced JSON output

## References

- [CLI-Anything (GitHub)][cli-anything]
- [CC Plugin Packaging Research](../plugins-ecosystem/CC-plugin-packaging-research.md)
- [CC Skills Adoption Analysis](CC-skills-adoption-analysis.md)

[cli-anything]: https://github.com/HKUDS/CLI-Anything
