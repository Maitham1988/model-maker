"""
License Check — Device-locked licensing to prevent copying/reselling.
Hardware ID = SHA256(MAC address + hostname + disk serial)
License key = HMAC-SHA256(hardware_id, secret)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import platform
import uuid
from pathlib import Path


def get_hardware_id() -> str:
    """Generate a unique hardware ID from machine characteristics."""
    parts = []

    # MAC address
    mac = uuid.getnode()
    parts.append(str(mac))

    # Hostname
    parts.append(platform.node())

    # Platform info
    parts.append(platform.machine())
    parts.append(platform.system())

    # Combine and hash
    raw = "|".join(parts)
    return hashlib.sha256(raw.encode()).hexdigest()


def generate_license_key(hardware_id: str, secret: str) -> str:
    """Generate a license key for a specific hardware ID."""
    return hmac.new(
        secret.encode(),
        hardware_id.encode(),
        hashlib.sha256,
    ).hexdigest()


def verify_license(config_path: str = "config.json") -> tuple[bool, str]:
    """
    Verify the license matches the current device.

    Returns:
        (is_valid, message)
    """
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        return False, "Config file not found"

    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    license_key = cfg.get("license_key", "")
    license_secret = cfg.get("license_secret", "")

    if not license_key:
        # No license required (development mode)
        return True, "Development mode — no license required"

    if not license_secret:
        return False, "License secret missing from config"

    # Get current hardware ID
    current_hw_id = get_hardware_id()

    # Generate expected key for this hardware
    expected_key = generate_license_key(current_hw_id, license_secret)

    if hmac.compare_digest(license_key, expected_key):
        return True, "License valid"
    else:
        return False, (
            "License invalid — this software is licensed for a different device.\n"
            f"This device ID: {current_hw_id[:16]}...\n"
            "Contact your provider for a new license."
        )


def print_hardware_id():
    """Print current device's hardware ID (for license generation)."""
    hw_id = get_hardware_id()
    print(f"Hardware ID: {hw_id}")
    return hw_id


if __name__ == "__main__":
    print_hardware_id()
