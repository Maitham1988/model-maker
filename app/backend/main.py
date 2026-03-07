"""
FastAPI Application Entry Point
Mounts static frontend, includes API router, initializes engine + database.
"""

import json
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ── Paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent          # app/
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

# ── FastAPI App ─────────────────────────────────────────────────────
app = FastAPI(
    title="Local AI Chat",
    version="1.0.0",
    docs_url=None,       # Disable Swagger in production
    redoc_url=None,
)

# ── API Router ──────────────────────────────────────────────────────
from backend.routes import router, init as routes_init  # noqa: E402
routes_init(database=db, llm_engine=engine, cfg_path=str(CONFIG_PATH), knowledge_rag=rag)
app.include_router(router)

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
