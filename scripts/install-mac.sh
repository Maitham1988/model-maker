#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Model Maker — One-Click macOS Installer
#  Downloads, installs, and launches the offline AI assistant.
#  Works on macOS 12+ with Apple Silicon or Intel.
#
#  Usage:
#    curl -fsSL https://raw.githubusercontent.com/Maitham1988/model-maker/main/scripts/install-mac.sh | bash
#
#  Or download and run:
#    chmod +x install-mac.sh && ./install-mac.sh
# ═══════════════════════════════════════════════════════════════

set -e

# ── Colors ──────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ── Config ──────────────────────────────────────────────────
INSTALL_DIR="$HOME/model-maker"
REPO_URL="https://github.com/Maitham1988/model-maker.git"
VENV_DIR="$INSTALL_DIR/.venv"

# Model URLs (direct HuggingFace downloads)
MODEL_3B_URL="https://huggingface.co/bartowski/Qwen2.5-3B-Instruct-GGUF/resolve/main/Qwen2.5-3B-Instruct-Q4_K_M.gguf"
MODEL_7B_URL="https://huggingface.co/bartowski/Qwen2.5-7B-Instruct-GGUF/resolve/main/Qwen2.5-7B-Instruct-Q4_K_M.gguf"
MODEL_14B_URL="https://huggingface.co/bartowski/Qwen2.5-14B-Instruct-GGUF/resolve/main/Qwen2.5-14B-Instruct-Q4_K_M.gguf"

MODEL_3B_FILE="Qwen2.5-3B-Instruct-Q4_K_M.gguf"
MODEL_7B_FILE="Qwen2.5-7B-Instruct-Q4_K_M.gguf"
MODEL_14B_FILE="Qwen2.5-14B-Instruct-Q4_K_M.gguf"

# ── Functions ───────────────────────────────────────────────
print_header() {
    echo ""
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  Model Maker — Offline AI Installer (macOS)${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════${NC}"
    echo ""
}

print_step() {
    echo -e "${BOLD}${BLUE}[$1/6]${NC} $2"
}

print_ok() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_warn() {
    echo -e "  ${YELLOW}⚠${NC} $1"
}

print_fail() {
    echo -e "  ${RED}✗${NC} $1"
    exit 1
}

get_ram_gb() {
    # Returns total RAM in GB (integer)
    sysctl -n hw.memsize 2>/dev/null | awk '{printf "%d", $1/1073741824}'
}

get_arch() {
    uname -m
}

pick_model() {
    local ram_gb=$(get_ram_gb)
    if [ "$ram_gb" -ge 16 ]; then
        MODEL_TIER="premium"
        MODEL_URL="$MODEL_14B_URL"
        MODEL_FILE="$MODEL_14B_FILE"
        MODEL_SIZE="8.5 GB"
        MODEL_NAME="Qwen2.5-14B (Premium)"
    elif [ "$ram_gb" -ge 8 ]; then
        MODEL_TIER="standard"
        MODEL_URL="$MODEL_7B_URL"
        MODEL_FILE="$MODEL_7B_FILE"
        MODEL_SIZE="4.4 GB"
        MODEL_NAME="Qwen2.5-7B (Standard — Recommended)"
    else
        MODEL_TIER="lite"
        MODEL_URL="$MODEL_3B_URL"
        MODEL_FILE="$MODEL_3B_FILE"
        MODEL_SIZE="2.0 GB"
        MODEL_NAME="Qwen2.5-3B (Lite)"
    fi
}

# ── Main ────────────────────────────────────────────────────
print_header

RAM_GB=$(get_ram_gb)
ARCH=$(get_arch)
echo -e "  Device: macOS $(sw_vers -productVersion 2>/dev/null || echo 'unknown') — ${ARCH}"
echo -e "  RAM: ${RAM_GB} GB"
echo ""

# ── Step 1: Check Python ────────────────────────────────────
print_step 1 "Checking Python..."

PYTHON_CMD=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        PY_VERSION=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
        PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
        if [ "$PY_MAJOR" -ge 3 ] && [ "$PY_MINOR" -ge 9 ]; then
            PYTHON_CMD="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    print_warn "Python 3.9+ not found. Installing via Xcode Command Line Tools..."
    xcode-select --install 2>/dev/null || true
    echo ""
    echo -e "${YELLOW}  A popup may appear asking to install Xcode Command Line Tools.${NC}"
    echo -e "${YELLOW}  Click 'Install', wait for it to finish, then run this script again.${NC}"
    echo ""
    exit 1
fi

print_ok "Python: $($PYTHON_CMD --version)"

# ── Step 2: Download Model Maker ────────────────────────────
print_step 2 "Downloading Model Maker..."

if [ -d "$INSTALL_DIR/.git" ]; then
    print_ok "Already downloaded at $INSTALL_DIR"
    cd "$INSTALL_DIR"
    git pull --quiet origin main 2>/dev/null || true
else
    if [ -d "$INSTALL_DIR" ]; then
        print_warn "Directory exists but isn't a git repo. Backing up..."
        mv "$INSTALL_DIR" "$INSTALL_DIR.backup.$(date +%s)"
    fi
    git clone --depth 1 "$REPO_URL" "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    print_ok "Downloaded to $INSTALL_DIR"
fi

# ── Step 3: Set up Python environment ───────────────────────
print_step 3 "Setting up Python environment..."

if [ ! -d "$VENV_DIR" ]; then
    "$PYTHON_CMD" -m venv "$VENV_DIR"
    print_ok "Virtual environment created"
else
    print_ok "Virtual environment already exists"
fi

source "$VENV_DIR/bin/activate"

# Upgrade pip silently
pip install --upgrade pip --quiet 2>/dev/null

# Install dependencies
echo -e "  ${CYAN}Installing dependencies (this may take a few minutes)...${NC}"
pip install -r requirements.txt --quiet 2>/dev/null
print_ok "All dependencies installed"

# ── Step 4: Download AI Model ───────────────────────────────
print_step 4 "Downloading AI model..."

pick_model

MODEL_PATH="$INSTALL_DIR/models/$MODEL_FILE"

if [ -f "$MODEL_PATH" ]; then
    EXISTING_SIZE=$(stat -f%z "$MODEL_PATH" 2>/dev/null || echo "0")
    if [ "$EXISTING_SIZE" -gt 1000000000 ]; then
        print_ok "Model already downloaded: $MODEL_NAME"
    else
        print_warn "Incomplete download detected. Re-downloading..."
        rm -f "$MODEL_PATH"
    fi
fi

if [ ! -f "$MODEL_PATH" ] || [ "$(stat -f%z "$MODEL_PATH" 2>/dev/null || echo 0)" -lt 1000000000 ]; then
    mkdir -p "$INSTALL_DIR/models"
    echo ""
    echo -e "  ${BOLD}Downloading: $MODEL_NAME${NC}"
    echo -e "  Size: $MODEL_SIZE"
    echo -e "  This is a one-time download. It may take 10-30 minutes."
    echo ""
    
    # Use curl with progress bar
    curl -L --progress-bar -o "$MODEL_PATH" "$MODEL_URL"
    
    # Verify download
    DOWNLOADED_SIZE=$(stat -f%z "$MODEL_PATH" 2>/dev/null || echo "0")
    if [ "$DOWNLOADED_SIZE" -lt 1000000000 ]; then
        print_fail "Download failed or incomplete. Please check your internet and try again."
    fi
    
    echo ""
    print_ok "Model downloaded successfully ($(echo "scale=1; $DOWNLOADED_SIZE/1073741824" | bc) GB)"
fi

# ── Step 5: Create config ──────────────────────────────────
print_step 5 "Configuring..."

CONFIG_FILE="$INSTALL_DIR/app/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << JSONEOF
{
  "customer_name": "User",
  "customer_id": "local",
  "model_path": "../models/$MODEL_FILE",
  "chat_format": "auto",
  "context_length": 4096,
  "max_tokens": 2048,
  "temperature": 0.7,
  "top_p": 0.9,
  "repeat_penalty": 1.1,
  "gpu_layers": 0,
  "max_history_messages": 20,
  "system_prompt": "",
  "setup_completed": false
}
JSONEOF
    print_ok "Configuration created"
else
    print_ok "Configuration already exists"
fi

# ── Step 6: Create launcher shortcut ───────────────────────
print_step 6 "Creating launcher..."

LAUNCHER="$INSTALL_DIR/Start Model Maker.command"
cat > "$LAUNCHER" << 'LAUNCHEOF'
#!/bin/bash
# Model Maker — Quick Launcher
cd "$(dirname "$0")"
source .venv/bin/activate
echo ""
echo "🤖  Starting Model Maker..."
echo "    Browser will open automatically."
echo "    Press Ctrl+C to stop."
echo ""
python app/run.py
LAUNCHEOF
chmod +x "$LAUNCHER"

# Also create a Desktop shortcut
DESKTOP_LAUNCHER="$HOME/Desktop/Model Maker.command"
cat > "$DESKTOP_LAUNCHER" << DESKEOF
#!/bin/bash
# Model Maker — Desktop Launcher
cd "$INSTALL_DIR"
source .venv/bin/activate
python app/run.py
DESKEOF
chmod +x "$DESKTOP_LAUNCHER"

print_ok "Launcher created on Desktop"

# ── Done! ───────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${GREEN}  ✓ Installation Complete!${NC}"
echo -e "${BOLD}${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""
echo -e "  ${BOLD}Model:${NC}    $MODEL_NAME"
echo -e "  ${BOLD}Location:${NC} $INSTALL_DIR"
echo -e "  ${BOLD}RAM:${NC}      ${RAM_GB} GB"
echo ""
echo -e "  ${BOLD}To start:${NC}"
echo -e "    Double-click ${CYAN}\"Model Maker\"${NC} on your Desktop"
echo -e "    Or run: ${CYAN}cd ~/model-maker && source .venv/bin/activate && python app/run.py${NC}"
echo ""

# ── Auto-launch ─────────────────────────────────────────────
echo -e "  ${BOLD}Launching now...${NC}"
echo ""
python app/run.py
