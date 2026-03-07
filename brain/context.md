# Model Maker — Brain Context

## Quick Reference

### Project Structure

- `app/` — Main application (backend + frontend + knowledge + launcher)
- `models/` — Model registry, downloader, and GGUF files (gitignored)
- `website/` — Public website (S3/CloudFront, 28 languages)
- `training/` — Fine-tuning pipeline and datasets
- `tools/` — Developer utilities
- `tests/` — Test suite
- `docs/` — Documentation
- `scripts/` — Build & setup scripts

### Key Commands

```bash
# First-time setup
make setup
# or: bash scripts/setup.sh

# Start the app
make run
# or: cd app && python run.py

# Download a model
make download-model
# or: python models/download.py --tier standard

# Check device compatibility
make check-device
# or: python models/download.py --check

# Run tests
make test

# Preview website locally
make website
```

### Architecture Decisions Log

| Date       | Decision                       | Reason                            |
| ---------- | ------------------------------ | --------------------------------- |
| 2026-03-06 | Qwen2.5 over Llama-3.1        | Better Arabic support (29 langs)  |
| 2026-03-06 | SQLite over JSON files         | Better for conversations + search |
| 2026-03-06 | SSE over WebSocket             | Simpler, works everywhere         |
| 2026-03-06 | No framework (vanilla JS)      | Zero dependencies, fast loading   |
| 2026-03-06 | Setup wizard for system prompt | Easy customization for users      |
| 2026-03    | Apache 2.0 open source         | Community-driven, $1 download     |
| 2026-03    | 3-tier model system            | Lite/Standard/Premium for all HW  |
| 2026-03    | ONNX RAG + Arabic bridge       | Offline cross-lingual search      |

### Model Tiers

| Tier     | Model                           | Size   | RAM  | Use Case         |
| -------- | ------------------------------- | ------ | ---- | ---------------- |
| Lite     | Qwen2.5-3B-Instruct (Q4_K_M)   | 2.0 GB | 4 GB | Basic devices    |
| Standard | Qwen2.5-7B-Instruct (Q4_K_M)   | 4.4 GB | 8 GB | Most users ★     |
| Premium  | Qwen2.5-14B-Instruct (Q4_K_M)  | 8.5 GB | 16 GB| Best quality     |
