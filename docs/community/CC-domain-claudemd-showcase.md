---
title: CC Domain-Specific CLAUDE.md Showcase
description: Analysis of CLAUDE.md as a domain-specific pipeline controller — genome analysis toolkit case study demonstrating the pattern of CLAUDE.md orchestrating multi-script workflows beyond software development.
category: landscape
status: research
sources:
  - https://github.com/shmlkv/dna-claude-analysis
created: 2026-03-13
updated: 2026-03-13
---

**Status**: Research (informational)

## Summary

The dna-claude-analysis repo demonstrates CLAUDE.md used not as coding instructions but as a **domain-specific pipeline controller** — orchestrating 17 Python scripts for genome analysis through conversational interaction. This pattern generalizes: CLAUDE.md can define multi-script workflows for any domain where a non-developer needs to run analysis pipelines and explore results interactively.

## Case Study: dna-claude-analysis

**Repo**: [shmlkv/dna-claude-analysis](https://github.com/shmlkv/dna-claude-analysis)

### What It Is

A genome analysis toolkit: 17 Python scripts in `scripts/`, each targeting a distinct genomic domain, orchestrated by a CLAUDE.md that defines a four-step conversational workflow.

### Script Inventory (17)

| Script | Domain |
|--------|--------|
| `health_analysis.py` | General health risk variants |
| `ancestry_analysis.py` | Population genetics and haplogroups |
| `nutrition_analysis.py` | Nutrient metabolism (MTHFR, lactose, caffeine) |
| `carrier_status_analysis.py` | Recessive condition carrier screening |
| `cognitive_analysis.py` | Cognitive trait associations |
| `longevity_analysis.py` | Aging and telomere-related variants |
| `psychology_analysis.py` | Behavioral trait associations |
| `sports_fitness_analysis.py` | Athletic performance genetics |
| `sleep_chronotype_analysis.py` | Circadian rhythm variants |
| `immunity_analysis.py` | Immune system genetics |
| `detoxification_analysis.py` | Xenobiotic metabolism |
| `skin_analysis.py` | Dermatological trait variants |
| `vision_hearing_analysis.py` | Sensory genetics |
| `pain_sensitivity_analysis.py` | Pain perception variants |
| `reproductive_analysis.py` | Reproductive health genetics |
| `physical_traits_analysis.py` | Physical characteristic variants |
| *(+1 additional)* | |

Each script reads from a single configurable `GENOME_FILE` variable and outputs a markdown report to `reports/`.

### CLAUDE.md as Pipeline Controller

The CLAUDE.md defines a four-step workflow:

1. **Configuration**: user places DNA file in `data/` and tells Claude the filename. Claude updates `GENOME_FILE` across all 17 scripts simultaneously — no manual editing.
2. **Execution**: Claude runs all scripts: `for f in *_analysis.py; do python "$f"; done`
3. **Report ingestion**: Claude reads generated markdown reports from `reports/`
4. **Visualization**: Claude generates a single-file HTML dashboard at `webpage/dna_terminal.html`

**Output constraints encoded in CLAUDE.md**:

- Terminal aesthetic (JetBrains Mono, green-on-black)
- Russian localization
- No external dependencies beyond Google Fonts
- Fixed navigation header with 17 section anchors
- Color-coded findings (green/amber/red by risk level)
- Mandatory medical disclaimers
- Never commit DNA data to git

### Three-Stage Architecture

```
Stage 1: Analysis          Stage 2: Exploration        Stage 3: Visualization
scripts/*.py               Conversational Q&A          dna_terminal.html
  |                          |                            |
  v                          v                            v
Parse ~600-700K SNPs      "What does my MTHFR         Single-file HTML
Match against SNP DBs      status mean?"               dashboard with all
Emit markdown reports     Cross-domain synthesis       17 sections
to reports/               Practical implications       Self-contained, no
                                                       build step
```

### Conversational Exploration Pattern

The key differentiator from traditional analysis pipelines: results are explored through dialogue rather than static dashboards.

Example interaction flows:

- "Run health analysis" -> Claude executes script, reports results
- "What does my MTHFR status mean for daily life?" -> Claude contextualizes from report + domain knowledge
- "How does this affect my diet?" -> multi-turn follow-up
- "Connect my sleep issues to these variants" -> cross-script synthesis that no single script produces

### Supporting Patterns

- **`webpage/STYLE_GUIDE.md`**: defines HTML component patterns (tables, findings, charts) as a template contract for consistent visualization
- **Format auto-detection**: scripts handle multiple genotyping provider formats (23andMe, AncestryDNA, MyHeritage, Nebula, VCF) without user configuration
- **Privacy-first**: `.gitignore` protects raw genome data; nothing leaves local machine

## Generalizable Pattern: CLAUDE.md as Workflow Orchestrator

The dna-claude-analysis pattern abstracts to any domain where:

1. **Multiple scripts** produce independent analysis outputs
2. **A non-developer user** needs to run and explore results
3. **Cross-analysis synthesis** adds value beyond individual script outputs
4. **Conversational configuration** replaces manual config file editing

### Pattern Template

```markdown
# CLAUDE.md for [Domain] Analysis

## Setup
- User provides [input data] in `data/`
- Update [CONFIG_VAR] across all scripts in `scripts/`

## Execution
- Run all scripts: [batch command]
- Reports written to `reports/`

## Exploration
- Answer questions about results using reports as context
- Cross-reference findings across analysis domains
- Provide practical implications

## Output
- Generate [visualization format] at [output path]
- Follow [STYLE_GUIDE.md] for component patterns
- Constraints: [localization, accessibility, privacy]
```

### Potential Domains

This pattern applies wherever domain experts need to run and explore multi-script analysis:

- **Financial analysis**: portfolio risk scripts -> conversational exploration of exposures
- **Security auditing**: scanner scripts -> conversational triage of findings
- **Data quality**: validation scripts -> conversational investigation of anomalies
- **Research pipelines**: experiment analysis scripts -> conversational result exploration

## Cross-References

- [CC-memory-system-analysis.md](../cc-native/context-memory/CC-memory-system-analysis.md) — CLAUDE.md format and hierarchy
- [CC-skills-adoption-analysis.md](../cc-native/agents-skills/CC-skills-adoption-analysis.md) — skills as an alternative to CLAUDE.md-driven workflows
