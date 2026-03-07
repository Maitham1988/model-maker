#!/usr/bin/env python3
"""
Model Maker — Build & Ship Tool
=================================
Creates versioned, customer-ready builds from the fine-tuned model.

Usage:
    # Build a new version
    python tools/build_version.py --version medical-v1 --model models/Qwen2.5-7B-Medical-v1-Q4_K_M.gguf

    # Build for specific customer
    python tools/build_version.py --version medical-v1 --customer customer-001 --hardware-id "ABC123..."

    # List all versions
    python tools/build_version.py --list
"""

import argparse
import hashlib
import hmac
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = ROOT / "base"
PROJECTS_DIR = ROOT / "projects"
BUILDS_DIR = ROOT / "builds"
MODELS_DIR = ROOT / "models"

# Versioning metadata
VERSION_REGISTRY = ROOT / "builds" / "versions.json"

# License secret (in production, this should be in an env var or secure vault)
LICENSE_SECRET = "model-maker-2026-flexsell"


def generate_license_key(hardware_id: str) -> str:
    """Generate device-locked license key."""
    return hmac.new(
        LICENSE_SECRET.encode(),
        hardware_id.encode(),
        hashlib.sha256,
    ).hexdigest()


def load_versions() -> dict:
    """Load version registry."""
    if VERSION_REGISTRY.exists():
        with open(VERSION_REGISTRY) as f:
            return json.load(f)
    return {"versions": []}


def save_versions(data: dict):
    """Save version registry."""
    VERSION_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    with open(VERSION_REGISTRY, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cmd_build(args):
    """Build a versioned release."""
    version = args.version
    model_path = Path(args.model)
    field = args.field or "medical"

    if not model_path.exists():
        print(f"✗ Model not found: {model_path}")
        sys.exit(1)

    if not BASE_DIR.exists():
        print(f"✗ Base directory not found: {BASE_DIR}")
        sys.exit(1)

    # Create build directory
    build_dir = BUILDS_DIR / version
    if build_dir.exists():
        if not args.force:
            print(f"✗ Version {version} already exists. Use --force to overwrite.")
            sys.exit(1)
        shutil.rmtree(build_dir)

    print(f"\n{'=' * 60}")
    print(f"  BUILDING VERSION: {version}")
    print(f"  Model: {model_path.name}")
    print(f"  Field: {field}")
    print(f"{'=' * 60}\n")

    # Step 1: Copy base application
    print("1. Copying base application...")
    app_dir = build_dir / "app"
    shutil.copytree(
        BASE_DIR,
        app_dir,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "data", ".DS_Store"),
    )
    print(f"   ✓ Copied to {app_dir}")

    # Step 2: Create data directory
    (app_dir / "data").mkdir(exist_ok=True)

    # Step 3: Create model directory (model not copied — too large, will be on USB)
    model_dir = build_dir / "model"
    model_dir.mkdir(exist_ok=True)

    # Create a model manifest (tells the app where to find the model)
    model_manifest = {
        "model_name": model_path.stem,
        "model_file": model_path.name,
        "model_size_gb": round(model_path.stat().st_size / (1024**3), 1),
        "expected_location": f"./model/{model_path.name}",
    }
    with open(model_dir / "manifest.json", "w") as f:
        json.dump(model_manifest, f, indent=2)
    print(f"   ✓ Model manifest created (model file: {model_path.name})")

    # Step 4: Create version config
    config_path = app_dir / "config.json"
    config = {
        "model_path": f"../model/{model_path.name}",
        "field": field,
        "system_prompt": "",  # Will be set by setup wizard or customer config
        "context_length": 4096,
        "temperature": 0.7,
        "max_tokens": 2048,
        "version": version,
        "build_date": datetime.now().isoformat(),
    }
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("   ✓ Config created")

    # Step 5: Create README for customer
    readme = f"""# Model Maker — {version}
# Built: {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Setup Instructions

1. Copy this entire folder to the target computer
2. Copy the model file ({model_path.name}) into the `model/` folder
3. Install Python 3.11+ if not already installed
4. Open terminal in the `app/` folder
5. Run: pip install -r requirements.txt
6. Run: python run.py
7. Open browser to http://127.0.0.1:8000

## Files
- app/          — Application code (backend + frontend)
- model/        — Put the GGUF model file here
- LICENSE.key   — Generated per-device license (created during installation)

## Support
Contact: FlexSell International
"""
    with open(build_dir / "README.md", "w") as f:
        f.write(readme)

    # Step 6: Create install script for customer device
    install_script = """#!/usr/bin/env python3
\"\"\"Customer installation script — run on the target device.\"\"\"
import hashlib
import hmac
import subprocess
import sys
import uuid
import platform
from pathlib import Path

def get_hardware_id():
    mac = uuid.getnode()
    hostname = platform.node()
    hw_string = f"{mac}-{hostname}"
    return hashlib.sha256(hw_string.encode()).hexdigest()

def main():
    print("=" * 50)
    print("  Model Maker — Device Setup")
    print("=" * 50)

    # Step 1: Install dependencies
    print("\\n1. Installing dependencies...")
    app_dir = Path(__file__).parent / "app"
    req_file = app_dir / "requirements.txt"
    if req_file.exists():
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        print("   ✓ Dependencies installed")

    # Step 2: Generate license
    print("\\n2. Generating device license...")
    hw_id = get_hardware_id()
    print(f"   Hardware ID: {hw_id[:16]}...")

    # License key is generated and stored
    license_path = Path(__file__).parent / "LICENSE.key"
    with open(license_path, "w") as f:
        f.write(hw_id)
    print(f"   ✓ License saved to {license_path}")

    # Step 3: Check model
    print("\\n3. Checking model file...")
    model_dir = Path(__file__).parent / "model"
    gguf_files = list(model_dir.glob("*.gguf"))
    if gguf_files:
        print(f"   ✓ Model found: {gguf_files[0].name}")
    else:
        print("   ⚠ No model file found in model/ folder!")
        print("   Copy the .gguf model file to the model/ folder")

    print("\\n" + "=" * 50)
    print("  Setup complete!")
    print("  To start: cd app && python run.py")
    print("=" * 50)

if __name__ == "__main__":
    main()
"""
    with open(build_dir / "install.py", "w") as f:
        f.write(install_script)
    print("   ✓ Install script created")

    # Step 7: Update version registry
    registry = load_versions()
    registry["versions"].append(
        {
            "version": version,
            "model": model_path.name,
            "field": field,
            "build_date": datetime.now().isoformat(),
            "model_size_gb": model_manifest["model_size_gb"],
            "path": str(build_dir),
        }
    )
    save_versions(registry)
    print("   ✓ Version registered")

    # Summary
    total_size = sum(f.stat().st_size for f in build_dir.rglob("*") if f.is_file())
    print(f"\n{'=' * 60}")
    print(f"  BUILD COMPLETE: {version}")
    print(f"  Location: {build_dir}")
    print(f"  App size: {total_size / (1024**2):.1f} MB (without model)")
    print(f"  Model: {model_path.name} ({model_manifest['model_size_gb']} GB)")
    print("\n  To ship:")
    print(f"  1. Copy {build_dir}/ to USB drive")
    print(f"  2. Copy {model_path} to USB drive model/ folder")
    print("  3. On customer device: python install.py")
    print(f"{'=' * 60}")


def cmd_customer(args):
    """Build for a specific customer with license pre-generated."""
    version = args.version
    customer = args.customer
    hardware_id = args.hardware_id

    build_dir = BUILDS_DIR / version
    if not build_dir.exists():
        print(f"✗ Version {version} not found. Build it first.")
        sys.exit(1)

    customer_dir = PROJECTS_DIR / customer
    if customer_dir.exists() and not args.force:
        print(f"✗ Customer {customer} already exists. Use --force to overwrite.")
        sys.exit(1)

    print(f"\nPreparing for customer: {customer}")

    # Copy build to customer folder
    if customer_dir.exists():
        shutil.rmtree(customer_dir)
    shutil.copytree(build_dir, customer_dir)

    # Generate license if hardware_id provided
    if hardware_id:
        license_key = generate_license_key(hardware_id)
        license_path = customer_dir / "LICENSE.key"
        with open(license_path, "w") as f:
            f.write(f"{hardware_id}\n{license_key}")
        print(f"  ✓ License generated for device {hardware_id[:16]}...")

    print(f"  ✓ Customer build ready at {customer_dir}")


def cmd_list(args):
    """List all built versions."""
    registry = load_versions()
    if not registry["versions"]:
        print("No versions built yet.")
        return

    print(f"\n{'Version':<25} {'Model':<40} {'Field':<10} {'Date':<20} {'Size'}")
    print("─" * 110)
    for v in registry["versions"]:
        print(
            f"{v['version']:<25} {v['model']:<40} {v['field']:<10} {v['build_date'][:19]:<20} {v.get('model_size_gb', '?')} GB"
        )


def main():
    parser = argparse.ArgumentParser(description="Model Maker — Build & Ship Tool")
    sub = parser.add_subparsers(dest="command")

    # Build command
    build = sub.add_parser("build", help="Build a versioned release")
    build.add_argument("--version", required=True, help="Version name (e.g., medical-v1)")
    build.add_argument("--model", required=True, help="Path to GGUF model file")
    build.add_argument("--field", default="medical", help="Product field (default: medical)")
    build.add_argument("--force", action="store_true", help="Overwrite existing version")

    # Customer command
    cust = sub.add_parser("customer", help="Prepare build for a specific customer")
    cust.add_argument("--version", required=True, help="Version to use")
    cust.add_argument("--customer", required=True, help="Customer ID")
    cust.add_argument("--hardware-id", help="Target device hardware ID (for license)")
    cust.add_argument("--force", action="store_true", help="Overwrite existing customer")

    # List command
    sub.add_parser("list", help="List all built versions")

    args = parser.parse_args()

    if args.command == "build":
        cmd_build(args)
    elif args.command == "customer":
        cmd_customer(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
