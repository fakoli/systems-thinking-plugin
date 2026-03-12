# systems-thinking-plugin

A Claude Code plugin that helps senior infrastructure and network engineers surface hidden complexity, reuse proven design patterns, and produce decision-ready artifacts from large or messy source material. Everything is local, file-based, and auditable.

## Who this is for

Engineers who do architecture reviews, vendor evaluations, connectivity design, migration planning, or any work where the real risks hide in the details. The plugin is most useful when you have too much source material for a single clean reasoning pass, or when you need structured outputs that hold up in design reviews and stakeholder conversations.

## Core workflows

### 1. Context Sharding

Break large input (big repos, multi-document vendor packages, sprawling architecture notes) into focused chunks. Extraction agents process each chunk independently and produce Context Packets with findings, caveats, and source anchors. This prevents the common failure mode where early impressions bias how later material is read.

**Invoke with:** `/context-sharding`

### 2. Complexity Mapper

Take extracted findings and surface hidden implementation complexity, operational burden, cost traps, and architectural risks that are not obvious from a surface reading. Produces a Complexity Heat Map (ranked areas of difficulty) and a Hidden Risk Summary (non-obvious risks with impact assessment).

**Invoke with:** `/complexity-mapper`

### 3. Pattern Remix

Adapt prior proven work to a new problem. Feed in a known-good design and a set of new constraints, and get back a draft plan that identifies what transfers, what needs adaptation, and what risks the adaptation introduces.

**Invoke with:** `/pattern-remix`

### Supporting skills

- `/decision-brief` — Package findings into a stakeholder-ready Decision Brief with evidence, risks, and next steps.
- `/architecture-risk-review` — Targeted review of failure modes, hidden dependencies, and operational burden.

## Quick start

### 1. Populate your reference material

Drop source documents into the `reference/` subdirectories:

```
reference/
├── previous_designs/    # Prior design docs, ADRs, architecture notes
├── vendor_docs/         # Vendor PDFs, pricing sheets, technical guides
├── prompts/             # Prompts and patterns that have worked before
└── examples/            # Example outputs showing the quality bar you want
```

The more relevant material you provide, the better the extraction agents perform. Even one good prior design or one vendor doc is enough to start.

### 2. Invoke a skill

For a vendor risk scan:
```
/complexity-mapper
Scan reference/vendor_docs/vendor-x/ for hidden risks, quota limits, and operational constraints.
```

For a repo orientation:
```
/context-sharding
Orient me to this repo. Map the major modules, flag complexity areas, and tell me what to inspect first.
```

For reusing a prior design:
```
/pattern-remix
Prior work: reference/previous_designs/hub-spoke-v2/
Target: Extend to a third cloud provider.
Constraints: No BGP community support on the new provider.
```

### 3. Review the output

All outputs follow structured contracts (see `docs/output-contracts.md`). Every finding includes source anchors so you can verify claims against the original material. Assumptions and unresolved questions are called out explicitly.

## Directory structure

```
systems-thinking-plugin/
├── .claude/
│   ├── agents/              # Subagent definitions
│   │   ├── doc-indexer.md           # Scan and map document structure
│   │   ├── doc-reader.md           # Extract technical claims and limits
│   │   ├── caveat-extractor.md     # Find buried limitations and traps
│   │   ├── cost-capacity-analyst.md # Surface cost and scaling issues
│   │   ├── architecture-dependency-mapper.md # Map dependencies
│   │   ├── pattern-remix-planner.md # Adapt prior work to new problems
│   │   └── synthesis-brief-writer.md # Turn evidence into decision briefs
│   ├── skills/              # Workflow playbooks
│   │   ├── pattern-remix.md
│   │   ├── complexity-mapper.md
│   │   ├── context-sharding.md
│   │   ├── decision-brief.md
│   │   └── architecture-risk-review.md
│   └── settings.json        # Hooks configuration
├── specs/                   # Design specifications (00-11 numbered files)
├── reference/               # Your source material goes here
├── docs/                    # Reference documentation
│   ├── output-contracts.md          # The 5 output format definitions
│   ├── agent-design-principles.md   # How agents are designed and why
│   └── repo-conventions.md          # Naming, structure, and style rules
├── examples/
│   └── usage-scenarios.md           # 4 worked examples with agent flows
├── CLAUDE.md                # Project instructions for Claude Code
├── COMPATIBILITY_NOTES.md   # Notes on Cursor and other platforms
└── README.md
```

## How to populate reference/ for better results

The agents work best when they have real source material to extract from. Here is what to put in each directory:

**`reference/previous_designs/`** — Drop in design documents, architecture decision records, implementation plans, or Terraform module structures from prior work you want to reuse or reference. The pattern-remix workflow reads from here.

**`reference/vendor_docs/`** — Vendor technical documentation, pricing pages, SLA descriptions, quota tables, API references. The complexity-mapper and context-sharding workflows read from here when doing vendor evaluations.

**`reference/prompts/`** — Prompts, prompt chains, or instruction sets that have produced good results in the past. These help calibrate agent behavior to your preferred style and depth.

**`reference/examples/`** — Example outputs showing the quality bar and format you expect. If you have a particularly good decision brief or risk summary from prior work, drop it here.

You do not need all four directories populated to start. One vendor doc or one prior design is enough for a useful run.

## Further reading

- `docs/output-contracts.md` — Detailed definitions of the 5 output formats
- `docs/agent-design-principles.md` — Why agents are designed the way they are
- `docs/repo-conventions.md` — Naming, structure, and contribution conventions
- `examples/usage-scenarios.md` — 4 detailed usage scenarios with agent flows
- `COMPATIBILITY_NOTES.md` — Notes on Cursor compatibility and platform differences
