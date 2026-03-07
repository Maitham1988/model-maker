"""
Tests for API endpoints using FastAPI TestClient.
Tests run without a real LLM model — they verify routing, validation, and database integration.
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add app/ to path
APP_DIR = Path(__file__).parent.parent / "app"
sys.path.insert(0, str(APP_DIR))


@pytest.fixture
def api_client(temp_db, sample_config):
    """Create a FastAPI TestClient with mocked LLM engine."""
    from fastapi.testclient import TestClient

    from backend.routes import router, init

    # Create a minimal FastAPI app for testing
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(router)

    # Mock the LLM engine
    mock_engine = MagicMock()
    mock_engine.chat_stream.return_value = iter(["Hello", " from", " AI"])

    init(database=temp_db, llm_engine=mock_engine, cfg_path=sample_config)

    client = TestClient(app)
    yield client


class TestConversationEndpoints:
    """Test /api/conversations endpoints."""

    def test_list_conversations_empty(self, api_client):
        resp = api_client.get("/api/conversations")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_conversation(self, api_client):
        resp = api_client.post(
            "/api/conversations", json={"title": "Emergency Chat"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Emergency Chat"
        assert "id" in data

    def test_create_conversation_default_title(self, api_client):
        resp = api_client.post("/api/conversations", json={})
        assert resp.status_code == 200
        assert resp.json()["title"] == "New Chat"

    def test_list_after_create(self, api_client):
        api_client.post("/api/conversations", json={"title": "Chat 1"})
        api_client.post("/api/conversations", json={"title": "Chat 2"})
        resp = api_client.get("/api/conversations")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_get_messages_empty(self, api_client):
        conv = api_client.post(
            "/api/conversations", json={"title": "Test"}
        ).json()
        resp = api_client.get(f"/api/conversations/{conv['id']}/messages")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_messages_not_found(self, api_client):
        resp = api_client.get("/api/conversations/nonexistent/messages")
        assert resp.status_code == 404

    def test_rename_conversation(self, api_client):
        conv = api_client.post(
            "/api/conversations", json={"title": "Old"}
        ).json()
        resp = api_client.put(
            f"/api/conversations/{conv['id']}", json={"title": "New"}
        )
        assert resp.status_code == 200

    def test_delete_conversation(self, api_client):
        conv = api_client.post(
            "/api/conversations", json={"title": "Delete Me"}
        ).json()
        resp = api_client.delete(f"/api/conversations/{conv['id']}")
        assert resp.status_code == 200


class TestChatEndpoint:
    """Test /api/chat SSE streaming endpoint."""

    def test_chat_returns_sse_stream(self, api_client):
        conv = api_client.post(
            "/api/conversations", json={"title": "Chat"}
        ).json()
        resp = api_client.post(
            "/api/chat",
            json={"conversation_id": conv["id"], "message": "Help me"},
        )
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers.get("content-type", "")

    def test_chat_nonexistent_conversation(self, api_client):
        resp = api_client.post(
            "/api/chat",
            json={"conversation_id": "nonexistent", "message": "Hello"},
        )
        assert resp.status_code == 404

    def test_chat_missing_fields(self, api_client):
        resp = api_client.post("/api/chat", json={})
        assert resp.status_code == 422  # Pydantic validation error


class TestMemoryEndpoints:
    """Test /api/memory endpoints."""

    def test_list_memory_empty(self, api_client):
        resp = api_client.get("/api/memory")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_add_memory(self, api_client):
        resp = api_client.post(
            "/api/memory",
            json={"key": "blood_type", "value": "A+", "category": "medical"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["key"] == "blood_type"
        assert data["value"] == "A+"

    def test_delete_memory(self, api_client):
        mem = api_client.post(
            "/api/memory",
            json={"key": "temp", "value": "data"},
        ).json()
        resp = api_client.delete(f"/api/memory/{mem['id']}")
        assert resp.status_code == 200


class TestConfigEndpoints:
    """Test /api/config endpoints."""

    def test_get_config(self, api_client):
        resp = api_client.get("/api/config")
        assert resp.status_code == 200
        data = resp.json()
        assert "system_prompt" in data or "language" in data

    def test_update_config(self, api_client):
        resp = api_client.put(
            "/api/config",
            json={"system_prompt": "You are a survival expert."},
        )
        assert resp.status_code == 200
