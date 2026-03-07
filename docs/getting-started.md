# Getting Started

Welcome to **Model Maker** — an offline AI assistant for emergency, medical, and survival situations.

## Quick Start (3 Steps)

### 1. Clone & Setup

```bash
git clone https://github.com/Maitham1988/model-maker.git
cd model-maker
bash scripts/setup.sh
```

The setup script will:
- Check Python 3.11+ is installed
- Create a virtual environment
- Install all dependencies
- Optionally download an AI model

### 2. Download a Model

If you didn't download during setup:

```bash
source .venv/bin/activate
python models/download.py
```

The downloader will:
- **Detect your device** (RAM, storage, GPU)
- **Recommend** the best model tier
- **Download** with progress bar and resume support

**Model Tiers:**

| Tier | Model | Size | RAM | Best For |
|------|-------|------|-----|----------|
| Lite | Qwen2.5-3B | 2.0 GB | 4 GB | Older phones, basic laptops |
| Standard | Qwen2.5-7B | 4.4 GB | 8 GB | Most devices (★ recommended) |
| Premium | Qwen2.5-14B | 8.5 GB | 16 GB | Powerful laptops & desktops |

### 3. Launch

```bash
cd app && python run.py
```

This opens your browser to `http://localhost:8000` with the chat interface.

## Alternative: Manual Setup

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download model (choose tier)
python models/download.py --tier standard

# Run
cd app && python run.py
```

## Using Makefile

If you have `make` installed:

```bash
make setup          # Full setup
make download-model # Download AI model
make run            # Start the app
make test           # Run tests
make help           # See all commands
```

## First Launch

On first launch:
1. The app opens in your default browser
2. You'll see the chat interface
3. Start typing — the AI responds in real-time via streaming
4. All conversations are saved locally in SQLite

## Features

- **Chat**: Ask about medical emergencies, survival, first aid, or anything
- **29 Languages**: Interface and AI support Arabic, English, French, Chinese, and 25 more
- **Memory**: The AI remembers facts you share (allergies, conditions, etc.)
- **Knowledge System**: Built-in RAG searches verified medical documents
- **Dark Theme**: Professional dark UI, easy on the eyes
- **Share**: Copy or export conversations to share knowledge

## Troubleshooting

**"Python not found"**
- Install from [python.org](https://python.org) (3.11+)

**"Model not found"**
- Run `python models/download.py` to download

**"Out of memory"**
- Use a smaller model: `python models/download.py --tier lite`

**Slow responses**
- Close other apps to free RAM
- Try the Lite model for faster responses
- On Mac, ensure Metal GPU acceleration is active

**Port already in use**
- Change the port: edit `app/run.py` or use `--port 8001`

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| Python | 3.11 | 3.12+ |
| RAM | 4 GB | 8-16 GB |
| Storage | 4 GB free | 10 GB free |
| OS | macOS 12+, Windows 10+, Linux | macOS 14+, Windows 11 |
| GPU | Not required | Apple Silicon / NVIDIA |
