"""
Knowledge RAG — Offline semantic search over medical/survival knowledge files.

Uses ONNX Runtime + Tokenizers (lightweight, no PyTorch) for embeddings.
Model: all-MiniLM-L6-v2 (384-dim, ~80 MB ONNX)

Includes Arabic→English medical keyword mapping so Arabic queries
find the correct English knowledge chunks.
"""

from __future__ import annotations

import time
from pathlib import Path

import numpy as np

# ── Arabic → English Medical Keyword Map ────────────────────────────
# Maps Arabic medical/emergency terms to English search queries.
# This bridges the gap between Arabic user input and English knowledge base.
ARABIC_MEDICAL_MAP: dict[str, list[str]] = {
    # Burns
    "حرق": [
        "burn treatment first aid cool water",
        "do not apply on burns",
        "burn care without supplies",
    ],
    "احترق": [
        "burn treatment first aid cool water",
        "do not apply on burns",
        "burn care without supplies",
    ],
    "حروق": [
        "burn treatment first aid cool water",
        "do not apply on burns",
        "burn care without supplies",
    ],
    "نار": ["burn treatment first aid", "fire burn treatment"],
    "لهب": ["burn treatment first aid", "flame burn treatment"],
    "حريق": ["burn treatment first aid", "fire burn care"],
    # Bleeding
    "نزيف": ["bleeding", "stop bleeding", "hemorrhage"],
    "دم": ["bleeding", "blood loss", "wound bleeding"],
    "ينزف": ["bleeding", "stop bleeding", "severe bleeding"],
    "جرح": ["wound care", "wound cleaning", "wound treatment"],
    "جروح": ["wound care", "wounds", "wound treatment"],
    # Breathing
    "تنفس": ["breathing difficulty", "choking", "breathing emergency"],
    "اختناق": ["choking", "breathing emergency", "airway obstruction"],
    "غاز": ["gas exposure", "chemical gas", "tear gas", "toxic fumes"],
    "دخان": ["smoke inhalation", "gas exposure", "breathing difficulty"],
    "ربو": ["asthma attack", "breathing difficulty"],
    # Choking
    "شرق": ["choking", "choking first aid", "Heimlich maneuver"],
    "بلع": ["choking", "swallowed", "poisoning"],
    # Fractures / bones
    "كسر": ["fracture", "broken bone", "splint"],
    "عظم": ["fracture", "broken bone", "bone injury"],
    "عظام": ["fracture", "broken bone", "bone injury"],
    "خلع": ["dislocation", "joint injury"],
    # Head / spine
    "رأس": ["head injury", "concussion", "head trauma"],
    "ارتجاج": ["concussion", "head injury"],
    "ظهر": ["spinal injury", "back injury", "spine"],
    "رقبة": ["spinal injury", "neck injury", "spine"],
    # Shock
    "صدمة": ["shock treatment", "medical shock", "shock emergency"],
    "إغماء": ["unconscious", "fainting", "shock"],
    "وعي": ["unconscious", "loss of consciousness"],
    # CPR
    "قلب": ["CPR", "heart", "cardiac arrest", "chest compressions"],
    "إنعاش": ["CPR", "resuscitation", "cardiac arrest"],
    "نبض": ["CPR", "pulse", "heart stopped"],
    # Pain
    "ألم": ["pain", "pain management", "injury treatment"],
    "وجع": ["pain", "pain management", "injury treatment"],
    # Water / food
    "ماء": ["water purification", "clean water", "dehydration"],
    "عطش": ["dehydration", "water", "dehydration treatment"],
    "جفاف": ["dehydration", "dehydration treatment", "water"],
    "أكل": ["food safety", "food poisoning", "safe food"],
    "طعام": ["food safety", "food poisoning", "safe food"],
    "تسمم": ["poisoning", "food poisoning", "poison treatment"],
    "سم": ["poisoning", "poison treatment", "venom"],
    # Bites / stings
    "لدغ": ["snake bite", "scorpion sting", "bite treatment"],
    "عقرب": ["scorpion sting", "scorpion treatment"],
    "ثعبان": ["snake bite", "snake bite first aid"],
    "حية": ["snake bite", "snake bite first aid"],
    "كلب": ["dog bite", "animal bite", "rabies"],
    # Psychological
    "خوف": ["panic attack", "psychological first aid", "fear"],
    "هلع": ["panic attack", "psychological first aid"],
    "قلق": ["panic attack", "anxiety", "psychological support"],
    "صدمة نفسية": ["psychological first aid", "trauma", "PTSD"],
    # Shelter / cold / heat
    "برد": ["hypothermia", "cold emergency", "warmth"],
    "حر": ["heat stroke", "heat exhaustion"],
    "مأوى": ["shelter", "emergency shelter"],
    # Chemical
    "كيميائي": ["chemical exposure", "chemical burns", "decontamination"],
    "إشعاع": ["radiation", "nuclear", "radiation protection"],
    # General
    "إسعاف": ["first aid", "emergency treatment"],
    "علاج": ["treatment", "first aid", "emergency care"],
    "دواء": ["treatment", "medicine", "first aid without medicine"],
    "دوا": ["treatment", "medicine", "first aid without medicine"],
    "طفل": ["infant", "child", "pediatric emergency"],
    "أطفال": ["infant", "child", "pediatric emergency"],
    "حامل": ["pregnancy emergency", "pregnant woman"],
}


def _extract_arabic_keywords(text: str) -> list[str]:
    """Extract English search queries from Arabic text using keyword mapping."""
    english_queries = []
    text_lower = text.strip()

    for arabic_term, english_terms in ARABIC_MEDICAL_MAP.items():
        if arabic_term in text_lower:
            english_queries.extend(english_terms)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for q in english_queries:
        if q not in seen:
            seen.add(q)
            unique.append(q)

    return unique


def _is_arabic(text: str) -> bool:
    """Check if text contains significant Arabic content."""
    if not text:
        return False
    arabic_chars = sum(
        1
        for c in text
        if "\u0600" <= c <= "\u06ff"
        or "\u0750" <= c <= "\u077f"
        or "\u08a0" <= c <= "\u08ff"
        or "\ufb50" <= c <= "\ufdff"
        or "\ufe70" <= c <= "\ufeff"
    )
    return arabic_chars > 3


class EmbeddingModel:
    """Lightweight ONNX-based sentence embedding model."""

    def __init__(self, model_dir: str):
        import onnxruntime as ort
        from tokenizers import Tokenizer

        model_dir = Path(model_dir)

        # Locate the ONNX model file (could be in onnx/ subfolder)
        onnx_path = model_dir / "onnx" / "model.onnx"
        if not onnx_path.exists():
            onnx_path = model_dir / "model.onnx"
        if not onnx_path.exists():
            raise FileNotFoundError(
                f"ONNX model not found in {model_dir}. Run: python tools/download_embedding.py"
            )

        # Locate the tokenizer
        tok_path = model_dir / "tokenizer.json"
        if not tok_path.exists():
            raise FileNotFoundError(
                f"tokenizer.json not found in {model_dir}. Run: python tools/download_embedding.py"
            )

        self.tokenizer = Tokenizer.from_file(str(tok_path))
        self.tokenizer.enable_truncation(max_length=128)
        self.tokenizer.enable_padding(length=128)

        # Create ONNX session (CPU only — lightweight)
        opts = ort.SessionOptions()
        opts.inter_op_num_threads = 2
        opts.intra_op_num_threads = 4
        self.session = ort.InferenceSession(
            str(onnx_path), opts, providers=["CPUExecutionProvider"]
        )

        # Detect which inputs the model accepts
        self._input_names = [inp.name for inp in self.session.get_inputs()]

    def encode(self, texts: list[str]) -> np.ndarray:
        """Encode texts to normalized 384-dim embeddings."""
        if not texts:
            return np.array([])

        encoded = self.tokenizer.encode_batch(texts)

        input_ids = np.array([e.ids for e in encoded], dtype=np.int64)
        attention_mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)

        feeds = {"input_ids": input_ids, "attention_mask": attention_mask}
        if "token_type_ids" in self._input_names:
            feeds["token_type_ids"] = np.zeros_like(input_ids)

        outputs = self.session.run(None, feeds)

        # Mean pooling over token_embeddings
        last_hidden = outputs[0]  # shape: (batch, seq_len, hidden_dim)
        mask = attention_mask[..., np.newaxis].astype(np.float32)
        pooled = (last_hidden * mask).sum(axis=1) / np.clip(mask.sum(axis=1), 1e-9, None)

        # L2 normalize
        norms = np.linalg.norm(pooled, axis=1, keepdims=True)
        return pooled / np.clip(norms, 1e-9, None)


class KnowledgeRAG:
    """
    Offline RAG engine for medical/survival knowledge.

    Loads markdown files → splits into semantic chunks → embeds at startup.
    On each user query, finds the most relevant chunks via cosine similarity.
    """

    def __init__(
        self,
        knowledge_dir: str,
        embedding_model_dir: str,
    ):
        self.chunks: list[dict] = []  # {"text", "source", "section", "search_text"}
        self.embeddings: np.ndarray | None = None
        self.model: EmbeddingModel | None = None

        # Try loading the embedding model
        try:
            t0 = time.time()
            self.model = EmbeddingModel(embedding_model_dir)
            print(f"✅ Embedding model loaded in {time.time() - t0:.1f}s")
        except Exception as e:
            print(f"⚠️  Embedding model not available: {e}")
            print("   RAG disabled. Run: python tools/download_embedding.py")
            return

        # Load and index knowledge
        self._load_knowledge(knowledge_dir)
        self._build_index()

    # ── Knowledge Loading ───────────────────────────────────────────

    def _load_knowledge(self, knowledge_dir: str) -> None:
        """Load all .md files from the knowledge directory."""
        kdir = Path(knowledge_dir)
        if not kdir.exists():
            print(f"⚠️  Knowledge directory not found: {knowledge_dir}")
            return

        md_files = sorted(kdir.glob("*.md"))
        for md_file in md_files:
            text = md_file.read_text(encoding="utf-8")
            source = md_file.stem
            chunks = self._split_into_chunks(text, source)
            self.chunks.extend(chunks)

        print(f"📚 Loaded {len(self.chunks)} knowledge chunks from {len(md_files)} files")

    def _split_into_chunks(self, text: str, source: str) -> list[dict]:
        """
        Split markdown into semantic chunks by ## headers.
        Each chunk includes its header chain for context.
        """
        chunks = []
        doc_title = ""
        current_h2 = ""
        current_h3 = ""
        current_lines: list[str] = []

        def flush():
            content = "\n".join(current_lines).strip()
            if not content or len(content) < 30:
                return
            section = " > ".join(filter(None, [doc_title, current_h2, current_h3]))
            # Build search_text: section headers + content (for embedding)
            search_text = f"{section}\n{content}"
            chunks.append(
                {
                    "text": content,
                    "source": source,
                    "section": section,
                    "search_text": search_text,
                }
            )

        for line in text.split("\n"):
            stripped = line.strip()

            if stripped.startswith("# ") and not stripped.startswith("## "):
                # H1 — document title
                if current_lines:
                    flush()
                    current_lines = []
                doc_title = stripped.lstrip("# ").strip()

            elif stripped.startswith("## "):
                # H2 — major section
                if current_lines:
                    flush()
                    current_lines = []
                current_h2 = stripped.lstrip("# ").strip()
                current_h3 = ""
                current_lines.append(line)

            elif stripped.startswith("### "):
                # H3 — subsection → flush previous subsection
                if current_lines:
                    flush()
                    current_lines = []
                current_h3 = stripped.lstrip("# ").strip()
                current_lines.append(line)

            else:
                current_lines.append(line)

        # Flush last chunk
        if current_lines:
            flush()

        return chunks

    # ── Indexing ────────────────────────────────────────────────────

    def _build_index(self) -> None:
        """Compute embeddings for all knowledge chunks."""
        if not self.chunks or not self.model:
            return

        t0 = time.time()
        texts = [c["search_text"] for c in self.chunks]

        # Encode in batches to manage memory
        batch_size = 32
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            emb = self.model.encode(batch)
            all_embeddings.append(emb)

        self.embeddings = np.vstack(all_embeddings)
        print(f"🔍 Knowledge index built: {len(self.chunks)} chunks in {time.time() - t0:.1f}s")

    # ── Search ──────────────────────────────────────────────────────

    @property
    def is_ready(self) -> bool:
        return self.model is not None and self.embeddings is not None and len(self.chunks) > 0

    def search(self, query: str, top_k: int = 3, min_score: float = 0.25) -> list[dict]:
        """
        Find the most relevant knowledge chunks for a query.
        For Arabic queries, translates keywords to English and searches multiple times.

        Returns list of {"text", "source", "section", "score"}.
        """
        if not self.is_ready:
            return []

        all_results: dict[int, dict] = {}  # chunk_index -> result (keeps best score)

        # 1) Always search with original query
        self._semantic_search(query, top_k * 2, min_score, all_results)

        # 2) If Arabic, also search with translated English keywords
        if _is_arabic(query):
            english_queries = _extract_arabic_keywords(query)
            for eq in english_queries[:8]:  # Search more keywords for better coverage
                self._semantic_search(eq, top_k, min_score, all_results)

        # Sort by score descending, but boost "Treatment" sections
        for idx, result in all_results.items():
            section = result["section"].lower()
            # Boost treatment/care sections over classification/emergency-identification sections
            if "treatment" in section or "burn treatment" in section or "care" in section:
                result["score"] = min(result["score"] + 0.08, 1.0)

        sorted_results = sorted(all_results.values(), key=lambda r: r["score"], reverse=True)
        return sorted_results[:top_k]

    def _semantic_search(
        self, query: str, top_k: int, min_score: float, results: dict[int, dict]
    ) -> None:
        """Run a single semantic search and merge into results dict."""
        query_emb = self.model.encode([query])
        scores = np.dot(self.embeddings, query_emb.T).flatten()

        top_indices = np.argsort(scores)[::-1][:top_k]
        for idx in top_indices:
            idx = int(idx)
            if scores[idx] >= min_score:
                existing = results.get(idx)
                if existing is None or scores[idx] > existing["score"]:
                    results[idx] = {
                        "text": self.chunks[idx]["text"],
                        "source": self.chunks[idx]["source"],
                        "section": self.chunks[idx]["section"],
                        "score": float(scores[idx]),
                    }

    def get_context(self, query: str, max_chars: int = 3000) -> str:
        """
        Get formatted knowledge context to inject into the LLM system prompt.

        Returns empty string if nothing relevant is found.
        """
        results = self.search(query, top_k=5)
        if not results:
            return ""

        parts = []
        total = 0
        for r in results:
            header = f"[{r['section']}] (relevance: {r['score']:.0%})"
            text = r["text"]

            # Truncate if exceeding budget
            if total + len(text) > max_chars:
                remaining = max_chars - total
                if remaining < 100:
                    break
                text = text[:remaining] + "..."

            parts.append(f"{header}\n{text}")
            total += len(text)

        return "\n\n---\n\n".join(parts)

    def get_stats(self) -> dict:
        """Return stats about the knowledge base."""
        return {
            "ready": self.is_ready,
            "total_chunks": len(self.chunks),
            "sources": list(set(c["source"] for c in self.chunks)),
            "embedding_dim": self.embeddings.shape[1] if self.embeddings is not None else 0,
        }
