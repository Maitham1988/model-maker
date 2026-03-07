#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Model Maker — macOS Installer
#  Double-click this file to install the offline AI assistant.
#  
#  What happens:
#    1. Downloads Model Maker from GitHub
#    2. Auto-detects your Mac and picks the best AI model
#    3. Creates a Desktop launcher for easy access
#
#  https://github.com/Maitham1988/model-maker
# ═══════════════════════════════════════════════════════════════

# Move to user's home directory (not wherever the download landed)
cd "$HOME"

clear
echo ""
echo "  ╔═══════════════════════════════════════════════════╗"
echo "  ║                                                   ║"
echo "  ║     🤖  Model Maker — Offline AI Installer        ║"
echo "  ║                                                   ║"
echo "  ║     This will install Model Maker on your Mac.    ║"
echo "  ║     No technical knowledge needed.                ║"
echo "  ║                                                   ║"
echo "  ╚═══════════════════════════════════════════════════╝"
echo ""
echo "  What will be installed:"
echo "    • Model Maker application (~50 MB)"
echo "    • AI model for your device (~2-8 GB)"
echo "    • Desktop launcher for easy access"
echo ""
echo "  Installation folder: ~/model-maker"
echo ""

# ── Ask for confirmation ──────────────────────────────────────
read -p "  Press Enter to start installation (or Ctrl+C to cancel)... " _

echo ""
echo "  Downloading installer..."
echo ""

# ── Download and run the full installer ───────────────────────
curl -fsSL https://raw.githubusercontent.com/Maitham1988/model-maker/main/scripts/install-mac.sh | bash

# ── Keep window open so user can see the result ───────────────
echo ""
echo "  ────────────────────────────────────────────────────"
echo "  Installation complete. You can close this window."
echo "  To start Model Maker later, double-click"
echo "  'Model Maker' on your Desktop."
echo "  ────────────────────────────────────────────────────"
echo ""
read -p "  Press Enter to close... " _
