"""
Pytest configuration and shared fixtures for Model Maker tests.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test artifacts."""
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture
def temp_db(temp_dir):
    """Create a temporary database instance."""
    import sys

    # Add app/ to path so we can import backend
    app_dir = Path(__file__).parent.parent / "app"
    sys.path.insert(0, str(app_dir))

    from backend.database import Database

    db_path = temp_dir / "test.db"
    db = Database(str(db_path))
    yield db


@pytest.fixture
def sample_config(temp_dir):
    """Create a sample config.json for testing."""
    config = {
        "model_path": "/nonexistent/model.gguf",
        "system_prompt": "You are a helpful medical assistant.",
        "language": "en",
        "context_length": 4096,
        "max_tokens": 2048,
        "temperature": 0.7,
    }
    config_path = temp_dir / "config.json"
    config_path.write_text(json.dumps(config, indent=2))
    return str(config_path)


@pytest.fixture
def model_registry():
    """Load the model registry."""
    registry_path = Path(__file__).parent.parent / "models" / "registry.json"
    if not registry_path.exists():
        pytest.skip("models/registry.json not found")
    with open(registry_path) as f:
        return json.load(f)
