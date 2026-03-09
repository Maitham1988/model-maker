"""
FastAPI Application Entry Point
Mounts static frontend, includes API router, initializes engine + database.
"""

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# ── Paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent  # app/
CONFIG_PATH = BASE_DIR / "config.json"
FRONTEND_DIR = BASE_DIR / "frontend"
DATA_DIR = BASE_DIR / "data"

# ── Load Config ─────────────────────────────────────────────────────
if not CONFIG_PATH.exists():
    # Copy template if available
    template = BASE_DIR / "config_template.json"
    if template.exists():
        import shutil

        shutil.copy(template, CONFIG_PATH)
        print("📋 Created config.json from template")
    else:
        print("❌ config.json not found. Run: make setup")
        sys.exit(1)

with open(CONFIG_PATH) as f:
    config = json.load(f)

# ── License Check (optional) ────────────────────────────────────────
# License enforcement is optional for open-source usage.
# Set "license_key" in config.json to enable device-locked licensing.
if config.get("license_key"):
    try:
        from backend.license_check import verify_license  # noqa: E402

        ok, msg = verify_license(str(CONFIG_PATH))
        if not ok:
            print(f"⚠️  License: {msg}")
        else:
            print(f"✅ License: {msg}")
    except Exception as e:
        print(f"⚠️  License check skipped: {e}")

# ── Database ────────────────────────────────────────────────────────
DATA_DIR.mkdir(parents=True, exist_ok=True)
db_path = DATA_DIR / "chat.db"

from backend.database import Database  # noqa: E402

db = Database(str(db_path))

# ── LLM Engine ──────────────────────────────────────────────────────
model_path = config.get("model_path", "")
if not model_path or not Path(model_path).exists():
    # Try resolving relative to app/ directory
    resolved = BASE_DIR / model_path if model_path else Path("")
    if not resolved.exists():
        print(f"⚠️  Model not found at: {model_path}")
        print("   The server will start but chat won't work until model is set.")
        engine = None
    else:
        model_path = str(resolved)

if model_path and Path(model_path).exists():
    from backend.llm_engine import LLMEngine  # noqa: E402

    engine = LLMEngine(config_path=str(CONFIG_PATH))
    print(f"✅ Model loaded: {Path(model_path).name}")
else:
    engine = None

# ── Knowledge RAG ───────────────────────────────────────────────────
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
EMBEDDING_MODEL_DIR = BASE_DIR.parent / "models" / "embedding" / "all-MiniLM-L6-v2"

rag = None
try:
    from backend.knowledge_rag import KnowledgeRAG  # noqa: E402

    rag = KnowledgeRAG(
        knowledge_dir=str(KNOWLEDGE_DIR),
        embedding_model_dir=str(EMBEDDING_MODEL_DIR),
    )
    if not rag.is_ready:
        print("⚠️  RAG loaded but no knowledge indexed — check knowledge/ folder")
        rag = None
except Exception as e:
    print(f"⚠️  Knowledge RAG not available: {e}")
    rag = None

# ── Voice Engine (offline STT + TTS) ───────────────────────────────
VOICE_MODEL_DIR = BASE_DIR.parent / "models" / "voice"
PIPER_VOICE = VOICE_MODEL_DIR / "en_US-lessac-medium.onnx"

voice_engine = None
try:
    from backend.voice_engine import VoiceEngine  # noqa: E402

    voice_engine = VoiceEngine(
        whisper_model="base",
        piper_voice_path=str(PIPER_VOICE) if PIPER_VOICE.exists() else None,
    )
    voice_engine.load()
except Exception as e:
    print(f"⚠️  Voice engine not available: {e}")
    voice_engine = None

# ── FastAPI App ─────────────────────────────────────────────────────
app = FastAPI(
    title="Model Maker — Local AI",
    version="1.0.0",
    docs_url=None,  # Disable Swagger in production
    redoc_url=None,
    openapi_url=None,  # Disable OpenAPI schema endpoint
)

# ── Security Middleware ─────────────────────────────────────────────
# Only accept connections from localhost (this is an offline app)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1"])

# Rate limiting (per-IP, in-memory — prevents abuse from local malware)
_rate_limit: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT_MAX = 60  # max requests
RATE_LIMIT_WINDOW = 60  # per window (seconds)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """Add security headers and rate limiting to all responses."""
    # Rate limit (skip static files)
    if request.url.path.startswith("/api"):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window = [t for t in _rate_limit[client_ip] if now - t < RATE_LIMIT_WINDOW]
        _rate_limit[client_ip] = window
        if len(window) >= RATE_LIMIT_MAX:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Try again later."},
            )
        _rate_limit[client_ip].append(now)

    response: Response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(self), geolocation=(), payment=()"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "media-src 'self' blob:; "
        "font-src 'self'; "
        "frame-ancestors 'none'"
    )
    # Prevent caching of API responses
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        response.headers["Pragma"] = "no-cache"

    return response


# ── API Router ──────────────────────────────────────────────────────
from backend.routes import init as routes_init  # noqa: E402
from backend.routes import router  # noqa: E402

routes_init(database=db, llm_engine=engine, cfg_path=str(CONFIG_PATH), knowledge_rag=rag)
app.include_router(router)

# ── Voice Router ────────────────────────────────────────────────────
from backend.voice_routes import init_voice, voice_router  # noqa: E402

init_voice(database=db, llm_engine=engine, voice_engine=voice_engine)
app.include_router(voice_router)

# ── Static Frontend ─────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def serve_index():
    """Serve the main chat UI."""
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model_loaded": engine is not None,
        "setup_completed": config.get("setup_completed", False),
    }
