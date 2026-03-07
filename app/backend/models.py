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
    conversation_id: str = Field(..., min_length=1, max_length=64)
    message: str = Field(..., min_length=1, max_length=32_000)


# ─── Conversations ────────────────────────────────────────────────

class ConversationCreate(BaseModel):
    title: str = Field("New Chat", max_length=200)


class ConversationRename(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)


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
    key: str = Field(..., min_length=1, max_length=200)
    value: str = Field(..., min_length=1, max_length=10_000)
    category: str = Field("general", max_length=50)


class MemoryResponse(BaseModel):
    id: int
    key: str
    value: str
    category: str
    created_at: str


# ─── Setup Wizard ─────────────────────────────────────────────────

class SetupAnswer(BaseModel):
    name: str = Field("", max_length=200, description="User or business name")
    field: str = Field("general", max_length=50, description="Field: medical, legal, education, business, personal, other")
    tasks: str = Field("general", max_length=100, description="Main tasks: chat, writing, research, learning, support")
    language: str = Field("both", max_length=20, description="Preferred language: arabic, english, both")
    special_instructions: str = Field("", max_length=5_000, description="Any special instructions")


class SetupQuestion(BaseModel):
    id: str
    question_en: str
    question_ar: str
    type: str  # "text", "select", "textarea"
    options: list[dict] | None = None


# ─── Config ───────────────────────────────────────────────────────

class ConfigUpdate(BaseModel):
    system_prompt: str | None = Field(None, max_length=10_000)
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, ge=64, le=32_768)
    max_history_messages: int | None = Field(None, ge=1, le=100)
    language: str | None = Field(None, max_length=20)
