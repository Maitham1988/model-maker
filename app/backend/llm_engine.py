"""
LLM Engine — Wraps llama-cpp-python for local inference.
Handles model loading, chat completion with streaming, and context management.
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from typing import Generator

from llama_cpp import Llama


class LLMEngine:
    """Manages a local GGUF model and provides streaming chat completion."""

    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.model: Llama | None = None
        self._load_model()

    def _load_config(self, config_path: str) -> dict:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(
                f"Config file not found: {config_path}. Run setup wizard first."
            )
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_model(self) -> None:
        model_path = self.config.get("model_path", "")
        if not model_path or not Path(model_path).exists():
            print(f"⚠️  Model file not found at: {model_path}")
            print("   Download a model first: python tools/download_model.py")
            return

        n_ctx = self.config.get("context_length", 4096)
        n_gpu_layers = self.config.get("gpu_layers", 0)

        # Auto-detect Apple Silicon for GPU acceleration
        try:
            import platform
            if platform.machine() == "arm64" and platform.system() == "Darwin":
                n_gpu_layers = -1  # Use all layers on Metal
        except Exception:
            pass

        print(f"🔄 Loading model: {Path(model_path).name}")
        print(f"   Context: {n_ctx} tokens | GPU layers: {n_gpu_layers}")

        self.model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            n_threads=os.cpu_count() or 4,
            verbose=False,
            chat_format="chatml",  # Qwen2.5 uses ChatML format
        )
        print("✅ Model loaded successfully")

    @property
    def is_loaded(self) -> bool:
        return self.model is not None

    @staticmethod
    def _is_arabic(text: str) -> bool:
        """Check if text is primarily Arabic."""
        if not text:
            return False
        arabic_chars = sum(
            1 for c in text if '\u0600' <= c <= '\u06FF'
            or '\u0750' <= c <= '\u077F'
            or '\u08A0' <= c <= '\u08FF'
            or '\uFB50' <= c <= '\uFDFF'
            or '\uFE70' <= c <= '\uFEFF'
        )
        alpha_chars = sum(1 for c in text if c.isalpha())
        return alpha_chars > 0 and arabic_chars / alpha_chars > 0.3

    @property
    def system_prompt(self) -> str:
        return self.config.get(
            "system_prompt",
            "You are a helpful AI assistant. Be accurate, concise, and friendly. "
            "Respond in the same language the user writes in.",
        )

    def chat_stream(
        self,
        messages: list[dict],
        memory_context: str = "",
        knowledge_context: str = "",
    ) -> Generator[str, None, None]:
        """
        Stream chat completion token by token.

        Args:
            messages: List of {"role": "user"|"assistant", "content": "..."}
            memory_context: Optional persistent memory to inject into system prompt
            knowledge_context: Optional RAG knowledge to inject into system prompt
        """
        if not self.is_loaded:
            yield "❌ Model not loaded. Please check config.json and model file."
            return

        # Build full message list with system prompt + memory
        full_messages = []

        # System prompt with optional memory and knowledge context
        system_content = self.system_prompt
        if knowledge_context:
            system_content += (
                "\n\n=== VERIFIED MEDICAL/SURVIVAL KNOWLEDGE ===\n"
                "CRITICAL: The information below is from a VERIFIED medical knowledge base.\n"
                "RULES FOR USING THIS KNOWLEDGE:\n"
                "1. You MUST base your answer on this knowledge. Follow the steps EXACTLY as written.\n"
                "2. Do NOT contradict or change any instruction. If it says COOL water, say COOL water — not warm water.\n"
                "3. Do NOT invent treatments or remedies not listed here. If only water and honey are listed as safe, say ONLY water and honey.\n"
                "4. Copy the DO NOT / NEVER / DANGER warnings exactly — these prevent the user from harming themselves.\n"
                "5. If the knowledge says 'NEVER apply X', you MUST tell the user to NEVER apply X.\n\n"
                + knowledge_context
                + "\n\n=== END OF VERIFIED KNOWLEDGE ==="
            )
        if memory_context:
            system_content += (
                f"\n\nIMPORTANT CONTEXT FROM PREVIOUS CONVERSATIONS:\n{memory_context}"
            )
        full_messages.append({"role": "system", "content": system_content})

        # Add conversation messages (limit to last N for context window)
        max_history = self.config.get("max_history_messages", 20)
        recent_messages = messages[-max_history:]
        full_messages.extend(recent_messages)

        # Detect if last user message is Arabic and add a language reminder
        last_user_msg = ""
        for m in reversed(recent_messages):
            if m.get("role") == "user":
                last_user_msg = m.get("content", "")
                break
        is_arabic_context = last_user_msg and self._is_arabic(last_user_msg)
        if is_arabic_context:
            full_messages.append({
                "role": "system",
                "content": (
                    "تنبيه مهم: المستخدم يكتب بالعربية. يجب أن تكون إجابتك بالكامل باللغة العربية فقط. "
                    "لا تستخدم الإنجليزية أو الصينية أو أي لغة أخرى على الإطلاق. "
                    "كل كلمة يجب أن تكون بالعربية."
                )
            })

        # Use lower temperature for Arabic to reduce code-switching
        temperature = self.config.get("temperature", 0.7)
        if is_arabic_context:
            temperature = min(temperature, 0.4)

        try:
            response = self.model.create_chat_completion(
                messages=full_messages,
                stream=True,
                max_tokens=self.config.get("max_tokens", 2048),
                temperature=temperature,
                top_p=self.config.get("top_p", 0.9),
                repeat_penalty=self.config.get("repeat_penalty", 1.1),
            )

            for chunk in response:
                choices = chunk.get("choices", [])
                if choices:
                    delta = choices[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        yield content

        except Exception as e:
            yield f"\n\n❌ Error generating response: {str(e)}"

    def chat(self, messages: list[dict], memory_context: str = "", knowledge_context: str = "") -> str:
        """Non-streaming chat completion. Returns full response."""
        parts = list(self.chat_stream(messages, memory_context, knowledge_context))
        return "".join(parts)

    def reload_config(self, config_path: str = "config.json") -> None:
        """Reload config without reloading model (for system prompt changes)."""
        self.config = self._load_config(config_path)

    def reload_model(self, config_path: str = "config.json") -> None:
        """Full reload — config + model."""
        self.config = self._load_config(config_path)
        self._load_model()
