# Systems Thinking Plugin

A Claude Code plugin for senior infrastructure and network engineers. It surfaces hidden complexity, reuses proven patterns, and produces decision-ready artifacts — all local and file-based.

## Project Target

- **Primary:** Claude Code local project usage
- **Secondary:** Cursor compatibility later (document in COMPATIBILITY_NOTES.md, don't block on it)

## Core Workflows

### 1. Pattern Remix
Use prior proven work, target-state goals, and constraints to generate high-quality first drafts and execution plans for new but related problems.

### 2. Complexity Mapper
Surface hidden complexity, side effects, risks, dependencies, and likely project blow-up points by analyzing documentation, costs, capacity, and operational constraints.

### 3. Context Sharding
Split large input across parallel subagents so narrower agents can extract structure, summaries, caveats, and signals before a primary agent synthesizes them.

## Architecture

### Subagents (`.claude/agents/`)
Seven v1 subagents with narrow, auditable roles:

| Agent | Role | Type |
|-------|------|------|
| `pattern-remix-planner` | Convert prior examples + constraints into draft plans | Synthesis |
| `doc-indexer` | Map document structure, flag high-value sections | Extraction |
| `doc-reader` | Extract technical claims, limits, dependencies | Extraction |
| `caveat-extractor` | Find limitations, quotas, buried traps | Extraction |
| `cost-capacity-analyst` | Highlight cost mechanics, scaling constraints | Extraction |
| `architecture-dependency-mapper` | Map control/data-plane dependencies | Extraction |
| `synthesis-brief-writer` | Turn extracted evidence into decision briefs | Synthesis |

### Skills (`.claude/skills/` or `skills/`)
Five reusable Markdown playbooks:

- `pattern-remix.md` — generate first drafts from prior work
- `complexity-mapper.md` — uncover hidden operational/cost/implementation complexity
- `context-sharding.md` — break large source material into digestible packets
- `decision-brief.md` — package findings for stakeholders
- `architecture-risk-review.md` — targeted review of failure modes and dependencies

### Hooks
Minimal in v1. Only include if straightforward and robust:
- **Pre-flight reminder:** Reinforce extraction/synthesis separation before complex workflows
- **Completion quality check:** Verify outputs include assumptions, risks, unresolved questions, next steps

If hooks feel brittle, stub or document them instead.

## Agent Design Principles

1. **Separate extraction from synthesis.** Extraction agents gather facts. Synthesis agents connect findings into decisions. Never both.
2. **Keep roles narrow.** One primary job per subagent, clear boundaries.
3. **Preserve source anchors.** Always reference file, section, or source location.
4. **Prefer structured outputs.** Predictable headings so downstream agents consume cleanly.
5. **Avoid hallucinated certainty.** Call out ambiguity, missing data, low-confidence inferences.
6. **Optimize for senior engineering judgment.** Help evaluate implementation burden, hidden risk, decision quality.

### Extraction Agent Rules
- Extract, do not over-interpret
- Preserve nuance, return caveats and counterexamples
- Include unknowns
- Avoid final recommendations unless explicitly asked

### Synthesis Agent Rules
- Distinguish evidence from inference
- Call out assumptions explicitly
- Include unresolved questions
- Avoid overselling certainty
- Produce outputs useful in design reviews and stakeholder conversations

## Output Contracts

All deliverables must follow these structures:

### Hidden Risk Summary
`scope reviewed` · `top hidden risks` · `likely impact areas` · `assumptions` · `unresolved questions` · `source anchors`

### Complexity Heat Map
`complexity area` · `why it matters` · `severity` · `confidence` · `source anchors`

### Decision Brief
`decision under review` · `options considered` · `evidence summary` · `inferred concerns` · `top risks` · `recommended next checks` · `unresolved questions`

### Pattern Remix Draft
`target outcome` · `reusable prior patterns` · `constraints` · `proposed approach` · `implementation steps` · `known risks`

### Context Packet
`source name` · `section/scope reviewed` · `extracted findings` · `caveats` · `confidence/ambiguity notes` · `source anchors`

## Conventions

- Prefer many small composable files over one giant file
- Markdown-based definitions for subagents and skills
- Human-readable, consistent naming (`kebab-case` for files)
- Scope tools deliberately for subagents
- Protect context windows — don't overload them
- No MCP in v1 unless clearly justified
- No autonomous long-running systems

## Reference Directory (`reference/`)

An active reference library of material that informs agent behavior and grounds outputs in real prior work:

| Folder | Contents |
|--------|----------|
| `previous_designs/` | Prior design docs, proposals, architecture notes, ADRs |
| `vendor_docs/` | Vendor documentation, pricing, quotas, limitations |
| `prompts/` | Effective prompts and patterns that worked before |
| `examples/` | Example outputs showing desired behavior |

## Build Phases

- **Phase 0:** Infer resources from `reference/` and existing repo conventions
- **Phase 1:** Discovery — propose structure, identify what goes where, list assumptions
- **Phase 2:** Scaffold — create folders, write subagents, skills, hooks, config
- **Phase 3:** Refine — tighten prompts, improve consistency, add usage examples

## Non-Goals (v1)

- Marketplace-ready packaging
- Deep Cursor-specific work
- Polished UI or dashboards
- Generalized enterprise workflow engine
- Fully autonomous systems
