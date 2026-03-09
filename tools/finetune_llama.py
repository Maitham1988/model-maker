#!/usr/bin/env python3
"""
Fine-tune Llama 3.2 3B Instruct on English medical/survival data.
Uses MLX-LM QLoRA on Apple Silicon.

Run:
    python tools/finetune_llama.py                    # Default: 1000 iterations
    python tools/finetune_llama.py --iters 2000       # More training
    python tools/finetune_llama.py --iters 500 --test # Quick test run

This creates adapters in models/adapters/llama-medical-v1/
After training, fuse + quantize:
    python tools/finetune_llama.py --fuse
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).parent.parent
MODEL_DIR = PROJECT / "models" / "mlx" / "Llama-3.2-3B-Instruct-4bit"
ADAPTER_DIR = PROJECT / "models" / "adapters" / "llama-medical-v1"
FUSED_DIR = PROJECT / "models" / "mlx" / "Llama-3.2-3B-Medical-v1"
TRAIN_DATA = PROJECT / "training" / "llama_splits" / "train.jsonl"
VALID_DATA = PROJECT / "training" / "llama_splits" / "valid.jsonl"
TEST_DATA = PROJECT / "training" / "llama_splits" / "test.jsonl"


def check_prerequisites():
    """Verify model and data exist."""
    if not MODEL_DIR.exists():
        print(f"❌ MLX model not found at: {MODEL_DIR}")
        print("   Run: python -c \"from huggingface_hub import snapshot_download; "
              "snapshot_download('mlx-community/Llama-3.2-3B-Instruct-4bit', "
              f"local_dir='{MODEL_DIR}')\"")
        sys.exit(1)

    if not TRAIN_DATA.exists():
        print(f"❌ Training data not found at: {TRAIN_DATA}")
        print("   Run: python training/build_english_dataset.py")
        sys.exit(1)

    print(f"✅ Model: {MODEL_DIR.name}")
    print(f"✅ Train: {TRAIN_DATA} ({sum(1 for _ in open(TRAIN_DATA))} examples)")
    print(f"✅ Valid: {VALID_DATA} ({sum(1 for _ in open(VALID_DATA))} examples)")


def train(iters: int = 1000, lr: float = 1e-5, batch_size: int = 1,
          num_layers: int = 16):
    """Run QLoRA fine-tuning with mlx_lm."""
    check_prerequisites()
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  🔥 FINE-TUNING Llama 3.2 3B — Medical/Survival Specialist")
    print(f"{'='*60}")
    print(f"  Iterations:  {iters}")
    print(f"  Learning rate: {lr}")
    print(f"  Num layers:  {num_layers}")
    print(f"  Batch size:  {batch_size}")
    print(f"  Adapter out: {ADAPTER_DIR}")
    print(f"{'='*60}\n")

    start = time.time()

    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", str(MODEL_DIR),
        "--data", str(TRAIN_DATA.parent),
        "--adapter-path", str(ADAPTER_DIR),
        "--train",
        "--iters", str(iters),
        "--learning-rate", str(lr),
        "--batch-size", str(batch_size),
        "--num-layers", str(num_layers),
        "--steps-per-eval", str(min(50, iters // 5)),
        "--save-every", str(min(100, iters // 4)),
        "--val-batches", "5",
        "--grad-checkpoint",
    ]

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=PROJECT)

    elapsed = time.time() - start
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)

    if result.returncode == 0:
        print(f"\n✅ Training complete in {hours}h {minutes}m")
        print(f"   Adapter saved to: {ADAPTER_DIR}")
    else:
        print(f"\n❌ Training failed (exit code {result.returncode})")
        sys.exit(1)


def fuse_and_quantize():
    """Fuse adapter into base model and quantize to GGUF."""
    if not ADAPTER_DIR.exists():
        print(f"❌ No adapter found at: {ADAPTER_DIR}")
        print("   Run training first.")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  🔗 FUSING adapter into base model")
    print(f"{'='*60}\n")

    # Step 1: Fuse adapter into MLX model
    FUSED_DIR.mkdir(parents=True, exist_ok=True)
    cmd_fuse = [
        sys.executable, "-m", "mlx_lm", "fuse",
        "--model", str(MODEL_DIR),
        "--adapter-path", str(ADAPTER_DIR),
        "--save-path", str(FUSED_DIR),
    ]
    print(f"Fusing: {' '.join(cmd_fuse)}")
    result = subprocess.run(cmd_fuse, cwd=PROJECT)
    if result.returncode != 0:
        print("❌ Fuse failed")
        sys.exit(1)
    print(f"✅ Fused model saved to: {FUSED_DIR}")

    # Step 2: Convert to GGUF using llama.cpp
    llama_convert = PROJECT / "tools" / "llama.cpp" / "convert_hf_to_gguf.py"
    gguf_out = PROJECT / "models" / "Llama-3.2-3B-Medical-v1-Q4_K_M.gguf"

    if llama_convert.exists():
        print(f"\n🔄 Converting to GGUF...")

        # First convert to F16 GGUF
        f16_path = FUSED_DIR / "model-f16.gguf"
        cmd_convert = [
            sys.executable, str(llama_convert),
            str(FUSED_DIR),
            "--outfile", str(f16_path),
            "--outtype", "f16",
        ]
        print(f"Converting: {' '.join(cmd_convert)}")
        result = subprocess.run(cmd_convert, cwd=PROJECT)
        if result.returncode != 0:
            print("❌ GGUF conversion failed")
            print("   You can manually convert using llama.cpp tools")
            return

        # Then quantize to Q4_K_M
        quantize_bin = PROJECT / "tools" / "llama.cpp" / "build" / "bin" / "llama-quantize"
        if quantize_bin.exists():
            cmd_quant = [
                str(quantize_bin),
                str(f16_path),
                str(gguf_out),
                "Q4_K_M",
            ]
            print(f"Quantizing: {' '.join(cmd_quant)}")
            result = subprocess.run(cmd_quant, cwd=PROJECT)
            if result.returncode == 0:
                print(f"\n✅ Final GGUF: {gguf_out}")
                print(f"   Size: {gguf_out.stat().st_size / (1024**3):.2f} GB")
                # Clean up F16
                f16_path.unlink(missing_ok=True)
            else:
                print("❌ Quantization failed")
        else:
            print(f"⚠️  llama-quantize not found at {quantize_bin}")
            print(f"   F16 GGUF saved at: {f16_path}")
            print(f"   Manually quantize: llama-quantize {f16_path} {gguf_out} Q4_K_M")
    else:
        print(f"\n⚠️  llama.cpp convert script not found at {llama_convert}")
        print("   Fused MLX model is ready at:", FUSED_DIR)
        print("   You'll need to convert to GGUF manually.")


def test():
    """Test the fine-tuned model on test examples."""
    if not ADAPTER_DIR.exists():
        print(f"❌ No adapter found at: {ADAPTER_DIR}")
        return

    print(f"\n{'='*60}")
    print(f"  🧪 TESTING fine-tuned model")
    print(f"{'='*60}\n")

    cmd = [
        sys.executable, "-m", "mlx_lm", "lora",
        "--model", str(MODEL_DIR),
        "--adapter-path", str(ADAPTER_DIR),
        "--data", str(TRAIN_DATA.parent),
        "--test",
    ]
    subprocess.run(cmd, cwd=PROJECT)


def generate_sample(prompt: str):
    """Generate a sample response from the fine-tuned model."""
    if not ADAPTER_DIR.exists():
        print(f"❌ No adapter found at: {ADAPTER_DIR}")
        return

    cmd = [
        sys.executable, "-m", "mlx_lm", "generate",
        "--model", str(MODEL_DIR),
        "--adapter-path", str(ADAPTER_DIR),
        "--prompt", prompt,
        "--max-tokens", "500",
        "--temp", "0.7",
    ]
    subprocess.run(cmd, cwd=PROJECT)


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Llama 3.2 3B for Medical/Survival")
    parser.add_argument("--iters", type=int, default=1000, help="Training iterations (default: 1000)")
    parser.add_argument("--lr", type=float, default=1e-5, help="Learning rate (default: 1e-5)")
    parser.add_argument("--batch-size", type=int, default=1, help="Batch size (default: 1)")
    parser.add_argument("--num-layers", type=int, default=16, help="Number of layers to fine-tune (default: 16)")
    parser.add_argument("--fuse", action="store_true", help="Fuse adapter + convert to GGUF")
    parser.add_argument("--test", action="store_true", help="Run test evaluation only")
    parser.add_argument("--generate", type=str, help="Generate response from prompt")

    args = parser.parse_args()

    if args.fuse:
        fuse_and_quantize()
    elif args.test:
        test()
    elif args.generate:
        generate_sample(args.generate)
    else:
        train(
            iters=args.iters,
            lr=args.lr,
            batch_size=args.batch_size,
            num_layers=args.num_layers,
        )


if __name__ == "__main__":
    main()
