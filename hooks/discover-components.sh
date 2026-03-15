#!/bin/bash
# Discovers skill and agent names from the plugin directory structure.
# Sourced by other hook scripts. Requires CLAUDE_PLUGIN_ROOT to be set.
#
# Exports:
#   SKILL_NAMES   — pipe-delimited skill directory names (e.g. "complexity-mapper|decision-brief|...")
#   AGENT_NAMES   — pipe-delimited agent file names without .md (e.g. "doc-reader|caveat-extractor|...")
#   PROMPT_KEYWORDS — SKILL_NAMES plus human-friendly variants for matching user prompts
#   INVOCATION_PATTERNS — regex matching actual agent/skill invocations in transcript JSON

PLUGIN_ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

# Discover skills from skills/ subdirectories
SKILL_NAMES=""
if [ -d "$PLUGIN_ROOT/skills" ]; then
  SKILL_NAMES=$(ls -1 "$PLUGIN_ROOT/skills" 2>/dev/null | tr '\n' '|' | sed 's/|$//')
fi

# Discover agents from agents/*.md files (strip .md extension)
AGENT_NAMES=""
if [ -d "$PLUGIN_ROOT/agents" ]; then
  AGENT_NAMES=$(ls -1 "$PLUGIN_ROOT/agents" 2>/dev/null | sed 's/\.md$//' | tr '\n' '|' | sed 's/|$//')
fi

# Build human-friendly prompt keywords from skill names (e.g. "complexity-mapper" -> "complexity map")
FRIENDLY_KEYWORDS=""
if [ -n "$SKILL_NAMES" ]; then
  FRIENDLY_KEYWORDS=$(echo "$SKILL_NAMES" | tr '|' '\n' | sed 's/-/ /g; s/er$//; s/or$//' | tr '\n' '|' | sed 's/|$//')
fi

# Combine all keywords for matching user prompts
PROMPT_KEYWORDS="systems-thinking"
[ -n "$SKILL_NAMES" ] && PROMPT_KEYWORDS="${PROMPT_KEYWORDS}|${SKILL_NAMES}"
[ -n "$AGENT_NAMES" ] && PROMPT_KEYWORDS="${PROMPT_KEYWORDS}|${AGENT_NAMES}"
[ -n "$FRIENDLY_KEYWORDS" ] && PROMPT_KEYWORDS="${PROMPT_KEYWORDS}|${FRIENDLY_KEYWORDS}"

# Build invocation patterns for transcript matching (actual tool calls, not mentions)
INVOCATION_PATTERNS='"subagent_type"\s*:\s*"systems-thinking-plugin:|"skill"\s*:\s*"systems-thinking-plugin:'
if [ -n "$AGENT_NAMES" ]; then
  INVOCATION_PATTERNS="${INVOCATION_PATTERNS}|\"subagent_type\"\s*:\s*\"(${AGENT_NAMES})\""
fi
if [ -n "$SKILL_NAMES" ]; then
  INVOCATION_PATTERNS="${INVOCATION_PATTERNS}|\"skill\"\s*:\s*\"(${SKILL_NAMES})\""
fi
INVOCATION_PATTERNS="(${INVOCATION_PATTERNS})"
