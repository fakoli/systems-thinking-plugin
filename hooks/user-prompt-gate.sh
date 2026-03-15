#!/bin/bash
# Only inject the extraction/synthesis reminder when the user's prompt
# references systems-thinking skills or workflows.
#
# Reads JSON from stdin (Claude Code hook system).
# Outputs a prompt message to stdout only when relevant.
# Exit 0 = always approve (never block user input).

set -uo pipefail

input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')

# Keywords that indicate the user is invoking systems-thinking workflows
SKILL_KEYWORDS="architecture-risk-review|complexity-mapper|context-sharding|decision-brief|pattern-remix|systems-thinking|risk review|complexity map|hidden risk|decision brief"
AGENT_KEYWORDS="doc-indexer|doc-reader|caveat-extractor|cost-capacity|architecture-dependency|synthesis-brief"

# Check the user's current prompt for systems-thinking intent
if echo "$user_prompt" | grep -qiE "$SKILL_KEYWORDS|$AGENT_KEYWORDS" 2>/dev/null; then
  echo "Before proceeding, remember: separate extraction from synthesis. Preserve source anchors (file, section, page) on every finding. Do not collapse raw evidence into inferred conclusions until extraction is complete."
  exit 0
fi

# Also check if a systems-thinking workflow is already active in the transcript
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
  INVOCATION_PATTERNS='"subagent_type"\s*:\s*"systems-thinking-plugin:|"skill"\s*:\s*"systems-thinking-plugin:|"subagent_type"\s*:\s*"(architecture-dependency-mapper|caveat-extractor|cost-capacity-analyst|doc-indexer|doc-reader|pattern-remix-planner|synthesis-brief-writer)"|"skill"\s*:\s*"(architecture-risk-review|complexity-mapper|context-sharding|decision-brief|pattern-remix)"'
  if grep -qE "$INVOCATION_PATTERNS" "$transcript_path" 2>/dev/null; then
    echo "Before proceeding, remember: separate extraction from synthesis. Preserve source anchors (file, section, page) on every finding. Do not collapse raw evidence into inferred conclusions until extraction is complete."
    exit 0
  fi
fi

# Not a systems-thinking workflow — no prompt injection needed
exit 0
