#!/usr/bin/env bash
# ─── Model Maker — One-Line Installer ────────────────────────────
# Usage: curl -fsSL https://raw.githubusercontent.com/Maitham1988/model-maker/main/scripts/install.sh | bash
#
# What this does:
#   1. Clones the repository
#   2. Creates Python virtual environment
#   3. Installs dependencies
#   4. Downloads the recommended AI model
#   5. Starts the app
#
# Requirements: Python 3.11+, git, 8GB+ RAM, 6GB+ free disk space
# ──────────────────────────────────────────────────────────────────

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${BLUE}ℹ${NC}  $1"; }
ok()    { echo -e "${GREEN}✅${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠️${NC}  $1"; }
fail()  { echo -e "${RED}❌${NC} $1"; exit 1; }

echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       Model Maker — Quick Installer      ║${NC}"
echo -e "${BOLD}║   Offline AI for Emergency & Survival    ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""

# ── Check Prerequisites ──────────────────────────────────────────

# Check Python
if command -v python3 &>/dev/null; then
    PYTHON=python3
elif command -v python &>/dev/null; then
    PYTHON=python
else
    fail "Python not found. Install Python 3.11+ from https://python.org"
fi

PY_VERSION=$($PYTHON -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
PY_MAJOR=$($PYTHON -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$($PYTHON -c 'import sys; print(sys.version_info.minor)')

if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]); then
    fail "Python $PY_VERSION found, but 3.11+ is required"
fi
ok "Python $PY_VERSION"

# Check git
if ! command -v git &>/dev/null; then
    fail "git not found. Install git from https://git-scm.com"
fi
ok "git $(git --version | cut -d' ' -f3)"

# Check disk space (need ~6GB)
if command -v df &>/dev/null; then
    FREE_GB=$(df -BG . 2>/dev/null | tail -1 | awk '{print $4}' | tr -d 'G' || echo "999")
    if [ "${FREE_GB:-999}" -lt 6 ] 2>/dev/null; then
        warn "Low disk space: ${FREE_GB}GB free. Recommend 6GB+"
    fi
fi

# ── Clone Repository ─────────────────────────────────────────────

INSTALL_DIR="${HOME}/model-maker"

if [ -d "$INSTALL_DIR" ]; then
    info "Found existing installation at $INSTALL_DIR"
    cd "$INSTALL_DIR"
    git pull --quiet 2>/dev/null || true
    ok "Updated existing installation"
else
    info "Cloning Model Maker..."
    git clone --depth 1 https://github.com/Maitham1988/model-maker.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    ok "Cloned to $INSTALL_DIR"
fi

# ── Create Virtual Environment ───────────────────────────────────

if [ ! -d ".venv" ]; then
    info "Creating Python virtual environment..."
    $PYTHON -m venv .venv
    ok "Virtual environment created"
fi

# Activate
source .venv/bin/activate

# ── Install Dependencies ─────────────────────────────────────────

info "Installing dependencies (this may take a few minutes)..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
ok "Dependencies installed"

# ── Download Model ───────────────────────────────────────────────

info "Detecting your hardware..."
echo ""

# Run the smart downloader in interactive mode
python models/download.py

echo ""
ok "Model ready"

# ── Copy Config ──────────────────────────────────────────────────

if [ ! -f "app/config.json" ]; then
    cp app/config_template.json app/config.json
    ok "Config created"
fi

# ── Done! ────────────────────────────────────────────────────────

echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║          Installation Complete!          ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${BOLD}To start Model Maker:${NC}"
echo ""
echo -e "    cd $INSTALL_DIR"
echo -e "    source .venv/bin/activate"
echo -e "    cd app && python run.py"
echo ""
echo -e "  Then open ${BLUE}http://127.0.0.1:8000${NC} in your browser."
echo ""
echo -e "  ${BOLD}Or use Make:${NC} cd $INSTALL_DIR && make run"
echo ""

# Ask if user wants to start now
read -p "Start Model Maker now? [Y/n] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    cd app
    $PYTHON run.py
fi
