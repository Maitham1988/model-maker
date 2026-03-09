"""
Voice API Routes — Push-to-talk voice conversation endpoints.
All processing is 100% offline using Whisper STT + Piper TTS + local LLM.
"""

from __future__ import annotations

import time

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response

from .database import Database
from .llm_engine import LLMEngine
from .voice_engine import VoiceEngine

voice_router = APIRouter(prefix="/api/voice")

# These will be injected by main.py
db: Database | None = None
engine: LLMEngine | None = None
voice: VoiceEngine | None = None


def init_voice(
    database: Database,
    llm_engine: LLMEngine | None,
    voice_engine: VoiceEngine | None,
):
    """Initialize voice routes with shared instances."""
    global db, engine, voice
    db = database
    engine = llm_engine
    voice = voice_engine


@voice_router.get("/status")
async def voice_status():
    """Check if voice features are available."""
    return {
        "available": voice is not None and voice.is_ready,
        "stt_ready": voice.has_stt if voice else False,
        "tts_ready": voice.has_tts if voice else False,
    }


@voice_router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe speech audio to text.

    Accepts audio file (WAV, WebM, or raw PCM).
    Returns transcribed text.
    """
    if not voice or not voice.has_stt:
        raise HTTPException(status_code=503, detail="STT not available")

    audio_bytes = await audio.read()
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio data")

    start = time.time()
    text = voice.transcribe(audio_bytes)
    elapsed = time.time() - start

    return {
        "text": text,
        "duration_ms": int(elapsed * 1000),
    }


@voice_router.post("/speak")
async def speak_text(text: str):
    """Convert text to speech audio.

    Returns WAV audio file.
    """
    if not voice or not voice.has_tts:
        raise HTTPException(status_code=503, detail="TTS not available")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty text")

    start = time.time()
    wav_bytes, sample_rate = voice.synthesize(text)
    elapsed = time.time() - start

    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={
            "X-Duration-Ms": str(int(elapsed * 1000)),
            "X-Sample-Rate": str(sample_rate),
        },
    )


@voice_router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    conversation_id: str = "",
):
    """Full voice conversation: Speech → Text → LLM → Speech.

    1. Transcribes audio (Whisper)
    2. Sends to LLM (local Llama)
    3. Synthesizes response (Piper TTS)
    4. Returns both audio + text

    Args:
        audio: Audio file from microphone
        conversation_id: Optional conversation ID for context

    Returns:
        WAV audio response with text in headers.
    """
    if not voice or not voice.is_ready:
        raise HTTPException(status_code=503, detail="Voice engine not ready")
    if not engine:
        raise HTTPException(status_code=503, detail="LLM not loaded")
    if not db:
        raise HTTPException(status_code=503, detail="Database not initialized")

    total_start = time.time()

    # ── Step 1: Transcribe speech to text ──
    audio_bytes = await audio.read()
    if not audio_bytes or len(audio_bytes) < 100:
        raise HTTPException(status_code=400, detail="Audio too short or empty")

    stt_start = time.time()
    user_text = voice.transcribe(audio_bytes)
    stt_time = time.time() - stt_start

    if not user_text.strip():
        raise HTTPException(status_code=400, detail="Could not understand speech")

    # ── Step 2: Get/create conversation ──
    if conversation_id:
        conv = db.get_conversation(conversation_id)
        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conv = db.create_conversation("Voice Chat")
        conversation_id = conv["id"]

    # Save user message
    db.add_message(conversation_id, "user", user_text)

    # Build message history
    recent = db.get_recent_messages(conversation_id, limit=10)
    messages = [{"role": m["role"], "content": m["content"]} for m in recent]

    # Get memory context
    memory_context = db.get_memory_context()

    # ── Step 3: Generate LLM response (non-streaming for voice) ──
    llm_start = time.time()

    # Build system prompt
    config = engine.config
    system_prompt = config.get("system_prompt", "You are a helpful assistant.")

    if memory_context:
        system_prompt += f"\n\n[Memory]\n{memory_context}"

    # Add voice-specific instruction
    system_prompt += (
        "\n\n[Voice Mode] You are in a voice conversation. "
        "Keep responses concise (2-4 sentences). "
        "Speak naturally as if talking. No markdown or formatting."
    )

    # Collect full response (non-streaming for TTS)
    full_response = ""
    for token in engine.chat(messages, system_prompt):
        full_response += token

    llm_time = time.time() - llm_start

    # Save assistant message
    db.add_message(conversation_id, "assistant", full_response)

    # ── Step 4: Synthesize response to speech ──
    tts_start = time.time()

    if voice.has_tts:
        wav_bytes, sample_rate = voice.synthesize(full_response)
    else:
        # No TTS — return text only
        return {
            "text": full_response,
            "user_text": user_text,
            "conversation_id": conversation_id,
            "timing": {
                "stt_ms": int(stt_time * 1000),
                "llm_ms": int(llm_time * 1000),
                "total_ms": int((time.time() - total_start) * 1000),
            },
        }

    tts_time = time.time() - tts_start
    total_time = time.time() - total_start

    return Response(
        content=wav_bytes,
        media_type="audio/wav",
        headers={
            "X-User-Text": user_text.replace("\n", " ")[:500],
            "X-Response-Text": full_response.replace("\n", " ")[:500],
            "X-Conversation-Id": conversation_id,
            "X-STT-Ms": str(int(stt_time * 1000)),
            "X-LLM-Ms": str(int(llm_time * 1000)),
            "X-TTS-Ms": str(int(tts_time * 1000)),
            "X-Total-Ms": str(int(total_time * 1000)),
            "Access-Control-Expose-Headers": (
                "X-User-Text, X-Response-Text, X-Conversation-Id, "
                "X-STT-Ms, X-LLM-Ms, X-TTS-Ms, X-Total-Ms"
            ),
        },
    )
