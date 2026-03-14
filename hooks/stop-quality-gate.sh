#!/bin/bash
# Gate script for the Stop hook: only trigger the quality check
# when systems-thinking agents or skills were used in the session.
#
# Reads JSON from stdin (provided by Claude Code hook system).
# Checks the transcript for systems-thinking usage markers.
# Exit 0 = approve (no quality check needed)
# Exit 2 + stderr = block (quality sections missing)

set -euo pipefail

input=$(cat)
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')

# If no transcript available, approve silently
if [ -z "$transcript_path" ] || [ ! -f "$transcript_path" ]; then
  exit 0
fi

# Systems-thinking agent and skill identifiers
PATTERNS="systems-thinking-plugin|architecture-dependency-mapper|caveat-extractor|cost-capacity-analyst|doc-indexer|doc-reader|pattern-remix-planner|synthesis-brief-writer|architecture-risk-review|complexity-mapper|context-sharding|decision-brief|pattern-remix"

# Check if any systems-thinking component was invoked
if ! grep -qiE "$PATTERNS" "$transcript_path" 2>/dev/null; then
  # No systems-thinking usage — approve, skip quality check
  exit 0
fi

# Systems-thinking was used — check for required quality sections
transcript=$(cat "$transcript_path")

missing=""
echo "$transcript" | grep -qi "assumption" || missing="${missing}assumptions, "
echo "$transcript" | grep -qi "risk" || missing="${missing}risks, "
echo "$transcript" | grep -qi "unresolved" || missing="${missing}unresolved questions, "
echo "$transcript" | grep -qi "next step\|next check\|recommended" || missing="${missing}next steps, "

if [ -n "$missing" ]; then
  missing="${missing%, }"  # trim trailing comma
  echo "{\"decision\": \"block\", \"reason\": \"Systems-thinking analysis is missing: ${missing}. Add these sections before completing.\"}" >&2
  exit 2
fi

# All quality sections present
exit 0
