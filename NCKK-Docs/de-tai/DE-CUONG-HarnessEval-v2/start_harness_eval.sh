#!/usr/bin/env bash
# ==============================================================================
# HarnessEval — One-click setup & launch
#
# Usage:
#   chmod +x start_harness_eval.sh
#   ./start_harness_eval.sh
#
# What it does:
#   1. Check Python 3.10+
#   2. Create venv (if needed)
#   3. Install dependencies
#   4. Check/create .env file (API keys)
#   5. Check Ollama (optional, for local mode)
#   6. Create trajectories/ dir
#   7. Launch Streamlit dashboard
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     HarnessEval — Setup & Launch             ║${NC}"
echo -e "${BLUE}║     Modular Harness Evaluation Toolkit        ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ------------------------------------------------------------------
# Step 1: Check Python
# ------------------------------------------------------------------
echo -e "${YELLOW}[1/7] Checking Python...${NC}"

if command -v python &>/dev/null; then
    PYTHON=python
elif command -v python3 &>/dev/null; then
    PYTHON=python3
else
    echo -e "${RED}ERROR: Python not found. Install Python 3.10+ first.${NC}"
    exit 1
fi

PY_VERSION=$($PYTHON -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    echo -e "${RED}ERROR: Python 3.10+ required (found $PY_VERSION)${NC}"
    exit 1
fi
echo -e "${GREEN}  Python $PY_VERSION ✓${NC}"

# ------------------------------------------------------------------
# Step 2: Virtual environment
# ------------------------------------------------------------------
echo -e "${YELLOW}[2/7] Setting up virtual environment...${NC}"

if [ ! -d ".venv" ]; then
    echo "  Creating .venv..."
    $PYTHON -m venv .venv
    echo -e "${GREEN}  Created .venv ✓${NC}"
else
    echo -e "${GREEN}  .venv already exists ✓${NC}"
fi

# Activate venv
if [ -f ".venv/Scripts/activate" ]; then
    # Windows (Git Bash / MSYS2)
    source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
    # Linux / Mac
    source .venv/bin/activate
fi

# ------------------------------------------------------------------
# Step 3: Install dependencies
# ------------------------------------------------------------------
echo -e "${YELLOW}[3/7] Installing dependencies...${NC}"

pip install -e ".[dev]" -q 2>&1 | tail -3
echo -e "${GREEN}  Dependencies installed ✓${NC}"

# ------------------------------------------------------------------
# Step 4: Check .env file
# ------------------------------------------------------------------
echo -e "${YELLOW}[4/7] Checking API keys (.env)...${NC}"

if [ ! -f ".env" ]; then
    echo "  Creating .env from .env.example..."
    cp .env.example .env
    echo -e "${YELLOW}  .env created — please add your API keys!${NC}"
fi

# Read and check keys
HAS_KEY=false
ENV_STATUS=""

check_key() {
    local key_name=$1
    local label=$2
    local value=$(grep "^${key_name}=" .env 2>/dev/null | cut -d'=' -f2-)
    if [ -n "$value" ] && [ "$value" != "" ]; then
        echo -e "  ${GREEN}${label}: ${value:0:10}...${NC}"
        HAS_KEY=true
    else
        echo -e "  ${RED}${label}: not set${NC}"
    fi
}

check_key "DEEPSEEK_API_KEY" "DeepSeek"
check_key "OPENAI_API_KEY" "OpenAI"
check_key "ANTHROPIC_API_KEY" "Anthropic"

if [ "$HAS_KEY" = false ]; then
    echo ""
    echo -e "${YELLOW}  ╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}  ║  No API keys found in .env                          ║${NC}"
    echo -e "${YELLOW}  ║                                                      ║${NC}"
    echo -e "${YELLOW}  ║  You can still use:                                  ║${NC}"
    echo -e "${YELLOW}  ║    • Ollama mode (free, local LLM)                   ║${NC}"
    echo -e "${YELLOW}  ║    • Dry-run mode (synthetic data)                   ║${NC}"
    echo -e "${YELLOW}  ║                                                      ║${NC}"
    echo -e "${YELLOW}  ║  To add keys later, edit: .env                       ║${NC}"
    echo -e "${YELLOW}  ╚══════════════════════════════════════════════════════╝${NC}"
    echo ""
fi

# ------------------------------------------------------------------
# Step 5: Check Ollama
# ------------------------------------------------------------------
echo -e "${YELLOW}[5/7] Checking Ollama (local LLM)...${NC}"

if command -v ollama &>/dev/null; then
    OLLAMA_VERSION=$(ollama --version 2>&1 | grep -oP '[\d.]+' | head -1)
    echo -e "${GREEN}  Ollama $OLLAMA_VERSION installed ✓${NC}"

    # Check if running
    if curl -s http://localhost:11434/api/tags &>/dev/null; then
        MODELS=$(curl -s http://localhost:11434/api/tags | $PYTHON -c "import sys,json; data=json.load(sys.stdin); print(', '.join(m['name'] for m in data['models']))" 2>/dev/null || echo "none")
        echo -e "${GREEN}  Ollama running — models: ${MODELS} ✓${NC}"
    else
        echo -e "${YELLOW}  Ollama installed but not running.${NC}"
        echo -e "${YELLOW}  Start with: ollama serve${NC}"
        echo -e "${YELLOW}  Pull a model: ollama pull qwen2.5:7b${NC}"
    fi
else
    echo -e "${YELLOW}  Ollama not installed (optional).${NC}"
    echo -e "${YELLOW}  Install: https://ollama.com/download${NC}"
    echo -e "${YELLOW}  Then: ollama pull qwen2.5:7b${NC}"
fi

# ------------------------------------------------------------------
# Step 6: Create directories
# ------------------------------------------------------------------
echo -e "${YELLOW}[6/7] Preparing directories...${NC}"

mkdir -p trajectories
echo -e "${GREEN}  trajectories/ ready ✓${NC}"

# ------------------------------------------------------------------
# Step 7: Launch dashboard
# ------------------------------------------------------------------
echo ""
echo -e "${BLUE}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Launching HarnessEval Dashboard          ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}  Run modes available:${NC}"

if [ "$HAS_KEY" = true ]; then
    echo -e "    ${GREEN}• Real mode (API) — uses configured API keys${NC}"
fi
if command -v ollama &>/dev/null; then
    echo -e "    ${GREEN}• Ollama mode — free, local LLM${NC}"
fi
echo -e "    ${GREEN}• Dry-run mode — synthetic data for testing${NC}"
echo ""
echo -e "  Dashboard will open at: ${BLUE}http://localhost:8501${NC}"
echo ""

streamlit run streamlit_app.py --server.port 8501
