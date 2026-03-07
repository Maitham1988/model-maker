# GitHub Copilot Instructions for Model Maker

## Project Overview

**Model Maker** is a free, open-source offline AI assistant for emergency, medical, and
survival situations. It runs 100% offline on the user's device — no internet required.

**License**: Apache 2.0 — Free forever
**Created**: March 2026
**Owner**: Maitham (FlexSell International W.L.L)
**Language**: Python 3.11+
**Target Users**: Global — 29 languages, Arabic + English primary
**GitHub**: https://github.com/Maitham1988/model-maker

---

## Architecture

```
model-maker/
├── .github/                    ← CI/CD, issue templates, Copilot config
│   └── workflows/              ← GitHub Actions (CI, release, website deploy)
├── app/                        ← Main application
│   ├── backend/                ← FastAPI + llama-cpp-python
│   │   ├── main.py             ← Entry point, mounts static + API
│   │   ├── llm_engine.py       ← LLM wrapper (streaming, context)
│   │   ├── knowledge_rag.py    ← ONNX RAG + Arabic bridge
│   │   ├── database.py         ← SQLite (conversations, messages, memory)
│   │   ├── routes.py           ← API endpoints
│   │   ├── models.py           ← Pydantic schemas
│   │   └── license_check.py    ← Device-locked license (optional)
│   ├── frontend/               ← ChatGPT-like dark UI
│   │   ├── index.html          ← Single page app
│   │   ├── style.css           ← Dark theme
│   │   ├── app.js              ← Chat client + SSE streaming + share
│   │   └── translations.js     ← 28 language translations
│   ├── knowledge/              ← Medical/survival markdown files (RAG)
│   ├── run.py                  ← One-click launcher
│   └── config.json             ← Runtime config (model path, settings)
├── models/                     ← Model management
│   ├── registry.json           ← Model catalog (tiers, URLs, requirements)
│   ├── download.py             ← Smart downloader with device detection
│   └── *.gguf                  ← Model files (gitignored)
├── website/                    ← Public website (S3/CloudFront)
│   ├── index.html              ← Landing page (28 languages)
│   ├── css/style.css           ← Dark theme
│   └── js/                     ← i18n, hardware checker, main
├── training/                   ← Fine-tuning pipeline
├── tools/                      ← Developer utilities
├── tests/                      ← Test suite
├── docs/                       ← Documentation
├── scripts/                    ← Build & setup scripts
├── pyproject.toml              ← Python packaging
├── Makefile                    ← Common commands
└── requirements.txt            ← Python dependencies
```

---

## Tech Stack

| Component | Tool | Version |
| --- | --- | --- |
| LLM Engine | llama-cpp-python | Latest |
| Backend | FastAPI + uvicorn | 0.100+ |
| Frontend | Vanilla HTML/CSS/JS | No framework |
| Database | SQLite3 | Built-in |
| Streaming | Server-Sent Events (SSE) | Native |
| RAG | ONNX Runtime + MiniLM | 384-dim embeddings |
| Packaging | pyproject.toml + Makefile | Modern Python |
| CI/CD | GitHub Actions | Multi-platform |
| Website | Static HTML + CloudFront | S3 hosted |

---

## Models Supported

| Model | Tier | Size | RAM | Languages | Use Case |
| --- | --- | --- | --- | --- | --- |
| Qwen2.5-3B-Instruct (Q4_K_M) | Lite | 2.0 GB | 4 GB | 29 | Basic devices |
| Qwen2.5-7B-Instruct (Q4_K_M) | Standard | 4.4 GB | 8 GB | 29 | Most users ★ |
| Qwen2.5-14B-Instruct (Q4_K_M) | Premium | 8.5 GB | 16 GB | 29 | Best quality |

All models use GGUF format from Hugging Face.

---

## API Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| POST | /api/chat | Send message, get SSE stream response |
| GET | /api/conversations | List all conversations |
| POST | /api/conversations | Create new conversation |
| GET | /api/conversations/{id}/messages | Get messages for conversation |
| PUT | /api/conversations/{id} | Rename conversation |
| DELETE | /api/conversations/{id} | Delete conversation |
| GET | /api/setup | Get setup wizard questions |
| POST | /api/setup | Save system prompt from wizard answers |
| GET | /api/config | Get current config |
| PUT | /api/config | Update config (system prompt, etc.) |
| GET | /api/memory | Get persistent memory facts |
| POST | /api/memory | Save a memory fact |
| DELETE | /api/memory/{id} | Delete a memory fact |

---

## Code Standards

- Python 3.11+ with type hints
- Async FastAPI routes
- Pydantic v2 models for request/response
- SQLite for all persistence (zero setup)
- No external services — everything runs locally
- Error handling with proper HTTP status codes

---

## License System

- Hardware ID = SHA256(MAC address + hostname + disk serial)
- License key = HMAC-SHA256(hardware_id, secret_key)
- Checked on every app launch
- Customer cannot copy to another device

---

## Customer Installation Flow

1. User downloads from website or GitHub
2. Runs `scripts/setup.sh` (or `make setup`)
3. Runs `python models/download.py` to get AI model
4. Runs `python app/run.py` → opens browser → setup wizard
5. Chat ready to use — no internet needed after initial download

---

## Critical Rules

- ❌ NEVER require internet for any feature after initial setup
- ❌ NEVER send data outside the local machine
- ❌ NEVER hardcode model paths — always use config.json
- ❌ NEVER add paid dependencies or proprietary code
- ✅ ALWAYS use streaming (SSE) for chat responses
- ✅ ALWAYS save conversations to SQLite
- ✅ ALWAYS support Arabic + English (RTL + LTR)
- ✅ ALWAYS keep the app runnable with zero configuration
- ✅ ALWAYS test on Mac, Windows, and Linux
