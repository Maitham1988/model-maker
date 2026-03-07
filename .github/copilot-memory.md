# Copilot Memory — Model Maker

## Project Facts

- Created: March 6, 2026
- Owner: Maitham (FlexSell International W.L.L)
- Purpose: Commercial offline AI chat system for Bahrain/GCC market
- Emergency use case: Works without internet during wartime/outages
- Business model: Install on customer devices, charge per installation
- Anti-piracy: Device-locked license (hardware ID based)

## Technical Decisions

- Model: Qwen2.5-7B-Instruct GGUF Q4_K_M (standard), 14B for premium
- Backend: FastAPI + llama-cpp-python
- Frontend: Vanilla HTML/CSS/JS, dark theme like ChatGPT
- Database: SQLite (conversations, messages, memory)
- Streaming: Server-Sent Events (SSE)
- No internet dependency — 100% offline
- System prompt: User-facing setup wizard with questions

## Customer Setup

- System prompt generated from wizard questions (name, field, language, tasks)
- User can also directly edit system prompt in settings
- Each customer gets unique folder in projects/
- License locked to hardware ID

## Model Information

- Qwen2.5-7B supports 29 languages including Arabic and English
- Arabic quality: Very good (formal Arabic, MSA)
- Gulf Arabic dialect: Supported but may default to MSA
- 8GB RAM minimum for 7B model
- 16GB RAM minimum for 14B model

## Related Projects

- FlexSell (Flutter app): ~/Projects/flexsell.pre — separate project, different tech stack
