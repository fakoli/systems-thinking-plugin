# systems-thinking-plugin

A Claude Code plugin for senior infrastructure and network engineers. Surface hidden complexity, reuse proven design patterns, and produce decision-ready artifacts — all local and file-based.

## Install

```bash
git clone https://github.com/fakoli/systems-thinking-plugin.git
cd systems-thinking-plugin
./setup.sh
```

The setup script checks for `uv`, `python3`, `tmux` (optional), and the `claude` CLI (optional), then syncs dependencies and runs validation.

## Workflows

The plugin provides five slash-command skills, each orchestrating a set of focused subagents.

### `/complexity-mapper`

Surface hidden implementation complexity, cost traps, and architectural risks. Runs extraction agents (caveat-extractor, cost-capacity-analyst, architecture-dependency-mapper) in parallel, then synthesizes findings into a **Complexity Heat Map** and **Hidden Risk Summary**.

### `/context-sharding`

Break large or varied source material (vendor packages, sprawling repos, multi-document specs) into focused chunks. Extraction agents process each chunk independently, producing **Context Packets** with findings, caveats, and source anchors. Prevents early-impression bias from a single-pass read.

### `/pattern-remix`

Adapt prior proven work to a new problem. Provide a known-good design and a set of new constraints to get a **Pattern Remix Draft** identifying what transfers, what needs adaptation, and what risks the adaptation introduces.

### `/decision-brief`

Package extracted findings into a stakeholder-ready **Decision Brief** with evidence, options, risks, and next steps.

### `/architecture-risk-review`

Targeted review of failure modes, hidden dependencies, and operational burden for a specific architecture. Produces a **Hidden Risk Summary** with architectural focus.

## Agents

Seven subagents with narrow, auditable roles. Each agent has a designated model tier to balance speed and quality:

| Agent | Role | Model |
|-------|------|-------|
| `doc-indexer` | Map document structure, flag high-value sections | Haiku |
| `doc-reader` | Extract technical claims, limits, dependencies | Haiku |
| `caveat-extractor` | Find buried limitations, quotas, traps | Sonnet |
| `cost-capacity-analyst` | Surface cost mechanics, scaling constraints | Sonnet |
| `architecture-dependency-mapper` | Map control/data-plane dependencies | Sonnet |
| `pattern-remix-planner` | Adapt prior work to new problems | Opus |
| `synthesis-brief-writer` | Turn extracted evidence into decision briefs | Opus |

Extraction agents (Haiku/Sonnet) run fast and in parallel. Synthesis agents (Opus) run last and produce the final outputs.

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

- `docs/output-contracts.md` — Output format definitions
- `docs/agent-design-principles.md` — Agent design rationale
- `docs/repo-conventions.md` — Naming and structure conventions
- `examples/usage-scenarios.md` — Worked examples with agent flows
- `COMPATIBILITY_NOTES.md` — Cursor compatibility notes
