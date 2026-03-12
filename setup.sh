#!/usr/bin/env bash
# systems-thinking-plugin setup
# Run this once after cloning to verify dependencies and initialize the environment.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "systems-thinking-plugin setup"
echo "=============================="
echo ""

# ---- Check: uv ----
if ! command -v uv &> /dev/null; then
    echo -e "${RED}✗ uv is not installed${NC}"
    echo ""
    echo "  uv is required for dependency management in this project."
    echo ""
    read -p "  Install uv now? [Y/n] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        echo "  Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
        if command -v uv &> /dev/null; then
            echo -e "  ${GREEN}✓ uv installed ($(uv --version))${NC}"
        else
            echo -e "  ${RED}✗ uv installation failed${NC}"
            echo "  Try manually: curl -LsSf https://astral.sh/uv/install.sh | sh"
            exit 1
        fi
    else
        echo -e "  ${YELLOW}Skipped. Install uv manually:${NC}"
        echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo ""
        echo "  Or via Homebrew:"
        echo "    brew install uv"
        exit 1
    fi
else
    echo -e "${GREEN}✓ uv $(uv --version)${NC}"
fi

# ---- Check: Python ----
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ python3 not found${NC}"
    echo "  Install Python 3.11+ via uv:"
    echo "    uv python install 3.12"
    exit 1
else
    PY_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}✓ $PY_VERSION${NC}"
fi

# ---- Check: tmux (optional) ----
if command -v tmux &> /dev/null; then
    echo -e "${GREEN}✓ tmux $(tmux -V)${NC}"
else
    echo -e "${YELLOW}○ tmux not installed (optional — needed for --tmux flag in orchestrator)${NC}"
fi

# ---- Check: claude CLI (optional) ----
if command -v claude &> /dev/null; then
    echo -e "${GREEN}✓ claude CLI available${NC}"
else
    echo -e "${YELLOW}○ claude CLI not found (needed for orchestrator workers and evals)${NC}"
fi

# ---- Sync dependencies ----
echo ""
echo "Syncing project dependencies..."
cd "$SCRIPT_DIR"
uv sync 2>&1 | sed 's/^/  /'
echo -e "${GREEN}✓ Dependencies synced${NC}"

# ---- Sync test dependencies ----
echo "Syncing test dependencies..."
uv sync --group test 2>&1 | sed 's/^/  /'
echo -e "${GREEN}✓ Test dependencies synced${NC}"

# ---- Run quick validation ----
echo ""
echo "Running quick validation..."
uv run pytest tests/unit tests/contracts -q --tb=line 2>&1 | sed 's/^/  /'

# ---- Verify utils ----
echo ""
echo "Verifying utility scripts..."
UTILS_OK=true
for script in index_doc.py scan_patterns.py slice_sections.py estimate_tokens.py aggregate.py validate_output.py build_prompt.py orchestrate.py tmux_runner.py; do
    if [[ -f "$SCRIPT_DIR/utils/$script" ]]; then
        echo -e "  ${GREEN}✓${NC} utils/$script"
    else
        echo -e "  ${RED}✗${NC} utils/$script missing"
        UTILS_OK=false
    fi
done

# ---- Summary ----
echo ""
echo "=============================="
echo -e "${GREEN}Setup complete.${NC}"
echo ""
echo "Quick start:"
echo "  uv run pytest tests/unit tests/contracts    # run tests"
echo "  uv run python utils/orchestrate.py --help   # orchestrator help"
echo ""
echo "For tmux-based parallel workflows:"
echo "  uv run python utils/orchestrate.py --workflow complexity-mapper --input doc.md --output output/ --tmux"
