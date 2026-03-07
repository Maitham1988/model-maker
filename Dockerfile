# ─── Build Stage ───────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake gcc g++ && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python packages (CPU-only llama-cpp by default)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─── Runtime Stage ─────────────────────────────────────────────────
FROM python:3.11-slim

LABEL maintainer="Maitham <maitham@flexsell.com>"
LABEL org.opencontainers.image.title="Model Maker"
LABEL org.opencontainers.image.description="Offline AI assistant for emergency, medical, and survival situations"
LABEL org.opencontainers.image.source="https://github.com/Maitham1988/model-maker"
LABEL org.opencontainers.image.licenses="Apache-2.0"

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application
COPY app/ ./app/
COPY models/registry.json ./models/
COPY models/download.py ./models/

# Create data directory
RUN mkdir -p /app/app/data /app/models/gguf

# Copy config template as default config
RUN cp /app/app/config_template.json /app/app/config.json 2>/dev/null || true

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Environment
ENV PYTHONUNBUFFERED=1
ENV MODEL_MAKER_DOCKER=1

# Run the app
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

WORKDIR /app/app
