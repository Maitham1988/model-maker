#!/usr/bin/env python3
"""
Generate License — Creates a device-locked license key for a customer.

Usage:
    python tools/generate_license.py --hardware-id abc123... --customer-id 001

The hardware ID comes from running `python backend/license_check.py` on the
customer's device. The secret is read from projects/customer-XXX.secret.
"""

import argparse
import hashlib
import hmac
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = PROJECT_ROOT / "projects"


def generate_license(hardware_id: str, secret: str) -> str:
    """Generate HMAC-SHA256 license key."""
    return hmac.new(
        secret.encode(),
        hardware_id.encode(),
        hashlib.sha256,
    ).hexdigest()


def activate_customer(customer_id: str, hardware_id: str):
    """Generate and save license key to customer's config."""

    # Read secret from .secret file
    secret_file = PROJECTS_DIR / f"customer-{customer_id}.secret"
    if not secret_file.exists():
        print(f"❌ Secret file not found: {secret_file}")
        print("   Run install_customer.py first.")
        return

    secret = ""
    with open(secret_file) as f:
        for line in f:
            if line.startswith("License Secret:"):
                secret = line.split(":", 1)[1].strip()
                break

    if not secret:
        print(f"❌ Could not read license secret from {secret_file}")
        return

    # Generate license key
    license_key = generate_license(hardware_id, secret)

    # Update customer config
    config_path = PROJECTS_DIR / f"customer-{customer_id}" / "config.json"
    if not config_path.exists():
        print(f"❌ Customer config not found: {config_path}")
        return

    with open(config_path, encoding="utf-8") as f:
        config = json.load(f)

    config["license_key"] = license_key

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ License activated for customer {customer_id}")
    print(f"   Hardware ID: {hardware_id[:16]}...")
    print(f"   License Key: {license_key[:16]}...")
    print(f"   Saved to: {config_path}")
    print("\n   Copy the updated config.json to the customer's device.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate device-locked license")
    parser.add_argument("--hardware-id", required=True, help="Customer's hardware ID")
    parser.add_argument("--customer-id", required=True, help="Customer ID (e.g., 001)")
    args = parser.parse_args()

    activate_customer(args.customer_id, args.hardware_id)
