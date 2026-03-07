#!/bin/bash
# ══════════════════════════════════════════════════════════════
#  Model Maker — First-Time Setup
#  Creates virtual environment, installs dependencies,
#  downloads embedding model, and optionally downloads LLM.
# ══════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Colors
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
CYAN='\033[0;96m'
BOLD='\033[1m'
RESET='\033[0m'

echo -e "${BOLD}${CYAN}"
echo "╔══════════════════════════════════════════════╗"
echo "║       🏥 Model Maker — Setup                ║"
echo "║    Offline AI for Emergency & Survival       ║"
echo "╚══════════════════════════════════════════════╝"
echo -e "${RESET}"

# ── Check Python ──────────────────────────────────────────────
echo -e "${BOLD}1/4 Checking Python...${RESET}"
if command -v python3 &>/dev/null; then
    PYTHON=python3
    PY_VERSION=$($PYTHON --version 2>&1)
    echo -e "  ${GREEN}✓ Found: $PY_VERSION${RESET}"
elif command -v python &>/dev/null; then
    PYTHON=python
    PY_VERSION=$($PYTHON --version 2>&1)
    echo -e "  ${GREEN}✓ Found: $PY_VERSION${RESET}"
else
    echo -e "  ${RED}✗ Python not found!${RESET}"
    echo -e "  Install Python 3.11+ from: ${CYAN}https://python.org${RESET}"
    exit 1
fi

# Check version >= 3.11
PY_MAJOR=$($PYTHON -c "import sys; print(sys.version_info.major)")
PY_MINOR=$($PYTHON -c "import sys; print(sys.version_info.minor)")
if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]); then
    echo -e "  ${YELLOW}⚠ Python 3.11+ recommended (found $PY_MAJOR.$PY_MINOR)${RESET}"
fi

# ── Create Virtual Environment ────────────────────────────────
echo -e "\n${BOLD}2/4 Setting up virtual environment...${RESET}"
if [ -d ".venv" ]; then
    echo -e "  ${GREEN}✓ Virtual environment exists${RESET}"
else
    echo -e "  ${CYAN}Creating .venv...${RESET}"
    $PYTHON -m venv .venv
    echo -e "  ${GREEN}✓ Virtual environment created${RESET}"
fi

# Activate
source .venv/bin/activate

# ── Install Dependencies ──────────────────────────────────────
echo -e "\n${BOLD}3/4 Installing dependencies...${RESET}"
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "  ${GREEN}✓ All dependencies installed${RESET}"

# ── Download Model ────────────────────────────────────────────
echo -e "\n${BOLD}4/4 AI Model${RESET}"

# Check if any GGUF model exists
if ls models/*.gguf 2>/dev/null 1>&2; then
    echo -e "  ${GREEN}✓ AI model found${RESET}"
    echo -e "  $(ls models/*.gguf | head -1)"
else
    echo -e "  ${YELLOW}No AI model found.${RESET}"
    echo ""
    read -p "  Download an AI model now? [Y/n] " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        python models/download.py
    else
        echo -e "  ${CYAN}You can download later: python models/download.py${RESET}"
    fi
fi

# ── Done ──────────────────────────────────────────────────────
echo -e "\n${GREEN}${BOLD}✅ Setup complete!${RESET}\n"
echo -e "  To start Model Maker:"
echo -e "  ${CYAN}source .venv/bin/activate${RESET}"
echo -e "  ${CYAN}cd app && python run.py${RESET}"
echo ""
