# ══════════════════════════════════════════════════════════════
#  Model Maker — Makefile
#  Common commands for development, testing, and building
# ══════════════════════════════════════════════════════════════

.PHONY: help setup run test lint format clean build download-model website

PYTHON = .venv/bin/python
PIP = .venv/bin/pip

# Default target
help: ## Show this help
	@echo "🏥 Model Maker — Available Commands"
	@echo "═══════════════════════════════════════"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ── Setup ─────────────────────────────────────────────────────

setup: ## First-time setup (venv + dependencies)
	@bash scripts/setup.sh

venv: ## Create virtual environment
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

install-dev: ## Install dev dependencies
	$(PIP) install -e ".[dev]"

# ── Run ───────────────────────────────────────────────────────

run: ## Start Model Maker (app + browser)
	cd app && $(PYTHON) run.py

run-server: ## Start backend server only
	cd app && $(PYTHON) -m uvicorn backend.main:app --host 127.0.0.1 --port 8000

# ── Model ─────────────────────────────────────────────────────

download-model: ## Download AI model (interactive)
	$(PYTHON) models/download.py

download-lite: ## Download Lite model (3B, 2GB)
	$(PYTHON) models/download.py --tier lite

download-standard: ## Download Standard model (7B, 4.4GB)
	$(PYTHON) models/download.py --tier standard

download-premium: ## Download Premium model (14B, 8.5GB)
	$(PYTHON) models/download.py --tier premium

check-device: ## Check device compatibility
	$(PYTHON) models/download.py --check

# ── Testing ───────────────────────────────────────────────────

test: ## Run all tests
	$(PYTHON) -m pytest tests/ -v --tb=short

test-api: ## Run API tests only
	$(PYTHON) -m pytest tests/test_api.py -v

test-medical: ## Run medical accuracy tests (needs model)
	$(PYTHON) tools/test_medical_accuracy.py

test-quick: ## Run fast tests (skip LLM)
	SKIP_LLM_TESTS=1 $(PYTHON) -m pytest tests/ -v --tb=short -m "not slow"

# ── Code Quality ──────────────────────────────────────────────

lint: ## Check code with ruff
	$(PYTHON) -m ruff check app/backend/ tools/ models/download.py

format: ## Format code with ruff
	$(PYTHON) -m ruff format app/backend/ tools/ models/download.py

format-check: ## Check formatting without changing
	$(PYTHON) -m ruff format --check app/backend/ tools/

# ── Website ───────────────────────────────────────────────────

website: ## Preview website locally
	@echo "🌐 Opening website at http://localhost:8080"
	cd website && python3 -m http.server 8080

# ── Build ─────────────────────────────────────────────────────

build: ## Build release package
	@echo "📦 Building release package..."
	@mkdir -p dist/model-maker
	@cp -r app/ dist/model-maker/app/
	@cp -r models/registry.json dist/model-maker/
	@cp models/download.py dist/model-maker/
	@cp requirements.txt dist/model-maker/
	@cp LICENSE dist/model-maker/
	@cp README.md dist/model-maker/
	@cp scripts/setup.sh dist/model-maker/
	@echo "✅ Build complete: dist/model-maker/"

# ── Clean ─────────────────────────────────────────────────────

clean: ## Remove build artifacts and caches
	rm -rf dist/ build/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned"

clean-all: clean ## Clean everything including venv and data
	rm -rf .venv
	rm -rf app/data/*.db
	@echo "✅ Deep clean complete"
