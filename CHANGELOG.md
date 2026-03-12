# Changelog

All notable changes to the systems-thinking-plugin will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-11

### Added

- **7 subagents** in `.claude/agents/`
  - 5 extraction agents: `doc-indexer`, `doc-reader`, `caveat-extractor`, `cost-capacity-analyst`, `architecture-dependency-mapper`
  - 2 synthesis agents: `pattern-remix-planner`, `synthesis-brief-writer`
- **5 skills** in `.claude/skills/`
  - `pattern-remix` — generate first drafts from prior work
  - `complexity-mapper` — surface hidden operational/cost/implementation complexity
  - `context-sharding` — split large source material across parallel agents
  - `decision-brief` — package findings for stakeholders
  - `architecture-risk-review` — targeted failure mode and dependency review
- **2 prompt-based hooks** in `.claude/settings.json`
  - Pre-flight reminder: enforce extraction/synthesis separation
  - Completion quality check: verify assumptions, risks, unresolved questions, next steps
- **5 output contracts** defined in `docs/output-contracts.md`
  - Hidden Risk Summary, Complexity Heat Map, Decision Brief, Pattern Remix Draft, Context Packet
- **Reference directory** (`reference/`) with 4 subdirectories
  - `previous_designs/`, `vendor_docs/`, `prompts/`, `examples/`
  - All agents and skills are aware of and pull from this directory
- **Testing infrastructure** with 182 passing tests
  - Unit tests: hook prompts, YAML frontmatter, file structure
  - Contract tests: plugin layout, agent specs, skill specs, output contracts
  - Eval harness: scenario-based testing with graders (file_exists, section_check, schema_match, forbidden_check, composite)
  - 3 eval cases with realistic fixture documents
- **CI pipeline** via GitHub Actions (`.github/workflows/test.yml`)
  - Unit + contract tests on every PR
  - Eval tests on labeled PRs and nightly schedule
  - Plugin structure validation
- **Documentation**
  - `CLAUDE.md` — project instructions and conventions
  - `README.md` — usage guide with quick start
  - `docs/agent-design-principles.md` — extraction vs synthesis rules
  - `docs/repo-conventions.md` — naming, structure, and output conventions
  - `COMPATIBILITY_NOTES.md` — Cursor adaptation notes
  - `examples/usage-scenarios.md` — 4 worked scenarios
- **Design specs** preserved in `specs/` (00–11 numbered documents)
