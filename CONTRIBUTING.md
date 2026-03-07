# Contributing to Model Maker

Thank you for your interest in contributing to Model Maker! This project can save lives, and every contribution matters — whether it's code, medical knowledge, translations, or simply spreading the word.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Help?](#how-can-i-help)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Pull Request Process](#pull-request-process)
- [Medical Knowledge Guidelines](#medical-knowledge-guidelines)
- [Translation Guidelines](#translation-guidelines)

## Code of Conduct

This project follows our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold a welcoming, respectful environment for everyone.

## How Can I Help?

### 🩺 Medical Knowledge (High Impact)
- Review existing medical content for accuracy
- Add new emergency scenarios
- Verify treatment protocols against current guidelines
- Flag dangerous or outdated information

### 🌍 Translations (High Impact)
- Improve existing translations in any of our 28 languages
- Add new languages
- Review RTL language support (Arabic, Hebrew)

### 💻 Code
- Bug fixes
- New features (see [Issues](https://github.com/Maitham1988/model-maker/issues))
- Performance improvements
- Platform support (iOS, Android, HarmonyOS)
- Test coverage

### 📖 Documentation
- Improve setup guides
- Add tutorials
- Translate documentation

### 🧪 Testing
- Test on different devices and OS versions
- Report bugs with detailed reproduction steps
- Test medical accuracy in your language

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/model-maker.git
   cd model-maker
   ```
3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Requirements
- Python 3.11+
- macOS / Windows / Linux
- 8 GB RAM minimum (for running the model)
- ~10 GB disk space (model + dependencies)

### Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download embedding model (for RAG)
python models/download.py --component embeddings

# Download LLM (choose tier based on your RAM)
python models/download.py --tier standard  # 8GB+ RAM
python models/download.py --tier lite      # 4GB+ RAM

# Run the app
cd app && python run.py

# Run tests
make test
```

## Project Structure

```
model-maker/
├── app/                    # Main application
│   ├── backend/            # FastAPI server
│   │   ├── main.py         # App entry point
│   │   ├── routes.py       # API endpoints
│   │   ├── llm_engine.py   # LLM inference wrapper
│   │   ├── knowledge_rag.py # RAG knowledge system
│   │   ├── database.py     # SQLite persistence
│   │   └── models.py       # Pydantic schemas
│   ├── frontend/           # Web UI
│   │   ├── index.html      # Single page app
│   │   ├── app.js          # Chat client + i18n
│   │   ├── style.css       # Dark theme
│   │   └── translations.js # 28 languages
│   └── knowledge/          # Medical/survival knowledge base
├── website/                # Public website
├── models/                 # Model registry + downloader
├── training/               # Fine-tuning pipeline
├── docs/                   # Documentation
├── scripts/                # Build & deploy
└── tests/                  # Test suite
```

## Pull Request Process

1. **One PR per feature/fix** — keep changes focused
2. **Test your changes** — run `make test` before submitting
3. **Update documentation** if you changed behavior
4. **Follow existing code style** — match the patterns you see
5. **Write descriptive commit messages**

### Medical Content PRs

Medical contributions require extra care:
- **Cite your sources** — link to WHO, Red Cross, or peer-reviewed guidelines
- **Flag the severity** — is this life-critical information?
- **Test in multiple languages** — verify the AI gives correct advice
- **Never remove safety warnings** without discussion

## Medical Knowledge Guidelines

Knowledge files are in `app/knowledge/` as Markdown files.

### Format
```markdown
## Topic Name

### Subtopic

**Signs/Symptoms:**
- Sign 1
- Sign 2

**Treatment:**
1. Step 1
2. Step 2

**DO NOT:**
- Dangerous myth 1
- Dangerous myth 2

**DANGER:** Explicit warning about life-threatening mistakes
```

### Rules
- Write in clear, simple English
- Use numbered steps for procedures
- Always include DO NOT sections to bust myths
- Mark life-threatening information with **DANGER:**
- Assume the reader has NO medical training
- Assume NO access to hospital or professional help
- NEVER include "consult a doctor" — if they could, they wouldn't be using this app

## Translation Guidelines

Translations are in `app/frontend/translations.js`.

### Adding a New Language
1. Copy the `en` block as a template
2. Add your language code and translations
3. Set the correct `dir` (ltr or rtl)
4. Test RTL rendering if applicable
5. Submit as a PR with the language name in the title

### Quality Standards
- Use natural, conversational language
- Avoid overly formal or technical terms
- Test that the UI renders correctly with your translations
- For medical terms, use the most commonly understood term in your region

---

Thank you for helping make this project better. Together, we can help millions of people access critical emergency knowledge when they need it most.
