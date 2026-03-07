"""
Download the embedding model for offline knowledge RAG.

Model: all-MiniLM-L6-v2 (ONNX format from Xenova/all-MiniLM-L6-v2)
Size:  ~80 MB (model) + ~0.7 MB (tokenizer)

Usage:
    python tools/download_embedding.py
"""

import sys
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────
REPO_ID = "Xenova/all-MiniLM-L6-v2"
MODEL_DIR = Path(__file__).parent.parent / "models" / "embedding" / "all-MiniLM-L6-v2"

FILES_TO_DOWNLOAD = [
    "onnx/model.onnx",
    "tokenizer.json",
    "config.json",
]


def main():
    try:
        from huggingface_hub import hf_hub_download
    except ImportError:
        print("❌ huggingface-hub not installed. Run: pip install huggingface-hub")
        sys.exit(1)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📦 Downloading embedding model: {REPO_ID}")
    print(f"   Target: {MODEL_DIR}\n")

    for filename in FILES_TO_DOWNLOAD:
        target = MODEL_DIR / filename
        if target.exists():
            size_mb = target.stat().st_size / (1024 * 1024)
            print(f"   ✅ {filename} already exists ({size_mb:.1f} MB)")
            continue

        print(f"   ⬇️  Downloading {filename} ...")
        try:
            hf_hub_download(
                repo_id=REPO_ID,
                filename=filename,
                local_dir=str(MODEL_DIR),
            )
            target = MODEL_DIR / filename
            if target.exists():
                size_mb = target.stat().st_size / (1024 * 1024)
                print(f"   ✅ {filename} ({size_mb:.1f} MB)")
            else:
                print(f"   ✅ {filename} downloaded")
        except Exception as e:
            print(f"   ❌ Failed to download {filename}: {e}")
            sys.exit(1)

    # Verify all files present
    print("\n🔍 Verifying files...")
    all_ok = True
    for filename in FILES_TO_DOWNLOAD:
        path = MODEL_DIR / filename
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"   ✅ {filename} ({size_mb:.1f} MB)")
        else:
            print(f"   ❌ Missing: {filename}")
            all_ok = False

    if all_ok:
        total_mb = sum(
            (MODEL_DIR / f).stat().st_size for f in FILES_TO_DOWNLOAD
        ) / (1024 * 1024)
        print(f"\n✅ Embedding model ready! Total size: {total_mb:.1f} MB")
        print(f"   Path: {MODEL_DIR}")
    else:
        print("\n❌ Some files are missing. Try running again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
