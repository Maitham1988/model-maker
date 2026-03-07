# Changelog

All notable changes to Model Maker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-06

### Added

- **Offline AI Chat** — Full conversational AI powered by Qwen2.5 (GGUF), running 100% offline
- **3-Tier Model System** — Lite (3B), Standard (7B), Premium (14B) for different hardware capabilities
- **Medical & Survival Knowledge** — RAG system with ONNX embeddings covering emergency topics
- **Arabic Cross-Language Search** — 90+ medical term Arabic→English bridge for RAG queries
- **28 Language Support** — UI translations for Arabic, English, French, Spanish, Hindi, Chinese, and 22 more
- **Setup Wizard** — Interactive onboarding to customize the AI assistant for user's situation
- **Conversation Management** — Create, rename, delete conversations stored in SQLite
- **Persistent Memory** — Save facts the AI remembers across conversations
- **SSE Streaming** — Real-time token-by-token response streaming
- **Share Feature** — Copy messages, share via Web Share API, export full conversations
- **Dark Theme UI** — ChatGPT-like interface with RTL support
- **Smart Model Downloader** — Auto-detects hardware, recommends best model tier, resumes downloads
- **Website** — Public landing page with hardware checker, 28 languages, download guide
- **CI/CD Pipeline** — GitHub Actions for testing, releases, and website deployment
- **Documentation** — Getting started guide, architecture docs, API reference

### Technical

- FastAPI + uvicorn backend with async routes
- llama-cpp-python with Metal (macOS) and CUDA (Linux/Windows) GPU acceleration
- ONNX Runtime + all-MiniLM-L6-v2 for 384-dim embeddings
- SQLite3 for all persistence (zero configuration)
- Vanilla HTML/CSS/JS frontend (no framework dependencies)
- pyproject.toml with ruff, pytest, mypy configuration
- Cross-platform: macOS, Windows, Linux

[1.0.0]: https://github.com/Maitham1988/model-maker/releases/tag/v1.0.0
