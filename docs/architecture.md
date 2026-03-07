# Architecture

## Overview

Model Maker is a **fully offline AI chat application** built with a clean three-layer architecture:

```
┌─────────────────────────────────────────────┐
│                  Frontend                    │
│           (HTML/CSS/JS — Dark UI)           │
│   Chat interface, i18n, streaming display    │
├─────────────────────────────────────────────┤
│               FastAPI Backend                │
│       Routes, SSE Streaming, Database        │
├──────────┬──────────────┬───────────────────┤
│ LLM      │ Knowledge    │ Database           │
│ Engine   │ RAG System   │ (SQLite)           │
│          │              │                    │
│ llama-   │ ONNX +       │ Conversations      │
│ cpp-     │ MiniLM-L6    │ Messages           │
│ python   │ Embeddings   │ Memory             │
├──────────┴──────────────┴───────────────────┤
│              GGUF Model File                 │
│         (Qwen2.5 — 3B/7B/14B)              │
└─────────────────────────────────────────────┘
```

## Directory Structure

```
model-maker/
├── app/                     # Main application
│   ├── backend/             # FastAPI server
│   │   ├── main.py          # Entry point, ASGI app
│   │   ├── routes.py        # API endpoints
│   │   ├── llm_engine.py    # LLM wrapper + streaming
│   │   ├── knowledge_rag.py # RAG search + Arabic bridge
│   │   ├── database.py      # SQLite operations
│   │   ├── models.py        # Pydantic schemas
│   │   └── license_check.py # Device-locked licensing
│   ├── frontend/            # Web interface
│   │   ├── index.html       # Single page app
│   │   ├── app.js           # Chat client + SSE
│   │   ├── style.css        # Dark theme
│   │   └── translations.js  # 28 language translations
│   ├── knowledge/           # RAG knowledge base (markdown)
│   ├── run.py               # One-click launcher
│   └── config.json          # Runtime configuration
├── models/                  # AI model management
│   ├── registry.json        # Model catalog + requirements
│   ├── download.py          # Smart model downloader
│   └── *.gguf               # Model files (gitignored)
├── website/                 # Public website (S3/CloudFront)
├── training/                # Fine-tuning pipeline
├── tools/                   # Developer utilities
├── tests/                   # Test suite
├── docs/                    # Documentation
└── scripts/                 # Build & setup scripts
```

## Components

### Frontend (app/frontend/)

- **Technology**: Vanilla HTML/CSS/JS — no framework
- **Why**: Zero build step, works offline, tiny size
- **Features**: Dark theme, streaming display, RTL support
- **i18n**: 28 languages via translations.js
- **Communication**: SSE (Server-Sent Events) for streaming

### Backend (app/backend/)

- **Technology**: FastAPI + uvicorn
- **Entry Point**: `main.py` creates the ASGI app
- **API**: RESTful with SSE streaming for chat
- **Database**: SQLite via `database.py`
- **Config**: JSON-based configuration

### LLM Engine (app/backend/llm_engine.py)

- **Wrapper**: `llama-cpp-python` binding
- **Models**: Qwen2.5 family (3B, 7B, 14B) in GGUF format
- **Streaming**: Token-by-token via generator
- **GPU**: Metal (Apple Silicon), CUDA (NVIDIA), CPU fallback
- **Context**: 4096 tokens default

### Knowledge RAG (app/backend/knowledge_rag.py)

- **Embeddings**: all-MiniLM-L6-v2 (ONNX Runtime)
- **Chunks**: Markdown split into ~500-char segments
- **Search**: Cosine similarity over embedding vectors
- **Arabic Bridge**: 90+ medical term mappings (Arabic → English)
- **Treatment Boost**: Extra weight for treatment-related chunks

### Database (app/backend/database.py)

```
SQLite
├── conversations (id, title, created_at)
├── messages (id, conversation_id, role, content, created_at)
└── memory (id, fact, category, created_at)
```

### Model Registry (models/)

- **registry.json**: Catalog of available models with:
  - Download URLs (HuggingFace)
  - Size and RAM requirements
  - Device presets (phone/computer models)
  - Quality ratings
- **download.py**: Smart downloader with:
  - Device detection (RAM, storage, GPU)
  - Tier recommendation
  - Progress bar + resume support
  - SHA256 verification

## Data Flow

### Chat Request

```
User types message
       │
       ▼
   Frontend (app.js)
   POST /api/chat
       │
       ▼
   FastAPI Router (routes.py)
       │
       ├── Search Knowledge Base (knowledge_rag.py)
       │   └── Embed query → cosine search → top 3 chunks
       │
       ├── Load Memory Facts (database.py)
       │
       ├── Build Prompt
       │   └── System prompt + memory + knowledge + history
       │
       └── Stream to LLM (llm_engine.py)
           └── Token-by-token generation
                │
                ▼
           SSE EventSource → Frontend updates display
                │
                ▼
           Save to SQLite (database.py)
```

### Arabic Cross-Language Search

```
Arabic query: "كيف أوقف النزيف"
       │
       ▼
   Arabic Bridge Maps:
   نزيف → bleeding, hemorrhage
       │
       ▼
   Combined embedding: Arabic + English terms
       │
       ▼
   Cosine search → finds English chunks about bleeding
       │
       ▼
   AI responds in Arabic (using English knowledge)
```

## Security Model

- **No network**: App binds to localhost only (127.0.0.1)
- **No telemetry**: Zero data collection
- **Local storage**: All data in SQLite on disk
- **License**: HMAC-SHA256 device lock (optional)
- **No dependencies on external services**

## Deployment

### Development
```bash
make run  # or: cd app && python run.py
```

### Production (Customer)
```bash
# Package
make build

# Delivers: dist/model-maker/
#   ├── app/           (application)
#   ├── registry.json  (model catalog)
#   ├── download.py    (model downloader)
#   └── setup.sh       (first-time setup)
```

### Website
```bash
# Local preview
make website

# Production deploy (S3 + CloudFront)
# Automated via .github/workflows/deploy-website.yml
```
