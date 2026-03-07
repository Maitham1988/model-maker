"""
API Routes — All endpoints for chat, conversations, memory, setup, and config.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from .database import Database
from .llm_engine import LLMEngine
from .knowledge_rag import KnowledgeRAG
from .models import (
    ChatRequest,
    ConfigUpdate,
    ConversationCreate,
    ConversationRename,
    MemoryCreate,
    SetupAnswer,
)

router = APIRouter(prefix="/api")

# These will be injected by main.py
db: Database | None = None
engine: LLMEngine | None = None
rag: KnowledgeRAG | None = None
config_path: str = "config.json"


def init(
    database: Database,
    llm_engine: LLMEngine,
    cfg_path: str = "config.json",
    knowledge_rag: KnowledgeRAG | None = None,
):
    """Initialize routes with shared instances."""
    global db, engine, config_path, rag
    db = database
    engine = llm_engine
    config_path = cfg_path
    rag = knowledge_rag


# ─── Chat (SSE Streaming) ────────────────────────────────────────

@router.post("/chat")
async def chat(request: ChatRequest):
    """Send a message and get streaming response via SSE."""
    if not db or not engine:
        raise HTTPException(status_code=503, detail="Service not initialized")

    conv = db.get_conversation(request.conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Save user message
    db.add_message(request.conversation_id, "user", request.message)

    # Auto-title on first message
    msg_count = db.get_message_count(request.conversation_id)
    if msg_count == 1:
        db.auto_title_conversation(request.conversation_id, request.message)

    # Build message history for LLM
    recent = db.get_recent_messages(request.conversation_id, limit=20)
    messages = [{"role": m["role"], "content": m["content"]} for m in recent]

    # Get memory context
    memory_context = db.get_memory_context()

    # Get relevant knowledge via RAG
    knowledge_context = ""
    if rag and rag.is_ready:
        knowledge_context = rag.get_context(request.message)

    # Stream response
    async def generate() -> AsyncGenerator[str, None]:
        full_response = []
        for token in engine.chat_stream(messages, memory_context, knowledge_context):
            full_response.append(token)
            # SSE format
            yield f"data: {json.dumps({'token': token})}\n\n"

        # Save complete assistant response
        complete = "".join(full_response)
        db.add_message(request.conversation_id, "assistant", complete)

        # Send done signal
        yield f"data: {json.dumps({'done': True, 'conversation_id': request.conversation_id})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ─── Conversations ────────────────────────────────────────────────

@router.get("/conversations")
async def list_conversations():
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return db.list_conversations()


@router.post("/conversations")
async def create_conversation(data: ConversationCreate):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return db.create_conversation(data.title)


@router.get("/conversations/{conv_id}/messages")
async def get_messages(conv_id: str):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    conv = db.get_conversation(conv_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db.get_messages(conv_id)


@router.put("/conversations/{conv_id}")
async def rename_conversation(conv_id: str, data: ConversationRename):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    success = db.rename_conversation(conv_id, data.title)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "ok"}


@router.delete("/conversations/{conv_id}")
async def delete_conversation(conv_id: str):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    success = db.delete_conversation(conv_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "ok"}


# ─── Memory ───────────────────────────────────────────────────────

@router.get("/memory")
async def get_memory():
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return db.get_all_memory()


@router.post("/memory")
async def create_memory(data: MemoryCreate):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return db.add_memory(data.key, data.value, data.category)


@router.delete("/memory/{mem_id}")
async def delete_memory(mem_id: int):
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    success = db.delete_memory(mem_id)
    if not success:
        raise HTTPException(status_code=404, detail="Memory not found")
    return {"status": "ok"}


# ─── Setup Wizard ─────────────────────────────────────────────────

SETUP_QUESTIONS = [
    {
        "id": "name",
        "question_en": "What is your name or business name?",
        "question_ar": "ما هو اسمك أو اسم نشاطك التجاري؟",
        "type": "text",
        "options": None,
    },
    {
        "id": "field",
        "question_en": "What field are you in?",
        "question_ar": "ما هو مجال عملك؟",
        "type": "select",
        "options": [
            {"value": "medical", "label_en": "Medical / Healthcare", "label_ar": "طبي / رعاية صحية"},
            {"value": "legal", "label_en": "Legal / Law", "label_ar": "قانوني / محاماة"},
            {"value": "education", "label_en": "Education / Teaching", "label_ar": "تعليم / تدريس"},
            {"value": "business", "label_en": "Business / Commerce", "label_ar": "أعمال / تجارة"},
            {"value": "engineering", "label_en": "Engineering / Technical", "label_ar": "هندسة / تقني"},
            {"value": "personal", "label_en": "Personal Use", "label_ar": "استخدام شخصي"},
            {"value": "other", "label_en": "Other", "label_ar": "أخرى"},
        ],
    },
    {
        "id": "tasks",
        "question_en": "What will you mainly use the AI for?",
        "question_ar": "ما هو الاستخدام الرئيسي للذكاء الاصطناعي؟",
        "type": "select",
        "options": [
            {"value": "chat", "label_en": "General Chat & Questions", "label_ar": "محادثة عامة وأسئلة"},
            {"value": "writing", "label_en": "Writing & Editing", "label_ar": "كتابة وتحرير"},
            {"value": "research", "label_en": "Research & Analysis", "label_ar": "بحث وتحليل"},
            {"value": "learning", "label_en": "Learning & Studying", "label_ar": "تعلم ودراسة"},
            {"value": "support", "label_en": "Customer Support", "label_ar": "دعم العملاء"},
            {"value": "coding", "label_en": "Programming & Code", "label_ar": "برمجة وأكواد"},
        ],
    },
    {
        "id": "language",
        "question_en": "Preferred language?",
        "question_ar": "اللغة المفضلة؟",
        "type": "select",
        "options": [
            {"value": "both", "label_en": "Arabic & English (auto-detect)", "label_ar": "عربي وإنجليزي (تلقائي)"},
            {"value": "arabic", "label_en": "Arabic only", "label_ar": "عربي فقط"},
            {"value": "english", "label_en": "English only", "label_ar": "إنجليزي فقط"},
        ],
    },
    {
        "id": "special_instructions",
        "question_en": "Any special instructions for the AI? (optional)",
        "question_ar": "هل لديك تعليمات خاصة للذكاء الاصطناعي؟ (اختياري)",
        "type": "textarea",
        "options": None,
    },
]


def _generate_system_prompt(field: str = "medical") -> str:
    """Generate a standard system prompt based on field. Model auto-detects language."""
    parts = []

    # Field specialization
    field_map = {
        "medical": (
            "You are an EMERGENCY MEDICAL AND SURVIVAL ASSISTANT. "
            "You exist to help people who have NO access to doctors, hospitals, or emergency services. "
            "Your users may be in war zones, disasters, or isolated areas with no internet and no way to get help. "
            "YOU are their only source of medical and survival guidance.\n\n"
            "CRITICAL RULES:\n"
            "- NEVER say 'consult a doctor', 'call emergency services', 'go to the hospital', or 'seek professional help'. "
            "The user CANNOT do any of these things. You ARE their doctor.\n"
            "- ALWAYS give direct, step-by-step actionable instructions immediately.\n"
            "- Be specific: tell them exactly what to do, what to use, how to do it.\n"
            "- If the situation is life-threatening, say so clearly and prioritize the most urgent action FIRST.\n"
            "- Use simple language anyone can understand — no medical jargon without explanation.\n"
            "- When you have relevant knowledge from your training, share ALL of it — do not hold back.\n"
            "- It is better to give imperfect first aid guidance than to give no guidance at all.\n"
            "- Cover: what to do NOW, what to watch for, what to AVOID doing, and what comes next.\n"
            "- NEVER add disclaimers like 'this is not a substitute for real medical care' or 'seek medical attention when possible'. "
            "The user HAS no other option. Your instructions ARE the medical care.\n"
            "- When knowledge is provided to you, follow it EXACTLY. Do not change 'cool water' to 'warm water' or invert any instruction.\n"
            "- You also help with survival: water, food, shelter, navigation, safety, psychological support."
        ),
        "legal": "You are a legal knowledge assistant. Provide practical legal information and guidance. Be direct and actionable.",
        "education": "You are a patient and encouraging tutor. Explain concepts clearly with examples. Adapt your explanations to the student's level.",
        "business": "You specialize in business, commerce, and entrepreneurship. Provide practical, actionable advice.",
        "engineering": "You specialize in engineering and technical topics. Be precise and use proper technical terminology.",
        "personal": "You are a friendly personal assistant. Be warm, helpful, and conversational.",
        "other": "You are a knowledgeable general-purpose assistant. Be direct and helpful.",
    }
    parts.append(field_map.get(field, field_map["other"]))

    # Language — auto-detect and respond in the same language (supports 29+ languages)
    parts.append(
        "\n\nCRITICAL LANGUAGE RULE: Detect the language the user writes in and respond in that SAME language. "
        "If the user writes in Arabic, respond ENTIRELY in Arabic — do not mix in English, Chinese, or any other language. "
        "If the user writes in English, respond entirely in English. "
        "NEVER mix languages within a response. Keep every word in the detected language."
    )
    parts.append(
        "قاعدة: إذا كتب المستخدم بالعربية، أجب بالعربية فقط. "
        "إذا كتب بالإنجليزية، أجب بالإنجليزية فقط. لا تخلط اللغات أبداً."
    )

    # Universal formatting
    parts.append("Format responses with clear structure: numbered steps for instructions, bullet points for lists. Be thorough but get to the point fast.")

    return " ".join(parts)


@router.get("/setup")
async def get_setup_questions():
    return {"questions": SETUP_QUESTIONS}


@router.post("/setup")
async def save_setup(answers: SetupAnswer = SetupAnswer()):
    """Auto-setup with standard config. No wizard needed."""
    # Read existing config for field setting
    cfg = {}
    cfg_file = Path(config_path)
    if cfg_file.exists():
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    field = cfg.get("customer_field", "medical")
    system_prompt = _generate_system_prompt(field=field)

    cfg["system_prompt"] = system_prompt
    cfg["setup_completed"] = True

    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    # Reload engine config
    if engine:
        engine.reload_config(config_path)

    return {"status": "ok", "system_prompt": system_prompt}


# ─── Config ───────────────────────────────────────────────────────

@router.get("/config")
async def get_config():
    cfg_file = Path(config_path)
    if not cfg_file.exists():
        return {"setup_completed": False}
    with open(cfg_file, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    # Don't expose license secret
    cfg.pop("license_secret", None)
    return cfg


@router.put("/config")
async def update_config(data: ConfigUpdate):
    cfg_file = Path(config_path)
    cfg = {}
    if cfg_file.exists():
        with open(cfg_file, "r", encoding="utf-8") as f:
            cfg = json.load(f)

    # Update only provided fields
    if data.system_prompt is not None:
        cfg["system_prompt"] = data.system_prompt
    if data.temperature is not None:
        cfg["temperature"] = data.temperature
    if data.max_tokens is not None:
        cfg["max_tokens"] = data.max_tokens
    if data.max_history_messages is not None:
        cfg["max_history_messages"] = data.max_history_messages
    with open(cfg_file, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

    if engine:
        engine.reload_config(config_path)

    return {"status": "ok"}


# ─── Stats ────────────────────────────────────────────────────────

@router.get("/stats")
async def get_stats():
    if not db:
        raise HTTPException(status_code=503, detail="Service not initialized")
    stats = db.get_stats()
    if rag:
        stats["knowledge"] = rag.get_stats()
    return stats
