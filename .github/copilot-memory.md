# Copilot Memory — Model Maker

## Project Facts

- Created: March 6, 2026
- Owner: Maitham (FlexSell International W.L.L)
- Purpose: Free open-source offline AI for emergency medical & survival situations
- Emergency use case: Works without internet during wartime/outages
- License: Apache 2.0

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
- Setup wizard customizes the AI for each user's situation

## Model Information

- Qwen2.5-7B supports 29 languages including Arabic and English
- Arabic quality: Very good (formal Arabic, MSA)
- Gulf Arabic dialect: Supported but may default to MSA
- 8GB RAM minimum for 7B model
- 16GB RAM minimum for 14B model

## Related Projects

- FlexSell (Flutter app): ~/Projects/flexsell.pre — separate project, different tech stack
