#!/bin/bash
# Only inject the extraction/synthesis reminder when the user's prompt
# references systems-thinking skills or workflows.
#
# Reads JSON from stdin (Claude Code hook system).
# Outputs a prompt message to stdout only when relevant.
# Exit 0 = always approve (never block user input).

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/discover-components.sh"

input=$(cat)
user_prompt=$(echo "$input" | jq -r '.user_prompt // empty')
transcript_path=$(echo "$input" | jq -r '.transcript_path // empty')

REMINDER="Before proceeding, remember: separate extraction from synthesis. Preserve source anchors (file, section, page) on every finding. Do not collapse raw evidence into inferred conclusions until extraction is complete."

# Check the user's current prompt for systems-thinking intent
if echo "$user_prompt" | grep -qiE "$PROMPT_KEYWORDS" 2>/dev/null; then
  echo "$REMINDER"
  exit 0
fi

# Also check if a systems-thinking workflow is already active in the transcript
if [ -n "$transcript_path" ] && [ -f "$transcript_path" ]; then
  if grep -qE "$INVOCATION_PATTERNS" "$transcript_path" 2>/dev/null; then
    echo "$REMINDER"
    exit 0
  fi
fi

# Not a systems-thinking workflow — no prompt injection needed
exit 0
