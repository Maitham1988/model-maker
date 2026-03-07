#!/usr/bin/env python3
"""
Download Model — Downloads GGUF models from Hugging Face.
No account or API key needed for public models.

Usage:
    python tools/download_model.py                    # Default: Qwen2.5-7B
    python tools/download_model.py --model qwen2.5-7b
    python tools/download_model.py --model qwen2.5-14b
    python tools/download_model.py --list             # Show available models
"""

import argparse
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("❌ huggingface_hub not installed. Run: pip install huggingface-hub")
    exit(1)

PROJECT_ROOT = Path(__file__).parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

# Available models (repo_id, filename, description)
MODELS = {
    "qwen2.5-7b": {
        "repo": "bartowski/Qwen2.5-7B-Instruct-GGUF",
        "file": "Qwen2.5-7B-Instruct-Q4_K_M.gguf",
        "size": "4.7 GB",
        "ram": "8 GB",
        "desc": "Standard tier — Best balance of speed + quality + Arabic",
    },
    "qwen2.5-14b": {
        "repo": "bartowski/Qwen2.5-14B-Instruct-GGUF",
        "file": "Qwen2.5-14B-Instruct-Q4_K_M.gguf",
        "size": "8.9 GB",
        "ram": "16 GB",
        "desc": "Premium tier — Better quality, needs more RAM",
    },
    "qwen2.5-3b": {
        "repo": "bartowski/Qwen2.5-3B-Instruct-GGUF",
        "file": "Qwen2.5-3B-Instruct-Q4_K_M.gguf",
        "size": "2.1 GB",
        "ram": "4 GB",
        "desc": "Budget tier — Fast, works on low-end devices",
    },
}


def list_models():
    print("\n📦 Available Models:\n")
    for name, info in MODELS.items():
        print(f"  {name}")
        print(f"    Repo: {info['repo']}")
        print(f"    File: {info['file']}")
        print(f"    Size: {info['size']} | RAM: {info['ram']}")
        print(f"    {info['desc']}")
        print()


def download_model(model_name: str):
    if model_name not in MODELS:
        print(f"❌ Unknown model: {model_name}")
        list_models()
        return

    info = MODELS[model_name]
    target = MODELS_DIR / info["file"]

    if target.exists():
        print(f"✅ Model already exists: {target}")
        print(f"   Size: {target.stat().st_size / 1e9:.1f} GB")
        return

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"📥 Downloading: {info['file']}")
    print(f"   From: {info['repo']}")
    print(f"   Size: {info['size']}")
    print(f"   To: {target}")
    print("   This may take a while...\n")

    downloaded = hf_hub_download(
        repo_id=info["repo"],
        filename=info["file"],
        local_dir=str(MODELS_DIR),
        local_dir_use_symlinks=False,
    )

    print(f"\n✅ Download complete: {downloaded}")
    print(f"   Size: {Path(downloaded).stat().st_size / 1e9:.1f} GB")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download GGUF models")
    parser.add_argument("--model", default="qwen2.5-7b", help="Model to download")
    parser.add_argument("--list", action="store_true", help="List available models")
    args = parser.parse_args()

    if args.list:
        list_models()
    else:
        download_model(args.model)
