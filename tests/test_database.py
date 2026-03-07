"""
Tests for the Database layer.
Verifies conversations, messages, and memory CRUD operations.
"""

import pytest


class TestConversations:
    """Test conversation CRUD operations."""

    def test_create_conversation(self, temp_db):
        conv = temp_db.create_conversation("Test Chat")
        assert conv["id"]
        assert conv["title"] == "Test Chat"
        assert conv["created_at"]
        assert conv["updated_at"]

    def test_create_conversation_default_title(self, temp_db):
        conv = temp_db.create_conversation()
        assert conv["title"] == "New Chat"

    def test_list_conversations_empty(self, temp_db):
        convs = temp_db.list_conversations()
        assert convs == []

    def test_list_conversations_order(self, temp_db):
        c1 = temp_db.create_conversation("First")
        c2 = temp_db.create_conversation("Second")
        convs = temp_db.list_conversations()
        assert len(convs) == 2
        # Most recent first
        assert convs[0]["title"] == "Second"
        assert convs[1]["title"] == "First"

    def test_get_conversation(self, temp_db):
        created = temp_db.create_conversation("Find Me")
        found = temp_db.get_conversation(created["id"])
        assert found is not None
        assert found["title"] == "Find Me"

    def test_get_conversation_not_found(self, temp_db):
        result = temp_db.get_conversation("nonexistent-id")
        assert result is None

    def test_rename_conversation(self, temp_db):
        conv = temp_db.create_conversation("Old Name")
        temp_db.rename_conversation(conv["id"], "New Name")
        updated = temp_db.get_conversation(conv["id"])
        assert updated["title"] == "New Name"

    def test_delete_conversation(self, temp_db):
        conv = temp_db.create_conversation("Delete Me")
        temp_db.delete_conversation(conv["id"])
        assert temp_db.get_conversation(conv["id"]) is None

    def test_delete_conversation_cascades_messages(self, temp_db):
        conv = temp_db.create_conversation("With Messages")
        temp_db.add_message(conv["id"], "user", "Hello")
        temp_db.add_message(conv["id"], "assistant", "Hi there")
        temp_db.delete_conversation(conv["id"])
        messages = temp_db.get_messages(conv["id"])
        assert messages == []


class TestMessages:
    """Test message CRUD operations."""

    def test_add_and_get_messages(self, temp_db):
        conv = temp_db.create_conversation()
        temp_db.add_message(conv["id"], "user", "Hello")
        temp_db.add_message(conv["id"], "assistant", "Hi!")
        msgs = temp_db.get_messages(conv["id"])
        assert len(msgs) == 2
        assert msgs[0]["role"] == "user"
        assert msgs[0]["content"] == "Hello"
        assert msgs[1]["role"] == "assistant"
        assert msgs[1]["content"] == "Hi!"

    def test_message_has_timestamp(self, temp_db):
        conv = temp_db.create_conversation()
        temp_db.add_message(conv["id"], "user", "Test")
        msgs = temp_db.get_messages(conv["id"])
        assert msgs[0]["timestamp"]

    def test_get_recent_messages(self, temp_db):
        conv = temp_db.create_conversation()
        for i in range(30):
            temp_db.add_message(conv["id"], "user", f"Message {i}")
        recent = temp_db.get_recent_messages(conv["id"], limit=10)
        assert len(recent) == 10

    def test_message_count(self, temp_db):
        conv = temp_db.create_conversation()
        assert temp_db.get_message_count(conv["id"]) == 0
        temp_db.add_message(conv["id"], "user", "One")
        assert temp_db.get_message_count(conv["id"]) == 1
        temp_db.add_message(conv["id"], "assistant", "Two")
        assert temp_db.get_message_count(conv["id"]) == 2

    def test_auto_title_conversation(self, temp_db):
        conv = temp_db.create_conversation()
        temp_db.auto_title_conversation(conv["id"], "How do I treat a burn wound?")
        updated = temp_db.get_conversation(conv["id"])
        assert updated["title"] != "New Chat"
        assert len(updated["title"]) <= 50  # Auto-title should be concise


class TestMemory:
    """Test persistent memory operations."""

    def test_add_memory(self, temp_db):
        mem = temp_db.add_memory("name", "Maitham", "personal")
        assert mem["key"] == "name"
        assert mem["value"] == "Maitham"
        assert mem["category"] == "personal"

    def test_list_memory(self, temp_db):
        temp_db.add_memory("name", "Maitham", "personal")
        temp_db.add_memory("location", "Bahrain", "personal")
        memories = temp_db.get_all_memory()
        assert len(memories) == 2

    def test_delete_memory(self, temp_db):
        mem = temp_db.add_memory("temp", "data", "test")
        temp_db.delete_memory(mem["id"])
        memories = temp_db.get_all_memory()
        assert len(memories) == 0

    def test_memory_context_string(self, temp_db):
        temp_db.add_memory("blood_type", "O+", "medical")
        temp_db.add_memory("allergies", "penicillin", "medical")
        context = temp_db.get_memory_context()
        assert "blood_type" in context or "O+" in context
        assert "allergies" in context or "penicillin" in context
