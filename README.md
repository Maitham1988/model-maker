<p align="center">
  <img src="website/assets/logo.svg" alt="Model Maker" width="120" />
</p>

<h1 align="center">Model Maker</h1>

<p align="center">
  <strong>Offline AI for everyone. No internet. No cloud. No tracking.</strong><br>
  Emergency medical &amp; survival assistant that runs 100% on your device.
</p>

<p align="center">
  <a href="https://github.com/Maitham1988/model-maker/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/Maitham1988/model-maker/ci.yml?style=flat-square&label=CI" alt="CI" /></a>
  <a href="https://github.com/Maitham1988/model-maker/releases"><img src="https://img.shields.io/github/v/release/Maitham1988/model-maker?style=flat-square" alt="Release" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square" alt="License" /></a>
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/platforms-macOS%20|%20Windows%20|%20Linux-lightgrey?style=flat-square" alt="Platforms" />
  <a href="https://github.com/Maitham1988/model-maker/stargazers"><img src="https://img.shields.io/github/stars/Maitham1988/model-maker?style=flat-square" alt="Stars" /></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome" /></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#supported-platforms">Platforms</a> •
  <a href="#languages">Languages</a> •
  <a href="#contributing">Contributing</a> •
  <a href="docs/">Docs</a>
</p>

---

## Why Model Maker?

**When disaster strikes, the internet goes down first.** In war zones, natural disasters, and remote areas, people lose access to search engines, hospitals, and emergency services — exactly when they need help the most.

Model Maker puts a trained AI doctor and survival expert directly on your device. It works without internet, without cloud servers, without any external connection. Your data never leaves your device.

> *"This started on day 3 of a war. The question was simple: if we lose internet, if we lose access to hospitals — what do we do?"*
> — Maitham, Founder

## Features

- **100% Offline** — No internet required. Ever. Works in airplane mode, in a bunker, in a blackout.
- **Emergency Medical AI** — Trained on verified medical knowledge: burns, bleeding, CPR, fractures, poisoning, shock, and more.
- **Survival Knowledge** — Water purification, shelter building, fire starting, navigation, rescue signals.
- **28 Languages** — Arabic, English, Chinese, Japanese, Korean, French, Spanish, Portuguese, German, Italian, Russian, Dutch, Polish, Czech, Turkish, Vietnamese, Thai, Indonesian, Swedish, Danish, Norwegian, Finnish, Hungarian, Greek, Romanian, Ukrainian, Hebrew, Hindi.
- **Privacy First** — Zero telemetry. Zero tracking. Your conversations stay on your device.
- **Myth Protection** — Actively warns against dangerous medical myths (butter on burns, sucking snake venom, etc.)
- **Smart Hardware Detection** — Recommends the right model for your device's RAM and storage.
- **Open Source** — Apache 2.0 licensed. Inspect, modify, and share the code.

## Quick Start

### One-Line Install (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/Maitham1988/model-maker/main/scripts/install.sh | bash
```

### Run from Source

```bash
# Clone the repository
git clone https://github.com/Maitham1988/model-maker.git
cd model-maker

# Set up (auto-installs Python deps + downloads model)
make setup

# Run
make run
```

Or manually:

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Download a model (choose your tier)
python models/download.py --tier standard  # 4.5GB, needs 8GB RAM

# Start the app
cd app && python run.py
```

Open **http://127.0.0.1:8000** in your browser.

### Docker

```bash
git clone https://github.com/Maitham1988/model-maker.git
cd model-maker

# Download a model first
python models/download.py --tier standard

# Run with Docker Compose
docker compose up -d

# Open http://localhost:8000
```

## Supported Platforms

| Platform | Status | Min RAM | Min Storage |
|----------|--------|---------|-------------|
| **macOS** (Apple Silicon) | ✅ Ready | 8 GB | 6 GB |
| **macOS** (Intel) | ✅ Ready | 8 GB | 6 GB |
| **Windows** 10/11 | ✅ Ready | 8 GB | 6 GB |
| **Linux** (Ubuntu 20+) | ✅ Ready | 8 GB | 6 GB |
| **iOS** (iPhone/iPad) | 🔄 Planned | 6 GB | 6 GB |
| **Android** | 🔄 Planned | 6 GB | 6 GB |
| **HarmonyOS** (Huawei) | 🔄 Planned | 6 GB | 6 GB |

## Model Tiers

Choose the right model for your hardware:

| Tier | Model | Size | Min RAM | Languages | Quality |
|------|-------|------|---------|-----------|---------|
| **Lite** | Qwen2.5-3B | ~2 GB | 4 GB | 29 | ★★★☆☆ |
| **Standard** | Qwen2.5-7B | ~4.5 GB | 8 GB | 29 | ★★★★☆ |
| **Premium** | Qwen2.5-14B | ~8.5 GB | 16 GB | 29 | ★★★★★ |

All models are fine-tuned specifically for emergency medical and survival scenarios.

## Languages

<details>
<summary>28 supported languages (click to expand)</summary>

| Language | Code | Direction |
|----------|------|-----------|
| English | en | LTR |
| العربية (Arabic) | ar | RTL |
| 中文 (Chinese) | zh | LTR |
| 日本語 (Japanese) | ja | LTR |
| 한국어 (Korean) | ko | LTR |
| Français (French) | fr | LTR |
| Español (Spanish) | es | LTR |
| Português (Portuguese) | pt | LTR |
| Deutsch (German) | de | LTR |
| Italiano (Italian) | it | LTR |
| Русский (Russian) | ru | LTR |
| Nederlands (Dutch) | nl | LTR |
| Polski (Polish) | pl | LTR |
| Čeština (Czech) | cs | LTR |
| Türkçe (Turkish) | tr | LTR |
| Tiếng Việt (Vietnamese) | vi | LTR |
| ไทย (Thai) | th | LTR |
| Bahasa Indonesia | id | LTR |
| Svenska (Swedish) | sv | LTR |
| Dansk (Danish) | da | LTR |
| Norsk (Norwegian) | no | LTR |
| Suomi (Finnish) | fi | LTR |
| Magyar (Hungarian) | hu | LTR |
| Ελληνικά (Greek) | el | LTR |
| Română (Romanian) | ro | LTR |
| Українська (Ukrainian) | uk | LTR |
| עברית (Hebrew) | he | RTL |
| हिन्दी (Hindi) | hi | LTR |

</details>

## Architecture

```
model-maker/
├── app/                    # Main application
│   ├── backend/            # FastAPI + llama-cpp-python
│   ├── frontend/           # Chat UI (HTML/CSS/JS)
│   ├── knowledge/          # Verified medical/survival data
│   └── run.py              # One-click launcher
├── website/                # Public website (S3/CloudFront)
├── models/                 # Model registry + downloader
├── training/               # Fine-tuning pipeline
├── docs/                   # Documentation
├── scripts/                # Build & deploy scripts
└── tests/                  # Automated tests
```

See [docs/architecture.md](docs/architecture.md) for the full technical overview.

## Contributing

We need your help! This project can save lives, and every contribution matters.

**Ways to contribute:**
- 🩺 **Medical knowledge** — Review and improve medical accuracy
- 🌍 **Translations** — Improve language support
- 💻 **Code** — Features, bug fixes, platform support
- 📖 **Documentation** — Help others get started
- 🧪 **Testing** — Report issues, test on different devices
- 📢 **Spread the word** — Share with communities that need this

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Roadmap

- [x] Core chat engine with streaming
- [x] RAG knowledge system (131 chunks, 8 knowledge files)
- [x] Arabic ↔ English cross-lingual search
- [x] 28-language UI
- [x] Automated medical accuracy testing
- [x] Fine-tuning pipeline (QLoRA on Apple Silicon)
- [ ] Mobile apps (iOS, Android, HarmonyOS)
- [ ] Offline voice input
- [ ] Offline image recognition (wound/burn classification)
- [ ] Community knowledge sharing
- [ ] Custom knowledge packs (car repair, farming, etc.)
- [ ] Government/NGO distribution partnerships

## License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

Open source. Modify, distribute, and use commercially under Apache 2.0.

## Acknowledgments

- **Qwen team** (Alibaba) for the multilingual LLM
- **llama.cpp** for efficient local inference
- **sentence-transformers** for embedding models
- The open-source community
- Everyone who shared survival knowledge

---

<p align="center">
  <strong>Built with urgency. Built to save lives.</strong><br>
  <em>Apache 2.0 — Open Source</em><br><br>
  <a href="https://github.com/Maitham1988/model-maker">⭐ Star this repo</a> •
  <a href="https://github.com/Maitham1988/model-maker/issues">Report Issue</a> •
  <a href="https://github.com/Maitham1988/model-maker/discussions">Discuss</a>
</p>
