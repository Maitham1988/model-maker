#!/usr/bin/env python3
"""
Model Maker — Smart Model Downloader

Downloads GGUF models from the registry with:
  - Automatic device detection (RAM, storage, GPU)
  - Smart tier recommendation
  - Progress bar with speed + ETA
  - Resume interrupted downloads
  - SHA256 checksum verification
  - Interactive or CLI mode

Usage:
    python models/download.py                   # Interactive mode
    python models/download.py --tier standard   # Direct download
    python models/download.py --list            # List available models
    python models/download.py --check           # Check device compatibility
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

# ── Constants ─────────────────────────────────────────────────────────────────
REGISTRY_PATH = Path(__file__).parent / "registry.json"
MODELS_DIR = Path(__file__).parent
PROJECT_ROOT = Path(__file__).parent.parent

# ── ANSI Colors ───────────────────────────────────────────────────────────────
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


def _no_color():
    """Disable colors if terminal doesn't support them."""
    for attr in dir(C):
        if not attr.startswith("_"):
            setattr(C, attr, "")


if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    _no_color()


# ── Device Detection ──────────────────────────────────────────────────────────

def get_system_info() -> dict:
    """Detect system RAM, storage, OS, and GPU information."""
    info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "ram_gb": 0,
        "free_storage_gb": 0,
        "gpu": "none",
        "gpu_metal": False,
        "gpu_cuda": False,
    }

    # RAM detection
    try:
        if info["os"] == "Darwin":  # macOS
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                capture_output=True, text=True, timeout=5
            )
            info["ram_gb"] = int(result.stdout.strip()) / (1024 ** 3)
            # Apple Silicon has Metal GPU
            if platform.machine() == "arm64":
                info["gpu"] = "apple_silicon"
                info["gpu_metal"] = True

        elif info["os"] == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        kb = int(line.split()[1])
                        info["ram_gb"] = kb / (1024 ** 2)
                        break
            # Check for NVIDIA GPU
            try:
                subprocess.run(["nvidia-smi"], capture_output=True, timeout=5)
                info["gpu"] = "nvidia"
                info["gpu_cuda"] = True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

        elif info["os"] == "Windows":
            result = subprocess.run(
                ["wmic", "computersystem", "get", "totalphysicalmemory"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                info["ram_gb"] = int(lines[1].strip()) / (1024 ** 3)
            # Check for NVIDIA GPU
            try:
                subprocess.run(["nvidia-smi"], capture_output=True, timeout=5)
                info["gpu"] = "nvidia"
                info["gpu_cuda"] = True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

    except Exception:
        pass

    # Free storage detection
    try:
        usage = shutil.disk_usage(str(MODELS_DIR))
        info["free_storage_gb"] = usage.free / (1024 ** 3)
    except Exception:
        pass

    return info


def recommend_tier(system_info: dict) -> str:
    """Recommend model tier based on system capabilities."""
    ram = system_info["ram_gb"]
    storage = system_info["free_storage_gb"]

    if ram >= 16 and storage >= 12:
        return "premium"
    elif ram >= 8 and storage >= 6:
        return "standard"
    elif ram >= 4 and storage >= 4:
        return "lite"
    else:
        return "lite"  # Try lite even on low-end devices


# ── Registry ──────────────────────────────────────────────────────────────────

def load_registry() -> dict:
    """Load the model registry."""
    if not REGISTRY_PATH.exists():
        print(f"{C.RED}Error: Registry not found at {REGISTRY_PATH}{C.RESET}")
        sys.exit(1)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def get_model_by_tier(registry: dict, tier: str) -> dict | None:
    """Find model config by tier name."""
    for model in registry["models"]:
        if model["tier"] == tier:
            return model
    return None


# ── Download ──────────────────────────────────────────────────────────────────

def format_size(bytes_count: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_count < 1024:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024
    return f"{bytes_count:.1f} TB"


def format_time(seconds: float) -> str:
    """Format seconds as human-readable time."""
    if seconds < 60:
        return f"{seconds:.0f}s"
    elif seconds < 3600:
        return f"{seconds // 60:.0f}m {seconds % 60:.0f}s"
    else:
        return f"{seconds // 3600:.0f}h {(seconds % 3600) // 60:.0f}m"


def download_with_progress(url: str, dest: Path, expected_size: int = 0) -> bool:
    """Download a file with progress bar and resume support."""
    dest_tmp = dest.with_suffix(dest.suffix + ".downloading")

    # Resume support
    resume_pos = 0
    if dest_tmp.exists():
        resume_pos = dest_tmp.stat().st_size
        print(f"  {C.CYAN}Resuming from {format_size(resume_pos)}...{C.RESET}")

    # Create request with range header for resume
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "ModelMaker/1.0")
    if resume_pos > 0:
        req.add_header("Range", f"bytes={resume_pos}-")

    try:
        response = urllib.request.urlopen(req, timeout=30)
    except Exception as e:
        print(f"\n  {C.RED}Connection error: {e}{C.RESET}")
        print(f"  {C.YELLOW}Tip: Check your internet connection and try again.{C.RESET}")
        return False

    # Total size
    content_length = response.headers.get("Content-Length")
    if content_length:
        total_size = int(content_length) + resume_pos
    elif expected_size:
        total_size = expected_size
    else:
        total_size = 0

    # Download
    start_time = time.time()
    downloaded = resume_pos
    block_size = 1024 * 256  # 256 KB blocks

    mode = "ab" if resume_pos > 0 else "wb"
    try:
        with open(dest_tmp, mode) as f:
            while True:
                data = response.read(block_size)
                if not data:
                    break
                f.write(data)
                downloaded += len(data)

                # Progress bar
                elapsed = time.time() - start_time
                speed = (downloaded - resume_pos) / elapsed if elapsed > 0 else 0

                if total_size > 0:
                    pct = downloaded / total_size * 100
                    eta = (total_size - downloaded) / speed if speed > 0 else 0

                    bar_width = 30
                    filled = int(bar_width * downloaded / total_size)
                    bar = "█" * filled + "░" * (bar_width - filled)

                    print(
                        f"\r  {C.GREEN}{bar}{C.RESET} "
                        f"{pct:5.1f}% "
                        f"{format_size(downloaded)}/{format_size(total_size)} "
                        f"@ {format_size(speed)}/s "
                        f"ETA {format_time(eta)}   ",
                        end="",
                        flush=True,
                    )
                else:
                    print(
                        f"\r  {C.GREEN}Downloading{C.RESET} "
                        f"{format_size(downloaded)} "
                        f"@ {format_size(speed)}/s   ",
                        end="",
                        flush=True,
                    )

        print()  # Newline after progress bar

        # Move temp file to final destination
        dest_tmp.rename(dest)
        return True

    except KeyboardInterrupt:
        print(f"\n\n  {C.YELLOW}Download paused. Run again to resume.{C.RESET}")
        return False
    except Exception as e:
        print(f"\n  {C.RED}Download error: {e}{C.RESET}")
        print(f"  {C.YELLOW}Run again to resume from where it stopped.{C.RESET}")
        return False


def verify_checksum(filepath: Path, expected_sha256: str) -> bool:
    """Verify file SHA256 checksum."""
    if not expected_sha256:
        return True  # No checksum to verify

    print(f"  {C.CYAN}Verifying checksum...{C.RESET}", end="", flush=True)
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(1024 * 1024)  # 1 MB blocks
            if not data:
                break
            sha256.update(data)

    actual = sha256.hexdigest()
    if actual == expected_sha256:
        print(f" {C.GREEN}✓ OK{C.RESET}")
        return True
    else:
        print(f" {C.RED}✗ MISMATCH{C.RESET}")
        print(f"  Expected: {expected_sha256}")
        print(f"  Got:      {actual}")
        return False


# ── CLI Interface ─────────────────────────────────────────────────────────────

def print_banner():
    """Print the Model Maker banner."""
    print(f"""
{C.BOLD}{C.CYAN}╔══════════════════════════════════════════════╗
║       🏥 Model Maker — Model Downloader      ║
║    Offline AI for Emergency & Survival        ║
╚══════════════════════════════════════════════╝{C.RESET}
""")


def print_system_info(info: dict):
    """Display detected system information."""
    print(f"{C.BOLD}📊 Your Device:{C.RESET}")
    print(f"  OS:      {info['os']} ({info['machine']})")
    print(f"  RAM:     {info['ram_gb']:.1f} GB")
    print(f"  Storage: {info['free_storage_gb']:.1f} GB free")
    gpu_str = {
        "apple_silicon": "Apple Silicon (Metal ⚡)",
        "nvidia": "NVIDIA (CUDA ⚡)",
        "none": "CPU only",
    }.get(info["gpu"], info["gpu"])
    print(f"  GPU:     {gpu_str}")
    print()


def print_model_table(registry: dict, recommended_tier: str = ""):
    """Display available models as a table."""
    print(f"{C.BOLD}📦 Available Models:{C.RESET}\n")

    tier_colors = {"lite": C.YELLOW, "standard": C.GREEN, "premium": C.MAGENTA}
    tier_icons = {"lite": "🟡", "standard": "🟢", "premium": "🟣"}

    for model in registry["models"]:
        tier = model["tier"]
        color = tier_colors.get(tier, C.WHITE)
        icon = tier_icons.get(tier, "•")
        stars = "⭐" * model["quality_stars"]
        rec = f" {C.BOLD}{C.GREEN}← RECOMMENDED{C.RESET}" if tier == recommended_tier else ""

        print(f"  {icon} {color}{C.BOLD}{model['name']}{C.RESET} ({model['tier']}){rec}")
        print(f"     Model:    {model['base_model']} ({model['quantization']})")
        print(f"     Size:     {model['size_display']}")
        print(f"     Quality:  {stars}")
        print(f"     RAM:      {model['requirements']['min_ram_gb']}GB min / {model['requirements']['recommended_ram_gb']}GB optimal")
        print(f"     About:    {model['description']['en']}")
        print()


def check_existing_models(registry: dict) -> list[str]:
    """Check which models are already downloaded."""
    existing = []
    for model in registry["models"]:
        model_path = MODELS_DIR / model["file"]
        if model_path.exists():
            size = model_path.stat().st_size
            expected = model["size_bytes"]
            # Allow 5% tolerance for size check
            if abs(size - expected) / expected < 0.05 if expected > 0 else True:
                existing.append(model["tier"])
    return existing


def update_config(model: dict):
    """Update app config.json with the downloaded model path."""
    config_path = PROJECT_ROOT / "app" / "config.json"
    template_path = PROJECT_ROOT / "app" / "config_template.json"

    # Load existing config or template
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
    elif template_path.exists():
        with open(template_path) as f:
            config = json.load(f)
    else:
        config = {}

    # Update model path
    model_path = str(MODELS_DIR / model["file"])
    config["model_path"] = model_path
    config["chat_format"] = model.get("chat_format", "chatml")

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"  {C.GREEN}✓ Config updated: {config_path}{C.RESET}")


def interactive_mode():
    """Run the interactive model selection and download."""
    print_banner()

    # Detect system
    print(f"{C.DIM}Detecting your device...{C.RESET}\n")
    info = get_system_info()
    print_system_info(info)

    # Load registry
    registry = load_registry()
    recommended = recommend_tier(info)

    # Check existing models
    existing = check_existing_models(registry)
    if existing:
        print(f"{C.GREEN}✓ Already downloaded: {', '.join(existing)}{C.RESET}\n")

    # Show models
    print_model_table(registry, recommended)

    # Ask user
    print(f"{C.BOLD}Choose a model to download:{C.RESET}")
    print("  1) Lite     (2.0 GB) — Basic devices, fast")
    print(f"  2) Standard (4.4 GB) — Most users {C.GREEN}★ Recommended{C.RESET}")
    print("  3) Premium  (8.5 GB) — Best quality, powerful devices")
    print("  q) Quit")
    print()

    tier_map = {"1": "lite", "2": "standard", "3": "premium"}

    try:
        choice = input(f"{C.BOLD}  Your choice [1-3]: {C.RESET}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C.YELLOW}Cancelled.{C.RESET}")
        return

    if choice == "q":
        return

    tier = tier_map.get(choice)
    if not tier:
        print(f"{C.RED}Invalid choice. Use 1, 2, or 3.{C.RESET}")
        return

    model = get_model_by_tier(registry, tier)
    if not model:
        print(f"{C.RED}Model not found in registry.{C.RESET}")
        return

    # Check compatibility
    ram = info["ram_gb"]
    min_ram = model["requirements"]["min_ram_gb"]
    if ram > 0 and ram < min_ram:
        print(f"\n{C.YELLOW}⚠ Warning: Your device has {ram:.0f}GB RAM but this model needs {min_ram}GB minimum.{C.RESET}")
        print(f"{C.YELLOW}  It may run slowly or crash. Consider a smaller model.{C.RESET}")
        try:
            cont = input("  Continue anyway? [y/N]: ").strip().lower()
            if cont != "y":
                return
        except (KeyboardInterrupt, EOFError):
            return

    # Check storage
    storage = info["free_storage_gb"]
    required_gb = model["size_bytes"] / (1024 ** 3) * 1.1  # 10% buffer
    if storage > 0 and storage < required_gb:
        print(f"\n{C.RED}✗ Not enough storage. Need {required_gb:.1f}GB free, have {storage:.1f}GB.{C.RESET}")
        print("  Free up some space and try again.")
        return

    # Check if already downloaded
    dest = MODELS_DIR / model["file"]
    if dest.exists():
        print(f"\n{C.GREEN}✓ {model['name']} already downloaded!{C.RESET}")
        print(f"  Path: {dest}")
        try:
            redownload = input("  Re-download? [y/N]: ").strip().lower()
            if redownload != "y":
                update_config(model)
                return
            dest.unlink()
        except (KeyboardInterrupt, EOFError):
            return

    # Download
    url = model["download_urls"][0]
    print(f"\n{C.BOLD}📥 Downloading {model['name']} ({model['size_display']})...{C.RESET}")
    print(f"  From: {url}\n")

    success = download_with_progress(url, dest, model["size_bytes"])

    if success:
        # Verify checksum
        if model.get("sha256"):
            if not verify_checksum(dest, model["sha256"]):
                print(f"{C.RED}Checksum verification failed! The file may be corrupt.{C.RESET}")
                print(f"Delete {dest} and try again.")
                return

        # Update config
        update_config(model)

        print(f"\n{C.GREEN}{C.BOLD}✅ {model['name']} is ready!{C.RESET}")
        print(f"  {C.DIM}Run the app:  cd app && python run.py{C.RESET}")
    else:
        print(f"\n{C.YELLOW}Download incomplete. Run this script again to resume.{C.RESET}")


def cli_mode():
    """Handle command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Model Maker — Download AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python models/download.py                    Interactive mode
  python models/download.py --tier standard    Download standard model
  python models/download.py --list             List available models
  python models/download.py --check            Check device compatibility
  python models/download.py --info standard    Model details
        """,
    )
    parser.add_argument("--tier", choices=["lite", "standard", "premium"],
                        help="Download a specific model tier")
    parser.add_argument("--list", action="store_true",
                        help="List available models")
    parser.add_argument("--check", action="store_true",
                        help="Check device and recommend model")
    parser.add_argument("--info", choices=["lite", "standard", "premium"],
                        help="Show details for a model tier")
    parser.add_argument("--no-config", action="store_true",
                        help="Don't update app config after download")

    args = parser.parse_args()

    if args.list:
        registry = load_registry()
        info = get_system_info()
        recommended = recommend_tier(info)
        print_banner()
        print_model_table(registry, recommended)
        existing = check_existing_models(registry)
        if existing:
            print(f"{C.GREEN}✓ Downloaded: {', '.join(existing)}{C.RESET}")
        return

    if args.check:
        print_banner()
        info = get_system_info()
        print_system_info(info)
        recommended = recommend_tier(info)
        print(f"{C.BOLD}Recommended tier: {C.GREEN}{recommended.upper()}{C.RESET}\n")
        return

    if args.info:
        registry = load_registry()
        model = get_model_by_tier(registry, args.info)
        if model:
            print(f"\n{C.BOLD}{model['name']}{C.RESET}")
            print(f"  Base model:    {model['base_model']}")
            print(f"  Quantization:  {model['quantization']}")
            print(f"  File:          {model['file']}")
            print(f"  Size:          {model['size_display']}")
            print(f"  RAM required:  {model['requirements']['min_ram_gb']}GB min")
            print(f"  RAM optimal:   {model['requirements']['recommended_ram_gb']}GB")
            print(f"  Storage:       {model['requirements']['min_storage_gb']}GB min")
            print(f"  Languages:     {model['languages']}")
            print(f"  Quality:       {'⭐' * model['quality_stars']}")
            print(f"  URL:           {model['download_urls'][0]}")
        return

    if args.tier:
        registry = load_registry()
        model = get_model_by_tier(registry, args.tier)
        if not model:
            print(f"{C.RED}Model tier '{args.tier}' not found.{C.RESET}")
            sys.exit(1)

        info = get_system_info()
        print_banner()
        print_system_info(info)

        dest = MODELS_DIR / model["file"]
        if dest.exists():
            print(f"{C.GREEN}✓ {model['name']} already downloaded at {dest}{C.RESET}")
            if not args.no_config:
                update_config(model)
            return

        url = model["download_urls"][0]
        print(f"{C.BOLD}📥 Downloading {model['name']} ({model['size_display']})...{C.RESET}")
        print(f"  From: {url}\n")

        success = download_with_progress(url, dest, model["size_bytes"])
        if success:
            if model.get("sha256"):
                verify_checksum(dest, model["sha256"])
            if not args.no_config:
                update_config(model)
            print(f"\n{C.GREEN}{C.BOLD}✅ {model['name']} ready!{C.RESET}")
        else:
            print(f"\n{C.YELLOW}Run again to resume.{C.RESET}")
            sys.exit(1)
        return

    # No args → interactive
    interactive_mode()


# ── Entry ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive_mode()
