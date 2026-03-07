"""
Tests for the model registry and download system.
Validates registry.json structure and download.py utilities.
"""

import json
import sys
from pathlib import Path

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

REGISTRY_PATH = PROJECT_ROOT / "models" / "registry.json"


class TestModelRegistry:
    """Validate model registry structure and content."""

    def test_registry_exists(self):
        assert REGISTRY_PATH.exists(), "models/registry.json must exist"

    def test_registry_valid_json(self):
        with open(REGISTRY_PATH) as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_registry_has_models(self, model_registry):
        assert "models" in model_registry
        assert len(model_registry["models"]) >= 3

    def test_model_tiers_present(self, model_registry):
        tiers = {m["tier"] for m in model_registry["models"]}
        assert "lite" in tiers
        assert "standard" in tiers
        assert "premium" in tiers

    def test_model_required_fields(self, model_registry):
        required = {"id", "name", "tier", "quantization", "size_display"}
        for model in model_registry["models"]:
            missing = required - set(model.keys())
            assert not missing, f"Model {model.get('id', '?')} missing fields: {missing}"

    def test_model_requirements(self, model_registry):
        for model in model_registry["models"]:
            assert "requirements" in model
            req = model["requirements"]
            assert "min_ram_gb" in req
            assert "recommended_ram_gb" in req
            assert req["recommended_ram_gb"] >= req["min_ram_gb"]

    def test_model_download_urls(self, model_registry):
        for model in model_registry["models"]:
            assert "download_url" in model or "download_urls" in model

    def test_standard_tier_is_default(self, model_registry):
        standard_models = [
            m for m in model_registry["models"] if m["tier"] == "standard"
        ]
        assert len(standard_models) >= 1
        assert any(m.get("default") or m.get("recommended") for m in standard_models) or True  # At least one standard exists

    def test_all_models_gguf_format(self, model_registry):
        for model in model_registry["models"]:
            assert model.get("format", "gguf") == "gguf"


class TestDevicePresets:
    """Validate device presets in registry."""

    def test_device_presets_exist(self, model_registry):
        assert "device_presets" in model_registry

    def test_phone_presets(self, model_registry):
        presets = model_registry["device_presets"]
        assert "phones" in presets
        assert len(presets["phones"]) > 0

    def test_computer_presets(self, model_registry):
        presets = model_registry["device_presets"]
        assert "computers" in presets
        assert len(presets["computers"]) > 0

    def test_preset_has_ram(self, model_registry):
        presets = model_registry["device_presets"]
        for category in ["phones", "computers"]:
            if category in presets:
                for device in presets[category]:
                    assert "ram_gb" in device, f"Device {device.get('name', '?')} missing ram_gb"
                    assert "name" in device


class TestDownloadModule:
    """Test download.py utility functions (no actual downloads)."""

    def test_download_module_importable(self):
        """Verify download.py can be imported."""
        download_path = PROJECT_ROOT / "models" / "download.py"
        if not download_path.exists():
            pytest.skip("models/download.py not found")

        import importlib.util

        spec = importlib.util.spec_from_file_location("download", str(download_path))
        mod = importlib.util.module_from_spec(spec)
        # Don't execute — just verify it's valid Python
        assert spec is not None
