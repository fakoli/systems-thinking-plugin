# systems-thinking-plugin

<p align="center">
  <img src="iceberg-banner.png" alt="Systems Thinking Plugin — the iceberg of hidden complexity" width="800">
</p>

A Claude Code plugin that applies systems thinking to infrastructure and architecture decisions — surfacing what vendors don't show you, what consultants gloss over, and what only becomes visible when you're in production with no exit.

## Why this exists

Systems engineers think differently. Whether the problem is a network design, a cloud migration, a storage architecture, or a vendor evaluation — the discipline is the same: understand what a system does well, understand what it *doesn't* do well, and build pathways to close the gap before you're in production wondering why nobody told you.

The pattern repeats across every technology and every era. First you get the rosy part, because that's what sells it. The vendor demo works. The POC looks clean. The pricing page makes sense. Then you commit, and you discover what was below the waterline the whole time — the quotas that bite at scale, the cost mechanics that compound non-linearly, the dependencies between services that nobody mapped, the caveats buried in page 47 of the docs.

This is the iceberg problem. The visible tip is what gets sold. The massive hidden mass below is what you actually have to operate. A systems engineer's job has always been to look below that waterline — to ask the questions that the sales pitch doesn't invite, to read the docs that the POC doesn't exercise, to map the dependencies that only matter when something fails. Whether you're evaluating a new cloud service, planning a multi-region architecture, designing a storage tier, or provisioning an OS at scale — the methodology is the same.

This plugin encodes that methodology into reusable workflows:

- **Extract before you synthesize.** Separate the work of gathering what a source *actually says* from the work of interpreting it. Extraction agents pull out every technical claim, limitation, cost mechanic, and dependency — faithfully, with source anchors. It's the difference between "what the vendor's doc claims" and "what you'll actually pay for." Synthesis agents connect those findings into decisions only after extraction is complete.
- **Preserve what you find.** Every finding traces back to a specific file, section, or page. Not "broadly available" when it says "us-east-1 only." Not "supports X" when the doc says "supports X when Y is also true." No collapsed nuance. The caveats are where the real decisions live.
- **Reuse what worked.** Prior designs, architecture decisions, and proven patterns are first-class inputs. The plugin adapts them to new constraints rather than starting from scratch, while flagging where the old context no longer applies. Lessons that got lost in the last vendor's sales pitch get carried forward.
- **Produce artifacts that travel.** Outputs follow structured contracts (Decision Briefs, Risk Summaries, Complexity Heat Maps) designed for design reviews, stakeholder conversations, and handoffs — not confident guesses dressed up as analysis.

Understanding what systems *don't* do well is as important as understanding what they do well. This plugin builds the discipline of looking below the waterline into reusable workflows — so the gaps surface before you've committed, not after. See `docs/systems-thinking-foundations.md` for the full conceptual mapping.

## Install

```bash
git clone https://github.com/fakoli/systems-thinking-plugin.git
cd systems-thinking-plugin
./setup.sh
```

The setup script checks for `uv`, `python3`, `tmux` (optional), and the `claude` CLI (optional), then syncs dependencies and runs validation.

## Workflows

Five workflows, each modeling a different phase of how a systems engineer navigates a problem:

### `/complexity-mapper`

The full below-the-waterline scan. When you have a design, a vendor proposal, or an architecture doc and you need to know where complexity is hiding — cost traps, scaling cliffs, dependency chains, operational burden that isn't in the pitch deck. Runs extraction agents in parallel, then synthesizes findings into a **Complexity Heat Map** and **Hidden Risk Summary**.

### `/context-sharding`

When the material is too large for a single pass — vendor doc packages, sprawling repos, multi-service specs. A systems engineer doesn't read 200 pages linearly and hope to catch everything. This workflow breaks material into focused chunks, extracts independently from each, and catches what a single-pass read would miss. Produces **Context Packets** with findings, caveats, and source anchors.

### `/pattern-remix`

Systems engineers don't start from scratch when a proven pattern exists. This workflow takes a known-good design and adapts it to new constraints — mapping what transfers, what needs to change, and what assumptions from the old context no longer hold. Produces a **Pattern Remix Draft** with source tracing and divergence risks.

### `/decision-brief`

Package extracted findings into a stakeholder-ready **Decision Brief** with evidence, options, risks, and next steps. The artifact that travels from the engineer's analysis to the review board's decision.

### `/architecture-risk-review`

Focused risk assessment of a specific architecture — failure modes, hidden dependencies, single points of failure, blast radius, operational survivability. The questions a systems engineer asks before signing off on a design. Produces a **Hidden Risk Summary** with architectural focus.

## How it works

Here's what a typical `/complexity-mapper` session looks like in Claude Code. The same pipeline pattern applies to all workflows — the agents and outputs change, but the rhythm is the same.

### 1. Invoke the skill

```
You: /complexity-mapper

     Analyze this multi-cloud VPC architecture for hidden risks.
     We're planning AWS as primary with GCP expansion, shared VPC
     model, 320K hosts, HA VPN initially moving to dedicated
     interconnect via Megaport.
```

You describe what you're evaluating and what concerns you. The skill takes it from there.

### 2. Document indexing (~10 seconds)

Claude invokes the `doc-indexer` agent, which scans your provided materials and maps the structure — headings, sections, high-value areas, caveat-rich zones:

```
  doc-indexer scanning 3 documents...

  Document: vpc-architecture.md
    12 sections mapped, 4 flagged as high-value
    Caveat-rich areas: Quotas table (L45), Pricing notes (L112)

  Document: interconnect-proposal.md
    8 sections mapped, 2 flagged
    Gap identified: no failover documentation

  Prioritized Reading List:
  | Priority | Section              | Recommended Agent           |
  |----------|----------------------|-----------------------------|
  | P1       | VPC quotas & limits  | caveat-extractor            |
  | P1       | Pricing mechanics    | cost-capacity-analyst       |
  | P1       | Service dependencies | architecture-dependency-mapper |
  | P2       | Migration timeline   | doc-reader                  |
```

### 3. Source discovery (when external docs are needed)

If the doc-indexer identifies gaps — vendor quotas not in your files, pricing pages you don't have locally — Claude invokes the `web-researcher` to find them:

```
  web-researcher discovering sources for 3 topics...

  Source Manifest:
  | # | Title                      | URL                              | Relevance |
  |---|----------------------------|----------------------------------|-----------|
  | 1 | AWS VPC IPAM Quotas        | docs.aws.amazon.com/vpc/...      | High      |
  | 2 | GCP Shared VPC Limits      | cloud.google.com/vpc/docs/...    | High      |
  | 3 | AWS Direct Connect Pricing | aws.amazon.com/directconnect/... | High      |

  Gaps: GCP VPN pricing page returned JavaScript-only content (not extractable)
```

Claude presents the Source Manifest for your review before proceeding. You can add or remove sources.

### 4. Dispatch planning (~10 seconds)

The `extraction-planner` looks at the total volume of material and decides how to parallelize the work — how many extraction agents to spawn and what scoped instructions each gets:

```
  extraction-planner assessing material volume...

  Dispatch Plan:
  - Total sections: 23
  - Material volume: Large
  - Recommended: 6 extraction agents

  | Agent # | Type                         | Focus Scope                    |
  |---------|------------------------------|--------------------------------|
  | 1       | caveat-extractor             | AWS VPC quotas, NAU limits     |
  | 2       | caveat-extractor             | GCP Shared VPC, GKE ranges     |
  | 3       | caveat-extractor             | Connectivity, VPN/interconnect |
  | 4       | cost-capacity-analyst        | Pricing across all services    |
  | 5       | architecture-dependency-mapper| Cross-cloud dependencies       |
  | 6       | architecture-dependency-mapper| Migration path dependencies    |
```

This step prevents the overload that happens when a single agent tries to process too much material at once. Each agent gets bounded, focused instructions.

### 5. Parallel extraction (~30-90 seconds)

Claude launches the extraction agents in parallel. Each one works on its assigned sections and produces findings with source anchors:

```
  Launching 6 extraction agents in parallel...

  ✓ caveat-extractor (AWS): 29 caveats found (9 critical)
  ✓ caveat-extractor (GCP): 31 caveats found (9 critical)
  ✓ caveat-extractor (connectivity): 18 caveats found (5 critical)
  ✓ cost-capacity-analyst: 22 pricing items confirmed, 6 unknown
  ✓ architecture-dependency-mapper (cross-cloud): 14 dependencies, 4 SPOFs
  ✓ architecture-dependency-mapper (migration): 7 dependencies, 2 chokepoints
```

### 6. Synthesis (~30-60 seconds)

The `synthesis-brief-writer` combines all extraction outputs into structured artifacts:

```
Complexity Heat Map

| Area                  | Type       | Likelihood | Impact | Visibility |
|-----------------------|------------|------------|--------|------------|
| GKE pod range sizing  | Cost       | High       | High   | Hidden     |
| VPC NAU ceiling 256K  | Quota      | Critical   | High   | Hidden     |
| No cross-cloud IPAM   | Dependency | High       | High   | Hidden     |
| HA VPN bandwidth cap  | Scaling    | Medium     | High   | Visible    |

Top 3 Risks:
1. 320K NAU exceeds AWS per-VPC ceiling (256K max) — multi-VPC mandatory
2. GKE pod ranges consume 47% of /8 at default sizing — immutable setting
3. No native cross-cloud IPAM — overlapping CIDRs undetectable
```

The full output includes source anchors for every finding, severity ratings, unresolved questions, and recommended next steps — ready for a design review or stakeholder conversation.

### What to expect

- **Total time:** 2-5 minutes for a typical analysis, depending on material volume and whether web research is needed
- **Token usage:** Varies with material size. Small analyses (≤5 sections) use minimal tokens. Large multi-cloud research can use significantly more.
- **User interaction:** The skill runs mostly autonomously. You'll be asked to review the Source Manifest (if web research fires) and may be asked clarifying questions if the material is ambiguous.
- **Output location:** Results are delivered inline in the conversation. Use `/decision-brief` afterward to package findings for stakeholders.

For more worked examples, see `examples/usage-scenarios.md`.

## Agents

The visible tip of the iceberg is what the vendor shows you. Everything below the waterline is what these agents find.

Nine subagents with narrow, auditable roles organized into three tiers — discovery agents cast the net, extraction agents pull out what matters, and synthesis agents connect it into decisions:

### Orchestration Agents (Discovery + Planning)

| Agent | Role | Model |
|-------|------|-------|
| `web-researcher` | Discover source material from web and local files | Sonnet |
| `extraction-planner` | Assess material volume, produce Dispatch Plans | Haiku |

### Extraction Agents (Fast + Parallel)

| Agent | Role | Model |
|-------|------|-------|
| `doc-indexer` | Map document structure, flag high-value sections | Haiku |
| `doc-reader` | Extract technical claims, limits, dependencies | Haiku |
| `caveat-extractor` | Find buried limitations, quotas, traps | Sonnet |
| `cost-capacity-analyst` | Surface cost mechanics, scaling constraints | Sonnet |
| `architecture-dependency-mapper` | Map control/data-plane dependencies | Sonnet |

### Synthesis Agents (High-Quality Output)

| Agent | Role | Model |
|-------|------|-------|
| `pattern-remix-planner` | Adapt prior work to new problems | Opus |
| `synthesis-brief-writer` | Turn extracted evidence into decision briefs | Opus |

**Pipeline flow for research-heavy workflows:**

```
web-researcher → doc-indexer → extraction-planner → [parallel extractors] → synthesis-brief-writer
   (discover)    (map structure)  (plan dispatch)    (scoped extraction)       (synthesize)
```

Only `web-researcher` has web access (WebSearch + WebFetch). All other agents work on pre-discovered material via Read, Grep, and Glob. The `extraction-planner` prevents extractor overload by right-sizing parallelization before agents are spawned.

## Reference material

Drop source documents into `reference/` subdirectories to give the agents real material to work with:

| Directory | Contents |
|-----------|----------|
| `previous_designs/` | Prior design docs, ADRs, architecture notes |
| `vendor_docs/` | Vendor documentation, pricing, quotas, SLAs |
| `prompts/` | Prompts and patterns that have worked before |
| `examples/` | Example outputs showing the quality bar you want |

Even one vendor doc or one prior design is enough to start.

## Output contracts

All outputs follow structured formats defined in `docs/output-contracts.md`:

- **Hidden Risk Summary** — scope, top risks, impact areas, assumptions, unresolved questions
- **Complexity Heat Map** — complexity areas ranked by severity and confidence
- **Decision Brief** — decision frame, options, evidence, risks, next steps
- **Pattern Remix Draft** — reusable patterns, adaptations, constraints, known risks
- **Context Packet** — extracted findings with caveats and source anchors

Every finding includes source anchors so you can verify claims against the original material.

## Testing

**CI (automated):** Unit and contract tests run on every push and PR.

```bash
uv run pytest tests/unit tests/contracts -v
```

**Evals (manual, local only):** Eval tests invoke the Claude CLI and require it on your PATH. These are not run in CI — run them locally when validating agent behavior.

```bash
# Run all evals
uv run pytest tests/evals -v -m eval --timeout=300

# Run a single eval
uv run pytest tests/evals -v -k complexity_mapper

# Dry-run (validate case files without executing)
python tests/evals/harness.py --dry-run
```

## Further reading

- `docs/systems-thinking-foundations.md` — Conceptual foundations and concept-to-capability mapping
- `docs/output-contracts.md` — Output format definitions
- `docs/agent-design-principles.md` — Agent design rationale
- `docs/repo-conventions.md` — Naming and structure conventions
- `examples/usage-scenarios.md` — Worked examples with agent flows
- `COMPATIBILITY_NOTES.md` — Cursor compatibility notes
