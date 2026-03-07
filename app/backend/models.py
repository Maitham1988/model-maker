"""
Pydantic models for API request/response validation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ─── Chat ─────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


# ─── Conversations ────────────────────────────────────────────────

class ConversationCreate(BaseModel):
    title: str = "New Chat"


class ConversationRename(BaseModel):
    title: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    timestamp: str


# ─── Memory ───────────────────────────────────────────────────────

class MemoryCreate(BaseModel):
    key: str
    value: str
    category: str = "general"


class MemoryResponse(BaseModel):
    id: int
    key: str
    value: str
    category: str
    created_at: str


# ─── Setup Wizard ─────────────────────────────────────────────────

class SetupAnswer(BaseModel):
    name: str = Field("", description="User or business name")
    field: str = Field("general", description="Field: medical, legal, education, business, personal, other")
    tasks: str = Field("general", description="Main tasks: chat, writing, research, learning, support")
    language: str = Field("both", description="Preferred language: arabic, english, both")
    special_instructions: str = Field("", description="Any special instructions")


class SetupQuestion(BaseModel):
    id: str
    question_en: str
    question_ar: str
    type: str  # "text", "select", "textarea"
    options: list[dict] | None = None


# ─── Config ───────────────────────────────────────────────────────

class ConfigUpdate(BaseModel):
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    max_history_messages: int | None = None
    language: str | None = None
