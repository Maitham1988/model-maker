#!/usr/bin/env python3
"""
Model Maker — Fine-Tuning Pipeline
====================================
Fine-tune Qwen2.5-7B-Instruct with QLoRA on Apple Silicon using MLX.

This script:
1. Converts existing GGUF → MLX safetensors (or downloads HF weights)
2. Runs QLoRA fine-tuning on the medical Q&A dataset
3. Fuses LoRA adapters into the base model
4. Converts back to GGUF for deployment with llama-cpp-python

Requirements:
    pip install mlx-lm

Usage:
    # Step 1: Download base model (one time)
    python tools/finetune.py download

    # Step 2: Prepare dataset (splits into train/val/test)
    python tools/finetune.py prepare

    # Step 3: Fine-tune
    python tools/finetune.py train

    # Step 4: Test the fine-tuned model
    python tools/finetune.py test

    # Step 5: Fuse adapters into base model
    python tools/finetune.py fuse

    # Step 6: Convert to GGUF for deployment
    python tools/finetune.py convert

    # Full pipeline
    python tools/finetune.py all
"""

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = ROOT / "training" / "medical_qa_dataset.jsonl"
TRAIN_DIR = ROOT / "training" / "splits"
BASE_MODEL_HF = "Qwen/Qwen2.5-7B-Instruct"
BASE_MODEL_DIR = ROOT / "models" / "mlx" / "Qwen2.5-7B-Instruct"
ADAPTER_DIR = ROOT / "models" / "adapters" / "medical-v1"
FUSED_DIR = ROOT / "models" / "mlx" / "Qwen2.5-7B-Medical-v1"
GGUF_OUTPUT = ROOT / "models" / "Qwen2.5-7B-Medical-v1-Q4_K_M.gguf"

# ─── Fine-tuning hyperparameters ─────────────────────────────────────────────
FINETUNE_CONFIG = {
    "model": str(BASE_MODEL_DIR),
    "train": True,
    "data": str(TRAIN_DIR),
    "seed": 42,
    "lora_layers": 16,
    "lora_rank": 16,            # Higher rank = more capacity, more memory
    "batch_size": 1,             # 1 for 7B on most Macs; increase if you have 64GB+
    "iters": 1000,               # Number of training iterations
    "val_batches": 5,
    "learning_rate": 1e-5,
    "steps_per_report": 10,
    "steps_per_eval": 100,
    "adapter_path": str(ADAPTER_DIR),
    "max_seq_length": 2048,
    "grad_checkpoint": True,     # Saves memory at cost of speed
}


def check_mlx():
    """Ensure mlx-lm is installed."""
    try:
        import mlx_lm  # noqa: F401
        print("✓ mlx-lm is installed")
        return True
    except ImportError:
        print("✗ mlx-lm not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mlx-lm"])
        print("✓ mlx-lm installed successfully")
        return True


def cmd_download():
    """Download and convert Qwen2.5-7B-Instruct to MLX format."""
    check_mlx()
    if BASE_MODEL_DIR.exists():
        print(f"✓ Base model already exists at {BASE_MODEL_DIR}")
        return

    print(f"Downloading {BASE_MODEL_HF} in MLX format...")
    print("This will download ~14GB. Make sure you have space and internet.")

    from mlx_lm import convert

    convert(
        BASE_MODEL_HF,
        mlx_path=str(BASE_MODEL_DIR),
        quantize=False,  # Keep full precision for fine-tuning
    )
    print(f"✓ Model saved to {BASE_MODEL_DIR}")


def cmd_prepare():
    """Split dataset into train/valid/test for mlx-lm."""
    if not DATASET_PATH.exists():
        print(f"✗ Dataset not found at {DATASET_PATH}")
        sys.exit(1)

    with open(DATASET_PATH) as f:
        data = [json.loads(line) for line in f if line.strip()]

    random.seed(42)
    random.shuffle(data)

    # Split: 80% train, 10% valid, 10% test
    n = len(data)
    train_end = int(n * 0.8)
    val_end = int(n * 0.9)

    splits = {
        "train": data[:train_end],
        "valid": data[train_end:val_end],
        "test": data[val_end:],
    }

    TRAIN_DIR.mkdir(parents=True, exist_ok=True)

    for name, items in splits.items():
        path = TRAIN_DIR / f"{name}.jsonl"
        with open(path, "w") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"✓ {name}.jsonl: {len(items)} examples")

    print(f"\n✓ Dataset split saved to {TRAIN_DIR}")
    print(f"  Total: {n} | Train: {len(splits['train'])} | Valid: {len(splits['valid'])} | Test: {len(splits['test'])}")


def cmd_train():
    """Run QLoRA fine-tuning with mlx-lm."""
    check_mlx()

    if not BASE_MODEL_DIR.exists():
        print(f"✗ Base model not found at {BASE_MODEL_DIR}")
        print("  Run: python tools/finetune.py download")
        sys.exit(1)

    if not (TRAIN_DIR / "train.jsonl").exists():
        print("✗ Training splits not found.")
        print("  Run: python tools/finetune.py prepare")
        sys.exit(1)

    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    # Save config
    config_path = ADAPTER_DIR / "finetune_config.json"
    with open(config_path, "w") as f:
        json.dump(FINETUNE_CONFIG, f, indent=2)
    print(f"✓ Config saved to {config_path}")

    print("\n" + "=" * 60)
    print("  STARTING FINE-TUNING")
    print("  Model: Qwen2.5-7B-Instruct")
    print(f"  Dataset: {TRAIN_DIR}")
    print(f"  LoRA Rank: {FINETUNE_CONFIG['lora_rank']}")
    print(f"  Iterations: {FINETUNE_CONFIG['iters']}")
    print(f"  Learning Rate: {FINETUNE_CONFIG['learning_rate']}")
    print(f"  Adapters → {ADAPTER_DIR}")
    print("=" * 60 + "\n")

    # Run fine-tuning via mlx_lm CLI
    cmd = [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", str(BASE_MODEL_DIR),
        "--data", str(TRAIN_DIR),
        "--train",
        "--iters", str(FINETUNE_CONFIG["iters"]),
        "--batch-size", str(FINETUNE_CONFIG["batch_size"]),
        "--lora-layers", str(FINETUNE_CONFIG["lora_layers"]),
        "--learning-rate", str(FINETUNE_CONFIG["learning_rate"]),
        "--steps-per-report", str(FINETUNE_CONFIG["steps_per_report"]),
        "--steps-per-eval", str(FINETUNE_CONFIG["steps_per_eval"]),
        "--val-batches", str(FINETUNE_CONFIG["val_batches"]),
        "--adapter-path", str(ADAPTER_DIR),
        "--max-seq-length", str(FINETUNE_CONFIG["max_seq_length"]),
        "--seed", str(FINETUNE_CONFIG["seed"]),
        "--grad-checkpoint",
    ]

    print(f"Running: {' '.join(cmd)}\n")
    subprocess.run(cmd, check=True)
    print(f"\n✓ Fine-tuning complete! Adapters saved to {ADAPTER_DIR}")


def cmd_test():
    """Test the fine-tuned model with sample prompts."""
    check_mlx()

    if not ADAPTER_DIR.exists():
        print("✗ No adapters found. Run fine-tuning first.")
        sys.exit(1)

    from mlx_lm import load, generate

    print("Loading model with LoRA adapters...")
    model, tokenizer = load(
        str(BASE_MODEL_DIR),
        adapter_path=str(ADAPTER_DIR),
    )

    test_prompts = [
        {"role": "user", "content": "My hand got burned. What should I do?"},
        {"role": "user", "content": "يدي احترقت شنو اسوي؟"},
        {"role": "user", "content": "Can I put butter on a burn?"},
        {"role": "user", "content": "Someone is bleeding heavily. No ambulance."},
        {"role": "user", "content": "واحد لدغته حية شنو اسوي؟"},
    ]

    system_msg = {
        "role": "system",
        "content": "You are an emergency medical and survival assistant. You give direct, actionable instructions. You ARE the user's doctor. Never say 'consult a doctor' or add disclaimers."
    }

    print("\n" + "=" * 60)
    print("  TESTING FINE-TUNED MODEL")
    print("=" * 60)

    for prompt in test_prompts:
        messages = [system_msg, prompt]
        text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        response = generate(model, tokenizer, prompt=text, max_tokens=512)

        print(f"\n{'─' * 50}")
        print(f"Q: {prompt['content']}")
        print(f"A: {response}")

    print(f"\n{'=' * 60}")


def cmd_fuse():
    """Fuse LoRA adapters into the base model."""
    check_mlx()

    if not ADAPTER_DIR.exists():
        print("✗ No adapters found. Run fine-tuning first.")
        sys.exit(1)

    print("Fusing LoRA adapters into base model...")

    cmd = [
        sys.executable, "-m", "mlx_lm.fuse",
        "--model", str(BASE_MODEL_DIR),
        "--adapter-path", str(ADAPTER_DIR),
        "--save-path", str(FUSED_DIR),
    ]

    subprocess.run(cmd, check=True)
    print(f"\n✓ Fused model saved to {FUSED_DIR}")


def cmd_convert():
    """Convert fused MLX model to GGUF for llama-cpp-python deployment."""
    if not FUSED_DIR.exists():
        print("✗ Fused model not found. Run fuse first.")
        sys.exit(1)

    # Check if llama.cpp convert script exists
    llama_cpp_dir = ROOT / "tools" / "llama.cpp"

    if not llama_cpp_dir.exists():
        print("Cloning llama.cpp for GGUF conversion...")
        subprocess.run([
            "git", "clone", "--depth", "1",
            "https://github.com/ggerganov/llama.cpp.git",
            str(llama_cpp_dir)
        ], check=True)

    convert_script = llama_cpp_dir / "convert_hf_to_gguf.py"
    if not convert_script.exists():
        print(f"✗ Convert script not found at {convert_script}")
        sys.exit(1)

    # Install requirements for conversion
    subprocess.run([
        sys.executable, "-m", "pip", "install", "gguf", "sentencepiece",
    ], check=True)

    # Step 1: Convert to GGUF (F16)
    gguf_f16 = ROOT / "models" / "Qwen2.5-7B-Medical-v1-F16.gguf"
    print(f"\nConverting to GGUF F16...")
    subprocess.run([
        sys.executable, str(convert_script),
        str(FUSED_DIR),
        "--outfile", str(gguf_f16),
        "--outtype", "f16",
    ], check=True)

    # Step 2: Quantize to Q4_K_M
    quantize_bin = llama_cpp_dir / "build" / "bin" / "llama-quantize"
    if not quantize_bin.exists():
        print("\nBuilding llama.cpp quantize tool...")
        build_dir = llama_cpp_dir / "build"
        build_dir.mkdir(exist_ok=True)
        subprocess.run(["cmake", "..", "-DLLAMA_METAL=ON"], cwd=str(build_dir), check=True)
        subprocess.run(["cmake", "--build", ".", "--config", "Release", "-j"], cwd=str(build_dir), check=True)

    print(f"\nQuantizing to Q4_K_M...")
    subprocess.run([
        str(quantize_bin),
        str(gguf_f16),
        str(GGUF_OUTPUT),
        "Q4_K_M",
    ], check=True)

    # Clean up F16
    gguf_f16.unlink(missing_ok=True)

    print(f"\n✓ GGUF model saved to {GGUF_OUTPUT}")
    print(f"  Size: {GGUF_OUTPUT.stat().st_size / (1024**3):.1f} GB")
    print(f"\n  To use: update config.json model_path to point to this file")


def cmd_all():
    """Run full pipeline: download → prepare → train → fuse → convert."""
    cmd_download()
    cmd_prepare()
    cmd_train()
    cmd_fuse()
    cmd_convert()
    print("\n" + "=" * 60)
    print("  FULL PIPELINE COMPLETE")
    print(f"  GGUF model ready at: {GGUF_OUTPUT}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Model Maker Fine-Tuning Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Steps:
  download   Download Qwen2.5-7B-Instruct in MLX format (~14GB)
  prepare    Split dataset into train/valid/test
  train      Run QLoRA fine-tuning on Apple Silicon
  test       Test fine-tuned model with sample prompts
  fuse       Fuse LoRA adapters into base model
  convert    Convert to GGUF (Q4_K_M) for deployment
  all        Run full pipeline (download → convert)
        """
    )
    parser.add_argument(
        "command",
        choices=["download", "prepare", "train", "test", "fuse", "convert", "all"],
        help="Pipeline step to run"
    )
    parser.add_argument(
        "--iters", type=int, default=None,
        help="Override number of training iterations"
    )
    parser.add_argument(
        "--lr", type=float, default=None,
        help="Override learning rate"
    )
    parser.add_argument(
        "--lora-rank", type=int, default=None,
        help="Override LoRA rank"
    )

    args = parser.parse_args()

    # Apply overrides
    if args.iters:
        FINETUNE_CONFIG["iters"] = args.iters
    if args.lr:
        FINETUNE_CONFIG["learning_rate"] = args.lr
    if args.lora_rank:
        FINETUNE_CONFIG["lora_rank"] = args.lora_rank

    commands = {
        "download": cmd_download,
        "prepare": cmd_prepare,
        "train": cmd_train,
        "test": cmd_test,
        "fuse": cmd_fuse,
        "convert": cmd_convert,
        "all": cmd_all,
    }

    commands[args.command]()


if __name__ == "__main__":
    main()
