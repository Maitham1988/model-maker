#!/usr/bin/env python3
"""
Install Customer — Copies base/ to projects/customer-XXX/ with unique config.
Run from model-maker root directory.

Usage:
    python tools/install_customer.py --name "Dr. Ahmed Clinic" --id 001
    python tools/install_customer.py --name "Student" --id 002 --model 14b
"""

import argparse
import json
import secrets
import shutil
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
BASE_DIR = PROJECT_ROOT / "app"
PROJECTS_DIR = PROJECT_ROOT / "projects"
MODELS_DIR = PROJECT_ROOT / "models"


def find_model_file(model_hint: str = "7b") -> str | None:
    """Find a GGUF model file matching the hint."""
    for f in MODELS_DIR.glob("*.gguf"):
        if model_hint.lower() in f.name.lower():
            return str(f)
    return None


def install_customer(name: str, customer_id: str, model_hint: str = "7b"):
    """Create a customer installation from base template."""
    customer_dir = PROJECTS_DIR / f"customer-{customer_id}"

    if customer_dir.exists():
        print(f"❌ Customer directory already exists: {customer_dir}")
        print("   Delete it first or use a different ID.")
        return

    print(f"📦 Creating customer installation: {name} (ID: {customer_id})")
    print(f"   Source: {BASE_DIR}")
    print(f"   Target: {customer_dir}")

    # Copy base directory
    shutil.copytree(BASE_DIR, customer_dir)

    # Create data directory
    (customer_dir / "data").mkdir(exist_ok=True)
    (customer_dir / "models").mkdir(exist_ok=True)

    # Find model
    model_file = find_model_file(model_hint)
    model_path = ""
    if model_file:
        model_name = Path(model_file).name
        # Copy model to customer's models folder
        target_model = customer_dir / "models" / model_name
        print(f"   Copying model: {model_name} ({Path(model_file).stat().st_size / 1e9:.1f} GB)")
        shutil.copy2(model_file, target_model)
        model_path = f"models/{model_name}"
    else:
        print(f"   ⚠️  No model found matching '{model_hint}' in {MODELS_DIR}")
        print("      Download a model first: python tools/download_model.py")
        model_path = "models/PLACE_MODEL_HERE.gguf"

    # Generate license secret
    license_secret = secrets.token_hex(32)

    # Create config
    config = {
        "model_path": model_path,
        "customer_name": name,
        "customer_id": customer_id,
        "system_prompt": "You are a helpful AI assistant. Be accurate, concise, and friendly. Respond in the same language the user writes in.",
        "setup_completed": False,
        "context_length": 4096,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.9,
        "repeat_penalty": 1.1,
        "max_history_messages": 20,
        "gpu_layers": 0,
        "license_key": "",
        "license_secret": license_secret,
    }

    config_path = customer_dir / "config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    # Save license secret separately for developer reference
    secrets_file = PROJECTS_DIR / f"customer-{customer_id}.secret"
    with open(secrets_file, "w") as f:
        f.write(f"Customer: {name}\n")
        f.write(f"ID: {customer_id}\n")
        f.write(f"License Secret: {license_secret}\n")
        f.write("\nTo generate license on customer's device:\n")
        f.write("  python backend/license_check.py  (prints hardware ID)\n")
        f.write(
            f"  python tools/generate_license.py --hardware-id <ID> --secret {license_secret}\n"
        )

    print("\n✅ Customer installation created!")
    print(f"   Directory: {customer_dir}")
    print(f"   Config: {config_path}")
    print(f"   Secret: {secrets_file}")
    print("\n📋 Next steps:")
    print(f"   1. Copy '{customer_dir}' to USB drive")
    print("   2. On customer's device:")
    print("      a. Install Python 3.11+")
    print("      b. pip install -r requirements.txt")
    print("      c. python run.py")
    print("   3. Generate license:")
    print("      a. python backend/license_check.py → get hardware ID")
    print("      b. Send hardware ID to you")
    print(
        f"      c. You run: python tools/generate_license.py --hardware-id <ID> --customer-id {customer_id}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create customer installation")
    parser.add_argument("--name", required=True, help="Customer name")
    parser.add_argument("--id", required=True, help="Customer ID (e.g., 001)")
    parser.add_argument("--model", default="7b", help="Model hint (7b, 14b)")
    args = parser.parse_args()

    install_customer(args.name, args.id, args.model)
