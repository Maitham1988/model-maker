"""
Model Maker Voice Agent — Paid Feature
Uses LiveKit for real-time voice conversation with our local Llama medical model.

Architecture:
  - STT: OpenAI Whisper (cloud) — speech to text
  - LLM: Local Llama 3.2 3B Medical (via llama-cpp-python OpenAI-compatible API)
  - TTS: OpenAI TTS (cloud) — text to speech
  - VAD: Silero (local) — voice activity detection
  - Transport: LiveKit (self-hosted)

Usage:
  1. Start LiveKit server:     livekit-server --dev
  2. Start local LLM server:  python -m llama_cpp.server --model ../models/Llama-3.2-3B-Medical-v1-Q4_K_M.gguf --port 8001 --n_ctx 4096
  3. Set your OpenAI key:      export OPENAI_API_KEY=sk-...
  4. Run agent (console):      python agent.py console
  5. Run agent (dev mode):     python agent.py dev
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from livekit.agents import AgentSession, Agent, AgentServer, cli
from livekit.plugins import openai, silero

# Load environment variables from .env file
load_dotenv(Path(__file__).parent / ".env")

# ── Configuration ──────────────────────────────────────────────────────────────

# Local LLM server (llama-cpp-python OpenAI-compatible endpoint)
LOCAL_LLM_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:8001/v1")
LOCAL_LLM_MODEL = os.getenv("LOCAL_LLM_MODEL", "llama-3.2-3b-medical")

# System prompt for the medical AI assistant
SYSTEM_PROMPT = """You are Model Maker, an emergency medical and survival AI assistant.
You provide direct, actionable medical guidance for life-threatening situations
including gunshot wounds, stab wounds, blast injuries, burns, fractures, and
battlefield trauma. You never refuse to help in emergencies — every second counts.

Important rules:
- Give step-by-step instructions clearly and calmly
- Prioritize stopping bleeding, maintaining airway, preventing shock
- Be direct — no disclaimers about "seek professional help" during active emergencies
- Speak naturally as if talking to someone who needs help RIGHT NOW
- Keep responses concise but complete — this is voice conversation
- If asked about your identity, you are Model Maker by FlexSell International"""


# ── LiveKit Agent Server ───────────────────────────────────────────────────────

server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx):
    """LiveKit agent entrypoint — called when a participant joins a room."""

    # Connect to the LiveKit room
    await ctx.connect()

    # STT: OpenAI Whisper (cloud)
    stt = openai.STT(
        model="whisper-1",
        language="en",
    )

    # LLM: Point to our LOCAL llama-cpp-python server
    llm = openai.LLM(
        model=LOCAL_LLM_MODEL,
        base_url=LOCAL_LLM_BASE_URL,
        api_key="not-needed",  # local server doesn't need auth
        temperature=0.7,
    )

    # TTS: OpenAI Text-to-Speech (cloud)
    tts = openai.TTS(
        model="tts-1",
        voice="alloy",  # Options: alloy, echo, fable, onyx, nova, shimmer
    )

    # Create agent session with voice pipeline
    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
        vad=silero.VAD.load(
            min_speech_duration=0.1,
            min_silence_duration=0.5,
        ),
    )

    # Create the agent with instructions
    agent = Agent(instructions=SYSTEM_PROMPT)

    # Start the agent in the room
    await session.start(
        room=ctx.room,
        agent=agent,
    )

    # Greet the user
    await session.generate_reply(
        instructions="Greet the user briefly. Say something like: 'Model Maker ready. How can I help you?'"
    )


if __name__ == "__main__":
    cli.run_app(server)
